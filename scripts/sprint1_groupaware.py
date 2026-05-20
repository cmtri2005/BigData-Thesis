#!/usr/bin/env python3
"""Sprint 1 utilities: duplicate audit, group-aware split, and benchmark rerun.

The split/audit path uses only the Python standard library. The benchmark path
requires pandas and scikit-learn, matching the Phase 4 notebook environment.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import random
import re
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FEATURES_PATH = ROOT / "output/phase2/viclickbait_eda_features.csv"
ORIGINAL_SPLIT_PATH = ROOT / "output/phase3/random_stratified_70_10_20.csv"
PHASE2_DUP_PATH = ROOT / "output/phase2/duplicate_title_groups.csv"
GROUP_SPLIT_PATH = ROOT / "output/phase3/random_group_stratified_70_10_20.csv"
GROUP_SPLIT_SUMMARY_PATH = ROOT / "output/phase3/groupaware_split_summary.csv"
SPLIT_AUDIT_PATH = ROOT / "output/phase3/split_leakage_audit.json"
GROUP_PHASE4_DIR = ROOT / "output/phase4_groupaware"
GROUP_RESULTS_PATH = GROUP_PHASE4_DIR / "random_split_results.csv"
GROUP_SUMMARY_PATH = GROUP_PHASE4_DIR / "phase4_summary.md"
GROUP_COMPARISON_PATH = GROUP_PHASE4_DIR / "groupaware_vs_original_comparison.csv"

RANDOM_STATE = 42
SPLIT_TARGETS = {
    "train": 2389,
    "validation": 342,
    "test": 683,
}
SPLIT_ORDER = ("train", "validation", "test")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def normalize_title(text: str) -> str:
    text = unicodedata.normalize("NFC", str(text or "")).lower().strip()
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"\s+-\s+báo\s+.+$", "", text)
    text = re.sub(r"\s+-\s+.+$", "", text)
    text = re.sub(r"[“”\"']", "", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def make_groups(rows: list[dict[str, str]]) -> tuple[dict[str, list[dict]], dict[str, str]]:
    by_title: dict[str, list[dict]] = defaultdict(list)
    for row in rows:
        by_title[normalize_title(row["title"])].append(row)

    group_id_by_title: dict[str, str] = {}
    for idx, title in enumerate(sorted(by_title), start=1):
        group_id_by_title[title] = f"g{idx:05d}"
    return by_title, group_id_by_title


def load_original_splits() -> dict[str, str]:
    if not ORIGINAL_SPLIT_PATH.exists():
        return {}
    return {row["id"]: row["split"] for row in read_csv(ORIGINAL_SPLIT_PATH)}


def export_duplicate_groups(
    by_title: dict[str, list[dict]],
    group_id_by_title: dict[str, str],
    original_split_by_id: dict[str, str],
) -> None:
    rows_out: list[dict] = []
    for norm_title, group_rows in sorted(by_title.items()):
        if len(group_rows) < 2:
            continue
        labels = {row["label"] for row in group_rows}
        sources = {row["source"] for row in group_rows}
        for row in sorted(group_rows, key=lambda item: item["id"]):
            rows_out.append(
                {
                    "duplicate_group": group_id_by_title[norm_title],
                    "normalized_title": norm_title,
                    "group_size": len(group_rows),
                    "cross_source": int(len(sources) > 1),
                    "cross_label": int(len(labels) > 1),
                    "id": row["id"],
                    "title": row["title"],
                    "label": row["label"],
                    "label_str": row.get("label_str", ""),
                    "source": row.get("source", ""),
                    "category": row.get("category", ""),
                    "original_split": original_split_by_id.get(row["id"], ""),
                }
            )

    fieldnames = [
        "duplicate_group",
        "normalized_title",
        "group_size",
        "cross_source",
        "cross_label",
        "id",
        "title",
        "label",
        "label_str",
        "source",
        "category",
        "original_split",
    ]
    write_csv(PHASE2_DUP_PATH, rows_out, fieldnames)


def summarize_split(rows: list[dict[str, str]], split_by_id: dict[str, str], protocol: str) -> list[dict]:
    total = len(rows)
    out: list[dict] = []
    for split in SPLIT_ORDER:
        split_rows = [row for row in rows if split_by_id.get(row["id"]) == split]
        n_click = sum(int(row["label"]) for row in split_rows)
        n_total = len(split_rows)
        out.append(
            {
                "protocol": protocol,
                "split": split,
                "n_total": n_total,
                "n_clickbait": n_click,
                "n_non_clickbait": n_total - n_click,
                "clickbait_rate": round(100 * n_click / n_total, 2) if n_total else 0.0,
                "share_of_dataset": round(100 * n_total / total, 2) if total else 0.0,
            }
        )
    return out


def target_click_counts(rows: list[dict[str, str]]) -> dict[str, int]:
    total_click = sum(int(row["label"]) for row in rows)
    total_rows = len(rows)
    raw = {split: total_click * target / total_rows for split, target in SPLIT_TARGETS.items()}
    floored = {split: math.floor(value) for split, value in raw.items()}
    remaining = total_click - sum(floored.values())
    for split, _ in sorted(raw.items(), key=lambda item: item[1] - math.floor(item[1]), reverse=True):
        if remaining <= 0:
            break
        floored[split] += 1
        remaining -= 1
    return floored


def build_groupaware_split(
    by_title: dict[str, list[dict]],
    group_id_by_title: dict[str, str],
    rows: list[dict[str, str]],
) -> dict[str, str]:
    rng = random.Random(RANDOM_STATE)
    groups = []
    for norm_title, group_rows in by_title.items():
        click = sum(int(row["label"]) for row in group_rows)
        groups.append(
            {
                "group_id": group_id_by_title[norm_title],
                "rows": group_rows,
                "n": len(group_rows),
                "click": click,
                "rand": rng.random(),
            }
        )

    click_targets = target_click_counts(rows)
    nonclick_targets = {split: SPLIT_TARGETS[split] - click_targets[split] for split in SPLIT_ORDER}
    stats = {split: {"n": 0, "click": 0, "nonclick": 0} for split in SPLIT_ORDER}
    split_by_id: dict[str, str] = {}

    def assign_group(group: dict, split: str) -> None:
        stats[split]["n"] += group["n"]
        stats[split]["click"] += group["click"]
        stats[split]["nonclick"] += group["n"] - group["click"]
        for row in group["rows"]:
            split_by_id[row["id"]] = split

    def remaining(split: str) -> tuple[int, int, int]:
        return (
            SPLIT_TARGETS[split] - stats[split]["n"],
            click_targets[split] - stats[split]["click"],
            nonclick_targets[split] - stats[split]["nonclick"],
        )

    def choose_split(group: dict, mode: str) -> str:
        candidates = []
        for split in SPLIT_ORDER:
            size_remaining, click_remaining, nonclick_remaining = remaining(split)
            group_nonclick = group["n"] - group["click"]
            hard_fit = (
                size_remaining >= group["n"]
                and click_remaining >= group["click"]
                and nonclick_remaining >= group_nonclick
            )
            if mode == "click":
                need = click_remaining
            elif mode == "nonclick":
                need = nonclick_remaining
            else:
                need = min(click_remaining, nonclick_remaining)
            overflow = max(0, group["n"] - size_remaining)
            label_overflow = max(0, group["click"] - click_remaining) + max(0, group_nonclick - nonclick_remaining)
            candidates.append((hard_fit, need, size_remaining, -overflow, -label_overflow, split))

        fitting = [item for item in candidates if item[0]]
        pool = fitting or candidates
        return max(pool, key=lambda item: (item[1], item[2], item[3], item[4], item[5]))[-1]

    mixed = [group for group in groups if 0 < group["click"] < group["n"]]
    click_only = [group for group in groups if group["click"] == group["n"]]
    nonclick_only = [group for group in groups if group["click"] == 0]
    for bucket in (mixed, click_only, nonclick_only):
        bucket.sort(key=lambda group: (-group["n"], group["rand"]))

    for group in mixed:
        assign_group(group, choose_split(group, "mixed"))
    for group in click_only:
        assign_group(group, choose_split(group, "click"))
    for group in nonclick_only:
        assign_group(group, choose_split(group, "nonclick"))

    # If the greedy label-aware pass leaves a split slightly off in size, move
    # singleton groups between splits without breaking duplicate grouping.
    for _ in range(1000):
        over = max(SPLIT_ORDER, key=lambda split: stats[split]["n"] - SPLIT_TARGETS[split])
        under = min(SPLIT_ORDER, key=lambda split: stats[split]["n"] - SPLIT_TARGETS[split])
        if stats[over]["n"] <= SPLIT_TARGETS[over] or stats[under]["n"] >= SPLIT_TARGETS[under]:
            break
        movable = [
            group for group in groups
            if group["n"] == 1 and split_by_id[group["rows"][0]["id"]] == over
        ]
        if not movable:
            break
        target_click_rate = click_targets[under] / max(1, SPLIT_TARGETS[under])
        best_split = None
        best_cost = None
        for group in movable:
            group_click = group["click"]
            new_under_click_rate = (stats[under]["click"] + group_click) / max(1, stats[under]["n"] + 1)
            cost = abs(new_under_click_rate - target_click_rate)
            if best_cost is None or cost < best_cost:
                best_cost = cost
                best_split = group
        if best_split is None:
            break
        row_id = best_split["rows"][0]["id"]
        stats[over]["n"] -= 1
        stats[over]["click"] -= best_split["click"]
        stats[over]["nonclick"] -= 1 - best_split["click"]
        stats[under]["n"] += 1
        stats[under]["click"] += best_split["click"]
        stats[under]["nonclick"] += 1 - best_split["click"]
        split_by_id[row_id] = under

    return split_by_id


def count_cross_split_duplicate_groups(
    by_title: dict[str, list[dict]],
    split_by_id: dict[str, str],
) -> int:
    count = 0
    for group_rows in by_title.values():
        if len(group_rows) < 2:
            continue
        splits = {split_by_id.get(row["id"], "") for row in group_rows}
        splits.discard("")
        if len(splits) > 1:
            count += 1
    return count


def audit_duplicates(
    by_title: dict[str, list[dict]],
    original_split_by_id: dict[str, str],
    group_split_by_id: dict[str, str],
) -> dict:
    duplicate_groups = {title: rows for title, rows in by_title.items() if len(rows) > 1}
    cross_source = 0
    cross_label = 0
    for group_rows in duplicate_groups.values():
        if len({row["source"] for row in group_rows}) > 1:
            cross_source += 1
        if len({row["label"] for row in group_rows}) > 1:
            cross_label += 1

    max_group = max((len(rows) for rows in by_title.values()), default=0)
    return {
        "n_total_rows": sum(len(rows) for rows in by_title.values()),
        "n_title_groups": len(by_title),
        "n_duplicate_groups": len(duplicate_groups),
        "n_duplicate_rows": sum(len(rows) for rows in duplicate_groups.values()),
        "max_group_size": max_group,
        "n_cross_source_duplicate_groups": cross_source,
        "n_cross_label_duplicate_groups": cross_label,
        "original_random_split_cross_duplicate_groups": count_cross_split_duplicate_groups(
            by_title, original_split_by_id
        ),
        "groupaware_random_split_cross_duplicate_groups": count_cross_split_duplicate_groups(
            by_title, group_split_by_id
        ),
    }


def run_split() -> None:
    rows = read_csv(FEATURES_PATH)
    original_split_by_id = load_original_splits()
    by_title, group_id_by_title = make_groups(rows)
    export_duplicate_groups(by_title, group_id_by_title, original_split_by_id)
    group_split_by_id = build_groupaware_split(by_title, group_id_by_title, rows)

    split_rows = []
    for row in sorted(rows, key=lambda item: item["id"]):
        norm_title = normalize_title(row["title"])
        split_rows.append(
            {
                "id": row["id"],
                "split": group_split_by_id[row["id"]],
                "label": row["label"],
                "label_str": row.get("label_str", ""),
                "source": row.get("source", ""),
                "category": row.get("category", ""),
                "publish_dt": row.get("publish_dt", ""),
                "duplicate_group": group_id_by_title[norm_title],
            }
        )
    write_csv(
        GROUP_SPLIT_PATH,
        split_rows,
        ["id", "split", "label", "label_str", "source", "category", "publish_dt", "duplicate_group"],
    )

    summary_rows = summarize_split(rows, group_split_by_id, "random_group_stratified_70_10_20")
    write_csv(
        GROUP_SPLIT_SUMMARY_PATH,
        summary_rows,
        [
            "protocol",
            "split",
            "n_total",
            "n_clickbait",
            "n_non_clickbait",
            "clickbait_rate",
            "share_of_dataset",
        ],
    )

    audit = audit_duplicates(by_title, original_split_by_id, group_split_by_id)
    audit["split_summary"] = summary_rows
    SPLIT_AUDIT_PATH.parent.mkdir(parents=True, exist_ok=True)
    SPLIT_AUDIT_PATH.write_text(json.dumps(audit, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"Wrote {PHASE2_DUP_PATH.relative_to(ROOT)}")
    print(f"Wrote {GROUP_SPLIT_PATH.relative_to(ROOT)}")
    print(f"Wrote {GROUP_SPLIT_SUMMARY_PATH.relative_to(ROOT)}")
    print(f"Wrote {SPLIT_AUDIT_PATH.relative_to(ROOT)}")
    print(json.dumps(audit, ensure_ascii=False, indent=2))


def run_benchmark() -> None:
    try:
        import numpy as np
        import pandas as pd
        from sklearn.ensemble import RandomForestClassifier
        from sklearn.feature_extraction.text import TfidfVectorizer
        from sklearn.linear_model import LogisticRegression
        from sklearn.metrics import (
            accuracy_score,
            average_precision_score,
            balanced_accuracy_score,
            f1_score,
            precision_recall_fscore_support,
            roc_auc_score,
        )
        from sklearn.naive_bayes import MultinomialNB
        from sklearn.pipeline import FeatureUnion, Pipeline
        from sklearn.svm import LinearSVC
    except ModuleNotFoundError as exc:
        raise SystemExit(
            "Benchmark requires pandas and scikit-learn. "
            "Run this command in the same environment used for Phase 4 notebooks.\n"
            f"Missing dependency: {exc.name}"
        ) from exc

    def compute_metrics(y_true, y_pred, y_score=None):
        precision, recall, f1, _ = precision_recall_fscore_support(
            y_true, y_pred, labels=[0, 1], zero_division=0
        )
        row = {
            "accuracy": accuracy_score(y_true, y_pred),
            "balanced_accuracy": balanced_accuracy_score(y_true, y_pred),
            "macro_f1": f1_score(y_true, y_pred, average="macro", zero_division=0),
            "weighted_f1": f1_score(y_true, y_pred, average="weighted", zero_division=0),
            "clickbait_precision": precision[1],
            "clickbait_recall": recall[1],
            "clickbait_f1": f1[1],
            "roc_auc": "",
            "pr_auc": "",
        }
        if y_score is not None and len(set(y_true)) == 2:
            row["roc_auc"] = roc_auc_score(y_true, y_score)
            row["pr_auc"] = average_precision_score(y_true, y_score)
        return row

    def add_result(results, model_name, feature_set, train_size, run_name, eval_df, y_pred, y_score=None):
        y_true = eval_df["label"].to_numpy()
        row = {
            "protocol": "random_group_stratified_70_10_20",
            "run_name": run_name,
            "model_name": model_name,
            "feature_set": feature_set,
            "train_size": train_size,
            "eval_size": len(eval_df),
        }
        row.update(compute_metrics(y_true, y_pred, y_score))
        results.append(row)

    def keyword_score(series):
        keywords = [
            "bất ngờ",
            "sốc",
            "không ngờ",
            "người này",
            "điều này",
            "sự thật",
            "lý do",
            "hé lộ",
            "gây chú ý",
            "khiến",
        ]
        text = series.fillna("").str.lower()
        score = np.zeros(len(text), dtype=float)
        for keyword in keywords:
            score += text.str.contains(keyword, regex=False).astype(float).to_numpy()
        score += text.str.contains(r"\?", regex=True).astype(float).to_numpy()
        return score

    def best_threshold(values, y_true):
        best = (None, -1.0)
        for threshold in sorted(set(values)):
            pred = (values >= threshold).astype(int)
            score = f1_score(y_true, pred, average="macro", zero_division=0)
            if score > best[1]:
                best = (threshold, score)
        return best[0]

    def build_vectorizer(kind):
        if kind == "word":
            return TfidfVectorizer(
                analyzer="word", ngram_range=(1, 2), min_df=2, max_df=0.95, sublinear_tf=True, lowercase=True
            )
        if kind == "char":
            return TfidfVectorizer(
                analyzer="char_wb", ngram_range=(3, 5), min_df=2, max_df=0.95, sublinear_tf=True, lowercase=True
            )
        if kind == "word_char":
            return FeatureUnion([("word", build_vectorizer("word")), ("char", build_vectorizer("char"))])
        raise ValueError(kind)

    def build_classifier(kind):
        if kind == "logreg":
            return LogisticRegression(max_iter=2000, class_weight="balanced", random_state=RANDOM_STATE)
        if kind == "svm":
            return LinearSVC(class_weight="balanced", random_state=RANDOM_STATE)
        if kind == "nb":
            return MultinomialNB()
        if kind == "rf":
            return RandomForestClassifier(
                n_estimators=300, class_weight="balanced", random_state=RANDOM_STATE, n_jobs=-1
            )
        raise ValueError(kind)

    specs = [
        ("tfidf_word_logreg", "word", "logreg"),
        ("tfidf_char_logreg", "char", "logreg"),
        ("tfidf_word_char_logreg", "word_char", "logreg"),
        ("tfidf_word_svm", "word", "svm"),
        ("tfidf_char_svm", "char", "svm"),
        ("tfidf_word_char_svm", "word_char", "svm"),
        ("tfidf_word_nb", "word", "nb"),
        ("tfidf_word_rf", "word", "rf"),
    ]

    features = pd.read_csv(FEATURES_PATH)
    split = pd.read_csv(GROUP_SPLIT_PATH)
    df = features.merge(split[["id", "split", "duplicate_group"]], on="id", how="inner")
    df["label"] = df["label"].astype(int)
    train_df = df[df["split"] == "train"].copy()
    val_df = df[df["split"] == "validation"].copy()
    test_df = df[df["split"] == "test"].copy()

    results = []
    y_train = train_df["label"].to_numpy()
    majority = int(pd.Series(y_train).mode().iloc[0])
    for run_name, eval_df in [("validation", val_df), ("test", test_df)]:
        add_result(
            results,
            "majority_class",
            "simple_rule",
            len(train_df),
            run_name,
            eval_df,
            np.full(len(eval_df), majority, dtype=int),
        )

    class_rate = y_train.mean()
    rng = np.random.default_rng(RANDOM_STATE)
    for run_name, eval_df in [("validation", val_df), ("test", test_df)]:
        y_score = np.full(len(eval_df), class_rate)
        y_pred = (rng.random(len(eval_df)) < class_rate).astype(int)
        add_result(results, "random_stratified", "simple_rule", len(train_df), run_name, eval_df, y_pred, y_score)

    length_threshold = best_threshold(val_df["title_char_len"].to_numpy(), val_df["label"].to_numpy())
    keyword_threshold = best_threshold(keyword_score(val_df["title"]), val_df["label"].to_numpy())
    for run_name, eval_df in [("validation", val_df), ("test", test_df)]:
        length_scores = eval_df["title_char_len"].to_numpy()
        add_result(
            results,
            f"length_heuristic_threshold_{length_threshold:.2f}",
            "simple_rule",
            len(train_df),
            run_name,
            eval_df,
            (length_scores >= length_threshold).astype(int),
            length_scores,
        )
        scores = keyword_score(eval_df["title"])
        add_result(
            results,
            f"keyword_heuristic_threshold_{keyword_threshold:.2f}",
            "simple_rule",
            len(train_df),
            run_name,
            eval_df,
            (scores >= keyword_threshold).astype(int),
            scores,
        )

    for model_name, vectorizer_kind, classifier_kind in specs:
        pipe = Pipeline([("tfidf", build_vectorizer(vectorizer_kind)), ("clf", build_classifier(classifier_kind))])
        pipe.fit(train_df["title"].fillna(""), y_train)
        for run_name, eval_df in [("validation", val_df), ("test", test_df)]:
            text = eval_df["title"].fillna("")
            y_pred = pipe.predict(text)
            clf = pipe.named_steps["clf"]
            if hasattr(clf, "predict_proba"):
                y_score = pipe.predict_proba(text)[:, 1]
            elif hasattr(clf, "decision_function"):
                y_score = pipe.decision_function(text)
            else:
                y_score = None
            add_result(results, model_name, "text_title", len(train_df), run_name, eval_df, y_pred, y_score)

    GROUP_PHASE4_DIR.mkdir(parents=True, exist_ok=True)
    result_df = pd.DataFrame(results)
    result_df = result_df.sort_values(["run_name", "macro_f1"], ascending=[True, False]).reset_index(drop=True)
    result_df.to_csv(GROUP_RESULTS_PATH, index=False)

    original = pd.read_csv(ROOT / "output/phase4/random_split_results.csv")
    original_test = original[original["run_name"] == "test"].copy()
    group_test = result_df[result_df["run_name"] == "test"].copy()
    compare_cols = ["model_name", "macro_f1", "clickbait_f1", "balanced_accuracy"]
    comparison = original_test[compare_cols].merge(group_test[compare_cols], on="model_name", suffixes=("_original", "_groupaware"))
    for metric in ["macro_f1", "clickbait_f1", "balanced_accuracy"]:
        comparison[f"{metric}_delta_groupaware_minus_original"] = (
            comparison[f"{metric}_groupaware"] - comparison[f"{metric}_original"]
        )
    comparison = comparison.sort_values("macro_f1_groupaware", ascending=False).reset_index(drop=True)
    comparison.to_csv(GROUP_COMPARISON_PATH, index=False)

    best = group_test.sort_values("macro_f1", ascending=False).iloc[0]
    summary = [
        "# Phase 4 Group-aware Benchmark Summary",
        "",
        "## Best Group-aware Test Model",
        "",
        f"- Model: `{best['model_name']}`",
        f"- Macro-F1: {best['macro_f1']:.4f}",
        f"- Clickbait F1: {best['clickbait_f1']:.4f}",
        f"- Balanced Accuracy: {best['balanced_accuracy']:.4f}",
        "",
        "## Outputs",
        "",
        f"- `{GROUP_RESULTS_PATH.relative_to(ROOT)}`",
        f"- `{GROUP_COMPARISON_PATH.relative_to(ROOT)}`",
        "",
        "## Notes",
        "",
        "- This benchmark uses `output/phase3/random_group_stratified_70_10_20.csv`.",
        "- Duplicate groups are kept within a single split.",
        "- Compare against original random split before drawing final conclusions.",
        "",
    ]
    GROUP_SUMMARY_PATH.write_text("\n".join(summary), encoding="utf-8")
    print(f"Wrote {GROUP_RESULTS_PATH.relative_to(ROOT)}")
    print(f"Wrote {GROUP_COMPARISON_PATH.relative_to(ROOT)}")
    print(f"Wrote {GROUP_SUMMARY_PATH.relative_to(ROOT)}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--split-only", action="store_true", help="Only create duplicate audit and group-aware split.")
    parser.add_argument("--benchmark-only", action="store_true", help="Only run benchmark from existing group-aware split.")
    args = parser.parse_args()

    if args.benchmark_only:
        run_benchmark()
        return
    run_split()
    if not args.split_only:
        run_benchmark()


if __name__ == "__main__":
    main()
