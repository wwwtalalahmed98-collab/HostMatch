# Final Project Writeup: Cell-Free Chromoprotein Microplate Mosaic Driven by a LacI/IPTG Genetic Circuit

---

# SECTION 1: ABSTRACT

Living color has long been the domain of pigments and dyes, but synthetic biology offers a radically different medium: genetically encoded chromoproteins whose visible hues emerge directly from protein structure. This project develops a cell-free chromoprotein microplate mosaic in which a LacI/IPTG genetic circuit controls the sequential de-repression of four chromoproteins — amilCP (blue-purple), spisPink (pink), amilGFP (yellow-green), and eforRed (red) — producing a visible color gradient across a 384-well plate that functions simultaneously as a work of biological art and a quantitative demonstration of synthetic genetic circuit logic. Four whole plasmids, each encoding a chromoprotein under a T7 promoter with a distinct lacO operator configuration, are synthesized by Twist Bioscience and combined in *E. coli* BL21(DE3) cell-free protein synthesis (CFPS) reactions. As IPTG concentration increases across plate columns, LacI repression is progressively lifted from each plasmid in sequence, shifting the dominant visible color from blue-purple through pink and yellow-green to red. The automated workflow uses Echo525 acoustic dispensing for precise plasmid and IPTG delivery, Multiflo for bulk CFPS master mix distribution, and the Spark Plate Reader for absorbance-based quantification of chromoprotein output at wavelengths specific to each protein. Validation confirms individual chromoprotein expression before the full mosaic run. This project demonstrates that cell-free synthetic biology can be both a rigorous scientific platform and a creative medium for biological art, with connections to industry partners including Twist Bioscience, Ginkgo Bioworks, Asimov, and BioFabricate.

---

# SECTION 2: PROJECT AIMS

### Aim 1 — Experimental Aim

The first aim of my final project is to **generate a visible color gradient microplate mosaic by expressing four chromoproteins — amilCP, spisPink, amilGFP, and eforRed — through a LacI/IPTG-regulated cell-free genetic circuit** by utilizing **four Twist Bioscience whole-plasmid synthesis orders, *E. coli* BL21(DE3) CFPS, Echo525 acoustic dispensing of IPTG gradients, and Spark Plate Reader absorbance quantification in a 384-flat-corning-3640 plate**.

---

### Aim 2 — Medium-Term Aim

Beyond the course, the circuit will be expanded to incorporate additional regulatory layers, including aTc-inducible TetR repressors and arabinose-inducible AraC activators, enabling a two-dimensional combinatorial input grid across the plate — rows controlled by IPTG, columns by aTc — that produces a 2D color map where each well's hue reflects the logical output of a multi-input genetic circuit. Additional chromoproteins from the expanded iGEM palette (tsPurple, cjBlue, gfasPurple) will be incorporated to increase color resolution, and computational design tools from Asimov's Kernel Platform will be used to model and optimize circuit transfer functions before synthesis. This phase will transition the mosaic from a gradient demonstration into a fully programmable biological pixel array capable of encoding arbitrary images through circuit state mapping.

---

### Aim 3 — Visionary Aim

Imagine a future where the walls of hospitals are grown, not painted — where living, protein-based surfaces shift color in response to environmental signals, displaying real-time biological data as art visible to the naked eye. This project plants the seed of that future: a **programmable biological display medium** where chromoprotein-expressing cell-free reactions, encapsulated in stable hydrogel matrices, form the pixels of a new kind of screen — one that runs on genetic logic, requires no electricity, and is fully biodegradable. Partnering with BioFabricate and the broader bio-art community, this technology could enable a new discipline of **synthetic chromatic design** — where architects, artists, and synthetic biologists co-design living color systems that merge aesthetics with function, bringing genetic circuits out of the laboratory and into the world.

---

# SECTION 3: BACKGROUND

## Literature Context

Chromoproteins are a class of naturally occurring colored proteins first characterized in reef-building corals, where they contribute to photoprotection and visual signaling, and have since been repurposed as visible reporters in synthetic biology due to their ability to produce intense color at room temperature without any fluorescence excitation equipment. Liljeruhm et al. (2018) systematically characterized a panel of coral-derived chromoproteins expressed in *E. coli*, demonstrating that amilCP, eforRed, amilGFP, and related proteins produce distinct, stable colors detectable by the naked eye within hours of induction, and that their expression levels correlate with spectrophotometrically measurable absorbance — establishing chromoproteins as quantitative as well as aesthetic reporters. However, that study expressed chromoproteins in living bacterial cultures requiring overnight growth, selective media, and containment, limiting their accessibility for art, education, and non-laboratory deployment. Pardee et al. (2016) demonstrated that cell-free transcription-translation (TX-TL) systems can execute complex genetic logic — including toehold switch RNA sensors and cascaded regulatory circuits — in open, shelf-stable formats outside living organisms, pointing toward a future where genetic circuits operate as standalone biochemical devices. Together, these works identify a compelling knowledge gap: no study has combined chromoprotein expression with a multi-layered cell-free genetic circuit to produce a programmable, visible color output array — the foundational architecture of a biological display medium.

---

## Innovation

This project is novel in three distinct respects. First, it applies chromoproteins not merely as reporters but as the terminal output nodes of a layered LacI/IPTG genetic circuit, where color is a direct readout of circuit logic state rather than simply a marker of gene expression. Second, by varying lacO operator configuration across four separate whole-plasmid constructs and mixing all four in each well, the design creates a competitive, concentration-dependent color mixing system in which the dominant visible hue emerges from the relative expression levels of competing chromoproteins — a fundamentally different mode of color generation from single-reporter systems. Third, the use of a 384-well flat clear-bottom plate as a display canvas, with IPTG dispensed at nanoliter precision by the Echo525, translates genetic circuit programming directly into a spatially resolved visual artwork, establishing a new paradigm for synthetic biology as both science and medium.

---

## Significance

The ability to encode visible color outputs into cell-free genetic circuits has broad implications for synthetic biology education, biosensing, and bio-art, as it eliminates the need for fluorescence microscopy or spectrometry and makes genetic circuit outputs accessible to non-specialist audiences. Cell-free systems remove biosafety barriers associated with living organisms, enabling chromoprotein-based displays to be used in open environments — classrooms, galleries, public installations — without containment requirements. The LacI/IPTG circuit logic demonstrated here is directly generalizable to other inducible systems, meaning that the same microplate mosaic architecture could be adapted to detect environmental analytes, pathogen markers, or metabolic signals by substituting IPTG for biosensor inputs. This project also addresses a cultural dimension of synthetic biology: by producing a visually compelling artwork, it creates a tangible demonstration of genetic circuit logic for public audiences who may not engage with abstract scientific data, advancing the public communication and acceptance of synthetic biology. Connections to industry partners — including BioFabricate for bio-art applications and Ginkgo Bioworks for scalable cell-free manufacturing — position this work at the intersection of science, design, and biotechnology commercialization.

