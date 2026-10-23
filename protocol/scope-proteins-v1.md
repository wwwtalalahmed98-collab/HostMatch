# Scope, version 1: proteins, and a design layer that reads data

**The stated idea, as of 2026-10-23:**

> *"design a universal chassis that can produce any protein based on data that is
> available — either genomic, metabolomic or genetic circuits … a system that
> will produce everything based on data that is required and available"*

This is **narrower in the product** and **wider in the deliverable** than what the
project had been assuming. Both changes are recorded here, with their
consequences, including the ones that weaken earlier conclusions.

---

## Change 1 — the product is a protein

Everything in `capability-set-v1.md` was built for "any product in
biotechnology": proteins, small molecules and materials. Filtering the set to
proteins only (reproduce with `python -I scripts/protein_scope.py`):

| | count |
|---|---:|
| Capabilities in the full set | 37 |
| **Required for protein production** | **22** |
| Dropped (small-molecule or materials only) | 15 |

**What drops out:** the entire cofactor category (C1–C5: heme, P450s, NADPH, SAM,
Fe-S), three of five precursor pathways (acetyl-CoA, isoprenoids, shikimate),
membrane capacity for anchored enzymes, subcellular compartmentalisation of toxic
intermediates, product-toxicity tolerance and efflux, multi-gene cluster
balancing, and repeat stability.

### This costs us our best piece of evidence

**Conflict 1 — the oxygen conflict — was the hardest problem in
`conflict-map-v1.md`, and it is now mostly out of scope.** It was a conflict
between **P450s needing oxygen** and **nitrogenase and radical-SAM enzymes being
destroyed by it**. P450s are C2. Nitrogenase and radical SAM are C5. Both are
small-molecule capabilities. Both just dropped.

So the precedent I presented as decisive on 2026-10-21 — *"a functional
oxygen-labile nitrogenase component in the mitochondrial matrix of aerobically
grown yeast"* — **no longer supports the design.** It is still a remarkable
result. It is no longer load-bearing for a protein chassis. The candidate
assessment's headline argument is weaker than I stated it.

**Conflict 2 survives, and it is the protein one.** Disulfide bonds need an
oxidising compartment; *"Both eukaryotic and prokaryotic organisms keep their
cytoplasm reduced."* That is B2, which is required.

**So requirement 1 (compartmentalised) survives — for a much more ordinary
reason.** The compartment a protein chassis needs is the **endoplasmic reticulum
and the secretory pathway**, which every eukaryote already has. We no longer need
to build designer organelles. We need to use and tune the ones that are there.
That is a large reduction in difficulty and a large reduction in novelty.

### And it makes the proteome arithmetic easy instead of tight

Of the 22 required capabilities, how many does *S. cerevisiae* already have
natively? **This split is my judgement from the literature in
`candidate-assessment-v1.md`, not a measurement.**

| | count |
|---|---:|
| Already native in *S. cerevisiae* | 17 |
| **Must be engineered in** | **5** |

The five: **A4** large-CDS capacity, **B4** humanised N-glycans, **D5**
sugar-nucleotide supply for those glycans, **E3** secretion capacity beyond
native, **G2** burden control.

| | break-even cost per capability |
|---|---:|
| When the target was all 37, constitutive | **1.08%** of proteome |
| With 5 engineered capabilities, constitutive | **8.0%** of proteome |

**Consequence: requirement 3 weakens.** `proteome-budget-v1.md` concluded the
chassis *must* be switchable because constitutive expression of 37 capabilities
was arithmetically impossible. At five capabilities it is comfortably possible.
Switching is now an **optimisation**, not a necessity.

**Consequence: requirement 4 weakens further.** `regulatory-capacity-v1.md`
concluded control must be nucleic-acid-addressed because protein transcription
factors cannot reach 37 distinct addresses. They can easily reach five — the
field's routine *"LacI, TetR and cI"* nearly covers it. **CRISPRa is no longer
required.** It remains the better choice if the capability count grows.

**Two of the four architectural requirements were consequences of the
37-capability target. Narrowing to proteins removes the pressure that produced
them.**

---

## Change 2 — the deliverable includes a design layer

The new half of the idea: the system takes **available data** and decides what to
build. The question that decides whether this is possible is **what data exists**.

### Leg 1 — sequence to outcome, statistical. Mature, plateaued, and E. coli.

There are dozens of models predicting whether a protein will express solubly from
its sequence alone: NetSolP, SoluProt, DeepSol, PaRSnIP, EPSOL, PLM_Sol, GATSol,
ProtSATT, DSResSol, SurfSol, DeepSoluE, RP3Net, PROSO II.

**Almost every one is *E. coli*.** Across roughly 40 search results I found one
*B. subtilis* model, one wheat-germ cell-free system, and no *S. cerevisiae*
model at all.

And the field says it has stopped improving:

> *"Sequence-based predictors of recombinant protein solubility in Escherichia
> coli have **plateaued** (NESG independent-test AUC 0.760 → ~0.80 over **eight
> years** of protein-language-model variants). The plateau hides a latent
> confound: **the centrifugation regime** used to…"* (Aiki-Sol, 2026)

