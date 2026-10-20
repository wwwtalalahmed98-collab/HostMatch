# Conflict map, version 1

**The question:** are any two of the 37 capabilities mutually exclusive? If so,
no single host can cover all of them, and a universal chassis is impossible on
physical grounds rather than engineering ones.

**The answer so far: yes — two hard physical conflicts, and three structural
ones. All five have implications, and one of them overturns the obvious design
route.**

**Coverage warning, stated up front.** 37 capabilities make **666 possible
pairs**. I have examined **five**. This is a first pass aimed at the conflicts
most likely to exist, not a systematic sweep. Absence of a conflict below means
it was not looked for, not that it does not exist.

---

## Hard conflict 1 — oxygen

**C2 (functional P450 expression) requires molecular oxygen.**

> *"P450s … use **molecular oxygen** and the hydride donor NAD(P)H"*

**A whole class of enzymes is destroyed by it, irreversibly.**

> *"nitrogenase is **irreversibly inactivated** within a few minutes after
> exposure to oxygen; current studies on the heterologous expression of
> nitrogenase are limited to anaerobic conditions"*

> *"Because radicals **irreversibly react with dioxygen**, most of these enzymes
> occur in anaerobic bacteria and archaea"* — on radical SAM enzymes

> *"Most radical SAM enzymes are highly sensitive to oxygen, **which destroys
> their Fe–S clusters**"*

These cannot both be satisfied in one compartment at one time. Not a matter of
optimisation — the word in the literature is *irreversibly*.

**But it is resolvable, and nature and engineers have both done it:**

> *"Certain filamentous cyanobacteria protect nitrogenase from O₂ by
> **sequestering the enzyme within internally micro-oxic**"* compartments

> *"Expression of a functional **oxygen-labile nitrogenase** component in the
> **mitochondrial matrix of aerobically grown yeast**"*

The resolution is **spatial separation** — put the oxygen-hating chemistry in a
compartment the oxygen does not reach. A second resolution is **temporal
separation**: run the aerobic phase, then the anaerobic phase, in sequence.

## Hard conflict 2 — redox state

**B2 (disulfide bond formation) requires an oxidising environment. C3 (NADPH
supply) and general metabolism require a reducing one.**

> *"Both eukaryotic and prokaryotic organisms **keep their cytoplasm reduced**
> and, consequently, **disulfide bond formation is impaired** in this"*
> compartment

> *"Oxidative protein folding is **confined to few compartments**, including the
> endoplasmic reticulum, the mitochondrial intermembrane space and the bacterial
> periplasm"*

Same shape as conflict 1, same resolution: a separate compartment.

There is also an engineering workaround — CyDisCo strains co-express a
sulfhydryl oxidase and a disulfide isomerase to oxidise the cytoplasm directly.
**It is not free.** Analysis of those strains identifies *"stress responses
related to protein production, oxidative stress and accumulation of misfolded
protein"* and the need for *"dissecting and mitigating redox heterogeneity."*

---

## The consequence of conflicts 1 and 2

Both hard conflicts are resolved the same way, and only that way: **by having
more than one internal compartment.**

**This promotes E2 (subcellular compartmentalisation) from one capability among
37 to the enabling condition for universality itself.** Without compartments, a
chassis can have oxygen chemistry or oxygen-free chemistry, but not both; it can
form disulfides or run reducing metabolism, but not both. With compartments, it
can do all four.

A single-compartment cell cannot be universal. That is a structural result, not
an engineering difficulty.

---

## Structural conflict 3 — capability breadth versus the proteome budget

Every capability added costs the cell resources it cannot get back.

> *"the production of heterologous proteins that are often **useless to host
> cells** represents a **burden on resources**, which have to be shared with
> normal cellular processes"*

> three constraint layers: *"competition for gene expression resources, limited
> precursor availability and flux distribution"*

> *"The inherent conflict between cellular growth and product synthesis, arising
> from limited resource allocation and metabolic burden, **fundamentally
> constrains** the performance of microbial chassis"*

A cell has a finite proteome. Therefore **there is a ceiling on total
capability**, independent of cleverness. Thirty-seven capabilities expressed at
once may simply not fit.

**No clean resolution exists.** Partial ones: inducible expression (carry the
genes, express only what this product needs), and division of labour across a
microbial consortium rather than one organism — though a consortium is arguably
an admission that one universal host is not achievable.

## Structural conflict 4 — minimal versus universal

**This one overturns the obvious design route, and it is the most important
finding in this document.**

The intuitive path to a universal chassis is to start from a minimal cell — a
clean slate with nothing in the way — and add capabilities. JCVI-syn3.0, the
field's flagship "versatile platform", is exactly that.

The evidence says minimisation destroys the robustness universality requires:

> *"genome reduction is associated with **substantial loss of cell fitness** and
> accumulation of synthetic-sick interactions"*

> *"genome reduction can lead to undesired traits, such as **decreased growth
> rate and metabolic imbalances**"*

> *"The **decreased growth and perturbations in physiological phenotype** of some
> genome-reduced strains **may limit their applications** as optimized cell
> factories"*

> *"In many cases, however, **no performance improvements** with the streamlined
> chassis were obtained"*

> *"**Genome streamlining was costly** — but 80% of fitness was regained in 2000
> generations"*

> *"**Oxidative stress sensitivity** of engineered E. coli cells with a reduced
> genome"*

> *"genome reductions in MDS42 **did not stabilize** the chassis under metabolic
> stress"*

The capabilities lost to minimisation are precisely **F3 (stress response), G1
(growth rate), G3 (genetic stability) and G4 (culture-condition range)** — four
of the 37, and the ones that make a chassis usable outside a laboratory.

**Minimisation and universality pull in opposite directions.** You cannot strip
a genome to a clean slate and retain the robustness that covering 37
capabilities demands.

## Structural conflict 5 — growth versus production

Named repeatedly and treated in the field as fundamental rather than solvable.
Listed for completeness; it constrains every chassis equally and does not
distinguish between candidates.

---

## What this implies for the design

Three conclusions follow from the five conflicts, and the first two are
counter-intuitive:

1. **A universal chassis must be compartmentalised.** Conflicts 1 and 2 have no
   other resolution. This rules out single-compartment bacteria as the
   end-state, whatever their convenience.
2. **A universal chassis should not be built from a minimal cell.** Conflict 4
   says minimisation removes the robustness universality needs. The field's most
   celebrated "versatile platform" is, by this argument, the wrong starting
   point.
3. **Together, 1 and 2 point away from minimal bacteria and toward a
   compartmentalised, robust organism** — which in practice means a eukaryote, or
   a bacterium engineered to acquire compartments.

That is a design conclusion derived from physics and published failure, not from
preference. It is also testable: if someone demonstrates a single-compartment
chassis performing both oxygen-requiring and oxygen-destroyed chemistry, the
argument fails.

## What is not done

- **661 of 666 capability pairs have not been examined.** Five were chosen
  because they looked most likely to conflict. A systematic sweep has not
  happened and is the obvious next piece of work.
- **The quotes are from abstracts, not full papers.** None has been verified
  against the source text.
- **No quantification.** "Burden limits total capability" is established
  qualitatively. How many capabilities actually fit in one proteome is unknown
  and is the number that would decide whether universality is reachable.
- **Temporal separation is under-explored.** Running incompatible chemistries in
  sequence rather than in parallel may dissolve conflict 1 at the process level
  rather than the cellular one. Not investigated.
- **No eukaryotic candidate has been assessed.** Conclusion 3 points at
  eukaryotes; nothing has been scored.
