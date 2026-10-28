"""
analysis.py

Aerodynamic analysis utilities for the Wind Tunnel Analyzer project.

Calculate lift and solve for angle of attack using a linear lift model.
"""

import numpy as np
from scipy.optimize import fsolve


def compute_cl(alpha, cl0=0.10, lift_slope=0.11):
    """
    Compute lift coefficient using a linear lift model.

    Parameters
    ----------
    alpha : float
        Angle of attack in degrees.
    cl0 : float, optional
        Lift coefficient at zero angle of attack.
    lift_slope : float, optional
        Lift curve slope in units of 1/degree.

    Returns
    -------
    float
        Lift coefficient.
    """
    return cl0 + lift_slope * alpha


def print_lift_summary(alpha, cl0=0.10, lift_slope=0.11):
    """
    Print a simple summary of the lift coefficient for a given angle of attack.

    Parameters
    ----------
    alpha : float
        Angle of attack in degrees.
    cl0 : float, optional
        Lift coefficient at zero angle of attack.
    lift_slope : float, optional
        Lift curve slope in units of 1/degree.
    """
    cl = compute_cl(alpha, cl0=cl0, lift_slope=lift_slope)

    print("Wind Tunnel Analyzer")
    print("--------------------")
    print(f"Angle of attack : {alpha:.2f} deg")
    print(f"Lift coefficient: {cl:.3f}")


def alpha_residual(alpha, target_cl, cl0=0.10, lift_slope=0.11):
    """Return the difference between the model and target lift coefficients."""
    return compute_cl(alpha, cl0=cl0, lift_slope=lift_slope) - target_cl


def solve_alpha(target_cl, cl0=0.10, lift_slope=0.11, initial_guess=0.0):
    """Find angle of attack in degrees for the requested lift coefficient.

    The lift slope is in 1/degree. This inverts the linear model, which
    does not describe stall or select a branch of the experimental curve.
    """
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
    # A reported root still has to satisfy the equation being solved.
    if not np.isfinite(alpha) or not np.isfinite(residual) or abs(residual) > 1e-8:
        raise RuntimeError("The angle solver returned an unacceptable residual.")
    return alpha
