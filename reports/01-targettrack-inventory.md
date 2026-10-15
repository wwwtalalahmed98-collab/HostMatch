# TargetTrack (PSI, 2000-2017): is it a usable multi-host expression dataset?

**Verdict: mostly no, with one narrow but real exception worth harvesting.**

**The headline answer is negative.** There is no expression-host field anywhere
in the TargetTrack schema — not on the target, not on the trial, not on the
protocol. The schema declares 110 elements and 11 controlled vocabularies, and
none of them is a host. Host is recoverable *only* by text-mining free-text
protocol prose, and where it is recoverable it is overwhelmingly *E. coli*:
of 335,771 targets, **129,831 (38.7%) yield any host label at all, and 128,849
of those are *E. coli***. The single machine-readable host convention that
exists — a `host:` key some centres write into a per-trial free-text field —
takes **exactly one distinct value across all 86,090 occurrences: *Escherichia*
(coli)**. This answers the "did nobody ask, or is it not there?" question: the
contrast is not there. Prior groups mined TargetDB/PepcDB for *E. coli*
solubility because that is what the data supports.

**The exception.** A handful of membrane-protein and eukaryotic-protein centres
(chiefly NYSGRC/AECOM, NYSGXRC/GNF and MPP) really did run the same target
through *E. coli*, insect, mammalian and cell-free pipelines as separate trials,
each trial carrying its own enumerated outcome status. Mining this out gives
1,784 targets whose trials carry 2+ host labels — but **only 989 of those
(0.29% of all targets) survive trial-by-trial verification** as genuine pairs.
The other 748 are an artefact of one CSGID protocol whose preamble mentions
*E. coli* rhetorically (see §4). At sequence level, 2,034 distinct proteins
carry 2+ host labels before verification, so roughly **1,100-1,200 after**.
A genuine record looks like:

```
NYSGRC target 005597   e-coli -> work stopped (x3)
                       insect -> soluble (x2)
                       mammalian -> work stopped
```

That is exactly the contrast this project needs, with sequences attached.

**Recommendation.** Do not rebuild the project on TargetTrack — it is an
*E. coli* monoculture and will not scale the paired dataset by an order of
magnitude. But ~1,000 verified multi-host proteins is the same order as the
current ~1,400 hand-curated observations, from a permissively licensed source
(CC-BY-SA 4.0), so it is worth extracting as a second corpus **after manual
validation** — the host labels are regex over prose, not curated fields, and
42.7% of the naive multi-host hits were false. Two caveats in opposite
directions: 245,733 protocol references (9.2%) dangle and their hosts are
unrecoverable, so 989 is a floor; but the pairs are concentrated in a few
membrane-protein centres, so the subset is not representative of proteins
generally.

---

## 1. Is expression host recorded? No.

**There is no host element at any level of the schema** — not on the target, not
on the trial, not on the protocol.

`targetTrack-v1.4.1.xsd` declares 110 elements. The complete list contains no
`host`, `expressionHost`, `strain`, `cellLine`, `vector` or `plasmid` element:

```
address contactInfo contactInfoId contactInfoList contactInfoRefList country
databaseId databaseName databaseRef databaseRefList dateComplete dateCreated
dateUpdated email formatVersion lab laboratoryList ligand ligandList ligandName
ligandRole ligandRoleAssignDate ligandType ligandTypeFormula ligandTypeList
ligandTypeName measurement measurementList measurementName measurementProcedure
measurementUncertainty measurementUnit measurementValue name oneLetterCode
organization outcomeDetails partnershipName partnershipRoleDetails
partnershipRoleDetailsRemark partnershipRoleDetailsValue partnershipTargetId
partnershipTargetIdSource partnershipTargetIdValue prevStatusHistoryId project
projectId projectList projectName protocol protocolDescription protocolDetails
protocolId protocolList protocolName protocolRef protocolText protocolType
relatedTargetId relatedTargetIdList remark role scientificName
sequenceChemicalType sequenceConstructType sequenceDetails sequenceModifications
sequenceName sequenceType site sourceOrganism status statusHistory
statusHistoryList stepDurationDays stopDetails stopStatus target
targetAnnotation targetCategory targetCategoryList targetCategoryName targetId
targetName targetPartnership targetPartnershipList targetProteinType
targetRationale targetReference targetSequence targetSequenceList
targetStopDetails targetTrack taxDB taxId trial trialDetails trialId trialList
trialMeasurement trialMeasurementId trialMeasurementList trialOutcome
trialOutcomeId trialOutcomeList trialProtocolId trialProtocolList trialSequence
trialSequenceList trialStep url
```