---

## Bioethical Considerations

This project operates entirely in a cell-free format using commercially synthesized plasmids and *E. coli* BL21(DE3) lysate, placing it at BSL-1 risk with no live organism release or environmental containment concerns. All plasmid sequences should be registered with SecureDNA's screening system prior to synthesis to confirm they contain no sequences of concern — a best practice for all synthetic DNA orders regardless of apparent risk — and Twist Bioscience's own biosecurity screening pipeline provides a second layer of review. The chromoproteins used are derived from coral species; while the genes themselves are synthetic and codon-optimized, researchers should acknowledge the ecological context of their biological origins, particularly given the threatened status of coral reef ecosystems, and consider how the synthetic biology community's use of coral-derived genetic material relates to biodiversity conservation. Open-sourcing all plasmid sequences through Addgene and publishing full protocols supports equitable access to this technology across institutions, community labs, and educational settings globally.

The intersection of synthetic biology and art raises distinct ethical questions around authenticity, authorship, and the commodification of living systems that deserve thoughtful engagement. This project deliberately positions cell-free biology — rather than living organisms — as its creative medium, reducing concerns about instrumentalizing life, but future iterations involving living cells, hydrogel encapsulation, or public installation would require renewed ethical review and transparent communication with audiences about the biological nature of the medium. Collaborations with partners such as BioFabricate should include explicit agreements about intellectual property, open access, and the responsible representation of synthetic biology to public and artistic audiences. Researchers are encouraged to engage with bio-art ethics frameworks and community guidelines, such as those developed by the Synthetic Biology Leadership Council, throughout the project lifecycle.

---

# SECTION 4: EXPERIMENTAL DESIGN

The following workflow details all steps for designing, synthesizing, validating, and running the cell-free chromoprotein mosaic.

---

**Step 1 — In Silico Circuit and Construct Design**
- **Method**: Design four plasmid constructs in Benchling using Asimov's Kernel Platform for circuit modeling. All constructs use a pTwist-Amp backbone (~2.7 kb, AmpR, ColE1 ori). Each encodes one chromoprotein under a T7 promoter with a distinct lacO configuration: pTwist-T7-amilCP (no lacO — constitutive), pTwist-T7lacO1-spisPink (1× weak lacO), pTwist-T7lacO2-amilGFP (2× medium lacO), pTwist-T7lacO3-eforRed (3× strong lacO). All chromoprotein CDSs are codon-optimized for *E. coli* K12. Include C-terminal His6 tags on all constructs for optional QC.
- **Machine**: Computational (Benchling, Asimov Kernel Platform)
- **Plate**: N/A
- **Expected Results**: Four annotated, sequence-verified plasmid maps; predicted circuit transfer functions showing sequential de-repression from 0–5000 µM IPTG
- **Timeline**: Day 1–3

**GenBank Record — pTwist-T7-amilCP (Reference Construct):**

```genbank
LOCUS       pTwist_T7_amilCP         3358 bp    DNA     circular  SYN  15-MAR-2026
DEFINITION  pTwist-Amp backbone encoding amilCP (blue-purple chromoprotein from
            Acropora millepora) under a constitutive T7 promoter; codon-optimized
            for E. coli BL21(DE3) cell-free expression. No lacO operator —
            constitutively expressed at all IPTG concentrations. Component of
            4-plasmid chromoprotein mosaic circuit.
ACCESSION   .
VERSION     .
KEYWORDS    amilCP; chromoprotein; cell-free; T7 expression; synthetic biology art;
            coral chromoprotein; BL21(DE3); CFPS; LacI circuit.
SOURCE      synthetic construct
  ORGANISM  synthetic construct
            other sequences; artificial sequences; vectors.
COMMENT     Designed for HTGAA 2026 Final Project: Cell-Free Chromoprotein Mosaic.
            Ordered as Twist Clonal Gene (whole plasmid synthesis).
            Companion plasmids: pTwist-T7lacO1-spisPink, pTwist-T7lacO2-amilGFP,
            pTwist-T7lacO3-eforRed. All four mixed in each CFPS well; IPTG
            gradient (0-5000 uM) determines dominant color output.
FEATURES             Location/Qualifiers
     source          1..3358
                     /organism="synthetic construct"
                     /mol_type="other DNA"
     promoter        1..19
                     /label="T7 promoter"
                     /note="consensus T7 promoter; no lacO operator; constitutive
                            expression in BL21(DE3) cell-free extract"
                     /seq="TAATACGACTCACTATA"
     RBS             27..32
                     /label="RBS"
                     /note="optimized Shine-Dalgarno; AGGAGG; spacing 7 nt to ATG"
     CDS             40..717
                     /label="amilCP"
                     /codon_start=1
                     /product="amilCP blue-purple chromoprotein"
                     /note="Derived from Acropora millepora; visible blue-purple
                            color at room temperature; peak absorbance ~588 nm;
                            no excitation required; codon-optimized for E. coli K12;
                            226 amino acids; MW ~25.4 kDa"
                     /translation="MASKVIVLNGLNMGEAGDATYGKLTLKFICTTEKLPVPWPTLVT
                     TLTYGVQCFSKYPDHMKQHDFFKSAMPEGYVQERTIFFKDDGNYKTRAEVKFEGDTLVN
                     RIELKGIDFKEDGNILGHKLEYNYNSHNVYIMADKQKNGIKVNFKIRHNIEDGSVQLAD
                     HYQQNTPIGDGPVLLPDNHYLSTQSVLSKDPNEKRDHVMEFVEAAGITHAMDELYK"
     CDS             718..735
                     /label="6xHis tag"
                     /note="C-terminal His6 affinity tag for QC verification"
     terminator      741..811
                     /label="T7 terminator"
                     /note="rrnB T1 terminator; efficient transcription termination"
     rep_origin      complement(900..1488)
                     /label="ColE1 ori"
                     /note="high-copy origin of replication; ~500 copies/cell"
     CDS             complement(1600..2460)
                     /label="AmpR"
                     /product="beta-lactamase TEM-1"
                     /note="ampicillin resistance; selection at 100 ug/mL"
     promoter        complement(2461..2565)
                     /label="AmpR promoter"
     misc_feature    2600..2700
                     /label="pTwist backbone region"
                     /note="Twist Bioscience proprietary backbone sequence"
ORIGIN
        1 taatacgact cactataggg agaccacaac ggtttccctc tagaaataat tttgtttaac
       61 tttaagaagg agatatacca tggcttctaa ggtaattgtt ttaaacggct tgaacatggg
      121 tgaagcaggt gatgcaacct acggtaaact gaccttaaag ttcatctgca ctactgaaaa
      181 acttcctgtt ccatggccta cactcgtgac cactttaacc tacggtgtcc agtgtttctc
      241 caagtatcca gatcacatga agcaacacga cttcttcaag tctgcaatgc cagaaggtca
      301 cgttcaagag cgtactatct tctttaaaga cgacggaaac tacaagactc gtgcagaagt
      361 taagtttgaa ggtgacactc tggtgaaccg tatcgagctt aagggtattg acttcaagga
      421 agacggcaac atcctgggac acaagttgga gtacaactac aactcccaca acgtctacat
      481 catggctgac aagcagaaga acggtatcaa ggtcaacttc aagattcgcc acaacattga
      541 agacggctct gtccagttag ctgaccacta ccagcagaac accccaatcg gcgatggccc
      601 tgtcctcttg ccagacaacc actacctgtc tacacaatct gtactgtcaa aggatccaaa
      661 cgagaaacgg gatcacgtca tggagttcgt cgaagcagcc ggaatcacac acgctatgga
      721 cgagctgtac aagtaaggatcccatcatcaccatcaccattgaagg atccgagctc gaattcgtc
      781 gagggcgcta atcgaaattt ttgtaatcag aaaattagag aagattaaag tttttttaat
      841 aacgtcttcg gctttttttt atttttaact ttttttctat ttttttatgg ttttttatcg
      901 aaaaaaaaac cccgcttcgg gggttttttt gcttttcgag gtttttttca ccggattttg
      961 attatttttg cctttttgaa aacaagtttt tttctttttt ttgaaaaaat tccccctttt
//
```

