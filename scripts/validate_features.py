"""Validate the chassis resolver's sequence features against UniProt annotations.

The resolver decides which capabilities a protein needs by reading features off
its sequence. Those features are checkable: UniProt carries curated,
largely experimentally determined annotations for the same things.

This measures four of them:

  N-glycosylation  our N-X-S/T sequon scan        vs UniProt observed N-linked sites
  disulfide bonds  our cysteine_count // 2        vs UniProt annotated bonds
  signal peptide   our hydropathy window heuristic vs UniProt Signal feature
  transmembrane    our hydropathy window heuristic vs UniProt Transmembrane features

It imports the real resolver rather than reimplementing it, so what is tested
is the code that ships.

What this does NOT validate: whether the capability-to-module mapping is right,
or whether any protein would actually express. Those need expression data this
project does not have.

Run:  python -I scripts/validate_features.py
      python -I scripts/validate_features.py --refetch
"""
import argparse
import json
import os
import sys
import urllib.request

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
CACHE = os.path.join(ROOT, "data", "uniprot")
OUT = os.path.join(ROOT, "reports", "02-feature-validation.tsv")

sys.path.insert(0, HERE)
from chassis_resolve import features as our_features  # the real resolver

FIELDS = "accession,protein_name,sequence,ft_signal,ft_disulfid,ft_carbohyd,ft_transmem"

# Chosen for annotation quality and spread, not for making the tool look good.
# secreted  - the resolver's intended domain
# cytosolic - negative control for the signal-peptide heuristic
# membrane  - out of the resolver's scope, included to test the TM heuristic
PANEL = [
    ("P01588", "Erythropoietin", "secreted"),
    ("P01308", "Insulin", "secreted"),
    ("P01241", "Somatotropin", "secreted"),
    ("P02768", "Serum albumin", "secreted"),
    ("P02787", "Serotransferrin", "secreted"),
    ("P01009", "Alpha-1-antitrypsin", "secreted"),
    ("P00750", "Tissue plasminogen activator", "secreted"),
    ("P00734", "Prothrombin", "secreted"),
    ("P01024", "Complement C3", "secreted"),
    ("P04275", "von Willebrand factor", "secreted"),
    ("P00738", "Haptoglobin", "secreted"),
    ("P05019", "IGF-1", "secreted"),
    ("P01344", "IGF-2", "secreted"),
    ("P61626", "Lysozyme C, human", "secreted"),
    ("P00698", "Lysozyme C, chicken", "secreted"),
    ("P01857", "Ig gamma-1 chain C region", "secreted"),
    ("P68871", "Hemoglobin beta", "cytosolic"),
    ("P69905", "Hemoglobin alpha", "cytosolic"),
    ("P04406", "GAPDH", "cytosolic"),
    ("P60709", "Beta-actin", "cytosolic"),
    ("P00558", "Phosphoglycerate kinase 1", "cytosolic"),
    ("P07550", "Beta-2 adrenergic receptor", "membrane"),
    ("P11166", "Glucose transporter 1", "membrane"),
    ("P08183", "Multidrug resistance protein 1", "membrane"),
]


