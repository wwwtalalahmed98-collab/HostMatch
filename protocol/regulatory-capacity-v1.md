# Regulatory capacity, version 1 — conflict 6

**The question:** the proteome analysis concluded the chassis must carry 37
capabilities and switch on only what each product needs. That requires 37
independently addressable switches. **Do they exist?**

**Answer: yes, but only by one route, and the margin is zero.**

Classical protein switches top out well short of 37. CRISPR-based *repression*
hits a measured ceiling of about a dozen. CRISPR-based *activation* — which is
the modality we actually need — is the one documented to scale, and it provides
unlimited addresses because the address is a programmable RNA sequence rather
than a protein.

---

## What is actually available, by type

### Classical protein transcription factors — short of 37

The field's own assessment of routine practice:

> *"most artificial networks still employ **the same core set of TFs (for example
> LacI, TetR and cI)**"*

Three. The best engineered toolkits do considerably better:

| Resource | Size |
|---|---|
| Engineered orthogonal dual TFs | **12 TFs**, across up to 270 synthetic promoters |
| Sigma-factor toolbox for *E. coli* | a characterised set with a published crosstalk map |
| Genomic mining of prokaryotic repressors | a library built by "part mining" natural repressors |
| LacI/GalR family chimeras | modular multi-input gating |
| COMET (mammalian) | *"a toolkit of multiple orthogonal and well-characterized transcription factors"* |

**Realistic ceiling: roughly 12–20 well-characterised orthogonal protein
regulators, and only after crosstalk mapping.** Short of 37, and each one costs
proteome.

There is also a theoretical floor on how good this can get:

> *"a **lower bound on crosstalk severity** can be analytically derived solely
> from the number of (co)regulated genes and a suitable parameter that describes
> binding site similarity"*

Crosstalk is not merely an engineering nuisance. It scales with how many genes
you regulate.

### CRISPR repression — a measured ceiling of about a dozen

This is the hard number:

> *"In E. coli, **CRISPRi cannot support more than about a dozen simultaneous
> gRNAs** before the fold repression of any individual gRNA drops below 10×"*

The cause is shared-resource competition, not specificity:

> *"despite **highly specific sgRNA-promoter binding**, multiple sgRNAs still
> **interfere with one another by competing for dCas9**"*

So programmability does not rescue you. Every guide draws on one pool of dCas9
protein, and the pool runs out.

### CRISPR activation — the one that scales, and the one we need

> *"Modeling predicts that **CRISPR-based activators, unlike CRISPR-based
> repressors, scale well** with increasing gRNA competition and dCas9
> bottlenecking"*

**This matters more than anything else in this document.** Switching capabilities
*on* is activation. The modality the architecture requires is the modality that
scales.

### De-novo-designed RNA regulators — a large address space

> *"Efforts to construct synthetic networks in living cells have been hindered by
> the **limited number of regulatory components**… Here, we report a class of
> **de-novo-designed** prokaryotic riboregulators called **toehold switches**"*

Plus de-novo-designed translational repressors and programmable trans-splicing
riboregulators. Because these are designed from sequence rather than mined from
nature, the orthogonal set is bounded by sequence space, not by discovery.

---

## The resolution

The requirement was stated imprecisely. Correcting it dissolves most of the
problem:

**We do not need 37 switches on at once. We need 37 distinct addresses, with
about 5–12 active at a time.**

| Requirement | Supply |
|---|---|
| **37 distinct addresses** | Unlimited with CRISPRa or de-novo riboregulators — the address is a nucleic-acid sequence, and sequence space is vast |
| **5–12 simultaneously active** | Matches the measured multiplexing ceiling of about a dozen |

The two halves fit. **Conflict 6 is resolved — for activation, not repression,
and with no margin at all.**

## The coincidence worth staring at

Two entirely independent analyses landed on the same number:

- **Proteome budget:** a product needs **5–12** capabilities on at once, and the budget accommodates up to about 12
- **Regulatory capacity:** about **a dozen** simultaneous CRISPR guides before performance degrades

Either there is a shared underlying constraint — both are shared-resource
competition problems, so this is plausible — or it is coincidence. Worth
examining, because if it is real it suggests **twelve is the natural width of an
engineered cell**, and the chassis should be designed around that number rather
than against it.

## Costs this introduces

- **dCas9 is a large protein and is toxic at high levels.** A paper exists titled
  *"Engineered dCas9 with reduced toxicity in bacteria: implications for genetic
  circuit design."* The control system itself consumes part of the proteome
  budget the control system was invented to manage.
- **Guide arrays must be expressed and processed.** dCas12a is noted as better
  here because of *"built-in RNase activity which can process a single CRISPR RNA
  array"*.
- **Leakiness.** CRISPRi *"often suffers from leakiness in the uninduced state"* —
  for a chassis carrying 37 silent capabilities, leak across all of them is a
  cumulative burden nobody has quantified.

## Fourth architectural requirement

Alongside *compartmentalised*, *not minimal*, and *switchable*:

**4. Control must be nucleic-acid-addressed (CRISPRa-type or designed
riboregulators), not protein-addressed.** Protein regulators cannot reach 37
distinct addresses, and each one spends proteome the capabilities need.

## What is not done

- **Nobody has demonstrated 37 addressable capabilities in one organism.** The
  largest multiplex found here is ten genes silenced simultaneously in
  *Legionella*. The argument is that the parts compose; it has not been shown.
- **The ~12 ceiling is measured for CRISPRi in *E. coli*.** The claim that
  CRISPRa scales better comes from **modelling**, not from an experiment that
  pushed activation to its limit. That is the weakest link in this document.
- **Cumulative leak across 37 silent capabilities is unquantified**, and could
  be the real ceiling.
- **Eukaryotic numbers are thinner.** Most hard figures here are *E. coli*, while
  the conflict map pointed toward eukaryotes.
- Quotes are from abstracts, unverified against full papers.