> **Trap:** `sourceOrganism` (`scientificName`, `taxId`, `taxDB`) is **required**
> on every target sequence and is easy to mistake for the host. It is the
> organism the protein *comes from*, not the organism it was *expressed in*. Any
> pipeline that reads `sourceOrganism` as a host label is simply wrong.

The enumerations spreadsheet (`targetTrackEnumeratedDataItems-v1.4.1.xls`)
confirms this independently. It defines **11 controlled vocabularies** and none
of them is a host:

1. Sequence Type · 2. Sequence Chemical Type · 3. Sequence Construct Type ·
4. Target Category Name · 5. Target Protein Type · 6. Status (Target or Trial) ·
7. Stop Status (Target or Trial) · 8. Protocol Type · 9. Partnership Name ·
10. Partnership Role Details Value · 11. Partnership Target ID Source

The strings "host", "strain" and "chassis" appear **zero** times in that
spreadsheet; "vector" appears once, as the partnership role
`provided vector sample`.

### Where host information does survive

Two free-text fields, neither enumerated, neither required:

| Field | Level | What it is |
|---|---|---|
| `protocol/protocolText` | shared protocol document | Prose SOP. Hosts appear as incidental prose ("transformed to expression host BL21(DE3)", "infect Sf9 insect cells"). |
| `trial/trialProtocolList/protocolRef/protocolDetails` | **per trial** | Free-text deviation note. A few centers write loose `key: value` text into it. |

The `protocolDetails` convention is the only per-trial host signal, e.g.

```
host: Escherichia coli  strain: BL21 DE3 gold magic  vector: pMCSG7
induction chemical: IPTG  expression temperature: 37  media: TB
```

Trials reference protocols through `protocolRef/protocolId`, which is
**center-local**: the join key is the protocol's `@id` attribute, formed as
`<CENTER>-<protocolId>`, and the center must be taken from the target's own
`@id` (`<CENTER>-<targetId>`). Joining on `protocolId` alone silently merges
protocols from different centers.

---

## 2. The protocol-level host vocabulary

There are **1,494 protocol documents** in the entire archive, shared across all
~350k targets. Only **301** are of `protocolType = "expression"`. Mining their
`protocolName` + `protocolDescription` + `protocolText`:

| Host label mined from protocol text | Expression protocols |
|---|---:|
| *E. coli* only | 198 |
| **no host determinable** | 59 |
| insect only | 16 |
| yeast only | 13 |
| cell-free only | 8 |
| mammalian only | 3 |
| *E. coli* + insect | 2 |
| *E. coli* + mammalian | 1 |
| *E. coli* + yeast | 1 |
| **total** | **301** |

242 of 301 (80.4%) yield a host; **198 of those 242 (81.8%) are *E. coli* only**,
and only 44 protocols involve any non-*E. coli* host at all.

### The per-trial `protocolDetails` vocabulary

Across the whole file there are **1,565,957** non-empty `protocolDetails`
blocks, of which **742,733 (47.4%)** contain at least one `key: value` pair:

| Key | Occurrences | Distinct values |
|---|---:|---:|
| `vector` | 572,617 | 867 (combined with `cloning vector`) |
| `media` | 356,716 | — |
| `cloning vector` | 153,135 | — |
| `strain` | 96,943 | 30 |
| **`host`** | **86,090** | **1** |
| `expression temperature` | 37,876 | — |
| `induction chemical` | 31,003 | — |

