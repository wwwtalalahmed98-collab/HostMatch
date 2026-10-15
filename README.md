# Multi-host protein expression prediction

Building the first harmonised, paired protein-host expression outcome dataset,
and a model that recommends an expression chassis from protein sequence.

**Status:** Phase 0 - protocol. No extraction has begun.

Every expression predictor in the literature is E. coli-only. This project
asks which host to use, not whether E. coli will work.

## Layout
- `protocol/`  decisions frozen BEFORE extraction (see protocol/README.md)
- `data/raw/`  fetched sources, not committed
- `scripts/`   fetch, extract, harmonise
- `reports/`   findings

## Rule
Nothing in `data/interim/` is produced before `protocol/` is committed and tagged.
