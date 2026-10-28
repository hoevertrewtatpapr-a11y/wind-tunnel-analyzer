"""
main.py

Entry point for the Wind Tunnel Analyzer project.

This script loads experimental wind tunnel data, generates basic plots,
and evaluates the current linear lift model. If the angle-of-attack solver
has been implemented in analysis.py, the script will also compute the
angle of attack required to achieve a target lift coefficient.
"""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

from analysis import compute_cl, solve_alpha

BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "data" / "test1.csv"
CL0 = 0.10
LIFT_SLOPE = 0.11


def main():
    """Run the Wind Tunnel Analyzer workflow."""

    cl0 = CL0
    lift_slope = LIFT_SLOPE
    target_cl = 0.80

    df = load_data(DATA_FILE)
    print_data_summary(df)
    plot_lift_curve(df, cl0=cl0, lift_slope=lift_slope)
    plot_drag_curve(df)

    alpha = solve_alpha(target_cl, cl0=cl0, lift_slope=lift_slope)
    achieved_cl = compute_cl(alpha, cl0=cl0, lift_slope=lift_slope)
    print(f"Target lift coefficient: {target_cl:.3f}")
    print(f"Required angle of attack: {alpha:.6f} deg")
    print(f"Model lift coefficient: {achieved_cl:.6f}")
    print(f"Lift coefficient residual: {achieved_cl - target_cl:.2e}")

    plt.show()


def load_data(filepath):
    """Load wind tunnel data from a CSV file using Pandas."""
    df = pd.read_csv(filepath)

    required_columns = {"alpha_deg", "cl", "cd"}
    missing = required_columns - set(df.columns)
    if missing:
        raise ValueError(
            f"Missing required column(s): {', '.join(sorted(missing))}"
        )

    return df


def print_data_summary(df):
    """Print a brief summary of the loaded dataset."""
    print("Wind Tunnel Analyzer")
    print("--------------------")
    print(f"Number of data points: {len(df)}")
    print(
        f"Alpha range          : "
        f"{df['alpha_deg'].min():.2f} to {df['alpha_deg'].max():.2f} deg"
    )
    print(
        f"CL range             : "
        f"{df['cl'].min():.3f} to {df['cl'].max():.3f}"
    )
    print(
        f"CD range             : "
        f"{df['cd'].min():.3f} to {df['cd'].max():.3f}"
    )
    print("\nFirst few rows:")
    print(df.head().to_string(index=False))
    print()


def plot_lift_curve(df, cl0=CL0, lift_slope=LIFT_SLOPE):
    """Plot experimental CL vs alpha data and overlay the linear lift model."""
    alpha_data = df["alpha_deg"]
    cl_data = df["cl"]

    alpha_model = alpha_data.sort_values()
    cl_model = [compute_cl(alpha, cl0=cl0, lift_slope=lift_slope) for alpha in alpha_model]

    plt.figure(figsize=(8, 5))
    plt.plot(alpha_data, cl_data, "o", label="Experimental data")
    plt.plot(alpha_model, cl_model, "-", label="Linear lift model (no stall)")
    plt.xlabel("Angle of attack, α (deg)")
    plt.ylabel("Lift coefficient, $C_L$")
    plt.title("Lift Curve")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()


def plot_drag_curve(df):
    """Plot experimental CD vs alpha data."""
    plt.figure(figsize=(8, 5))
    plt.plot(df["alpha_deg"], df["cd"], "o-")
    plt.xlabel("Angle of attack, α (deg)")
    plt.ylabel("Drag coefficient, $C_D$")
    plt.title("Drag Curve")
    plt.grid(True)
    plt.tight_layout()


if __name__ == "__main__":
    main()
    print("main.py ran successfully")
