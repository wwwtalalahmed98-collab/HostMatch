# Tool specification, version 1

**The idea, as stated 2026-10-23:**

> *"we will build a **tool** of universal chassis that has an ability to make any
> protein based by required data, circuits, engineering principles — all the
> things that are necessary when someone in the future has built this in lab"*

**What this settles: we build software, not an organism.** The tool emits a
complete build specification for a universal protein chassis. Someone with a lab
builds it later. **This removes the single largest practical obstacle in the
project** — there is no wet-lab step on our side.

The chassis is now the tool's **output**, not our deliverable.

---

## What the tool takes in, and what it emits

| | |
|---|---|
| **In** | A target protein: sequence, and optionally its product class (enzyme, antibody fragment, therapeutic, vaccine antigen) |
| **Out** | A build specification: which chassis, which capability switches on, the genetic circuit, the DNA parts, the engineering rationale, the predicted bottleneck, the expected failure modes, and what to measure first |

The output is the thing a future lab reads. It must be **auditable** — every
recommendation carries the evidence behind it and a confidence, not a bare
answer.

---

## The six modules

### 1. Requirement extraction — what does *this* protein need?

Take the sequence, decide which of the 22 protein capabilities it requires.
Disulfide bonds, N-glycosylation sites, O-glycosylation sites, transmembrane
domains, GPI anchors, signal peptide, size.

**This module does not need inventing. The field has already defined the exact
schema.** pcSecYeast ships `ComplementaryData/Protein_Information.xlsx`, the
**Protein Specific Information Matrix (PSIM)**, which holds for every
*S. cerevisiae* protein:

> *"whether the protein is processed by secretory pathway, the existence of the
> signal peptide, **number of disulfide bond sites, N-glycosylation sites,
> O-glycosylation sites, transmembrane domains, GPI sites**, protein
> localization, protein amino acid sequence and signal peptide sequence"*

**That is the feature vector this project needed, already specified, already
populated, under GPL-3.0.** It is the same mapping as `capability-set-v1.md`
applied one protein at a time. The PSIM is the single most useful artifact found
in this project so far.

**Buildable now, in Python, without MATLAB** — the schema is a spreadsheet, and
the same features can be computed for a novel protein from UniProt plus standard
sequence predictors.

### 2. Capability matching — which switches must be on?

Map requirements onto the capability set: 22 required for proteins, of which
*S. cerevisiae* appears to hold 17 natively, leaving **5 to engineer** (large-CDS
capacity, humanised N-glycans, sugar-nucleotide supply, extra secretion, burden
control). See `scope-proteins-v1.md`.

**This is our own contribution and it exists as documents, not code.**

### 3. Bottleneck prediction — where will it fail?

Query a proteome-constrained secretory model. **pcSecYeast exists and is public**
(`github.com/SysBioChalmers/pcSecYeast`, GPL-3.0) and does precisely this:
*"identified overexpression targets for improved recombinant protein
production."*

**And it has been extended across species since.** `pcSecYeastSpecies`
(LiLabTsinghua, updated December 2025):

> *"we built on the pcSecYeast model for S. cerevisiae and developed
> proteome-constrained protein secretion models for **Komagataella phaffii** and
> **Kluyveromyces marxianus**… integrating genome-scale metabolism, detailed
> secretory pathway representations, **proteome allocation constraints**,
> temperature-dependent enzyme kinetics, and **humanized glycosylation
> modules**"*

Two things in that sentence matter a great deal:

- **Proteome allocation constraints** — the same constraint
  `proteome-budget-v1.md` was built on. The two halves of this project already
  speak one language.
- **Humanized glycosylation modules** — that is capability **B4**, one of our
  five engineering targets, already modelled.

And it covers *K. phaffii*, which `candidate-assessment-v1.md` named as the best
secretor. **Cross-species chassis comparison is already modelled.** We would not
be building that from nothing.

### 4. Circuit design — how are the switches wired?