**The decisive number in this whole report: the `host:` key takes exactly one
distinct value across all 86,090 occurrences — `Escherichia` (coli).** Where a
center bothered to state the host explicitly and machine-readably, it was
*E. coli* every single time.

The 30 `strain:` values are likewise all *E. coli* strains (`BL21magic` 54,689,
`BL21Magic` 16,182, `DL41` 7,795, `BL21` 5,700, `HK100` 2,739,
`BL21-CodonPlus(DE3)-RIPL` 2,627, `BL21 DE3 gold magic` 1,749, `ROSETTA` 128, …).

Non-*E. coli* hosts appear in `protocolDetails` only as loose prose, not under
the `host:` key, and at trivial volume: `Sf9` 1,615 mentions, `wheat germ` 411,
`insect` 21, `cell free`/`cell-free` 22, `CHO` 15, `mammalian` 1 — against
86,136 `Escherichia` and 84,021 `BL21` mentions.

---

## 3. Coverage: how many of the 335,771 targets carry a usable host?

Denominators, counted directly from `tt.xml.gz`: **335,771 `<target>` elements**
and **961,548 `<trial>` elements**. (The commonly quoted ">350,000 targets"
includes legacy/withdrawn entries; the deposited XML holds 335,771.)

| Quantity | Targets | % of 335,771 |
|---|---:|---:|
| Targets in `tt.xml.gz` | 335,771 | 100% |
| …with a protein sequence | 334,987 | 99.8% |
| …with any `status` | 335,771 | 100% |
| …with a real experimental outcome (beyond "selected"/"work stopped") | 237,217 | 70.6% |
| …referencing an expression protocol | 129,607 | 38.6% |
| **…with a mined expression host** | **129,831** | **38.7%** |
| …with host **and** outcome | 128,538 | 38.3% |
| …with host **and** sequence | 129,800 | 38.7% |
| **…with host and outcome and sequence** | **128,507** | **38.3%** |
| **…with 2+ distinct hosts** | **1,784** | **0.53%** |

Where the host label comes from:

| Source | Targets |
|---|---:|
| shared `protocolText` only | 81,502 |
| per-trial `protocolDetails` only | 42,708 |
| both | 5,621 |
| **total with a host** | **129,831** |

At trial level, 572,914 of 961,548 trials (59.6%) carry a mined host.

### The host distribution is the problem

| Host | Targets | % of 129,831 with a host | Trials |
|---|---:|---:|---:|
| ***E. coli*** | **128,849** | **99.2%** | 566,267 |
| mammalian | 1,383 | 1.07% | 4,896 |
| insect | 982 | 0.76% | 3,981 |
| cell-free | 492 | 0.38% | 1,008 |
| yeast | 38 | 0.03% | 64 |
| other bacteria | 1 | 0.001% | 1 |

(Rows sum past 100% because a target may have several hosts.)

Non-*E. coli* host assignments total roughly 2,900 targets — **0.86% of the
archive**. There is effectively no yeast data and no plant/algal data at all.

Why coverage stops at 38.7%: 695,651 protocol references declare
`protocolType = expression`, but **108,417 of them resolve to a protocol whose
text yields no host**, and a further 245,733 references (9.2% of 2,927,151)
dangle — they name a protocol absent from `protocolList`, concentrated almost
entirely in CSGID. Those trials' hosts are unrecoverable at any effort.

---

## 4. The critical number: proteins tried in more than one host

Grouping by **exact target protein sequence identity** (SHA-1 of
`oneLetterCode`), restricted to sequences that carry at least one host:

| Distinct hosts for the same sequence | Distinct sequences |
|---|---:|
| 1 | 144,165 |
| 2 | 1,898 |
| 3 | 136 |
| **2 or more** | **2,034** |