---

**Step 2 — Twist Bioscience Whole Plasmid Synthesis Order**
- **Method**: Submit all four plasmid sequences to Twist Bioscience Clonal Genes portal (whole plasmid synthesis). Specify AmpR selection, ColE1 ori, *E. coli* K12 codon optimization for all chromoprotein CDSs, and delivery in TE buffer at ≥250 ng/µL. For the three inducible constructs, select **pTwist-Amp** as the backbone on the portal and paste the insert sequences below directly into the sequence field — no additional cloning or assembly is required.
- **Machine**: Twist Bioscience online portal
- **Plate**: N/A
- **Expected Results**: Four sequence-confirmed whole plasmids delivered within 10–14 business days
- **Timeline**: Day 3–4 (order placed); Day 14–17 (receipt)

### Twist Portal Insert Sequences — Inducible Chromoproteins

> **How to use:** On the Twist Clonal Genes portal, select **pTwist-Amp** as the backbone. Paste the FASTA sequence below into the insert field for each construct. The insert encodes: `T7 promoter → lacO operator(s) → RBS → chromoprotein CDS (E. coli codon-optimized) → 6×His tag → T7 terminator`. The amilCP construct (constitutive, no lacO) is provided as the GenBank record in Step 1 above and should be submitted as a full plasmid sequence.
>
> **Note:** Chromoprotein CDS sequences are E. coli codon-optimized representations based on iGEM registry source sequences (BBa_K592010 for amilGFP, BBa_K592012 for eforRed, BBa_K1033933 for spisPink). Verify against current iGEM registry entries before finalizing your Twist order.

---

**Insert A — pTwist-T7lacO1-spisPink** *(1× lacO1, de-repressed at ~50 µM IPTG)*
*Select pTwist-Amp backbone on Twist portal, paste insert below (~867 bp)*

```fasta
>pTwist_T7lacO1_spisPink_insert | T7promoter-1xlacO1-RBS-spisPink_CDS-His6-T7term | 867bp
TAATACGACTCACTATAGGGAGACCACAACGGTTTCCCTCTAGAATTGTGAGCGGATAAC
AATTAAATAATTTTGTTTAACTTTAAGAAGGAGATATACCAATGGTGAGCAAGGGCGAGG
AAGATAACATGGCTATCATCAAGGAGTTCATGCGCTTCAAGGTGCACATGGAGGGCTCCG
TGAACGGCCACGAGTTCGAGATCGAGGGCGAGGGCGACGGCACCTACGGCAAGCTGACCC
TGAAGTTCATCTGCACCACCGGCAAGCTGCCCGTGCCCTGGCCCACCCTCGTGACCACCCT
GACCTACGGCGTGCAATGCTTCGCCCGCTACCCCGACCACATGAAGCAGCACGACTTCTTC
AAGTCCGCCATGCCCGAAGGCTACGTGCAGGAGCGCACCATCTTCTTCAAGGACGACGGCA
ACTACAAGACCCGCGCCGAGGTGAAGTTCGAGGGCGACACCCTGGTGAACCGCATCGAGCT
GAAGGGCATCGACTTCAAGGAGGACGGCAACATCCTGGGACACAAGCTGGAGTACAACTAC
AACAGCCACAACGTCTACATCATGGCCGACAAGCAGAAGAACGGCATCAAGGCAAACTTCA
AGATCCGCCACAACATCGAGGACGGCAGCGTGCAGCTCGCCGACCACTACCAGCAGAACAC
CCCAATCGGCGACGGCCCCGTGCTGCTGCCCGACAACCACTACCTGTCCACCCAGTCCGTG
CTGTCCAAGGACCCCAACGAGAAGCGCGATCACATGGTCCTGCTGGAGTTCGTGACCGCCG
CCGGGATCACCCACATGGACGAGCTGTACAAGCATCACCATCACCATCACTAATAAGGATC
CGAGCTCGAATTCGTCGAGGGCGCTAATCGAAATTTTTGTAATCAGAAAATTAGAGAAGATT
```

**Key structural elements:**
| Element | Sequence | Position |
|---|---|---|
| T7 promoter | `TAATACGACTCACTATA` | bp 1–17 |
| lacO1 (×1) | `AATTGTGAGCGGATAACAATT` | bp 44–64 |
| Shine-Dalgarno | `AAGGAG` | bp 83–88 |
| ATG start | `ATG` | bp 97–99 |
| spisPink CDS | ~675 bp | bp 97–771 |
| 6×His tag | `CATCACCATCACCATCAC` | bp 772–789 |
| Stop codon | `TAA` | bp 790–792 |
| T7 terminator | `TAAGGATCC...GAAGATT` | bp 793–862 |

---

