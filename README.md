# Multi-host protein expression prediction

Building the first harmonised, paired protein-host expression outcome dataset,
and a model that recommends an expression chassis from protein sequence.

**Status:** goal reset to a universal chassis. See docs/PROJECT-STORY.md.

Every expression predictor in the literature is E. coli-only. This project
asks which host to use, not whether E. coli will work.

## Layout
- `protocol/`  decisions frozen BEFORE extraction (see protocol/README.md)
- `data/raw/`  fetched sources, not committed
- `scripts/`   fetch, extract, harmonise
- `reports/`   findings

## Rule
Nothing in `data/interim/` is produced before `protocol/` is committed and tagged.