Promoters, signal peptide choice, gene dosage, induction scheme, terminators,
and for five switches ordinary protein regulators suffice (see
`scope-proteins-v1.md` on why CRISPRa is no longer required).

**Not designed. No module exists for this in our repository.**

### 5. Specification output — the document a lab receives

Parts list, assembly plan, predicted titre range with its uncertainty, ranked
failure modes, and the first three experiments that would falsify the design.

**Not designed.**

### 6. Iteration — correct the design from results

Active learning over the configuration space, so measured results update the next
recommendation. The method is demonstrated elsewhere (4,000,000 cell-free
compositions; regulatory DNA; strain libraries) and **has never been aimed at
chassis configuration**.

**Not designed. This remains the published gap.**

---

## The blocker, stated plainly

**pcSecYeast and pcSecYeastSpecies both require MATLAB.** Specifically:

> *"MATLAB (R2020b or later), COBRA Toolbox for MATLAB, RAVEN Toolbox, solver
> SoPlex"*

MATLAB is commercial. This is a genuine obstacle, not a detail, and it has to be
resolved before module 3 can run. Three routes, in order of preference:

1. **A university MATLAB licence.** Many institutions have a site licence that
   covers students. This is the cheapest route if it exists.
2. **Treat the published results as a lookup rather than re-running the model.**
   The papers and their `Results/` directories contain simulation outputs. The
   tool could consume published predictions instead of generating new ones. This
   caps the tool at proteins already simulated — a real limitation.
3. **Re-implement the relevant constraints in Python** (COBRApy). This is a large
   piece of work and would be a research contribution on its own, not a weekend
   port. It should not be attempted first.

**A second warning sign:** pcSecYeast was **last updated 2021-07-20**, has **37
commits, 7 stars and 1 fork**. That is a research artifact accompanying a paper,
not maintained software. It may not run without repair. `pcSecYeastSpecies` is
much newer (December 2025) and is the better entry point.

---

## What the tool would be, that does not currently exist

The modelling science exists. **The tool does not.** What exists is MATLAB
research code that reproduces the figures in two papers, operated by its authors.

There is no software that takes an arbitrary target protein and returns a chassis
build specification. That is the thing being proposed, and it is a software and
integration contribution rather than a modelling one.

**This is a weaker scientific claim than "we discovered a new architecture" and a
much stronger practical one.** It is also achievable without a laboratory, which
is the point.

---

## Honest assessment of each module

| Module | Status | Blocked by |
|---|---|---|
| 1. Requirement extraction | **Schema exists and is populated** | Nothing |
| 2. Capability matching | Exists as documents, not code | Our own work |
| 3. Bottleneck prediction | **Model exists, needs MATLAB** | Licence; code age |
| 4. Circuit design | Not started | Design work |
| 5. Specification output | Not started | Design work |
| 6. Iteration / active learning | Not started — **this is the gap** | Research |

**Modules 1 and 2 can be built now with no new dependencies.** That is the
honest starting point, and it would produce something real: given a protein
sequence, a statement of which capabilities it needs and whether yeast has them.

---

## What is not done

- **No code written for any module.** This document is a specification, not an
  implementation. Nothing in the repository executes any part of the tool.
- **Neither model has been downloaded or run.** Everything about pcSecYeast and
  pcSecYeastSpecies comes from their README files and abstracts. Whether they run
  at all is unverified.
- **MATLAB availability is unresolved** and gates module 3.
- **The PSIM has not been inspected.** Its contents are described from the README
  only; the spreadsheet has not been opened or validated.
- **The repository is still named HostMatch**, from an earlier and now-rejected
  framing. The name no longer describes the project.
- **No accuracy claim can be made.** Module 3's predictions inherit whatever
  error pcSecYeast has, which we have not measured, and the Pichia scFv result
  (*"Structural Homology Fails to Predict Secretion Efficiency"*) says lookalike
  proteins diverge under identical engineering. **The tool must report
  uncertainty and what to test, not a confident single answer.**
- All quotes here are from README files and abstracts, not full papers.
