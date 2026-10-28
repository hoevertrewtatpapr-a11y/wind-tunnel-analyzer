"""Check the solver against the independent algebraic solution."""

from pathlib import Path
import sys
import unittest
from unittest.mock import patch

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from analysis import alpha_residual, compute_cl, solve_alpha


class AngleSolverTests(unittest.TestCase):
    def test_default_target(self):
        alpha = solve_alpha(0.80)
        self.assertAlmostEqual(alpha, (0.80 - 0.10) / 0.11, places=10)
        self.assertAlmostEqual(compute_cl(alpha), 0.80, places=12)

    def test_zero_and_negative_angles(self):
        for target in [0.10, 0.0, -0.45]:
            with self.subTest(target=target):
                alpha = solve_alpha(target)
                self.assertAlmostEqual(alpha, (target - 0.10) / 0.11, places=10)

    def test_custom_model_and_guess(self):
        alpha = solve_alpha(0.50, cl0=0.20, lift_slope=0.05, initial_guess=-4.0)
        self.assertAlmostEqual(alpha, 6.0, places=10)

    def test_negative_nonzero_slope(self):
        self.assertAlmostEqual(solve_alpha(0.50, lift_slope=-0.10), -4.0)

    def test_residual_at_known_root(self):
        self.assertAlmostEqual(alpha_residual(5.0, 0.65), 0.0, places=12)

    def test_zero_slope_rejected(self):
        for target in [0.10, 0.80]:
            with self.subTest(target=target):
                with self.assertRaises(ValueError):
                    solve_alpha(target, lift_slope=0.0)

    def test_nonfinite_inputs_rejected(self):
        for arguments in [
            {"target_cl": np.nan},
            {"target_cl": np.inf},
            {"target_cl": 0.80, "cl0": -np.inf},
            {"target_cl": 0.80, "lift_slope": np.nan},
            {"target_cl": 0.80, "initial_guess": np.inf},
        ]:
            with self.subTest(arguments=arguments):
                with self.assertRaises(ValueError):
                    solve_alpha(**arguments)

    def test_failed_convergence_rejected(self):
        result = (np.array([6.0]), {}, 5, "No progress")
        with patch("analysis.fsolve", return_value=result):
            with self.assertRaises(RuntimeError):
                solve_alpha(0.80)

    def test_incorrect_reported_root_rejected(self):
        result = (np.array([0.0]), {}, 1, "Converged")
        with patch("analysis.fsolve", return_value=result):
            with self.assertRaises(RuntimeError):
                solve_alpha(0.80)


if __name__ == "__main__":
    unittest.main()