**Eight years of better language models bought about four points of AUC, and a
2026 preprint attributes the ceiling to how hard the tube was spun — a
measurement artefact in the labels, not a limit of the algorithms.** A bigger
model will not fix this.

These models also predict the **wrong variable**. They output *will this protein
be soluble*. The design layer needs *which configuration should I build*.

### Leg 2 — mechanistic model to configuration. Exists, for yeast, and is the right shape.

> *"we present the **first proteome-constrained genome-scale protein secretory
> model** of a eukaryal cell, namely for the yeast **Saccharomyces cerevisiae**
> (**pcSecYeast**). We used pcSecYeast to **simulate various recombinant proteins
> production** and **identified overexpression targets** for improved recombinant
> protein production"* (*Nature Communications*, 2022)

**This is the closest thing in the literature to the design layer being
described.** It takes a recombinant protein, simulates its production, and
outputs **which genes to overexpress**. It is specific to the lead candidate
organism. And it is **proteome-constrained** — the same constraint
`proteome-budget-v1.md` was built around, which means the two halves of this
project speak the same language.

Also in this leg: **MaLPHAS** — *"Prediction of strain engineerings that amplify
recombinant protein secretion"*. And genome-scale metabolic models of yeast
(Yeast9) coupled to ML, though the published coupling optimises **biomass**, not
the production of a named heterologous protein.

### Leg 3 — closed-loop active learning. Demonstrated, but never on this problem.

> *"an **active learning** approach to explore a combinatorial space of
> **~4,000,000 cell-free compositions**"* (*Nature Communications*, 2020)

Also: *"Optimization of regulatory DNA with active learning"* (2025);
*"Iterative algorithm-guided design of **massive strain libraries**"* applied in
yeast; Active Learning-assisted Directed Evolution; *"Learning protein function
through **autonomous experimental interaction**"* — a 2026 closed loop where
agents design variants, a robot builds and measures them, and the system chooses
the next experiment.

**The method works. It has been pointed at cell-free mixtures, promoters, enzyme
variants and strain libraries. It has not been pointed at "choose the chassis
configuration for an arbitrary target protein."**

### Leg 4 — metabolomic input. The weakest leg, and it is in the stated idea.

The idea names metabolomic data as an input. **I did not find a dataset pairing
per-protein metabolomic state with that protein's expression outcome.** The
metabolic-model work I found optimises growth or small-molecule flux. If
metabolomics is to be an input, that link has to be made rather than reused, and
I should not pretend otherwise.

---

## The gap, stated precisely

Three things exist separately:

1. A **mechanistic yeast secretory model** that, given a protein, proposes which
   genes to overexpress (pcSecYeast).
2. **Active-learning methods** that efficiently search large configuration spaces
   with few experiments.
3. A **sequence-level predictive layer** — mature but plateaued, and for the
   wrong organism.

**Nobody has connected 1 to 2.** There is a model that can propose a
configuration for a given protein, and there are methods that can test proposals
efficiently, and no published system closes the loop between them for arbitrary
target proteins.

**That loop is the project.** Restated as a buildable claim:

> A chassis with a small number of engineered capability switches (5, not 37),
> plus a decision layer that reads a target protein sequence, queries a
> proteome-constrained secretory model for the predicted bottleneck, and selects
> which switches to turn on — iterating as results come back.

This is software plus a defined wet-lab loop, not a new organism.

---

## The strongest counter-evidence, stated plainly

A 2025 paper, on the lead organism's close relative:

> ***"Structural Homology Fails to Predict Secretion Efficiency in Pichia
> pastoris: Divergent Responses of Architecturally Similar scFvs to
> Multi-Parametric Genetic Engineering"***

Two proteins that look alike responded **differently** to the *same* engineering —
gene dosage, cassette design, and ER pathway reprogramming. **That is a direct
negative result against the core premise of a sequence-driven design layer.**

It does not kill the idea. It constrains it: it argues the loop cannot be
open-loop prediction, and must be **iterative**, measuring and correcting — which
is an argument *for* leg 3 and *against* relying on leg 1. But it is the single
most important paper to read in full before committing to this design.

---

## What is not done

- **The 17-native / 5-engineered split is my judgement, not a measurement.** It
  comes from reading abstracts, not from a per-capability verification in
  *S. cerevisiae*. The count could move either way.
- **The earlier documents have not been revised.** `conflict-map-v1.md`,
  `proteome-budget-v1.md`, `regulatory-capacity-v1.md` and
  `candidate-assessment-v1.md` still argue from the 37-capability target. Their
  conclusions about requirements 3 and 4 are now overstated for a protein-only
  scope. They are left in place as the record of how the reasoning went.
- **pcSecYeast has not been obtained or run.** Everything said about it here
  comes from its abstract. Whether it is usable, documented, or covers proteins
  other than the ones it was demonstrated on is unverified.
- **The Pichia scFv negative result is from its abstract.** It is the most
  consequential paper found and it has not been read in full.
- **No capability has been scored against the 22** individually with evidence.
- **The metabolomic leg has no identified data source.**
- **All quotes here are from abstracts.**