def fetch(acc, refetch=False):
    path = os.path.join(CACHE, acc + ".json")
    if os.path.exists(path) and not refetch:
        with open(path, encoding="utf-8") as fh:
            return json.load(fh)
    url = "https://rest.uniprot.org/uniprotkb/%s.json?fields=%s" % (acc, FIELDS)
    with urllib.request.urlopen(url, timeout=30) as r:
        raw = r.read().decode("utf-8")
    os.makedirs(CACHE, exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(raw)
    return json.loads(raw)


def curated(d):
    """Pull the annotated truth out of a UniProt record."""
    seq = d["sequence"]["value"]
    sig = False
    nglyc, oglyc, ss, tm, glycation, variant_only = set(), 0, 0, 0, 0, 0
    for f in d.get("features", []):
        t, loc = f["type"], f["location"]
        desc = (f.get("description") or "").lower()
        if t == "Signal":
            sig = True
        elif t == "Disulfide bond":
            ss += 1
        elif t == "Transmembrane":
            tm += 1
        elif t == "Glycosylation":
            pos = loc["start"]["value"]
            if desc.startswith("n-linked"):
                # UniProt also annotates GLYCATION - glucose stuck non-enzymatically
                # onto a lysine - as "N-linked (Glc) ... lysine". That is not
                # N-glycosylation and the resolver is not trying to find it.
                # Real N-glycosylation is on asparagine, so require that residue.
                if "in variant" in desc:
                    # Glycosylation that exists only in a sequence variant, e.g.
                    # albumin Casebrook, where the reference residue is not even
                    # an asparagine. Not a property of the sequence being tested.
                    variant_only += 1
                elif 1 <= pos <= len(seq) and seq[pos - 1] == "N":
                    nglyc.add(pos)
                else:
                    glycation += 1
            elif desc.startswith("o-linked"):
                oglyc += 1
    return {"seq": seq, "signal": sig, "nglyc": nglyc, "oglyc": oglyc, "ss": ss,
            "tm": tm, "glycation": glycation, "variant_only": variant_only}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--refetch", action="store_true")
    args = ap.parse_args()

    rows, tp = [], 0
    sig_misses, tm_misses = [], []
    glyc_total = 0
    variant_total = 0
    fp = fn = 0
    sig_ok = sig_n = tm_ok = tm_n = 0
    ss_exact = ss_n = ss_bound_ok = 0
    bound_violations = []
    oglyc_missed = 0

    print("Fetching %d UniProt records%s\n" % (len(PANEL), " (forced refetch)" if args.refetch else " (cached where present)"))

    for acc, name, cat in PANEL:
        try:
            d = fetch(acc, args.refetch)
        except Exception as e:
            print("  !! %s %s: %s" % (acc, name, e))
            continue
        c = curated(d)
        f = our_features(c["seq"])

        ours = set(f["n_glyc_positions"])
        hit = ours & c["nglyc"]
        miss = c["nglyc"] - ours
        extra = ours - c["nglyc"]
        tp += len(hit); fn += len(miss); fp += len(extra)

        sig_n += 1
        sig_match = (f["signal_peptide_predicted"] == c["signal"])
        sig_ok += sig_match
        if not sig_match: sig_misses.append((name, cat, c["signal"], f["signal_peptide_predicted"]))

        tm_n += 1
        tm_match = (f["tm_segments_predicted"] > 0) == (c["tm"] > 0)
        tm_ok += tm_match
        if not tm_match: tm_misses.append((name, cat, c["tm"], f["tm_segments_predicted"]))

        ss_n += 1
        ss_exact += (f["cysteine_pairs"] == c["ss"])
        if f["cysteine_pairs"] >= c["ss"]:
            ss_bound_ok += 1
        else:
            bound_violations.append((name, c["ss"], f["cysteine_pairs"]))
        if c["oglyc"]: oglyc_missed += 1
        glyc_total += c["glycation"]
        variant_total += c["variant_only"]

        rows.append([acc, name, cat, f["length_aa"],
                     len(c["nglyc"]), f["n_glyc_sequons"], len(hit), len(miss), len(extra),
                     c["ss"], f["cysteine_pairs"],
                     int(c["signal"]), int(f["signal_peptide_predicted"]), int(sig_match),
                     c["tm"], f["tm_segments_predicted"], int(tm_match), c["oglyc"]])

        flag = "" if (sig_match and tm_match) else "   <-- heuristic miss"
        print("  %-7s %-32s %-9s %4daa  Nglyc %d/%d found, %d extra | SS %d vs %d | sig %s%s"
              % (acc, name[:32], cat, f["length_aa"], len(hit), len(c["nglyc"]), len(extra),
                 c["ss"], f["cysteine_pairs"],
                 ("ok" if sig_match else "MISS"), flag))

    hdr = ["accession","name","category","length","uniprot_nglyc","our_sequons","nglyc_found",
           "nglyc_missed","sequons_not_glycosylated","uniprot_ss_bonds","our_ss_pairs",
           "uniprot_signal","our_signal","signal_match","uniprot_tm","our_tm","tm_match","uniprot_oglyc"]
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8", newline="") as fh:
        fh.write("\t".join(hdr) + "\n")
        for r in rows:
            fh.write("\t".join(str(x) for x in r) + "\n")

    n = len(rows)
    bar = "=" * 74
    print("\n" + bar)
    print("RESULTS over %d proteins" % n)
    print(bar)

    rec = tp / (tp + fn) if tp + fn else 0
    prec = tp / (tp + fp) if tp + fp else 0
    print("\nN-GLYCOSYLATION  (our N-X-S/T scan vs UniProt observed sites)")
    print("-" * 74)
    print("  annotated sites found      : %d of %d   recall %.0f%%" % (tp, tp + fn, 100 * rec))
    print("  sequons that are NOT glycosylated : %d   precision %.0f%%" % (fp, 100 * prec))
    print("  -> the scan finds POTENTIAL sites. Not every sequon is used.")

    print("\nDISULFIDE BONDS  (our cysteine_count // 2 vs UniProt annotated bonds)")
    print("-" * 74)
    print("  exactly right              : %d of %d   %.0f%%" % (ss_exact, ss_n, 100 * ss_exact / ss_n))
    print("  a VALID upper bound        : %d of %d   %.0f%%" % (ss_bound_ok, ss_n, 100 * ss_bound_ok / ss_n))
    if bound_violations:
        print("  upper bound BROKEN for %d - our count is lower than the annotated bonds:" % len(bound_violations))
        for nm, real, ours in bound_violations:
            print("     %-32s annotated %d, we say %d" % (nm[:32], real, ours))
        print("  cause: inter-chain disulfides pair a cysteine with ANOTHER molecule,")
        print("  so counting this chain's cysteines and halving undercounts them.")

    print("\nSIGNAL PEPTIDE  (hydropathy heuristic vs UniProt Signal feature)")
    print("-" * 74)
    print("  correct                    : %d of %d   %.0f%%" % (sig_ok, sig_n, 100 * sig_ok / sig_n))
    for nm, cat, real, ours in sig_misses:
        print("     MISS %-30s (%s) UniProt %s, we said %s" % (nm[:30], cat, "yes" if real else "no", "yes" if ours else "no"))

    print("\nTRANSMEMBRANE  (hydropathy heuristic, has-TM vs has-no-TM)")
    print("-" * 74)
    print("  correct                    : %d of %d   %.0f%%" % (tm_ok, tm_n, 100 * tm_ok / tm_n))
    for nm, cat, real, ours in tm_misses:
        print("     MISS %-30s (%s) UniProt %d TM, we said %d" % (nm[:30], cat, real, ours))

    print("\nO-GLYCOSYLATION")
    print("-" * 74)
    print("  proteins UniProt says are O-glycosylated : %d of %d" % (oglyc_missed, n))
    print("  the resolver reports every one of them as 'unknown'.")
    print("\nGLYCATION (excluded, not a target of the resolver)")
    print("-" * 74)
    print("  non-enzymatic glucose adducts on lysine, annotated by UniProt as")
    print("  'N-linked (Glc)': %d sites across the panel. Counting these as" % glyc_total)
    print("  N-glycosylation was a bug in an earlier run of this script.")
    print("  variant-only glycosylation sites also excluded: %d" % variant_total)

    print("\n" + bar)
    print("NOT TESTED: whether the capability-to-module mapping is correct, or")
    print("whether any of these would express in yeast. That needs expression")
    print("data this project does not have.")
    print(bar)
    print("\nPer-protein table written to reports/02-feature-validation.tsv")


if __name__ == "__main__":
    main()
