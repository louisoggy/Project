import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import pandas as pd
import matplotlib.pyplot as plt

RESULTS_DIR = os.path.join(os.path.dirname(__file__), "results")
FIGURES_DIR = os.path.join(os.path.dirname(__file__), "figures")

SYSTEM_COLOURS = {"hi_lo": "#1f77b4", "ko": "#ff7f0e", "zen": "#2ca02c"}
SYSTEM_LABELS  = {"hi_lo": "Hi-Lo",   "ko": "KO",      "zen": "Zen"}


def _ensure_figures_dir():
    os.makedirs(FIGURES_DIR, exist_ok=True)


def _save_fig(filename):
    _ensure_figures_dir()
    path = os.path.join(FIGURES_DIR, filename)
    plt.savefig(path, dpi=150, bbox_inches="tight")
    print(f"saved -> {path}")


def plot_perfect_play():
    df = pd.read_csv(os.path.join(RESULTS_DIR, "perfect_play_simulation.csv"))

    systems = df["system"].tolist()
    labels  = [SYSTEM_LABELS[s] for s in systems]
    colours = [SYSTEM_COLOURS[s] for s in systems]

    fig = plt.figure(figsize=(6, 4))
    plt.bar(labels, df["mean_edge"], yerr=df["stderr_edge"],
            color=colours, capsize=5, width=0.5)
    plt.xlabel("Counting system")
    plt.ylabel("Player edge (%)")
    plt.title("Player edge by counting system (perfect play)")
    plt.grid(axis="y", linewidth=0.5, alpha=0.7)
    plt.tight_layout()
    _save_fig("perfect_play_edge.png")
    plt.close(fig)


def plot_error_robustness():
    df = pd.read_csv(os.path.join(RESULTS_DIR, "err_robustness_simulation.csv"))

    # convert error_rate fraction to percentage for the x axis
    df["error_rate_pct"] = df["error_rate"] * 100

    fig = plt.figure(figsize=(7, 4))
    for system, group in df.groupby("system", sort=False):
        group = group.sort_values("error_rate_pct")
        plt.errorbar(
            group["error_rate_pct"], group["mean_edge"],
            yerr=group["stderr_edge"],
            label=SYSTEM_LABELS[system],
            color=SYSTEM_COLOURS[system],
            marker="o", markersize=5,
            capsize=4, linewidth=1.5,
        )
    plt.xlabel("Count error rate (%)")
    plt.ylabel("Player edge (%)")
    plt.title("Edge vs counting error rate")
    plt.legend()
    plt.grid(linewidth=0.5, alpha=0.7)
    plt.tight_layout()
    _save_fig("error_robustness.png")
    plt.close(fig)


def plot_risk_of_ruin():
    df = pd.read_csv(os.path.join(RESULTS_DIR, "ruin_simulation.csv"))

    # broke_rate is stored as a fraction; convert to percentage
    df["broke_pct"] = df["broke_rate"] * 100

    fig = plt.figure(figsize=(7, 4))
    for system, group in df.groupby("system", sort=False):
        group = group.sort_values("bankroll")
        plt.plot(
            group["bankroll"], group["broke_pct"],
            label=SYSTEM_LABELS[system],
            color=SYSTEM_COLOURS[system],
            marker="o", markersize=5, linewidth=1.5,
        )
    plt.xlabel("Starting bankroll (units)")
    plt.ylabel("Risk of ruin (%)")
    plt.title("Risk of ruin vs starting bankroll")
    plt.legend()
    plt.grid(linewidth=0.5, alpha=0.7)
    plt.tight_layout()
    _save_fig("risk_of_ruin.png")
    plt.close(fig)


def generate_all():
    plot_perfect_play()
    plot_error_robustness()
    plot_risk_of_ruin()


if __name__ == "__main__":
    generate_all()
