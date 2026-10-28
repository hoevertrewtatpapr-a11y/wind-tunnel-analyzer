"""Lift calculations and angle-of-attack solver."""

import numpy as np
from scipy.optimize import fsolve


def compute_cl(alpha, cl0=0.10, lift_slope=0.11):
    """Return CL; alpha is in degrees and lift_slope is per degree."""
    return cl0 + lift_slope * alpha


def print_lift_summary(alpha, cl0=0.10, lift_slope=0.11):
    """Print alpha in degrees and its lift coefficient."""
    cl = compute_cl(alpha, cl0=cl0, lift_slope=lift_slope)

    print("Wind Tunnel Analyzer")
    print("--------------------")
    print(f"Angle of attack : {alpha:.2f} deg")
    print(f"Lift coefficient: {cl:.3f}")


def alpha_residual(alpha, target_cl, cl0=0.10, lift_slope=0.11):
    """Return model CL minus target CL."""
    return compute_cl(alpha, cl0=cl0, lift_slope=lift_slope) - target_cl


def solve_alpha(target_cl, cl0=0.10, lift_slope=0.11, initial_guess=0.0):
    """Find alpha in degrees using the linear, pre-stall lift model."""
    parameters = np.array([target_cl, cl0, lift_slope, initial_guess], dtype=float)
    if not np.all(np.isfinite(parameters)):
        raise ValueError("The target, model parameters, and guess must be finite.")
    if lift_slope == 0:
        raise ValueError("A nonzero lift slope is needed for a unique angle.")

    root, info, ier, message = fsolve(
        alpha_residual,
        x0=initial_guess,
        args=(target_cl, cl0, lift_slope),
        full_output=True,
        xtol=1e-10,
    )
    if ier != 1:
        raise RuntimeError(f"The angle solver did not converge: {message.strip()}")

    alpha = float(root[0])
    residual = float(alpha_residual(alpha, target_cl, cl0, lift_slope))
    # Check the root against the lift equation.
    if not np.isfinite(alpha) or not np.isfinite(residual) or abs(residual) > 1e-8:
        raise RuntimeError("The angle solver returned an unacceptable residual.")
    return alpha
