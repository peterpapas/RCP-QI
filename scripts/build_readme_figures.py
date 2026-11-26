"""Build source-backed README charts without changing historical results."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from math import asin, pi, sin, sqrt
from pathlib import Path
from xml.etree import ElementTree
from xml.sax.saxutils import escape

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "docs" / "assets" / "figures"
SOURCES = {
    "v1": ROOT / "results" / "one_iteration.json",
    "partial": ROOT / "results" / "corrections" / "partial_search_20261127" / "thresholds.csv",
    "v3": ROOT / "results" / "phase2_partition_register.json",
}
FIGURES = (
    "interference-bias.svg",
    "partial-search-comparison.svg",
    "query-complexity-scaling.svg",
    "recursive-query-cost.svg",
)
STATIC = (
    ROOT / "docs" / "assets" / "branding" / "hero-banner.svg",
    ROOT / "docs" / "assets" / "concepts" / "recursive-quantum-partitioning.svg",
    ROOT / "docs" / "assets" / "concepts" / "research-findings.svg",
    ROOT / "docs" / "assets" / "timeline" / "research-timeline.svg",
)

BG = "#071321"
PANEL = "#0d2034"
GRID = "#26415b"
TEXT = "#edf5ff"
MUTED = "#b5c8dc"
CYAN = "#58e2df"
BLUE = "#6baaff"
VIOLET = "#c2a7ff"
AMBER = "#f6c36c"


def digest(path: Path) -> dict[str, int | str]:
    data = path.read_bytes()
    return {"bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}


def style() -> None:
    plt.rcParams.update(
        {
            "font.family": "Arial",
            "font.size": 12,
            "text.color": TEXT,
            "axes.labelcolor": TEXT,
            "axes.edgecolor": GRID,
            "axes.facecolor": PANEL,
            "axes.titlecolor": TEXT,
            "xtick.color": MUTED,
            "ytick.color": MUTED,
            "grid.color": GRID,
            "grid.alpha": 0.65,
            "figure.facecolor": BG,
            "savefig.facecolor": BG,
            "svg.fonttype": "none",
            "svg.hashsalt": "rcp-qi-readme-figures-v1",
        }
    )


def frame(title: str, subtitle: str, *, width: float = 12, height: float = 5.8) -> plt.Figure:
    fig = plt.figure(figsize=(width, height))
    fig.subplots_adjust(left=0.085, right=0.965, top=0.79, bottom=0.21, wspace=0.27)
    fig.suptitle(title, x=0.055, y=0.96, ha="left", fontsize=21, fontweight="bold", color=TEXT)
    fig.text(0.055, 0.89, subtitle, ha="left", va="top", color=MUTED, fontsize=10.5)
    return fig


def save(fig: plt.Figure, path: Path, description: str) -> None:
    fig.savefig(
        path,
        format="svg",
        metadata={"Title": path.stem.replace("-", " ").title(), "Description": description, "Date": None},
        bbox_inches="tight",
        pad_inches=0.32,
    )
    plt.close(fig)
    svg = path.read_text(encoding="utf-8").replace("\r\n", "\n")
    svg = svg.replace("</title>", f"</title>\n <desc>{escape(description)}</desc>", 1)
    path.write_bytes(svg.encode("utf-8"))


def bias_figure(path: Path) -> None:
    data = json.loads(SOURCES["v1"].read_text(encoding="utf-8"))
    observed: dict[int, list[float]] = {}
    for row in data["rows"]:
        n = int(row["N"])
        expected = 0.5 + 4 / n - 8 / n**2
        assert abs(row["analytic_probability"] - expected) < 1e-12
        assert abs(row["statevector_probability"] - expected) < 1e-11
        observed.setdefault(n, []).append(row["statevector_probability"])
    ns = np.array([2**k for k in range(2, 13)])
    probability = 0.5 + 4 / ns - 8 / ns**2
    points = sorted(observed)
    point_values = [float(np.mean(observed[n])) for n in points]
    fig = frame("The signal fades as the space grows", "V1 · one Grover iteration · unique marker · ideal statevector")
    axes = fig.subplots(1, 2, gridspec_kw={"width_ratios": [1.25, 1]})
    axes[0].plot(ns, probability, color=BLUE, linewidth=3, label="Analytical prediction")
    axes[0].scatter(points, point_values, color=CYAN, edgecolors=BG, linewidths=1.5, s=65, zorder=4, label="Archived statevectors")
    axes[0].axhline(0.5, color=AMBER, linestyle="--", linewidth=1.8, label="Random half · 50%")
    axes[0].set(xscale="log", xlabel="Search-space size N", ylabel="Correct-half probability", ylim=(0.48, 1.04))
    axes[0].set_xticks([4, 16, 64, 256, 1024, 4096], ["4", "16", "64", "256", "1,024", "4,096"])
    axes[0].legend(loc="upper right", fontsize=9, frameon=False, labelcolor=TEXT)
    axes[0].grid(axis="y")
    axes[1].plot(ns, probability - 0.5, color=VIOLET, linewidth=3)
    axes[1].scatter(points, np.array(point_values) - 0.5, color=CYAN, edgecolors=BG, s=52, zorder=4)
    axes[1].set(xscale="log", yscale="log", xlabel="Search-space size N", ylabel="Bias above 50%", ylim=(7e-4, 1))
    axes[1].set_xticks([4, 16, 64, 256, 1024, 4096], ["4", "16", "64", "256", "1,024", "4,096"])
    axes[1].grid()
    fig.text(0.055, 0.055, "Line: formula to N=4,096  ·  points: archived N=4–256  ·  no sampled shots or hardware data", color=MUTED, fontsize=10)
    save(fig, path, "Analytical correct-half probability approaches 50%; archived V1 statevector points match it through N=256.")


def partial_figure(path: Path) -> None:
    import csv

    with SOURCES["partial"].open(newline="", encoding="utf-8") as stream:
        rows = [r for r in csv.DictReader(stream) if int(r["N"]) == 256]
    rows.sort(key=lambda row: float(row["threshold"]))
    thresholds = [float(r["threshold"]) for r in rows]
    assert thresholds == [0.9, 0.95, 0.99]
    partial = [int(r["partial_calls"]) for r in rows]
    full_half = [int(r["v2_full_grover_calls"]) for r in rows]
    theta = asin(1 / sqrt(256))
    full_exact = [next(k for k in range(30) if sin((2 * k + 1) * theta) ** 2 >= p) for p in thresholds]
    assert partial == [7, 8, 9] and full_half == [9, 10, 11] and full_exact == [10, 11, 12]
    v3 = json.loads(SOURCES["v3"].read_text(encoding="utf-8"))
    bit_only = [r for r in v3["rows"] if r["variant"] == "local_partition_diffuser"]
    assert bit_only and max(abs(r["correct_half_probability_from_data"] - 0.5) for r in bit_only) < 1e-10
    fig = frame("Identifying a half takes fewer queries than an item", "N=256 · one-shot ideal equality oracle · thresholds ≥ target accuracy", height=6.2)
    ax = fig.add_subplot()
    x = np.arange(3)
    width = 0.23
    for offset, values, color, label in (
        (-width, partial, CYAN, "Partial search · half label"),
        (0, full_half, BLUE, "Global Grover · half label"),
        (width, full_exact, VIOLET, "Global Grover · exact item"),
    ):
        bars = ax.bar(x + offset, values, width=width * 0.92, color=color, label=label)
        ax.bar_label(bars, padding=5, fontsize=12, color=TEXT, fontweight="bold")
    ax.set(xticks=x, xticklabels=["90%", "95%", "99%"], xlabel="Required one-shot accuracy", ylabel="Phase-oracle queries", ylim=(0, 14))
    ax.grid(axis="y")
    ax.set_axisbelow(True)
    ax.legend(loc="upper left", ncol=3, fontsize=9, frameon=False, labelcolor=TEXT)
    fig.text(0.055, 0.115, "Historical V3 partition-bit-only reflection: 50% correct-half in tested N=4–64; not tested at N=256.", color=AMBER, fontsize=10)
    fig.text(0.055, 0.06, "Bars: analytic threshold minima in defined schedules; partial-search statevectors independently verified. Exact item is a different task.", color=MUTED, fontsize=9.5)
    save(fig, path, "For N=256, partial-search half-label queries are 7, 8, 9; global Grover half-label queries 9, 10, 11; exact-item queries 10, 11, 12.")


def scaling_figure(path: Path) -> None:
    n = np.arange(4, 31)
    root = 2.0 ** (n / 2)
    fig = frame("The access model changes the curve", "Analytical asymptotic illustration · unique marked item · no measured runtimes", height=6.0)
    axes = fig.subplots(1, 2, gridspec_kw={"width_ratios": [1.4, 0.8]})
    axes[0].plot(n, 2.0**n, color=AMBER, linewidth=2.8, label="Classical exhaustive · N")
    axes[0].plot(n, pi / 4 * root, color=BLUE, linewidth=2.8, label="Full Grover · ≈π√N/4")
    axes[0].plot(n, pi / (4 * sqrt(2)) * root, color=CYAN, linewidth=2.8, label="Two-block partial · ≈π√N/(4√2)")
    axes[0].set(yscale="log", xlabel="Address bits n = log2 N", ylabel="Verification-oracle calls", xlim=(4, 30))
    axes[0].legend(loc="upper left", fontsize=9, frameon=False, labelcolor=TEXT)
    axes[0].grid()
    axes[1].plot(n, n, color=VIOLET, linestyle="--", linewidth=3)
    axes[1].set(xlabel="Address bits n = log2 N", ylabel="Ideal partition decisions", xlim=(4, 30), ylim=(0, 35))
    axes[1].text(0.06, 0.89, "HYPOTHETICAL", transform=axes[1].transAxes, color=AMBER, fontsize=13, fontweight="bold")
    axes[1].text(0.06, 0.78, "n decisions only if a cheap\npartition-existence oracle exists", transform=axes[1].transAxes, color=TEXT, fontsize=10)
    axes[1].grid()
    fig.text(0.055, 0.055, "Panels use different oracle strengths. The right-hand oracle is unavailable at the assumed cheap cost; curves must not be compared as achieved algorithms.", color=MUTED, fontsize=9.5)
    save(fig, path, "Left: classical N and quantum square-root phase-query growth. Right: hypothetical logarithmic decisions with an uncosted partition oracle.")


def recursive_figure(path: Path) -> None:
    depth = 16
    levels = np.arange(depth)
    sizes = 2.0 ** (depth - levels)
    costs = np.sqrt(sizes)
    cumulative = np.cumsum(costs)
    fig = frame("Shrinking the space does not erase test cost", "Analytical model · N=2¹⁶ · hypothetical C(m)=√m at each level · coefficient set to 1", height=5.8)
    ax = fig.add_subplot()
    ax.bar(levels, costs, color=BLUE, width=0.72, label="Cost of this partition decision")
    ax.plot(levels, cumulative, color=CYAN, marker="o", markersize=4, linewidth=2.5, label="Cumulative query cost")
    ax.set(xlabel="Recursive decision level", ylabel="Illustrative phase-oracle queries", xlim=(-0.7, 15.8), ylim=(0, 920))
    ax.set_xticks([0, 3, 7, 11, 15])
    ax.grid(axis="y")
    ax.set_axisbelow(True)
    ax.legend(loc="center right", fontsize=10, frameon=False, labelcolor=TEXT)
    ax.annotate("first test: √N = 256", xy=(0, costs[0]), xytext=(2.0, 510), color=TEXT, fontsize=11, arrowprops={"arrowstyle": "->", "color": MUTED})
    ax.annotate(f"total ≈ {cumulative[-1]:.0f} = Θ(√N)", xy=(15, cumulative[-1]), xytext=(7.5, 760), color=CYAN, fontsize=11, arrowprops={"arrowstyle": "->", "color": CYAN})
    fig.text(0.055, 0.055, "Each stage calls a real subproblem test. Repetitions, errors, preparation and final verification would add cost.", color=MUTED, fontsize=10)
    save(fig, path, "Analytical per-stage square-root costs shrink through recursion, while cumulative cost remains order square root of initial N.")


def build(output: Path) -> None:
    output.mkdir(parents=True, exist_ok=True)
    style()
    bias_figure(output / FIGURES[0])
    partial_figure(output / FIGURES[1])
    scaling_figure(output / FIGURES[2])
    recursive_figure(output / FIGURES[3])
    manifest = {
        "classification": "Analytical predictions and archived ideal statevector observations; no new quantum experiment.",
        "sources": {name: digest(path) for name, path in SOURCES.items()},
        "figures": {name: digest(output / name) for name in FIGURES},
        "static_assets": {str(path.relative_to(ROOT)).replace("\\", "/"): digest(path) for path in STATIC},
    }
    (output / "manifest.json").write_bytes((json.dumps(manifest, indent=2) + "\n").encode("utf-8"))
    print(f"Built {len(FIGURES)} README figures in {output}")


def check(output: Path) -> None:
    manifest = json.loads((output / "manifest.json").read_text(encoding="utf-8"))
    if manifest["sources"] != {name: digest(path) for name, path in SOURCES.items()}:
        raise ValueError("README figure source digest mismatch")
    if manifest["figures"] != {name: digest(output / name) for name in FIGURES}:
        raise ValueError("README figure artifact digest mismatch")
    if manifest["static_assets"] != {
        str(path.relative_to(ROOT)).replace("\\", "/"): digest(path) for path in STATIC
    }:
        raise ValueError("README static-asset digest mismatch")
    for path in (*STATIC, *(output / name for name in FIGURES)):
        root = ElementTree.parse(path).getroot()
        names = {element.tag.rsplit("}", 1)[-1] for element in root}
        if root.tag.rsplit("}", 1)[-1] != "svg" or not {"title", "desc"} <= names:
            raise ValueError(f"SVG lacks title or description: {path}")
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    for alt, target in re.findall(r"!\[([^]]*)\]\(([^)]+)\)", readme):
        if not alt.strip():
            raise ValueError("README image lacks alternative text")
        if not target.startswith("https://") and not (ROOT / target).is_file():
            raise ValueError(f"README image missing: {target}")
    print(f"Verified {len(FIGURES)} generated figures, {len(STATIC)} static SVGs and {len(SOURCES)} archived sources")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=OUTPUT)
    parser.add_argument("--check", action="store_true", help="verify committed source and figure digests")
    args = parser.parse_args()
    if args.check:
        check(args.output_dir)
    else:
        build(args.output_dir)


if __name__ == "__main__":
    main()