**Insert B — pTwist-T7lacO2-amilGFP** *(2× lacO1 tandem, de-repressed at ~500 µM IPTG)*
*Select pTwist-Amp backbone on Twist portal, paste insert below (~919 bp)*

```fasta
>pTwist_T7lacO2_amilGFP_insert | T7promoter-2xlacO1-RBS-amilGFP_CDS-His6-T7term | 919bp
TAATACGACTCACTATAGGGAGACCACAACGGTTTCCCTCTAGAATTGTGAGCGGATAAC
AATTGCGCAAATTGTGAGCGGATAACAATTAAATAATTTTGTTTAACTTTAAGAAGGAGA
TATACCAATGAGTAAAGGAGAAGAACTTTTCACTGGAGTTGTCCCAATTCTTGTTGAATT
AGATGGTGATGTTAATGGGCACAAATTTTCTGTCAGTGGAGAGGGTGAAGGTGATGCAAC
ATACGGAAAACTTACCCTTAAATTTATTTGCACTACTGGAAAACTACCTGTTCCATGGCCA
ACACTTGTCACTACTTTCGGTTATGGTGTTCAATGCTTTGCGAGATATCCCAGATCATATG
AAACAGCATGACTTTTTCAAGAGTGCCATGCCAGAAGGTTATGTACAGGAAAGAACTATCT
TCTTTAAAGATGACGGAAACTACAAGACACGTGCTGAAGTCAAGTTTGAAGGTGATACCCTT
GTTAATAGAATCGAGTTAAAAGGTATTGATTTTAAAGAAGACGGAAACATTCTCGGACACA
AATTGGAATACAACTATAACTCACACAATGTATACATCATGGCAGACAAACAAAAGAATGGA
ATCAAAGCTAACTTCAAAATTAGACACAACATTGAAGATGGAAGCGTTCAACTAGCAGACCA
TTATCAACAAAATACTCCAATTGGCGATGGCCCTGTCCTTTTACCAGACAACCATTACCTGT
CCACACAATCTGCCCTTTCGAAAGATCCCAACGAAAAGAGAGATCACATGGTCCTTCTTGAG
TTTGTAACTGCTGCTGGGATTACACATGGCATGGATGAACTCTACAAGCATCACCATCACCA
TCACTAATAAGGATCCGAGCTCGAATTCGTCGAGGGCGCTAATCGAAATTTTTGTAATCAGA
AAATTAGAGAAGATT
```

**Key structural elements:**
| Element | Sequence | Position |
|---|---|---|
| T7 promoter | `TAATACGACTCACTATA` | bp 1–17 |
| lacO1 site 1 | `AATTGTGAGCGGATAACAATT` | bp 44–64 |
| 5 bp spacer | `GCGCA` | bp 65–69 |
| lacO1 site 2 | `AATTGTGAGCGGATAACAATT` | bp 70–90 |
| Shine-Dalgarno | `AAGGAG` | bp 109–114 |
| ATG start | `ATG` | bp 123–125 |
| amilGFP CDS | ~711 bp | bp 123–833 |
| 6×His tag | `CATCACCATCACCATCAC` | bp 834–851 |
| Stop codon | `TAA` | bp 852–854 |
| T7 terminator | `TAAGGATCC...GAAGATT` | bp 855–924 |

---

**Insert C — pTwist-T7lacO3-eforRed** *(3× lacO1 tandem, de-repressed at ~5000 µM IPTG)*
*Select pTwist-Amp backbone on Twist portal, paste insert below (~945 bp)*

```fasta
>pTwist_T7lacO3_eforRed_insert | T7promoter-3xlacO1-RBS-eforRed_CDS-His6-T7term | 945bp
TAATACGACTCACTATAGGGAGACCACAACGGTTTCCCTCTAGAATTGTGAGCGGATAAC
AATTGCGCAAATTGTGAGCGGATAACAATTGCGCAAATTGTGAGCGGATAACAATTAAATA
ATTTTGTTTAACTTTAAGAAGGAGATATACCAATGGTGAGCAAGGGCGAGGAGGATAACATG
GCCATCATCAAGGAGTTCATGCGCTTCAAGGTGCACATGGAGGGCTCCGTGAACGGCCACGA
GTTCGAGATCGAGGGCGAGGGCGAGGGCCGCCCCTACGAGGGCACCCAGACCGCCAAGCTGA
AGGTGACCAAGGGTGGCCCCCTGCCCTTCGCCTGGGACATAGTCGCCCAGCAGTTCATGTAC
GGCTCCAAGGCCTACGTGAAGCACCCCGCCGACATCCCCGACTACTTGAAGCTGTCCTTCCCC
GAGGGCTTCAAATGGGAGCGCGTGATGAACTTCGAGGACGGCGGCGTGGTGACCGTGACGCAG
GACTCCTCCCTGCAGGACGGCGAGTTCATCTACAAGGTGAAGCTGCGCGGCACCAACTTCCCC
TCCGACGGCCCCGTAATGCAGAAGAAGACCATGGGCTGGGAGGCCTCCTCCGAGCGGATGTAC
CCCGAGGACGGCGCCCTGAAGGGCGAGATCAAGCAGAGGCTGAAGCTGAAGGACGGCGGCCAC
TACGACGCTGAGGTCAAGACCACCTACAAGGCCAAGAAGCCCGTGCAGCTGCCCGGCGCCTACA
ACGTCAACATCAAGTTGGACATCACCTCCCACAACGAGGACTACACCATCGTGGAACAGTACGA
GCGCGCCGAGGGCCGCCACTCCACCGGCGGCATGGACGAGCTGTACAAGCATCACCATCACCATC
ACTAATAAGGATCCGAGCTCGAATTCGTCGAGGGCGCTAATCGAAATTTTTGTAATCAGAAAATT
AGAGAAGATT
```

**Key structural elements:**
| Element | Sequence | Position |
|---|---|---|
| T7 promoter | `TAATACGACTCACTATA` | bp 1–17 |
| lacO1 site 1 | `AATTGTGAGCGGATAACAATT` | bp 44–64 |
| 5 bp spacer | `GCGCA` | bp 65–69 |
| lacO1 site 2 | `AATTGTGAGCGGATAACAATT` | bp 70–90 |
| 5 bp spacer | `GCGCA` | bp 91–95 |
| lacO1 site 3 | `AATTGTGAGCGGATAACAATT` | bp 96–116 |
| Shine-Dalgarno | `AAGGAG` | bp 135–140 |
| ATG start | `ATG` | bp 149–151 |
| eforRed CDS | ~711 bp | bp 149–859 |
| 6×His tag | `CATCACCATCACCATCAC` | bp 860–877 |
| Stop codon | `TAA` | bp 878–880 |
| T7 terminator | `TAAGGATCC...GAAGATT` | bp 881–950 |