146,199 distinct sequences carry a host; **2,034 of them (1.4%) were tried in
two or more distinct hosts.**

At target level, 1,784 targets have 2+ hosts, distributed as:

| Host combination | Targets |
|---|---:|
| *E. coli* + mammalian | 776 |
| *E. coli* + insect | 547 |
| insect + mammalian | 185 |
| cell-free + *E. coli* | 145 |
| *E. coli* + insect + mammalian | 130 |
| *E. coli* + yeast | 1 |

and are concentrated in a few labs: AECOM 890, GNF 739, MPP 95, Pagliarini_UW
34, everything else ≤5.

### Are these real pairs, or text artefacts? Only about half are real.

A target counts as multi-host above if the union of host labels mined across
its trials has 2+ members. That union can be produced two ways: by *different
trials carrying different hosts* (a real pair) or by *one trial's protocol text
mentioning two hosts* (an artefact). Re-examining every multi-host target trial
by trial over the whole archive:

| Verdict | Targets | Share |
|---|---:|---:|
| **REAL** — different trials, each with its own single host | **989** | **56.5%** |
| ARTEFACT — one trial's text names two hosts | 748 | 42.7% |
| MIXED — mostly real, but one trial's text names two hosts | 14 | 0.8% |

**744 of the 748 artefacts trace to a single protocol**, CSGID's
`WU_PEI_transient_transfection`. It is a mammalian transfection protocol whose
introduction reads "The majority of targets produced by the CSGID are expressed
in *E. coli*… for proteins not amenable… we have been exploring… mammalian
cells". The *E. coli* mention is rhetorical background, not the host used, and
every target referencing that protocol inherited a spurious
`e-coli|mammalian` label. This is a good illustration of why regex-over-prose
host labels need human validation before use.

So the genuine count is **989 targets**, broken down as:

| Host combination | Real pairs |
|---|---:|
| *E. coli* + insect | 513 |
| insect + mammalian | 172 |
| cell-free + *E. coli* | 145 |
| *E. coli* + insect + mammalian | 105 |
| *E. coli* + mammalian | 54 |
| **total** | **989** |

Applying the same 56.5% genuine rate to the 2,034 sequence-level figure gives
roughly **1,100-1,200 distinct proteins** with a verified multi-host record.

For those real pairs the outcome genuinely varies by host, which is the whole
point — these are per-trial statuses, not a target-level union:

| Host | work stopped | soluble | expression tested | purified | expressed | crystallized |
|---|---:|---:|---:|---:|---:|---:|
| *E. coli* | 2,117 | 722 | 382 | 198 | 136 | 23 |
| insect | 1,037 | 571 | 418 | 308 | 83 | 40 |
| mammalian | 352 | 191 | 175 | 21 | 4 | 0 |
| cell-free | 4 | 69 | 0 | 16 | 133 | 0 |

Insect reaches soluble/purified notably more often than *E. coli* on this
membrane-protein-heavy subset, and cell-free almost never records a hard
failure. Real, usable signal — on ~1,000 proteins, not ~350,000.

Representative records:

```
NYSGRC 005597   e-coli -> work stopped (x3) | insect -> soluble (x2) | mammalian -> work stopped
MPP GO.111408   e-coli -> work stopped (x3) | cell-free -> soluble
MPP GO.111407   e-coli -> soluble           | cell-free -> soluble
```


---

## 5. Vector and strain granularity

Better than the host granularity, because the `protocolDetails` convention
records them explicitly.

| | Distinct values | Targets covered |
|---|---:|---:|
| Vector | 877 | 143,235 (42.7%) |
| Strain | 58 | 108,076 (32.2%) |

Top vectors (from `vector:` / `cloning vector:`): `SpeedET` 273,097, `pMCSG7`
66,424, `pET21_NESG` 54,324, `pSGC-His` 41,338, `pMCSG19` 25,600,
`pET15_NESG` 25,141, `pSGX3 (BC)` 23,375, `pMCSG68` 15,062, `pMCSG73` 13,422,
`p15Tv lic` 10,835.

