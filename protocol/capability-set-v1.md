# The capability set, version 1

**Status:** first draft. Derived from literature, not exhaustive. Expect it to
change once we try to score real hosts against it — that is what a v1 is for.

## Why this document exists

"A chassis that produces everything" cannot be worked on. The product space is
infinite and untestable.

**A chassis that covers every capability** can be worked on. Products do not
demand infinite things from their host — they demand a finite set of abilities,
in combinations. Enumerate the abilities, score every host against them, and
"universal" becomes a measurable claim instead of a slogan.

This document is that enumeration.

## The rule for inclusion

A capability belongs on this list only if the literature names it as something
that **blocks production when absent**. Not "would be nice", but "this is why
that product cannot be made in that host".

Each entry below carries the evidence that put it there.

---

## A. Genetic expression

Getting the instructions read at all.

| ID | Capability | Why it blocks production when absent |
|---|---|---|
| A1 | Codon usage compatible with host tRNA pool | *"the codon usage in E. coli … limit[s] its use for the production of slightly complex recombinant biopharmaceuticals"* |
| A2 | Promoter function (transcription initiation) | Circuits behave differently per host; *"most advances in engineered genetic systems rely on host-specific"* parts |
| A3 | Translation initiation (RBS / Kozak) | Same |
| A4 | Large coding sequence capacity | *"this bacterium cannot express very large proteins"* (of *E. coli*) |
| A5 | Repetitive-sequence stability | Spidroin production problems include *"genetic instability"* — repeat-rich genes recombine out |
| A6 | Multi-gene cluster expression | Biosynthetic gene clusters need many genes expressed in balance; polyketide work shows *"complex pathway interactions"* |

## B. Protein maturation

Getting the protein into its working shape.

| ID | Capability | Why it blocks production when absent |
|---|---|---|
| B1 | Folding / chaperone capacity | *"Different codon usage, missing chaperones, and posttranslational"* modifications make bacterial expression of eukaryotic genes fail |
| B2 | Disulfide bond formation | *"The capacity of E. coli for protein folding and forming disulfide bonds is not sufficient for many recombinant proteins"* |
| B3 | N-glycosylation present at all | *"The low capacity for PTMs hinders the production of heterologous proteins in the widely used prokaryotic systems"* |
| B4 | **Human-like** N-glycan structure | *"The cells of nonhuman species do not glycosylate their proteins in the same way as human cells do."* Yeast gives high-mannose, not human |
| B5 | O-glycosylation | Named alongside N-glycosylation in PTM failure lists |
| B6 | Other PTMs: phosphorylation, myristoylation, palmitoylation, proteolytic processing | *"Prediction of some PTMs, such as myristoylation, glycosylation, palmitoylation, and disulfide bond formation, was found to significantly worsen"* expression outcomes |
| B7 | Protease balance (product not degraded) | Recurrent in secretion and yield literature |

## C. Catalysis and cofactors

Running the chemistry.

| ID | Capability | Why it blocks production when absent |
|---|---|---|
| C1 | Heme biosynthesis and supply | *"P450s are heme-containing enzymes"* — no heme, no P450 chemistry |
| C2 | **Functional cytochrome P450 expression** | *"Cytochrome P450 enzymes are prevalent in plant specialized metabolism and are **particularly difficult to express heterologously**."* Needs membrane anchoring *and* a redox partner *and* heme *and* oxygen, together |
| C3 | NADPH supply and regeneration | P450s *"use molecular oxygen and the hydride donor NAD(P)H"*; a *Pichia* diterpenoid paper had to relieve *"precursor acetyl-coenzyme A and cofactor NADPH limitations"* |
| C4 | S-adenosyl methionine (SAM) supply | Methylation steps across natural product pathways |
| C5 | Other cofactors: FAD, PLP, B12, Fe-S clusters | Pathway-specific but blocking where required |

## D. Precursor supply

Having the raw material.

