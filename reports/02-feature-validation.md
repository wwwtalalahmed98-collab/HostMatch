# Feature validation against UniProt

**The first test of this project's code against evidence it did not choose.**

Reproduce with `python -I scripts/validate_features.py`. Per-protein numbers in
`02-feature-validation.tsv`. The script imports the real resolver rather than
reimplementing it, so what is measured is the code that ships.

---

## What was tested, and what was not

The resolver decides which capabilities a protein needs by reading features off
its sequence. Those features are checkable: UniProt carries curated, largely
experimental annotations for the same properties.

**Tested:** N-glycosylation sites, disulfide bonds, signal peptide,
transmembrane segments, on **24 human and chicken proteins** — 16 secreted (the
resolver's intended domain), 5 cytosolic, 3 membrane.

**Not tested:** whether the capability-to-module mapping is correct, or whether
any of these would express in yeast. **No expression data was used, because this
project has none.** This validates the tool's perception, not its judgement.

---

## Two bugs were found in the validator before any in the resolver

**First: glycation counted as glycosylation.** UniProt annotates non-enzymatic
glucose adducts on lysine as *"N-linked (Glc) (glycation) lysine"*. My first
pass matched on `n-linked` and swept up **32 such sites**. That made serum
albumin appear to have 24 N-glycosylation sites and haemoglobin 6 — both are
famously not N-glycosylated; haemoglobin glycation is what HbA1c measures. The
first run reported **54% recall**. It was wrong.

**Second: variant-only sites.** Albumin's only asparagine-linked annotations are
*"in variant Redhill"* and *"in variant Casebrook"*. At position 518 the
reference residue is aspartate, so no sequon can exist there at all. **2 sites
excluded.**

**Corrected recall: 96%.** Both corrections made the tool look better, which is
why they are recorded here rather than quietly applied.

---

## Results

### N-glycosylation — the sequon scan works

| | |
|---|---|
| Annotated sites found | **43 of 45 — 96% recall** |
| Sequons that are not actually glycosylated | 17 — **72% precision** |

The scan finds **potential** sites. Not every N-X-S/T sequon is used by the
cell, so over-prediction is expected behaviour rather than a defect: for the
binary decision the resolver makes — *does this protein need glycosylation
capability* — one real site is enough.

### Disulfide bonds — the weakest part of the resolver

| | |
|---|---|
| Exactly right | 7 of 24 — **29%** |
| A valid upper bound | 21 of 24 — **88%** |

The resolver computes `cysteine_count // 2` and reports it as *"up to N pairs"*.
As an upper bound it **fails on three proteins**:

| Protein | Annotated bonds | Resolver says |
|---|---:|---:|
| Complement C3 | 14 | 13 |
| Haptoglobin | 7 | 6 |
| Ig gamma-1 chain C region | 8 | 5 |

**Cause: inter-chain disulfides.** A cysteine can bond to a *different* molecule
— an antibody heavy chain to its light chain, haptoglobin across its subunits.
Counting one chain's cysteines and halving them cannot see those, so the stated
upper bound is not actually an upper bound. **This is a real defect and it is
not currently disclosed in the resolver's output.**

### Signal peptide and transmembrane — 88% each

| Heuristic | Correct | The failures |
|---|---|---|
| Signal peptide | 21 of 24 | Missed IGF-1. False positive on Ig gamma-1 C region and GLUT1 |
| Transmembrane | 21 of 24 | **All three failures are false positives on secreted proteins**: alpha-1-antitrypsin, tPA, complement C3 |

The transmembrane failures are systematic rather than random: large secreted
proteins contain hydrophobic stretches that a window-scan cannot distinguish
from a membrane-spanning helix. **Both calls remain labelled `[HEURISTIC]` in
every run**, and the fix is SignalP and DeepTMHMM rather than a better threshold.

### O-glycosylation — honestly unknown

**5 of 24** proteins are O-glycosylated according to UniProt. The resolver
reports *unknown* for every one, which is correct behaviour and a real
limitation: it cannot see a modification that five of these products need.

---

## The number that matters: does the error change the decision?

The resolver does not output site counts to a user. It outputs **which
capabilities switch on**. Measured at that level:

| | All 24 proteins | **Secreted only (n=16)** |
|---|---|---|
| Glycosylation decision correct | 22 of 24 | **16 of 16** |
| Disulfide decision correct | 17 of 24 | **15 of 16** |

**Inside its intended domain the resolver gets the glycosylation decision right
every time, and the disulfide decision right 15 times out of 16.**

Outside that domain it degrades in one specific way. Seven proteins have the
disulfide capability **wrongly switched on** — GAPDH, beta-actin,
phosphoglycerate kinase, haemoglobin beta, GLUT1, MDR1, and alpha-1-antitrypsin.
Every one is a case of **free cysteines that do not form bonds**. The rule
assumes every cysteine pairs, and in a reducing cytosol they do not.

That failure has a principled fix, and it is already written down in this
project: **conflict 2 of `protocol/conflict-map-v1.md`** records that the
cytoplasm is kept reduced and disulfides need an oxidising compartment. So a
cytosolically-retained product with cysteines does not need the native disulfide
capability — it needs *engineered* cytoplasmic disulfide machinery, which is a
different answer, not the same one. The resolver currently conflates them.

---

## What should change in the code

1. **`cysteine_pairs` must stop being described as an upper bound** until
   inter-chain disulfides are handled. Three proteins in 24 break it.
2. **B2 should branch on secretion.** Cysteines plus secretion means the native
   ER handles it. Cysteines plus intracellular retention is a problem needing an
   engineered module, not a satisfied native capability.
3. **Replace both hydropathy heuristics** with SignalP and DeepTMHMM. 88% is not
   good enough for a call that feeds a build specification.

**None of these has been done.** This report is the evidence that they are
needed.

---

## What this still does not establish

- **Nothing here says any protein would express in yeast.** Feature extraction
  being right does not make the chassis design right.
- **24 proteins is small**, and they are well-studied ones with good annotation,
  which is the easy case.
- **UniProt annotation is not ground truth everywhere.** Some entries are
  predicted rather than observed, and this analysis did not filter by evidence
  code.
- **The capability-to-module mapping remains completely untested.**
- **No measured proteome cost exists for any module**, so the budget constraint
  still cannot be checked against a real configuration.
