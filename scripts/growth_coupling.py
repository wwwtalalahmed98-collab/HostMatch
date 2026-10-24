"""Growth-law coupling: what the proteome budget looks like with physics in it.

The current budget model (scripts/proteome_budget.py) asks one question:
does the sum of module costs fit under the measured ceiling? It treats the
cell as a box with a fixed volume.

That is wrong in a specific, consequential way. The ceiling is not a wall you
can walk up to. Expressing heterologous protein SLOWS GROWTH, and the product
you collect depends on both how much each cell makes and how many cells there
are. At the ceiling, growth is zero and so is yield.

This implements the bacterial growth laws (Scott & Hwa and successors) to
compute that trade-off instead of ignoring it.

THE THEORY
----------
The proteome splits into sectors whose mass fractions vary linearly with
growth rate (Hui et al., Mol Syst Biol 2015, "Quantitative proteomic analysis
reveals a simple strategy of global resource allocation in bacteria"):

    phi_R  ribosomal sector, grows with growth rate
    phi_P  metabolic sector
    phi_Q  growth-rate-independent housekeeping, roughly fixed

Heterologous protein is carved out of the adjustable part. To first order the
growth rate falls linearly with the heterologous mass fraction:

    lambda(phi_H) / lambda_0  =  1 - phi_H / phi_max

where phi_max is the heterologous mass fraction at which growth stops. That is
the quantity our literature search already measured: 33% in E. coli, >40% in
yeast.

Volumetric productivity is the product of how much each cell makes and how
fast cells accumulate:

    productivity  proportional to  phi_H * lambda(phi_H)

Maximising that over phi_H gives  phi_H* = phi_max / 2.

WHAT THIS CHANGES
-----------------
The existing budget model says "anything under the ceiling fits". The
growth-coupled model says the best operating point is HALF the ceiling, and
that running at the ceiling produces nothing at all.

PARAMETERS AND THEIR STATUS
---------------------------
phi_max is measured and cited in protocol/proteome-budget-v1.md.
The LINEAR form of the growth reduction is the first-order result from the
growth-law literature; it is well supported in E. coli and much less tested in
yeast. Yeast-specific growth-law parameters are a gap in this project.

Run:  python -I scripts/growth_coupling.py
"""
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# Heterologous mass fraction at which growth stops. Measured values, cited in
# protocol/proteome-budget-v1.md.
PHI_MAX = {"E. coli": 0.33, "S. cerevisiae": 0.40}

# What a single engineered module might cost, as a fraction of total protein.
# NOT measured for any module in chassis-v1.json. Swept, as before.
MODULE_COST_SWEEP = [0.01, 0.02, 0.03, 0.05, 0.08]

# Modules the resolver switches on for the two worked examples.
EXAMPLES = [("Human preproinsulin", 2), ("Human erythropoietin", 4)]


def growth_fraction(phi_H, phi_max):
    """Growth rate relative to an unburdened cell. Zero at the ceiling."""
    return max(0.0, 1.0 - phi_H / phi_max)


def productivity(phi_H, phi_max):
    """Product per unit volume per unit time, in arbitrary units.

    Proportional to (protein per cell) * (rate of cell accumulation).
    """
    return phi_H * growth_fraction(phi_H, phi_max)


def line(c="-", n=72):
    print(c * n)


print("GROWTH-COUPLED PROTEOME BUDGET")
line("=")
print("  The old model: does the total fit under the ceiling?")
print("  This model:    what does the total do to growth, and to yield?")
print()

for host, phi_max in PHI_MAX.items():
    best = phi_max / 2
    print("%s  (growth stops at phi_max = %.0f%% heterologous protein)" % (host, 100 * phi_max))
    line()
    print("%12s %12s %14s %14s" % ("burden", "growth", "productivity", "vs optimum"))
    line()
    pts = [0.02, 0.05, 0.10, best, 0.25, 0.30, phi_max]
    pmax = productivity(best, phi_max)
    for phi in sorted(set(round(p, 4) for p in pts)):
        g = growth_fraction(phi, phi_max)
        p = productivity(phi, phi_max)
        mark = "  <- optimum" if abs(phi - best) < 1e-9 else ""
        rel = (p / pmax * 100) if pmax else 0
        print("%11.1f%% %11.0f%% %14.4f %13.0f%%%s" % (100 * phi, 100 * g, p, rel, mark))
    line()
    print("  Optimal burden      : %.1f%% of total protein" % (100 * best))
    print("  At the ceiling      : growth 0%, productivity 0. The ceiling is not")
    print("                        a budget you may spend up to.")
    print()

print("WHAT THIS MEANS FOR THE CHASSIS AS IT IS DEFINED")
line("=")
phi_max = PHI_MAX["S. cerevisiae"]
best = phi_max / 2
print("Yeast optimum is %.0f%% of total protein across ALL engineered modules.\n" % (100 * best))
print("%-26s %8s %10s %10s %12s" % ("product", "modules", "cost each", "total", "verdict"))
line()
for name, n_mod in EXAMPLES:
    for cost in MODULE_COST_SWEEP:
        total = n_mod * cost
        g = growth_fraction(total, phi_max)
        if total > phi_max:
            verdict = "NO GROWTH"
        elif total > best * 1.5:
            verdict = "past optimum"
        elif total < best * 0.5:
            verdict = "under-using"
        else:
            verdict = "near optimum"
        print("%-26s %8d %9.0f%% %9.1f%% %12s   growth %.0f%%"
              % (name if cost == MODULE_COST_SWEEP[0] else "", n_mod,
                 100 * cost, 100 * total, verdict, 100 * g))
    print()

line("=")
print("THE CORRECTION THIS MAKES")
line("=")
print("  proteome_budget.py and the simulator both treat %.0f%% as a budget" % (100 * phi_max))
print("  that may be spent up to. Under the growth laws that is the point of")
print("  ZERO yield. The useful operating point is %.0f%%, and the penalty for" % (100 * best))
print("  overshooting is steeper than the penalty for undershooting, because")
print("  growth falls while the per-cell gain is already saturating.")
print()
print("WHAT IS NOT DONE")
line("=")
print("  - The linear growth reduction is a FIRST-ORDER result, strongly")
print("    supported in E. coli and much less tested in yeast.")
print("  - No module in chassis-v1.json has a measured cost, so the module")
print("    column above is still a sweep, not a prediction.")
print("  - This ignores WHICH protein is expressed. Two modules of equal mass")
print("    can differ in burden if one competes for a scarcer resource.")
print("  - Real productivity also depends on fermentation mode and duration;")
print("    this is steady-state exponential growth only.")
print("  - Yeast-specific growth-law parameters have not been collected.")
