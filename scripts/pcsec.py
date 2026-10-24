"""Load and solve the pcSecYeast proteome-constrained secretory model in Python.

WHY THIS EXISTS
---------------
Both pcSecYeast repositories say they require MATLAB, the COBRA Toolbox, the
RAVEN Toolbox and the SoPlex solver. That was recorded in this project as the
central obstacle, because the secretory model is the only available source of
the proteome costs that chassis-v1.json records as "not measured".

MATLAB is needed to BUILD the model. It is not needed to USE it. The built
models are committed to the pcSecYeastSpecies repository as .mat files under an
MIT licence, and a .mat file is just a container: scipy reads it, and the
linear program inside is solved by HiGHS, which ships with scipy.

WHAT THIS DOES AND DOES NOT DO
------------------------------
Does: download the model, load it, solve flux balance analysis, search
reactions and metabolites by name, and report the secretory machinery present.

Does NOT: reproduce the authors' published simulations. Those set
species-specific media, heterologous protein constraints and enzyme bounds
through their own MATLAB scripts. Reimplementing that logic is the next piece
of work and has not been done. Solving the model as shipped is not the same as
using it the way the paper does.

Models available in the same directory of that repository:
    pcSecYeast.mat    S. cerevisiae
    pcSecPichia.mat   K. phaffii
    pcSecKmarx.mat    K. marxianus
    plus _NG variants

Run:  python -I scripts/pcsec.py
      python -I scripts/pcsec.py --find glycosyl
      python -I scripts/pcsec.py --model pcSecPichia
"""
import argparse
import os
import sys
import time
import urllib.request

import numpy as np
import scipy.io
import scipy.sparse as sp
from scipy.optimize import linprog

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODELDIR = os.path.join(ROOT, "data", "models")
BASE = "https://raw.githubusercontent.com/LiLabTsinghua/pcSecYeastSpecies/main/Model/"


def get_model(name):
    path = os.path.join(MODELDIR, name + ".mat")
    if not os.path.exists(path):
        os.makedirs(MODELDIR, exist_ok=True)
        print("downloading %s.mat ..." % name)
        urllib.request.urlretrieve(BASE + name + ".mat", path)
    size = os.path.getsize(path) / 1e6
    print("model file: %s  (%.1f MB)" % (path, size))
    return scipy.io.loadmat(path, struct_as_record=False, squeeze_me=True)["model"]


def arr(m, f):
    return np.asarray(getattr(m, f), dtype=object)


def solve(m, verbose=True):
    S = sp.csr_matrix(m.S)
    lb = np.asarray(m.lb, float)
    ub = np.asarray(m.ub, float)
    c = np.asarray(m.c, float)
    b = np.asarray(m.b, float)
    t0 = time.time()
    res = linprog(c=-c, A_eq=S, b_eq=b, bounds=np.column_stack([lb, ub]), method="highs")
    dt = time.time() - t0
    if verbose:
        print("  solver      : HiGHS, bundled with scipy. No MATLAB, no SoPlex.")
        print("  status      : %s" % res.message.split(".")[0])
        print("  solve time  : %.1f s" % dt)
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default="pcSecYeast")
    ap.add_argument("--find", help="substring to search in reaction names")
    ap.add_argument("--limit", type=int, default=15)
    args = ap.parse_args()

    m = get_model(args.model)
    rxns, mets = arr(m, "rxns"), arr(m, "mets")
    rxnNames = arr(m, "rxnNames") if hasattr(m, "rxnNames") else rxns
    S = sp.csr_matrix(m.S)

    print("\nMODEL: %s" % args.model)
    print("-" * 70)
    print("  metabolites : %6d" % len(mets))
    print("  reactions   : %6d" % len(rxns))
    print("  genes       : %6d" % len(arr(m, "genes")))
    print("  S nonzeros  : %6d  (%.3f%% dense)" % (S.nnz, 100 * S.nnz / (S.shape[0] * S.shape[1])))

    if args.find:
        q = args.find.lower()
        hits = [(str(rxns[i]), str(rxnNames[i]))
                for i in range(len(rxns))
                if q in str(rxns[i]).lower() or q in str(rxnNames[i]).lower()]
        print("\nREACTIONS MATCHING %r : %d" % (args.find, len(hits)))
        print("-" * 70)
        for rid, nm in hits[:args.limit]:
            print("  %-22s %s" % (rid[:22], nm[:46]))
        if len(hits) > args.limit:
            print("  ... and %d more" % (len(hits) - args.limit))
        return

    # What secretory machinery is represented?
    print("\nSECRETORY AND MATURATION MACHINERY IN THE MODEL")
    print("-" * 70)
    probes = ["glycosyl", "fold", "disulf", "transloc", "secre", "golgi",
              "dolichol", "mannos", "protein", "ribosome", "degrad"]
    low = [str(r).lower() + " " + str(n).lower() for r, n in zip(rxns, rxnNames)]
    for p in probes:
        n = sum(1 for s in low if p in s)
        print("  %-12s %5d reactions" % (p, n))

    print("\nFLUX BALANCE ANALYSIS")
    print("-" * 70)
    c = np.asarray(m.c, float)
    oi = np.flatnonzero(c)
    print("  objective   : %s  (sense: %s)" % (", ".join(str(rxns[i]) for i in oi),
                                               getattr(m, "osenseStr", "?")))
    res = solve(m)
    if res.status == 0:
        v = res.x
        print("  objective   : %.6f" % float(-res.fun))
        print("  active flux : %d of %d reactions" % (int(np.sum(np.abs(v) > 1e-9)), len(v)))
    else:
        print("  !! did not solve")

    print("\nWHAT THIS ESTABLISHES")
    print("=" * 70)
    print("  The model loads and solves in Python. MATLAB is required to BUILD")
    print("  these models, not to USE them. The MATLAB blocker recorded in")
    print("  protocol/theory-stack-v1.md does not apply to consuming the model.")
    print()
    print("WHAT IT DOES NOT ESTABLISH")
    print("=" * 70)
    print("  - This solves the model AS SHIPPED. The authors' published results")
    print("    set media, heterologous protein and enzyme constraints through")
    print("    their MATLAB scripts. That logic is NOT reimplemented here.")
    print("  - No proteome cost for any chassis module has been extracted yet.")
    print("  - The objective value above has not been checked against any")
    print("    published number, so it is a solve, not a validation.")


if __name__ == "__main__":
    main()