Top strains: `BL21magic` 54,689, `BL21Magic` 16,182, `DL41` 7,795, `BL21`
5,700, `HK100` 2,739, `BL21-CodonPlus(DE3)-RIPL` 2,627, `BL21 DE3 gold magic`
1,749, `BL21-CodonPlus(DE3)-RIL` 1,163, `BL21-CodonPlus(DE3)-RP` 480,
`ROSETTA`/`Rosetta`/`rosetta` 193.

Every one of the 30 `strain:` values is an *E. coli* strain. So the archive has
**fine-grained strain and vector detail within a single host** and almost no
detail across hosts — the opposite of what this project needs.

---

## 6. Are protein sequences included? Yes — this part is excellent.

Sequences are present inline in the XML (`targetSequence/oneLetterCode` and
`trialSequence/oneLetterCode`) and as standalone FASTA:

| File | Records |
|---|---:|
| `proteinTargetSeqs.fasta.gz` (target sequences) | 340,594 |
| `proteinTrialSeqs.fasta.gz` (per-trial constructs) | 963,470 |
| `dnaTargetSeqs.fasta.gz` / `dnaTrialSeqs.fasta.gz` | present |
| `rnaTargetSeqs.fasta.gz` / `rnaTrialSeqs.fasta.gz` | empty (0 bytes) |

340,594 target FASTA records collapse to **304,178 distinct protein sequences**.
Trial sequences are the actual expressed constructs (truncations, mutations,
tags) and their FASTA headers carry the trial's current status, so
sequence→outcome joins need no XML parsing at all.

Sequence availability is therefore *not* the blocker. The blocker is the host label.

### Upper bound on pairing potential

Even ignoring the host problem entirely, the ceiling on cross-center pairs is
modest. Grouping the 304,178 distinct target sequences by how many distinct
centers declared them:

| Distinct centers declaring the same sequence | Sequences |
|---|---:|
| 1 | 280,966 |
| 2 | 20,206 |
| 3 | 2,533 |
| 4 | 404 |
| 5 | 61 |
| 6 | 8 |
| **2 or more** | **23,212** |

So **23,212 proteins (7.6%)** were attempted at two or more centers. That is the
absolute maximum number of cross-center pairs — and it only becomes a *host*
pair if the two centers used different hosts. Since essentially every center ran
*E. coli*, almost none of these 23,212 are host-contrasting pairs.

---

## 7. Outcome fields: present, enumerated, and genuinely good

This is TargetTrack's strength. Outcome is recorded at both target and trial
level, from a 30-value controlled vocabulary (`status`), with a parallel
19-value failure vocabulary (`stopStatus`).

Trial-level current status, from the 963,470 `proteinTrialSeqs.fasta.gz` headers:

| Status | Trials |
|---|---:|
| work stopped | 180,562 |
| diffraction-quality crystals | 180,306 |
| purified | 177,347 |
| cloned | 96,719 |
| expressed | 91,056 |
| selected | 78,709 |
| soluble | 70,837 |
| crystallized | 24,301 |
| expression tested | 21,744 |
| in PDB | 15,713 |
| diffraction | 7,844 |
| mass spec verified | 4,748 |
| crystal structure | 4,446 |
| other | 3,861 |
| native diffraction-data | 2,905 |
| HSQC satisfactory | 1,446 |
| NMR structure | 288 |
| phasing diffraction-data | 205 |
| biological assay | 187 |
| membrane protein solubilized | 147 |
| biophysical analysis | 64 |
| NMR assigned | 12 |
| EM images | 10 |
| test target | 7 |
| EM fitted model | 2 |

Failure reasons (`stopStatus`, 210,748 values over 53,835 `targetStopDetails`
blocks plus trial-level `stopDetails`):