---

**Step 3 — Plasmid QC and Quantification**
- **Method**: Nanodrop all four plasmids (A260/A280 ≥1.8; A260/A230 ≥2.0). Run 1 µL each on agarose gel to confirm supercoiled band. Dilute each to 50 ng/µL working stock. Store at −20°C in Tundrastore.
- **Machine**: HiG Centrifuge (if ethanol precipitation needed), Tundrastore
- **Plate**: N/A
- **Expected Results**: All four plasmids at confirmed purity; correct size bands on gel (~3.3 kb each)
- **Timeline**: Day 17–18

---

**Step 4 — Prepare CFPS Master Mix**
- **Method**: Combine BL21(DE3) S12 extract (33% v/v, already prepared), PEP energy solution, 1 mM each amino acid, NTPs, Mg-glutamate (8 mM), K-glutamate (80 mM), spermidine (1 mM), PEG-8000 (2%). Keep on ice. Do not add plasmid yet. Prepare sufficient volume for ≥2 full 384-well plates plus validation wells.
- **Machine**: Manual preparation on ice
- **Plate**: N/A
- **Expected Results**: Homogeneous master mix; no precipitation; sufficient volume confirmed by calculation
- **Timeline**: Day 19

---

**Step 5 — Validation: Single-Plasmid Expression Setup**
- **Method**: Prepare 4 single-plasmid CFPS reactions (10 ng/µL each plasmid separately) in master mix. Include one no-DNA negative control. Dispense 10 µL per well into 4 columns (5 wells each) of 384-flat-corning-3640 plate using Multiflo.
- **Machine**: Multiflo
- **Plate**: 384-flat-corning-3640
- **Expected Results**: Uniform fill; no bubbles; CV <5%
- **Timeline**: Day 19

---

**Step 6 — Validation: Express and Read Single Chromoproteins**
- **Method**: Seal validation wells with A4s breathable seal. Incubate 37°C for 4 hours in Inheco Plate Incubator. Peel with XPeel. Read Spark Plate Reader at chromoprotein-specific absorbance wavelengths: amilCP (588 nm), spisPink (559 nm), amilGFP (507 nm), eforRed (525 nm). Record absorbance values. Photograph plate for visual color confirmation.
- **Machine**: A4s, Inheco Plate Incubator, XPeel, Spark Plate Reader
- **Plate**: 384-flat-corning-3640
- **Expected Results**: Each chromoprotein well shows absorbance >0.3 OD above background at its target wavelength; visible color detectable by eye; no-DNA control shows background only
- **Timeline**: Day 19–20

---

**Step 7 — Prepare 4-Plasmid Mix**
- **Method**: Combine all four plasmids at equal molar concentration (10 ng/µL each, 40 ng/µL total) in TE buffer. Vortex gently and centrifuge briefly. Store on ice in Ambistore until dispensing.
- **Machine**: Ambistore
- **Plate**: N/A
- **Expected Results**: Homogeneous 4-plasmid cocktail confirmed by Nanodrop; no aggregation
- **Timeline**: Day 20

---

**Step 8 — Prepare IPTG Gradient Source Plate**
- **Method**: Prepare 8-point IPTG dilution series in water: 0, 10, 50, 100, 500, 1000, 2500, 5000 µM. Load into Echo PP source plate with 3 columns per concentration (for triplicates). Include DMSO-free water as solvent control column.
- **Machine**: Manual preparation
- **Plate**: 384-well Echo PP
- **Expected Results**: Confirmed concentrations by dilution calculation; no precipitation at any concentration
- **Timeline**: Day 20

---

**Step 9 — Dispense CFPS Master Mix into Mosaic Plate**
- **Method**: Dispense 8 µL CFPS master mix per well into 384-flat-corning-3640 mosaic plate using Multiflo. Skip outer ring of wells (edge controls). Fill columns 2–23, rows B–O (288 active wells).
- **Machine**: Multiflo
- **Plate**: 384-flat-corning-3640
- **Expected Results**: Uniform 8 µL fill across all active wells; CV <5%; no cross-contamination
- **Timeline**: Day 20

---

**Step 10 — Acoustic Dispensing of Plasmid Mix**
- **Method**: Use Echo525 to dispense 4-plasmid cocktail from source plate into all active wells (200 nL per well, achieving 10 ng/µL each plasmid in 10 µL final volume).
- **Machine**: Echo525
- **Plate**: 384-flat-corning-3640
- **Expected Results**: Accurate transfer volumes confirmed by Echo report; uniform plasmid delivery across all wells
- **Timeline**: Day 20

---

**Step 11 — Acoustic Dispensing of IPTG Gradient**
- **Method**: Use Echo525 to dispense IPTG at target concentrations from source plate into mosaic plate wells. Each IPTG concentration occupies 3 adjacent columns (triplicates). Dispense 200 nL IPTG stock per well to achieve target final concentrations. No-IPTG wells receive water only.
- **Machine**: Echo525
- **Plate**: 384-flat-corning-3640
- **Expected Results**: Precise IPTG gradient across plate columns confirmed by Echo dispense log; IPTG concentrations span 0–5000 µM
- **Timeline**: Day 20

---

**Step 12 — Seal and Incubate for Chromoprotein Expression**
- **Method**: Apply A4s breathable membrane. Incubate at 37°C for 4 hours in Inheco Plate Incubator to allow full chromoprotein expression. The longer incubation (vs. 2 hr for fluorescent proteins) is required for visible chromoprotein color development.
- **Machine**: A4s, Inheco Plate Incubator
- **Plate**: 384-flat-corning-3640
- **Expected Results**: Visible color gradient detectable by eye across plate columns after 4 hr; blue-purple at 0 µM IPTG transitioning to red at 5000 µM
- **Timeline**: Day 20 (4 hr incubation)

---

**Step 13 — Peel and Read Absorbance**
- **Method**: Peel A4s with XPeel. Read Spark Plate Reader at all four chromoprotein wavelengths (507, 525, 559, 588 nm) plus reference wavelength (700 nm for background subtraction). Record full absorbance spectrum per well.
- **Machine**: XPeel, Spark Plate Reader
- **Plate**: 384-flat-corning-3640
- **Expected Results**: Absorbance at 588 nm highest at 0 µM IPTG; progressive shift through 559 nm, 507 nm, 525 nm peaks as IPTG increases; clean gradient visible in heatmap
- **Timeline**: Day 20

---

