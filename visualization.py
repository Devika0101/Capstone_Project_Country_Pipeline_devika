
"""Create a professional scatter plot of country population versus area."""

from pathlib import Path

import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.ticker import FuncFormatter


def create_scatter_plot(data, output_path=None):
    """Create and save a formatted population-versus-area scatter plot."""

    required_columns = {"population", "area"}
    missing = required_columns - set(data.columns)

    if missing:
        raise ValueError(f"Missing columns: {sorted(missing)}")

    # Keep only valid, positive numeric values for logarithmic axes.
    df = data.copy()
    df["population"] = pd.to_numeric(df["population"], errors="coerce")
    df["area"] = pd.to_numeric(df["area"], errors="coerce")
    df = df.dropna(subset=["population", "area"])
    df = df[(df["population"] > 0) & (df["area"] > 0)]

    if df.empty:
        raise ValueError("No valid positive population and area values found.")

    if output_path is None:
        output_path = (
            Path(__file__).resolve().parent / "population_vs_area.png"
        )
    else:
        output_path = Path(output_path)

    fig, ax = plt.subplots(figsize=(11, 7))

    ax.scatter(
        df["population"],
        df["area"],
        s=85,
        alpha=0.75,
        edgecolors="white",
        linewidths=0.8,
        label="Countries",
    )

    ax.set_xscale("log")
    ax.set_yscale("log")

    ax.set_title(
        "Country Population vs Area",
        fontsize=17,
        fontweight="bold",
        pad=18,
    )
    ax.set_xlabel("Population (people, log scale)", fontsize=12, labelpad=10)
    ax.set_ylabel("Area (sq. km, log scale)", fontsize=12, labelpad=10)

    ax.xaxis.set_major_formatter(
        FuncFormatter(lambda x, _: f"{x:,.0f}")
    )
    ax.yaxis.set_major_formatter(
        FuncFormatter(lambda y, _: f"{y:,.0f}")
    )

    ax.grid(True, which="major", linestyle="--", alpha=0.3)
    ax.grid(True, which="minor", linestyle=":", alpha=0.12)
    ax.legend(frameon=False)
    ax.set_axisbelow(True)

    fig.tight_layout()
    fig.savefig(output_path, dpi=200, bbox_inches="tight")
    plt.close(fig)

    print(f"Professional scatter plot saved to: {output_path}")
    return output_path