| Stop status | Count |
|---|---:|
| other | 84,719 |
| **expression failed** | **48,130** |
| cloning failed | 21,418 |
| purification failed | 18,371 |
| duplicate target found | 14,434 |
| structure successful | 10,024 |
| poor diffraction | 6,422 |
| crystallization failed | 5,155 |
| PDB duplicate found | 1,409 |
| sequencing failed | 512 |
| poor NMR | 75 |
| mass spec failed | 66 |
| membrane protein solubilization failed | 10 |
| biophysical analysis failed | 3 |

48,130 explicit "expression failed" records plus ~91k "expressed" and ~71k
"soluble" is a large, clean, labelled success/failure corpus. It is, however,
an *E. coli* corpus with the host left implicit — exactly the kind of data
SoluProt, EPSOL, ESPRESSO and RPOLP were already built on.

---

## 8. Data quality problems observed

1. **Host is free text, not an enumeration.** Recovering it requires regex over
   prose, with real false-positive traps. Naive patterns fail badly: bare
   `yeast` matches "5 g **yeast extract**" in LB/TB/SOC media recipes, and bare
   `cell-free` matches "drain off **cell-free media**" (the spun-off
   supernatant). Before tightening these two patterns, 21 of 274 expression
   protocols were mislabelled as yeast or cell-free. The classifier in
   `scripts/targettrack.py` requires an expression-system context for both.
2. **`sourceOrganism` is not the host** (see §1). It is required and populated,
   which makes it a very attractive wrong answer.
3. **Protocol prose mentions hosts it did not use.** CSGID's
   `WU_PEI_transient_transfection` opens by noting that most CSGID targets are
   expressed in *E. coli* before describing a mammalian method. Mining the text
   naively gave 744 targets a false `e-coli + mammalian` pair — 42.7% of all
   apparent multi-host targets in the archive. Host labels mined from prose must
   be verified trial-by-trial, and then by hand.
4. **`protocolId` is center-local and collides.** 1,494 protocol elements share
   only 1,352 distinct `protocolId` values; 123 ids are used by 2-3 different
   centers (e.g. `NU_default_expression` → CSGID and MCSG, `LP.1232` → MPP,
   NATPRO and TMPC). The `@id` attribute (`<CENTER>-<protocolId>`) is the only
   safe key.
5. **Dangling protocol references.** Of 2,927,151 `protocolRef` elements,
   **245,733 (9.2%) name a protocol that does not exist in `protocolList`**
   — not a truncation problem: a unique within-center prefix match recovers
   only 9 of them. They are concentrated almost entirely in CSGID, whose most
   common dangling key,
   `CSG-004_Transformation, Frozen Culture and Overexpression of Recombinant Protein`,
   accounts for ~19,700 references in a 25,000-target sample and is itself an
   *expression* protocol. Those trials' hosts are permanently unrecoverable.
6. **Placeholder references.** 42,859 `protocolRef` elements carry
   `protocolType = other` and an empty `protocolId` — they point at nothing.
7. **Free-text key:value is inconsistently spelled.** Host: `Escherichia coli`,
   `Escherichia Coli`, `E. coli`, `e.coli`. Strain: `BL21magic` / `BL21Magic`,
   `BL21` / `BL-21` / `BL21 DE3`, `ROSETTA` / `Rosetta` / `rosetta`,
   `BL21/PRK1037` / `BL21/pRK1037`. Normalisation is required before counting.
8. **Wrong values in the `strain:` field.** `pRK1037` (901), `PRK1037` (745),
   `prk1037` (124) and `MH4a` (119) are plasmids/vectors entered as strains.
9. **Schema elements that are declared but unused.** `trialOutcome`,
   `trialOutcomeList` and `outcomeDetails` never occur in the data;
   `sequenceModifications` and `ligandName` occur only tens of times. The
   schema is considerably richer than the deposited data.
10. **Center-skewed conventions.** Everything above varies by center: the
   `host:`/`strain:`/`vector:` convention is essentially an MCSG/CSGID habit,
   while most centers record nothing structured at all. Any coverage figure is
   really a statement about which handful of centers were tidy.

