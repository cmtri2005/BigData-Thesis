# Phase 6 Discussion Points

## Benchmark

- Best random split model: `tfidf_word_logreg` with Macro-F1 = 0.7259 and Clickbait F1 = 0.6429.
- Best k-fold model by mean Macro-F1: `tfidf_word_char_logreg` with Macro-F1 mean = 0.7464 ± 0.0048.
- Accuracy should remain secondary because the majority baseline has non-trivial accuracy but zero Clickbait F1.

## Domain Robustness

- Hardest held-out domain by Macro-F1: `category` = `Giải trí & Showbiz` using `tfidf_word_svm`; Macro-F1 = 0.5708.
- Largest Macro-F1 drop: `category` = `Giải trí & Showbiz` using `tfidf_word_svm`; drop = 0.1476.
- Largest Clickbait F1 drop: `category` = `Tin tức tổng hợp` using `tfidf_word_logreg`; drop = 0.3385.

## Error Analysis

- Best model error counts on random test: `{'TN': 360, 'FN': 60, 'FP': 110, 'TP': 153}`.
- The model produces more false positives (110) than false negatives (60), suggesting a tendency to over-predict clickbait for some informative but attention-grabbing headlines.
- Taxonomy annotation is complete; the most frequent annotated error category overall is `FP_emotional_but_informative` under `FP` (21 cases, 0.21 overall).

## Explainability

- Logistic Regression coefficients should be described as lexical associations, not causal explanations.
- Top clickbait cues can support analysis of Vietnamese curiosity/question framing, while top non-clickbait cues often reflect official/news discourse.
