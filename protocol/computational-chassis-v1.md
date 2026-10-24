# The computational chassis, version 1

**The idea, as stated 2026-10-24:**

> *"a tool that will be **the computational universal chassis** and that has an
> ability to make any protein based on genomic, metabolic, genetic circuits,
> data and all the other relevant data and principles that the field has
> established by research and are necessary when someone in the future want to
> build this in lab"*

**This is a different architecture from yesterday's, and the difference matters.**

Yesterday the project was a *pipeline that recommends a chassis*. Today the
chassis **is** the object: a machine-readable organism definition that integrates
the field's established data and principles, can be queried for any protein, and
is itself the blueprint a future lab would build from.

The tool does not *produce* a specification. **The tool is the chassis, and a
specification is what falls out when you query it.**

---

## Why that distinction is not word games

A recommender is a function. A chassis object is a **model of an organism** —
versioned, inspectable, citable, and arguable with. The consequences are
concrete:

| | Recommender pipeline | Chassis as an object |
|---|---|---|
| What you ship | Code that returns answers | A definition others can read, fork and dispute |
| What is reviewable | Outputs, one at a time | The organism design itself, all at once |
| Where evidence lives | Scattered in the code | Attached to each capability, with its quote |
| What a lab receives | A report | The design, plus a report derived from it |
| How it improves | Retrain or rewrite | Edit the definition; version it |

**Genome-scale models already work this way, which is why this framing is the
right one.** pcSecYeast is exactly this: a curated model object plus solvers.

---

## The novelty, stated precisely

**pcSecYeast models the yeast that exists. This project models the yeast that
should exist.**

That is the whole contribution in one sentence, and it is worth being careful
about:

- pcSecYeast and `pcSecYeastSpecies` are proteome-constrained models of **extant
  organisms** — wild-type *S. cerevisiae*, *K. phaffii*, *K. marxianus*, with
  some engineering modules such as humanised glycosylation.
- **UCP-1** (this project's object, in `chassis/chassis-v1.json`) is a definition
  of a **universal protein chassis that no laboratory has built** — the base
  organism plus five engineered capability modules, each carrying its published
  precedent, its missing cost, and its confidence.

**So the object describes a hypothetical organism.** That is the source of its
value and the source of its principal risk, and both must be stated in the same
breath. Every prediction it supports is a prediction about something that does
not exist yet.

---

## What exists now, and runs

### `chassis/chassis-v1.json` — the chassis object

The organism, written down. Contents:

- **Base organism** with its measured proteome headroom (40% of total protein)
  and its stated selection caveat (yeast is also the obvious choice).
- **22 capabilities** required for protein production, each with: category,
  binary or graded, **native / engineered / partly native** status, what triggers
  it, a confidence, and a note.
- **5 engineered modules** (`MOD-glycan`, `MOD-sugarnt`, `MOD-secretion`,
  `MOD-largecds`, `MOD-burden`), each with its goal, parts list, published
  precedent, **and an explicit `cost_status` of "not measured"**.
- **4 global constraints** — proteome budget, single-protein ceiling, regulator
  count, and the redox constraint with its resolution.
- **`what_this_object_cannot_do`** — a field in the object itself, so the
  limitations travel with the data rather than living in a separate document.
- **`provenance`** — every claim points back to the protocol file it came from.

### `scripts/chassis_resolve.py` — querying the chassis

Takes a protein sequence. Computes what the protein needs. Reports which chassis
capabilities go active, which are native, which require an engineered module, and
what cannot be concluded.

```
python -I scripts/chassis_resolve.py
python -I scripts/chassis_resolve.py --fasta my_targets.fasta --class therapeutic
```

**This is modules 1 and 2 of `tool-spec-v1.md`, working, in Python, with no
MATLAB and no external model.** It is the first part of this project that
executes rather than describes.

### What it produced on two real proteins

| | Human preproinsulin | Human erythropoietin |
|---|---|---|
| Capabilities active | 16 of 22 | 19 of 22 |
| Native to yeast | 14 | 15 |
| **Need engineering** | **2** | **4** |
| Modules to build | secretion, burden | + glycan, sugar-nucleotide |

The EPO result is the interesting one: **three N-glycosylation sequons at
residues 24, 38 and 83.** Those are the positions the literature reports for
erythropoietin. The sequon scan is sequence-exact rather than predictive, so this
is a correctness check rather than a discovery — but it is a check the code
passes.

And the resolver reaches the right conclusion for the right reason: EPO is a
**glycosylated therapeutic**, so it pulls in `MOD-glycan`, which pulls in
`MOD-sugarnt` to feed it. Insulin, having no sequons, does not. **The chassis
configures differently for different proteins, which is the behaviour the whole
idea rests on.**

---

## A failure worth recording

The signal-peptide heuristic **initially returned `False` for human
preproinsulin**, which carries a textbook signal peptide. The cause was
averaging hydropathy over a fixed N-terminal slice, which dilutes the short
hydrophobic h-region with the charged n-region and polar c-region on either side.

**The fix was principled rather than fitted:** scan short windows and take the
strongest, which is what the biology actually says. Preproinsulin now reads
`True` and mature EPO still reads `False` — both correct.

**The threshold was not tuned to make the example pass.** That distinction
matters, because tuning a constant until one test case agrees produces a number
that means nothing on the next protein.

Both the signal-peptide and transmembrane calls remain **heuristics**, labelled
as such in every run. The real answers need SignalP and DeepTMHMM.

---

## What the object still cannot do

- **No titre, yield or probability of success.** Module 3 — the
  proteome-constrained simulation — is not implemented, and is gated on MATLAB.
- **No engineered module has a measured proteome cost**, so the 40% budget
  constraint is recorded in the object but **cannot be checked against a
  resolved configuration**. The arithmetic that justified the architecture
  cannot yet be run on an actual answer.
- **O-glycosylation and other PTMs are not computable** from sequence here and
  come back as unknown, not as zero.
- **Confidences are judgement, not calibration.** They are the author's reading
  of abstracts and README files.
- **Tolerance (F3, F4) is the least assessed area** in the whole project, and the
  literature repeatedly names tolerance as the binding constraint on production.
- **The object describes an organism nobody has built.** Its internal
  consistency has been checked; its correspondence to reality has not and cannot
  be, until someone builds it.
- **No external validation.** Two proteins, chosen by the author, is not a test
  set. There is no held-out comparison against measured expression outcomes.
- **The repository is still named HostMatch**, from a framing that was rejected
  several checkpoints ago.
