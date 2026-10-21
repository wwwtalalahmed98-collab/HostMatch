# Candidate assessment, version 1

**The question:** the four architectural requirements say what a universal
chassis must *be*. Which real organism comes closest?

**Answer: *Saccharomyces cerevisiae* on the evidence, *Yarrowia lipolytica* as
the robustness alternative. And the interesting part is not the winner — it is
that the field is already building toward what the rules predict, without having
stated the rules.**

**Honesty about method, up front.** I have **not** scored four organisms against
all 37 capabilities. That would require evidence I do not have, and inventing it
would be worse than useless. What follows scores candidates against the **four
architectural requirements**, which are defensible from the evidence gathered,
plus category-level assessment where quotes exist. Cells marked *unknown* are
unknown, not zero.

---

## Who is eligible

Requirements 1 and 2 — compartmentalised, and not a stripped-down cell — rule
out prokaryotes as the end state. That removes *E. coli*, *Bacillus subtilis*,
*Vibrio natriegens* and every minimal-cell derivative, including JCVI-syn3.0.

What is left: yeasts and filamentous fungi.

| Candidate | Why it is on the list |
|---|---|
| *Saccharomyces cerevisiae* | Best-tooled eukaryote; facultative anaerobe; GRAS |
| *Komagataella phaffii* (Pichia) | *"the protein master"*; best secretion; industrial |
| *Yarrowia lipolytica* | GRAS, robust, unusual substrate tolerance, strong acetyl-CoA flux |
| *Aspergillus oryzae* | GRAS; very large secretion capacity; handles big gene clusters |

---

## Scored against the four requirements

### 1. Compartmentalised

The requirement with the most evidence behind it, because peroxisome
engineering has quietly become a real field.

| Candidate | Evidence |
|---|---|
| ***S. cerevisiae*** | **Strongest.** *"Towards repurposing the yeast peroxisome for compartmentalizing heterologous metabolic pathways"*; *"Peroxisome compartmentalization of a toxic enzyme improves alkaloid production"* (*Nat Chem Biol*); *"ML-enhanced peroxisome capacity enables compartmentalization of multienzyme pathway"* — targeting **up to eight enzymes**; *"Towards designer organelles by subverting the peroxisomal import pathway"*; an **orthogonal** peroxisomal transport system built for sesquiterpenes |
| *K. phaffii* | Established — peroxisome targeting signals characterised and screened; an NADPH redox shuttle rewired into the peroxisome |
| *Y. lipolytica* | Demonstrated — organelle targeting improved astaxanthin synthesis |
| *A. oryzae* | Compartmentalised by nature; engineering less documented in what I found |

**The decisive precedent sits with *S. cerevisiae*:** *"Expression of a
functional **oxygen-labile nitrogenase** component in the **mitochondrial matrix
of aerobically grown yeast**."* That is conflict 1 — the oxygen conflict —
already solved experimentally, in this organism.

### 2. Not built from a minimal cell

All four pass. None is a minimised genome. *Y. lipolytica* scores highest on the
*spirit* of the rule — robustness — with *"innate oleaginous metabolism and
unusual tolerance for hydrophobic substrates"*, and an HR-proficient chassis
where *"cellular robustness parameters showed marked increases"*.

### 3. Switchable, not constitutive

| Candidate | Evidence |
|---|---|
| ***S. cerevisiae*** | dCas12a multiplexing (*"built-in RNase activity which can process a single CRISPR RNA array"*); a dual-mode dCas9 activator for *"graded and large-scale multiplex"* |
| ***Y. lipolytica*** | **Simultaneous editing, repression *and* activation of multiple genes** in one strain — the closest thing found to the required architecture |
| *K. phaffii*, *A. oryzae* | Less documented |

### 4. Nucleic-acid-addressed control

Same two lead. *S. cerevisiae* has the deepest CRISPR toolkit; *Y. lipolytica*
has the most complete demonstration.

---

## The capability categories, where evidence exists

| Category | *S. cerevisiae* | Note |
|---|---|---|
| Protein maturation | Strong | Glycan humanisation done; disulfides native |
| **Proteome headroom** | **Best measured anywhere** | *"exceeding **40% of total protein**"* while growing — versus 33% for *E. coli* |
| Cofactors / P450s | Strong | Extensive alkaloid, terpenoid and Taxol-precursor work; chaperone pairing with P450s |
| Precursor supply | Good | MVA pathway well engineered; *Y. lipolytica* better on acetyl-CoA |
| Compartments | Strongest | See above |
| **Oxygen range** | **Unusual advantage** | *"a **facultative organism** able to utilize both anaerobic and aerobic metabolism"* — so conflict 1 can also be resolved in *time*, not only in space |
| Tolerance | Unknown | Not assessed |
| Process / scale-up | Strong | Centuries of industrial use; GRAS |

**Known weaknesses of *S. cerevisiae*, stated:** the Crabtree effect means it
ferments to ethanol even with oxygen present, wasting carbon; native glycans are
high-mannose and need engineering; it is not the best secretor — *K. phaffii* is.

---

## Verdict

**Lead candidate: *Saccharomyces cerevisiae*.** It has the highest measured
proteome headroom of any host found, the deepest compartment-engineering
literature, a direct experimental precedent for the hardest conflict, a
facultative oxygen metabolism that offers a second route around that conflict,
mature nucleic-acid-addressed control, and GRAS status.

**Honest counterargument: it is also the obvious choice.** Everyone uses yeast.
Selecting it is not a bold claim, and the analysis should be suspected of having
walked to the nearest familiar answer. The test of whether the four rules are
doing real work is not that they select yeast — it is that they **rule out
JCVI-syn3.0 and all the prokaryotes**, which the field does not.

**Alternative worth keeping: *Yarrowia lipolytica***, if robustness turns out to
dominate. It is the only candidate where simultaneous editing, repression and
activation have been demonstrated together, and the only one described in terms
of *increased* robustness after engineering rather than decreased.

## The result that matters more than the winner

**The four rules were derived abstractly — from oxygen chemistry, redox
chemistry, published failures of genome minimisation, proteome arithmetic and
regulator counts. They had nothing to say about yeast.**

Yet multiple independent groups are already engineering yeast peroxisomes into
exactly the kind of insulated compartments the rules demand, up to eight enzymes
at a time, with orthogonal import systems. One group put an oxygen-poisoned
enzyme inside yeast mitochondria and kept it working in open air.

**The field is converging on the architecture without having written it down.**
That is weak evidence the rules are right — convergent, not confirmatory — and
it is the strongest argument this project currently has.

## What is not done

- **No scoring against the individual 37 capabilities.** Only four requirements
  and seven categories, and several categories are unassessed.
- **Tolerance (category F) is entirely unassessed** for every candidate, and the
  literature says tolerance is often the binding constraint.
- ***A. oryzae* and *K. phaffii* are thinly covered** relative to the other two.
  Their apparent weakness may be my search coverage, not their biology.
- **No quantitative comparison.** "Strong" and "best" are judgements from
  abstracts, not numbers on a common scale.
- **The gap list does not exist yet.** The point of naming a candidate is to say
  *what it still lacks*. That is the obvious next piece and it has not been
  written.