| ID | Capability | Why it blocks production when absent |
|---|---|---|
| D1 | Acetyl-CoA and malonyl-CoA pool | Polyketide synthases use *"short-chain acyl-CoA monomers"* |
| D2 | Isoprenoid precursors (mevalonate or MEP) | Terpenoid chassis work proceeds by *"enhancing the expression of the MVA pathway for common precursor synthesis"* |
| D3 | Shikimate pathway flux (aromatics) | Tryptophan work required enhancing *"shikimate, serine, and glutamine"* availability |
| D4 | Amino acid pools | Same |
| D5 | Sugar-nucleotide pool | *"Glycosylation reactions rely on the stepwise addition of sugars using nucleotide diphosphate (NDP)-sugars"* |

## E. Compartments and membranes

Having somewhere to put things.

| ID | Capability | Why it blocks production when absent |
|---|---|---|
| E1 | Membrane capacity for membrane-anchored enzymes | P450s need it; this is part of why they fail in bacteria |
| E2 | Subcellular compartmentalisation | Demonstrated as an enabling strategy — *"Compartmentalized sesquiterpenoid biosynthesis and functionalization in the Chlamydomonas reinhardtii plastid"* |
| E3 | Secretion capacity | Determines whether product must be extracted by lysis |
| E4 | Export of large or repetitive proteins | Silk required engineering *"the Salmonella type III secretion system to export spider silk monomers"* |

## F. Tolerance and robustness

Surviving your own product. **The most under-rated category** — recent work keeps
finding this is the binding constraint, not the pathway.

| ID | Capability | Why it blocks production when absent |
|---|---|---|
| F1 | Product toxicity tolerance | *"the inherent toxicity of certain high-value chemicals to microbial cell factories presents a significant challenge, severely constraining production efficiency"* |
| F2 | Efflux transport of the product | *"Genome-scale overexpression screening identifies **product tolerance and efflux transport as key determinants**"* of high-level production |
| F3 | Stress response capacity | Evolved strains with *"reinforced cellular defenses"* outperform |
| F4 | Feedstock / substrate tolerance | Lignocellulosic and agave hydrolysates are themselves toxic |

## G. Process and deployment

Being usable outside a research lab.

| ID | Capability | Why it blocks production when absent |
|---|---|---|
| G1 | Growth rate / biomass accumulation | Cyanobacterial chassis limited by *"slow growth rate and low biomass accumulation"* |
| G2 | Growth–production balance | *"The inherent conflict between cellular growth and product synthesis … fundamentally constrains the performance of microbial chassis"* |
| G3 | Genetic stability over generations | Repeat-rich and burdened constructs are lost |
| G4 | Culture-condition range (aerobic/anaerobic, temperature, salinity) | Products demand different conditions; *Halomonas* is a chassis specifically because high salt *"minimizes contamination risks"* |
| G5 | Demonstrated scale-up | Separates a research organism from a manufacturing one |
| G6 | Safety / regulatory status (e.g. GRAS) | Blocks food and pharmaceutical use regardless of yield |

---

## Count

**37 capabilities across 7 categories** — 15 binary (you have it or you don't),
22 graded (a matter of how much).

| Category | Capabilities |
|---|---:|
| A. Genetic expression | 6 |
| B. Protein maturation | 7 |
| C. Catalysis and cofactors | 5 |
| D. Precursor supply | 5 |
| E. Compartments and membranes | 4 |
| F. Tolerance and robustness | 4 |
| G. Process and deployment | 6 |
| **Total** | **37** |

That number is the point. It is finite, it is scoreable, and it converts
"universal" into a testable claim: *does any host, with a bounded set of
additions, cover all 37?*

## What this version does not yet have

- **No scoring.** No host has been assessed against any of these.
- **No weighting.** All 35 are listed flat. In reality some are binary (you have
  heme or you don't) and some are graded (how *much* NADPH). That distinction is
  not yet encoded.
- **No conflict map.** The critical question — whether any two capabilities are
  *mutually exclusive* — is untouched. If, say, G4 anaerobic conflicts with C2
  P450s needing oxygen, universality may be impossible on physical grounds.
  **Finding such a conflict would be the most important result this project
  could produce, and we have not looked.**
- **Nucleic-acid products are under-covered.** mRNA, plasmid DNA and modified
  nucleotides demand capabilities (capping, modified bases, polymerase fidelity)
  that are not properly enumerated here.
- The evidence quotes above are from abstracts read during the literature sweep.
  **They have not been checked against the full papers.**
