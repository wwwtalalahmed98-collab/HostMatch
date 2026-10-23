"""Filter the 37-capability set down to what PROTEIN production actually needs.

The capability set was built for 'any product in biotechnology' - proteins,
small molecules and materials. The project scope is now proteins only.

Input: protocol/capabilities-v1.tsv (the product_classes_needing_it column)
Nothing here is assumed; the filter is the column as written.

Run:  python -I scripts/protein_scope.py
"""
import csv, sys, collections
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

rows = list(csv.DictReader(open('protocol/capabilities-v1.tsv', encoding='utf-8'), delimiter='\t'))

def needed_for_protein(classes):
    c = classes.strip()
    return (c == 'all') or ('proteins' in c)

keep = [r for r in rows if needed_for_protein(r['product_classes_needing_it'])]
drop = [r for r in rows if not needed_for_protein(r['product_classes_needing_it'])]

print(f"TOTAL capabilities in set            : {len(rows)}")
print(f"REQUIRED for protein production      : {len(keep)}")
print(f"DROPPED (small-molecule / materials) : {len(drop)}")
print()

print("DROPPED - not needed if the product is a protein")
print("-"*70)
for r in drop:
    print(f"  {r['id']:<3} {r['capability'][:52]:<54} [{r['product_classes_needing_it']}]")
print()

bycat = collections.Counter(r['category'] for r in keep)
print("KEPT, by category")
print("-"*70)
for cat, n in bycat.most_common():
    print(f"  {cat:<14} {n}")
print()

# Which of the kept ones does S. cerevisiae already have natively, and which
# must be engineered in? This mapping is a JUDGEMENT from the literature
# gathered in protocol/candidate-assessment-v1.md, not a measurement.
NATIVE = {
 'A1':'native (yeast codon tables well characterised)',
 'A2':'native (large characterised promoter sets)',
 'A3':'native (Kozak context understood)',
 'B1':'native (ER chaperone machinery; overexpression studied)',
 'B2':'native (ER disulfide machinery - PDI/Ero1)',
 'B3':'native (N-glycosylation present)',
 'B5':'native (O-mannosylation present)',
 'B6':'partly native (many PTMs present; some absent)',
 'B7':'native but needs tuning (protease deletions routine)',
 'D4':'native',
 'F3':'native (stress responses characterised)',
 'F4':'native',
 'G1':'native','G3':'native','G4':'native',
 'G5':'native (industrial scale demonstrated)',
 'G6':'native (GRAS)',
}
ENGINEER = {
 'A4':'ENGINEER - large-CDS assembly and stability',
 'B4':'ENGINEER - humanised N-glycan pathway (glycoengineering)',
 'D5':'ENGINEER - sugar-nucleotide supply for human glycans',
 'E3':'ENGINEER - secretion capacity beyond native',
 'G2':'ENGINEER - burden control (this is the switchable layer)',
}

print("KEPT capabilities: native in S. cerevisiae vs must be added")
print("-"*70)
n_native = n_eng = n_unk = 0
for r in keep:
    i = r['id']
    if i in NATIVE:
        print(f"  {i:<3} {r['capability'][:40]:<42} native       {NATIVE[i]}")
        n_native += 1
    elif i in ENGINEER:
        print(f"  {i:<3} {r['capability'][:40]:<42} ENGINEER     {ENGINEER[i]}")
        n_eng += 1
    else:
        print(f"  {i:<3} {r['capability'][:40]:<42} UNCLASSIFIED")
        n_unk += 1
print("-"*70)
print(f"  native in yeast      : {n_native}")
print(f"  must be engineered   : {n_eng}")
print(f"  unclassified         : {n_unk}")
print()

print("CONSEQUENCE FOR THE PROTEOME BUDGET")
print("="*70)
BUDGET_YEAST = 0.40
for cost in (0.01, 0.02, 0.03, 0.05, 0.10):
    print(f"  {n_eng} engineered capabilities at {cost:.0%} each = {n_eng*cost:.0%} of proteome"
          f"   {'fits 40%' if n_eng*cost <= BUDGET_YEAST else 'EXCEEDS 40%'}")
print()
print(f"  Break-even if all {n_eng} are constitutive: {BUDGET_YEAST/n_eng:.1%} each")
print(f"  (compare: {BUDGET_YEAST/37:.2%} each when the target was all 37)")