**Step 14 — Mosaic Photography and Documentation**
- **Method**: Remove plate lid. Photograph plate from above on a white light transilluminator or white background. Document gradient from above. Export images for artwork presentation.
- **Machine**: Manual imaging
- **Plate**: 384-flat-corning-3640
- **Expected Results**: Visually compelling color gradient from blue-purple → pink → yellow-green → red across plate columns; each chromoprotein color band clearly distinguishable by eye
- **Timeline**: Day 20

---

**Step 15 — Data Analysis and Circuit Characterization**
- **Method**: Subtract 700 nm background from each well. Normalize absorbance per chromoprotein to its maximum observed value across the plate. Plot normalized absorbance vs. IPTG concentration for each chromoprotein. Determine EC₅₀ of IPTG de-repression for each plasmid. Generate circuit transfer function heatmap.
- **Machine**: Computational (Python / R)
- **Plate**: N/A
- **Expected Results**: Four sigmoidal dose-response curves with staggered EC₅₀ values confirming sequential circuit de-repression; heatmap recapitulates visual gradient
- **Timeline**: Day 21

---

## Example Assay Plate Layout — 384-Well Mosaic Plate

```
         Col2    Col3    Col4    Col5    Col6    Col7    Col8    Col9
         Col10   Col11   Col12   Col13   Col14   Col15   Col16
IPTG:    0µM     0µM     10µM    10µM    50µM    50µM    100µM   100µM
         500µM   500µM   1000µM  1000µM  2500µM  2500µM  5000µM  5000µM

Row B:   [BLU]   [BLU]   [BLU]   [BLU]   [PNK]   [PNK]   [PNK]   [PNK]
Row C:   [BLU]   [BLU]   [BLU]   [BLU]   [PNK]   [PNK]   [PNK]   [PNK]
Row D:   [BLU]   [BLU]   [BLU]   [BLU]   [PNK]   [PNK]   [YLW]   [YLW]
Row E:   [BLU]   [BLU]   [BLU]   [PNK]   [PNK]   [YLW]   [YLW]   [YLW]
Row F:   [BLU]   [BLU]   [PNK]   [PNK]   [YLW]   [YLW]   [YLW]   [RED]
Row G:   [BLU]   [PNK]   [PNK]   [YLW]   [YLW]   [YLW]   [RED]   [RED]
Row H:   [BLU]   [PNK]   [YLW]   [YLW]   [YLW]   [RED]   [RED]   [RED]
Row I:   [BLU]   [PNK]   [YLW]   [YLW]   [RED]   [RED]   [RED]   [RED]
Row J:   [BLU]   [PNK]   [YLW]   [RED]   [RED]   [RED]   [RED]   [RED]
Row K:   [BLU]   [BLU]   [PNK]   [PNK]   [YLW]   [YLW]   [RED]   [RED]
Row L:   [BLU]   [BLU]   [BLU]   [PNK]   [PNK]   [YLW]   [YLW]   [RED]
Row M:   [BLU]   [BLU]   [BLU]   [BLU]   [PNK]   [PNK]   [YLW]   [YLW]
Row N:   [BLU]   [BLU]   [BLU]   [BLU]   [PNK]   [PNK]   [PNK]   [RED]
Row O:   [BLU]   [BLU]   [BLU]   [BLU]   [PNK]   [PNK]   [PNK]   [PNK]

LEGEND:
BLU  = amilCP dominant    (blue-purple, 588 nm absorbance)
PNK  = spisPink dominant  (pink,        559 nm absorbance)
YLW  = amilGFP dominant   (yellow-green,507 nm absorbance)
RED  = eforRed dominant   (red,         525 nm absorbance)
EDGE = outer ring excluded (evaporation artifacts)

Note: Gradient reads left-to-right (increasing IPTG), creating a diagonal
color wave pattern when LacI de-repression is plotted as a function of
IPTG concentration and row position.
```

---

# SECTION 5: TECHNIQUES, TOOLS, AND TECHNOLOGY

## Technique Checklist

- [x] DNA design and sequence optimization (Benchling, Asimov Kernel Platform)
- [x] Whole plasmid synthesis (Twist Bioscience Clonal Genes)
- [x] Cell-free protein synthesis (CFPS) — BL21(DE3) S12 extract
- [x] Genetic circuit design (LacI/IPTG repressor-operator system)
- [x] Chromoprotein expression and characterization
- [x] Automated liquid handling (Echo525, Multiflo)
- [x] Microplate-based screening (384-well)
- [x] Absorbance spectrophotometry (Spark Plate Reader)
- [x] Dose-response curve analysis (sigmoidal, EC₅₀)
- [x] Biological art / synthetic chromatic design
- [ ] Gibson Assembly / molecular cloning (not required — whole plasmid synthesis)
- [ ] Flow cytometry
- [ ] qPCR / gene expression analysis
- [ ] CRISPR genome editing

---

## Technique Expansion

### Technique 1 — Cell-Free Protein Synthesis (CFPS)

Cell-free protein synthesis reconstitutes transcription and translation in a cell lysate, enabling gene expression from exogenously added DNA templates without the need for living organisms, selective media, or biosafety containment. In this project, *E. coli* BL21(DE3) S12 extract is used, which retains endogenous T7 RNA polymerase (from the chromosomally integrated T7 RNAP gene under lacUV5 control), ribosomes, aminoacyl-tRNA synthetases, chaperones, and energy regeneration enzymes that collectively support robust protein synthesis from T7 promoter-driven plasmids. A key advantage of CFPS for chromoprotein art is that it enables direct, open-well expression in microplate format — chromoproteins develop visible color within hours at 37°C without any post-processing, making the plate itself the artwork rather than a data readout device. The LacI protein naturally present in BL21(DE3) lysate (from the chromosomal lacI gene) provides the repressive function needed for IPTG-dependent circuit control without requiring exogenous LacI addition, simplifying the experimental setup to a single master mix usable across all well conditions.

### Technique 2 — LacI/IPTG Genetic Circuit Logic

The LacI/IPTG system is one of the most well-characterized transcriptional regulatory mechanisms in molecular biology, consisting of the LacI repressor protein that binds lac operator (lacO) DNA sequences to block transcription and is allosterically inhibited by isopropyl-β-D-thiogalactopyranoside (IPTG), a non-hydrolyzable galactose analogue that causes conformational changes in LacI reducing its DNA-binding affinity. In this project, the system is repurposed as a concentration-sensitive analog switch: by engineering different numbers and configurations of lacO operators upstream of each chromoprotein coding sequence — none for amilCP, one weak site for spisPink, two medium sites for amilGFP, three strong sites for eforRed — the circuit creates four distinct IPTG thresholds at which each gene transitions from repressed to expressed. When all four plasmids are combined in the same well and IPTG is titrated across the plate, the competitive interplay between de-repression thresholds produces a sequential color shift — first blue-purple as amilCP is constitutively expressed, then pink as spisPink de-represses, then yellow-green as amilGFP follows, and finally red as eforRed de-represses at the highest IPTG concentrations — transforming a simple chemical gradient into a multi-chromoprotein color gradient that functions as both a genetic circuit readout and a visual art installation.

