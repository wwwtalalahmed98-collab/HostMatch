# Proteome budget, version 1

**The question that could have killed the project:** a cell has a finite protein
budget. Can one cell carry all 37 capabilities at once, or does the budget make
universality arithmetically impossible?

**Answer: the budget does not kill it. But it dictates the architecture — the
capabilities must be switchable, not permanently switched on.**

Reproduce with `python -I scripts/proteome_budget.py`.

---

## The measured numbers

| Quantity | Value | Source |
|---|---|---|
| Max heterologous protein, *E. coli* | **33% of total protein** | *"we estimated the maximum capacities of the cell for heterologous expression to be 46% of the total RNA and the **33% of the total protein**"* |
| Max heterologous protein, yeast | **>40%** | *"These proteins can be expressed at levels **exceeding 40% of total protein** while maintaining yeast growth"* |
| Ceiling for one single protein | **up to 15%** | *"The limits of some glycolytic proteins were **up to 15% of the total cellular protein**"* |
| Unused proteome in some conditions | **~50%** | *"nearly **half of the proteome mass is unused** in certain environments, and accounting for the cost of this unused protein expression explains >95% of the variance in growth rates"* |
| Permanent ribosome over-provision | **~8%** | *"cells produce excess ribosomal proteins, amounting to a constant **≈8% of the proteome**"* |

So the working budget is **roughly a third of the cell's protein**, with a
further reserve that exists for a reason — adaptation — and cannot be taken
without cost. (That reserve is the same robustness that minimisation destroys;
see `conflict-map-v1.md`, conflict 4.)

## Scenario 1 — everything switched on at once

Divide the budget by the cost of one capability.

| Cost per capability | *E. coli* fits | Yeast fits | Enough for 37? |
|---:|---:|---:|---|
| 0.5% | 66 | 80 | yes |
| 1.0% | 33 | 40 | yes |
| **2.0%** | **16** | **20** | **no** |
| 3.0% | 11 | 13 | no |
| 5.0% | 6 | 8 | no |
| 10.0% | 3 | 4 | no |

**Break-even: every one of the 37 would have to cost under 1.08% of proteome.**

That is plausible for a capability that is one enzyme. It is not plausible for
the expensive ones. **Human-like N-glycosylation** is a multi-step pathway plus
sugar-nucleotide supply. **Functional P450 expression** needs the enzyme, a
redox partner and membrane capacity. **Compartmentalisation** means building
organelles.

**So constitutive universality fails — not on the average capability, but
because one or two expensive ones exhaust the budget alone.**

## Scenario 2 — carried silent, switched on per product

No product needs all 37. A given product needs the always-on basics plus a
product-specific handful — call it 5 to 12.

| Cost per capability | 5 on | 12 on | Fits the 33% budget? |
|---:|---:|---:|---|
| 0.5% | 2.5% | 6.0% | yes |
| 1.0% | 5.0% | 12.0% | yes |
| 2.0% | 10.0% | 24.0% | yes |
| 3.0% | 15.0% | 36.0% | borderline |
| 5.0% | 25.0% | 60.0% | no |

**Switchable universality works while a capability costs under about 2.8% of
proteome** — demanding, but not absurd, and well above the 1.08% that
constitutive expression would require.

## The design conclusion

**The chassis carries every capability in its genome and expresses only the
subset the current product needs.**

Genome capacity is not the constraint — genomes hold megabases, and a 106 kb
biosynthetic cluster has already been assembled and expressed heterologously.
**Proteome capacity is the constraint, and it applies per product rather than
per chassis.**

This is the third architectural requirement the analysis has produced:

1. The chassis must be **compartmentalised** (conflict map, conflicts 1 and 2)
2. The chassis must **not be built from a minimal cell** (conflict 4)
3. The chassis must be **switchable, not constitutive** (this document)

## What this creates: a new conflict

Switchability needs **37 independent switches that do not interfere with each
other**. That runs straight into a limit the field already names:

> *"the scale and complexity of genetic circuits are limited by a **shortage of
> composable, programmable, and orthogonal regulatory parts**"*

**Conflict 6, for the conflict map: capability breadth requires regulatory
breadth, and orthogonal regulatory parts are themselves scarce.** This may be
the real ceiling on universality — not metabolism, but control. It has not been
quantified and should be next.

## What is not done

- **The per-capability cost is swept, not measured.** Nobody has published the
  proteome cost of a capability as defined here. The whole analysis is a
  sensitivity sweep across a plausible range, and the conclusion holds across
  that range — but a measured value would replace an argument with a number.
- **The 5–12 capabilities-per-product figure is reasoned, not measured.** It
  comes from reading the capability set, not from data.
- **Costs are treated as additive.** They may not be. Capabilities that share
  cofactors or precursors could be cheaper together, or compete and be more
  expensive.
- **The silent-DNA cost is ignored.** Carrying 37 capabilities' worth of unused
  genes has replication and genetic-stability costs (G3) that are not in this
  arithmetic.
- **Quotes are from abstracts** and have not been checked against full papers.
