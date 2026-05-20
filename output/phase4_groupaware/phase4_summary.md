# Phase 4 Group-aware Benchmark Summary

## Best Group-aware Test Model

- Model: `tfidf_word_logreg`
- Macro-F1: 0.7361
- Clickbait F1: 0.6476
- Balanced Accuracy: 0.7451

## Outputs

- `output/phase4_groupaware/random_split_results.csv`
- `output/phase4_groupaware/groupaware_vs_original_comparison.csv`

## Notes

- This benchmark uses `output/phase3/random_group_stratified_70_10_20.csv`.
- Duplicate groups are kept within a single split.
- Compare against original random split before drawing final conclusions.