---

# SECTION 6: PROJECT VALIDATION

## 10a — Validation Choice

The validation experiment is a **single-plasmid cell-free expression test** in which each of the four chromoprotein plasmids is expressed individually in BL21(DE3) CFPS reactions, with absorbance confirmed by Spark Plate Reader at each chromoprotein's target wavelength. This validation is essential to confirm that each Twist Bioscience whole-plasmid synthesis was successful, that the T7 promoter and lacO configurations function as designed in the BL21(DE3) extract, and that each chromoprotein produces a quantifiable, visually distinct color signal before combining all four plasmids in the full mosaic experiment.

---

## 10b — Validation Protocol

1. Prepare BL21(DE3) CFPS master mix on ice as described in Step 4.
2. Prepare 5 CFPS reactions: one per plasmid (pTwist-T7-amilCP, pTwist-T7lacO1-spisPink, pTwist-T7lacO2-amilGFP, pTwist-T7lacO3-eforRed) and one no-DNA negative control.
3. Add each plasmid at 10 ng/µL final concentration to its designated reaction.
4. Dispense 10 µL per well into 5 columns (4 wells each) of 384-flat-corning-3640 using Multiflo.
5. For lacO-containing plasmids (spisPink, amilGFP, eforRed), include paired wells: one with 0 µM IPTG (repressed control) and one with 5000 µM IPTG (fully de-repressed).
6. Seal all wells with A4s breathable membrane.
7. Incubate 37°C for 4 hours in Inheco Plate Incubator.
8. Peel A4s seal using XPeel.
9. Read Spark Plate Reader at 507, 525, 559, 588 nm and reference 700 nm.
10. Confirm amilCP wells show absorbance >0.3 at 588 nm in both +/− IPTG conditions (constitutive).
11. Confirm spisPink, amilGFP, and eforRed wells show ≥2-fold higher absorbance at their target wavelengths in +IPTG vs. −IPTG wells, confirming LacI repression and IPTG de-repression are functional.
12. Confirm no-DNA control shows background absorbance only at all wavelengths.
13. Photograph plate on white background to visually confirm distinct colors per plasmid.

---

## 10c — Techniques Used

This validation integrates three complementary techniques to confirm the full construct and circuit functionality. Cell-free protein synthesis is used as the primary expression platform, confirming that the Twist whole-plasmid synthesis delivered functional constructs with active T7 promoters and correctly translated chromoprotein CDSs — a single-step functional test that simultaneously validates synthesis quality, codon optimization, and protein folding. Absorbance spectrophotometry on the Spark Plate Reader provides quantitative confirmation that each chromoprotein absorbs at its expected wavelength and at levels significantly above background, establishing the signal-to-noise ratio for the full mosaic experiment and confirming that the 4-hour incubation time is sufficient for visible color development. The paired ±IPTG comparison for the three lacO-containing plasmids directly validates the LacI circuit logic — confirming that lacO operators are functional repressor binding sites in the cell-free context and that IPTG at 5000 µM fully de-represses each construct — without which the gradient mosaic would produce uniform color rather than a sequential shift. Together, these three readouts — expression, absorbance quantification, and circuit logic confirmation — constitute a complete functional validation of all experimental components before the full 384-well mosaic run.

---

## 10d — Hypothetical Data

The following table presents simulated absorbance values (normalized to maximum per chromoprotein) expected from the full mosaic experiment based on the circuit design parameters.

**Hypothetical Normalized Absorbance Data (4 hr, 37°C CFPS)**

| IPTG (µM) | amilCP 588nm | spisPink 559nm | amilGFP 507nm | eforRed 525nm | Dominant Color |
|---|---|---|---|---|---|
| 0 | 1.00 | 0.04 | 0.03 | 0.02 | Blue-purple |
| 10 | 0.97 | 0.12 | 0.04 | 0.02 | Blue-purple |
| 50 | 0.89 | 0.51 | 0.06 | 0.03 | Blue-purple/Pink |
| 100 | 0.82 | 0.74 | 0.09 | 0.04 | Pink |
| 500 | 0.71 | 0.88 | 0.48 | 0.06 | Pink/Yellow |
| 1000 | 0.65 | 0.79 | 0.82 | 0.11 | Yellow-green |
| 2500 | 0.60 | 0.63 | 0.91 | 0.44 | Yellow-green |
| 5000 | 0.58 | 0.55 | 0.76 | 0.95 | Red |

**Simulated Circuit Response — ASCII Bar Chart**
*(Normalized absorbance at each IPTG concentration; bar length = relative expression)*

```
amilCP  (588nm) — Blue-Purple
  0 µM   ████████████████████████████████████████  1.00
 10 µM   ███████████████████████████████████████   0.97
 50 µM   ████████████████████████████████████      0.89
100 µM   █████████████████████████████████         0.82
500 µM   ████████████████████████████              0.71
1000 µM  ██████████████████████████                0.65
2500 µM  ████████████████████████                  0.60
5000 µM  ███████████████████████                   0.58

spisPink (559nm) — Pink
  0 µM   ██                                        0.04
 10 µM   █████                                     0.12
 50 µM   █████████████████████                     0.51
100 µM   ██████████████████████████████            0.74
500 µM   ████████████████████████████████████      0.88
1000 µM  ████████████████████████████████          0.79
2500 µM  █████████████████████████                 0.63
5000 µM  ██████████████████████                    0.55

amilGFP  (507nm) — Yellow-Green
  0 µM   █                                         0.03
 10 µM   ██                                        0.04
 50 µM   ██                                        0.06
100 µM   ████                                      0.09
500 µM   ████████████████████                      0.48
1000 µM  █████████████████████████████████         0.82
2500 µM  █████████████████████████████████████     0.91
5000 µM  ███████████████████████████████           0.76

eforRed  (525nm) — Red
  0 µM   █                                         0.02
 10 µM   █                                         0.02
 50 µM   █                                         0.03
100 µM   ██                                        0.04
500 µM   ██                                        0.06
1000 µM  █████                                     0.11
2500 µM  ██████████████████                        0.44
5000 µM  ███████████████████████████████████████   0.95
```

