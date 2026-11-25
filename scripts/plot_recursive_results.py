"""Replot the committed recursive summary without rerunning any experiment."""

import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]


def build() -> Path:
    data = json.loads((ROOT / "results" / "phase2_recursive.json").read_text(encoding="utf-8"))
    summary = data["summary"]
    levels = sorted({row["confidence_target"] for row in summary})
    fig, axes = plt.subplots(1, len(levels), figsize=(5 * len(levels), 4.5), sharey=True, squeeze=False)
    styles = {
        "adaptive_rcp_qi": ("C0", "o", "Recursive partition"),
        "grover_with_confidence": ("C1", "s", "Full-space Grover"),
    }
    for ax, confidence in zip(axes[0], levels, strict=True):
        for algorithm, (color, marker, label) in styles.items():
            rows = sorted(
                (row for row in summary if row["confidence_target"] == confidence and row["algorithm"] == algorithm),
                key=lambda row: row["N"],
            )
            xs = [row["mean_total_predicate_queries"] for row in rows]
            ys = [row["success_probability_empirical"] for row in rows]
            ax.plot(xs, ys, color=color, marker=marker, label=label)
            for row in rows:
                offset = (0, 7) if algorithm == "adaptive_rcp_qi" else (0, -13)
                ax.annotate(
                    str(row["N"]),
                    (row["mean_total_predicate_queries"], row["success_probability_empirical"]),
                    xytext=offset,
                    textcoords="offset points",
                    ha="center",
                    fontsize=8,
                )
        ax.set(xlabel="mean total predicate calls", title=f"Target {confidence:.0%}")
        ax.set_ylim(0.78, 1.055)
        ax.grid(alpha=0.2)
    axes[0][0].set_ylabel("empirical final-solution accuracy")
    axes[0][0].legend(loc="lower left", fontsize=8)
    fig.suptitle("Accuracy versus query cost (point labels show N)")
    fig.tight_layout()
    output = ROOT / "results" / "figures" / "phase2_recursive_accuracy_v2.png"
    output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output, dpi=160)
    plt.close(fig)
    return output


if __name__ == "__main__":
    print(build())
