# Simulation layer

`chassis-sim.html` is an interactive simulation of the UCP-1 chassis definition.

It runs the same resolver logic as `scripts/chassis_resolve.py`, reimplemented in
JavaScript so it executes in the browser with no backend. The two were checked
against each other: for human preproinsulin both report 16 capabilities active,
14 native, 2 engineered; for human erythropoietin both report 19 active, 15
native, 4 engineered, with N-glycosylation sequons at residues 24, 38 and 83.

What it shows:

- a yeast cell cross-section with the product traced nucleus to medium, and
  marks appearing in the compartment where each step happens
- the 22 protein capabilities, coloured native / engineered / unknown / not
  needed
- a card per engineered module, each stating that its proteome cost is not
  measured
- the proteome budget as a **sweep across an assumed cost**, not a prediction,
  because no module's cost has been measured
- a panel listing what the simulation cannot tell you

Four reference sequences are built in (preproinsulin, erythropoietin, growth
hormone, hen egg lysozyme) and any sequence can be pasted. The disulfide counts
it derives for all four match the published biology: 3, 2, 2 and 4 pairs.

Not verified: the signal-peptide and transmembrane calls are hydropathy
heuristics rather than trained predictors, and are labelled as such in the
interface. No titre is predicted. The chassis described does not exist.