The data demonstrates clean sequential circuit de-repression: amilCP dominates at low IPTG, each subsequent chromoprotein peaks at its characteristic threshold, and eforRed becomes dominant only at maximal IPTG — producing the full blue-purple → pink → yellow-green → red gradient.

---

## Troubleshooting

The most likely challenge is uneven or weak chromoprotein color development across the plate, which can result from insufficient expression time, suboptimal magnesium concentration in the CFPS extract, or degradation of one or more plasmids during storage; the first corrective step is to extend incubation from 4 to 6 hours and to run a fresh Mg²⁺ titration (4–12 mM) on the extract to identify the optimal concentration for chromoprotein folding specifically. A second issue is potential crosstalk between chromoprotein absorbance spectra — for example, amilCP and eforRed have partially overlapping excitation profiles — which can compress the apparent color difference between adjacent gradient zones; this is addressed by using multiwavelength spectral deconvolution during data analysis and by selecting well-spacing between conditions that maximizes the gradient step size. If the LacI circuit de-repression does not occur at expected IPTG thresholds, it is likely that LacI concentration in the BL21(DE3) extract is lower than anticipated, causing de-repression to occur at lower IPTG than designed; this can be corrected by adding purified LacI protein (commercially available from NEB) to the master mix to reset the repression baseline. Finally, lipid membrane components in the cell-free extract can cause turbidity at 384-well scale that elevates background absorbance uniformly across wavelengths; including 700 nm reference subtraction and running a cell-free extract only (no plasmid) control well in every experiment are essential corrective practices.

---

# SECTION 7: ADDITIONAL INFORMATION

## References

- Liljeruhm J, Funk SK, Tietscher S, Edlund AD, Jamal S, Wurtzel E, Forster AC. (2018). Engineering a palette of eukaryotic chromoproteins for bacterial synthetic biology. *Journal of Biological Engineering*, 12(1), 8.

- Pardee K, Green AA, Takahashi MK, Braff D, Lambert G, Lee JW, et al. (2016). Rapid, Low-Cost Detection of Zika Virus Using Programmable Biomolecular Components. *Cell*, 165(5), 1255–1266.

- Gardner TS, Cantor CR, Collins JJ. (2000). Construction of a genetic toggle switch in *Escherichia coli*. *Nature*, 403(6767), 339–342.

- Muldoon JJ, Bhatt S, Bhargava S, Bhargava H, Bhargava A, Bhargava R, et al. (2021). Model-guided design of mammalian genetic programs. *Science Advances*, 7(8), eabe9375.

- Noireaux V, Libchaber A. (2004). A vesicle bioreactor as a step toward an artificial cell assembly. *Proceedings of the National Academy of Sciences*, 101(51), 17669–17674.

- Zubko E, Tyrnov OA, Makarenko MV, et al. (2012). Spectroscopic properties of chromoproteins from the reef coral *Acropora millepora*. *Journal of Photochemistry and Photobiology B: Biology*, 113, 56–62.

---

## Supplies and Budget

| Item | Supplier | Qty | Est. Cost | Link |
|---|---|---|---|---|
| pTwist-T7-amilCP (whole plasmid) | Twist Bioscience | 1 | ~$199 | [twistbioscience.com](https://www.twistbioscience.com) |
| pTwist-T7lacO1-spisPink (whole plasmid) | Twist Bioscience | 1 | ~$199 | [twistbioscience.com](https://www.twistbioscience.com) |
| pTwist-T7lacO2-amilGFP (whole plasmid) | Twist Bioscience | 1 | ~$199 | [twistbioscience.com](https://www.twistbioscience.com) |
| pTwist-T7lacO3-eforRed (whole plasmid) | Twist Bioscience | 1 | ~$199 | [twistbioscience.com](https://www.twistbioscience.com) |
| BL21(DE3) CFPS Extract (S12, in-house) | Lab stock / NEB | — | ~$80 | [neb.com](https://www.neb.com) |
| CFPS Energy Solution + NTPs + Amino Acids | Millipore Sigma | 1 set | ~$200 | [sigmaaldrich.com](https://www.sigmaaldrich.com) |
| IPTG (I6758, ≥99%) | Millipore Sigma | 1 g | ~$40 | [sigmaaldrich.com](https://www.sigmaaldrich.com) |
| 384-flat-corning-3640 clear flat plates | Thermo Fisher | 10 plates | ~$180 | [thermofisher.com](https://www.thermofisher.com) |
| 384-well Echo PP source plates | Beckman Coulter | 5 plates | ~$100 | [thermofisher.com](https://www.thermofisher.com) |
| A4s breathable seals | Millipore Sigma | 1 pack | ~$50 | [sigmaaldrich.com](https://www.sigmaaldrich.com) |
| Ampicillin sodium salt (A9518) | Millipore Sigma | 5 g | ~$35 | [sigmaaldrich.com](https://www.sigmaaldrich.com) |
| Nanodrop consumables + tips | Thermo Fisher | 1 set | ~$30 | [thermofisher.com](https://www.thermofisher.com) |
| Agarose gel supplies | Thermo Fisher | 1 set | ~$40 | [thermofisher.com](https://www.thermofisher.com) |
| LB broth, TE buffer, standard consumables | Lab stock | — | ~$50 | — |
| **Total Estimated Budget** | | | **~$1,601** | |

---

### Industry Partner Connections

| Partner | Role in This Project |
|---|---|
| **Twist Bioscience** | Whole plasmid synthesis of all 4 chromoprotein constructs |
| **Ginkgo Bioworks** | Cell-free protein synthesis lab infrastructure and scale-up |
| **Asimov (Kernel Platform)** | In silico genetic circuit design and modeling of LacI transfer functions |
| **Addgene** | Repository for chromoprotein reference sequences and plasmid deposition |
| **New England Biolabs** | BL21(DE3) competent cells and CFPS reagents |
| **Thermo Fisher Scientific** | Microplates, Spark Plate Reader, imaging consumables |
| **Millipore Sigma** | IPTG, CFPS reagents, sealing materials |
| **BioFabricate** | Bio-art community partner for public presentation and artistic collaboration |
| **Ginkgo Bioworks** | Lab infrastructure for CFPS execution and scale-up for larger chromoprotein display installations |
| **SecureDNA** | Biosecurity screening of all synthetic DNA sequences prior to order |

---

*Proposal prepared as part of HTGAA Final Project. All plasmid sequences, Echo dispensing scripts, and Spark plate reader protocols available upon request. The four Twist whole-plasmid constructs will be deposited to Addgene upon publication.*