---

## 9. What this means for the project

- **Do not rebuild the paired dataset on TargetTrack.** It is an *E. coli*
  monoculture with the host left implicit. The multi-host question this project
  asks was not recorded, which answers the "did nobody ask, or is it not there?"
  question: **it is not there.** Prior groups mined TargetDB/PepcDB for *E. coli*
  solubility precisely because that is all the data supports.
- **Keep the curated literature corpus as the primary source.** ~1,400
  hand-curated paired observations from seven multi-host comparison studies is
  thin, but it is real pairing; TargetTrack offers vastly more rows and almost
  no contrast.
- **Do harvest the 989 verified multi-host targets as a second corpus.** This
  is the one genuinely new thing here: ~1,000 proteins with per-trial outcomes
  in 2-3 hosts (*E. coli* vs insect vs mammalian vs cell-free), with sequences,
  openly licensed. It roughly doubles the paired data. Two conditions: every
  host label must be human-checked before use (42.7% of naive multi-host hits
  were false, 744 of them from one protocol's preamble), and the subset is
  membrane-protein-heavy and centre-skewed, so it should be modelled as its own
  stratum rather than pooled naively with the literature corpus.
- **There is a second, larger but weaker use.** If the project ever wants a large
  *E. coli*-only auxiliary signal — for pre-training a sequence encoder, for
  calibrating an *E. coli* baseline, or for benchmarking against SoluProt/EPSOL —
  TargetTrack provides ~963k trials with sequences and enumerated
  success/failure labels under a permissive licence. That is a pre-training
  corpus, not a host-recommendation dataset, and it should not be described as
  one.


## Provenance

| | |
|---|---|
| Source | PSI TargetTrack, final data files (timestamp 30 Jun 2017) |
| DOI | [10.5281/zenodo.821654](https://doi.org/10.5281/zenodo.821654) |
| File | `TargetTrack-1Jul2017.tar.gz` |
| Size | 832,912,731 bytes |
| MD5 | `200012a8a2a11ffd7e370ed142df36c3` (verified after download) |
| Licence | CC-BY-SA 4.0 |
| Schema | `targetTrack-v1.4.1.xsd` / `.pdf`, `targetTrackEnumeratedDataItems-v1.4.1.xls` |
| Main data | `TargetTrack XML files/tt.xml.gz` (238,560,402 bytes compressed) |
| Reproduce | `python -I scripts/targettrack.py fetch|extract|schema|protocols|inventory` |

The archive is kept outside the repository and is excluded by `.gitignore`.

## Reproducing these numbers

```sh
python -I scripts/targettrack.py fetch   --dest <outside-repo>/download
python -I scripts/targettrack.py extract --tarball <...>/TargetTrack-1Jul2017.tar.gz \
                                         --dest <outside-repo>/extract      # new empty dir
XML="<...>/TargetTrack-1Jul2017/TargetTrack XML files/tt.xml.gz"
python -I scripts/targettrack.py schema    --xml "$XML" --limit 5000 > schema.txt
python -I scripts/targettrack.py protocols --xml "$XML"                > protocols.tsv
python -I scripts/targettrack.py inventory --xml "$XML" --out-dir <outside-repo>/out
python -I scripts/targettrack.py pairs     --xml "$XML" --out-dir <outside-repo>/out
```

`inventory` streams the whole 238 MB gzip with `iterparse` (constant ~40 MB RSS,
~17 min) and writes `inventory.json` plus `multihost_targets.csv`. The archive
is third-party data: it is extracted into its own directory, never run from, and
`python -I` keeps the interpreter from importing anything out of it.

`pairs` is the §4 verification: it re-walks each multi-host target, asks whether
its hosts come from distinct trials or from one trial's text, writes
`verified_pairs.csv` (the genuine paired observations, one row per target with
its per-trial `host=status` list) and `pairs.json`, and attributes each artefact
to the protocol that caused it.
