"""Turn results.json from sieve_sim.py into the three report figures.

Usage:  python make_figures.py            (reads results.json next to this file)
Output: figures/fig_miss_ratio_vs_size.png
        figures/fig_miss_ratio_vs_skew.png
        figures/fig_reduction_vs_fifo.png
        figures/summary.txt   (numbers quoted in the report)
"""
import json
import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "figures")
os.makedirs(OUT, exist_ok=True)
r = json.load(open(os.path.join(HERE, "results.json")))

SIZES = ["0.1%", "0.5%", "1%", "5%", "10%"]
ALPHAS = [0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.4]
STYLE = {
    "FIFO": dict(color="#A6A6A6", marker="o"),
    "LRU": dict(color="#595959", marker="s"),
    "CLOCK": dict(color="#1A1A1A", marker="D", linestyle="--"),
    "SIEVE": dict(color="#C00000", marker="o", linewidth=2.6),
}
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 11, "axes.spines.top": False,
                     "axes.spines.right": False, "axes.grid": True, "grid.alpha": 0.3})

# Figure 1: miss ratio vs cache size, alpha 1.0 (pairs with paper Figure 8a)
fig, ax = plt.subplots(figsize=(6.2, 4.2), dpi=200)
for alg in ["FIFO", "LRU", "CLOCK", "SIEVE"]:
    ys = [r[f"a1.0|{s}|{alg}"] for s in SIZES]
    ax.plot(SIZES, ys, label=alg, **STYLE[alg])
ax.set_xlabel("Cache size (% of unique objects)")
ax.set_ylabel("Miss ratio")
ax.set_ylim(0, 0.9)
ax.set_title("Zipf alpha = 1.0, 100,000 objects, 1,000,000 requests", fontsize=10)
ax.legend(frameon=False)
fig.tight_layout()
fig.savefig(os.path.join(OUT, "fig_miss_ratio_vs_size.png"))

# Figure 2: miss ratio vs skew at 1% cache (pairs with paper Figure 9a)
fig, ax = plt.subplots(figsize=(6.2, 4.2), dpi=200)
for alg in ["FIFO", "LRU", "SIEVE"]:
    ys = [r[f"a{a}|1%|{alg}"] for a in ALPHAS]
    ax.plot(ALPHAS, ys, label=alg, **STYLE[alg])
ax.plot(ALPHAS, [r[f"a{a}|1%|BEST"] for a in ALPHAS], color="#1A1A1A", linestyle="--",
        linewidth=1.4, label="Best possible")
ax.set_xlabel("Zipf alpha (higher means more skew)")
ax.set_ylabel("Miss ratio")
ax.set_ylim(0, 1.0)
ax.set_title("Cache size 1% of unique objects", fontsize=10)
ax.legend(frameon=False)
fig.tight_layout()
fig.savefig(os.path.join(OUT, "fig_miss_ratio_vs_skew.png"))

# Figure 3: percent fewer misses than FIFO (pairs with paper Figure 11)
fig, ax = plt.subplots(figsize=(6.2, 4.2), dpi=200)
width = 0.26
xs = range(len(SIZES))
summary = ["SIEVE miss reduction relative to FIFO (percent)", "alpha  " + "  ".join(f"{s:>6}" for s in SIZES)]
for i, (a, col) in enumerate([(0.8, "#BFBFBF"), (1.0, "#7F7F7F"), (1.2, "#262626")]):
    red = [(r[f"a{a}|{s}|FIFO"] - r[f"a{a}|{s}|SIEVE"]) / r[f"a{a}|{s}|FIFO"] * 100 for s in SIZES]
    bars = ax.bar([x + (i - 1) * width for x in xs], red, width, color=col, label=f"alpha {a}")
    for b, v in zip(bars, red):
        ax.text(b.get_x() + b.get_width() / 2, v + 0.6, f"{v:.0f}", ha="center", fontsize=8)
    summary.append(f"{a:<6} " + "  ".join(f"{v:6.1f}" for v in red))
ax.set_xticks(list(xs))
ax.set_xticklabels(SIZES)
ax.set_xlabel("Cache size (% of unique objects)")
ax.set_ylabel("Fewer misses than FIFO (%)")
ax.set_ylim(0, 44)
ax.legend(frameon=False, loc="upper center", ncol=3)
fig.tight_layout()
fig.savefig(os.path.join(OUT, "fig_reduction_vs_fifo.png"))

# Numbers for the report text
summary.append("")
summary.append("Miss ratio at alpha 1.0 by cache size")
summary.append("alg    " + "  ".join(f"{s:>6}" for s in SIZES))
for alg in ["FIFO", "LRU", "CLOCK", "SIEVE"]:
    summary.append(f"{alg:<6} " + "  ".join(f"{r[f'a1.0|{s}|{alg}']:6.3f}" for s in SIZES))
summary.append("")
summary.append("Paper Figure 11 miss ratios (LRU, FIFO, SIEVE) for comparison")
summary.append("large cache 10%:  a0.8 0.51 0.55 0.43 | a1.0 0.22 0.25 0.18 | a1.2 0.05 0.06 0.04")
summary.append("small cache 0.1%: a0.8 0.90 0.91 0.80 | a1.0 0.60 0.63 0.49 | a1.2 0.25 0.28 0.19")
summary.append("Paper reduction vs FIFO: small 12.1, 22.2, 32.1 | large 21.8, 28.0, 33.3")
open(os.path.join(OUT, "summary.txt"), "w").write("\n".join(summary) + "\n")
print("\n".join(summary))
print("\nfigures written to", OUT)
