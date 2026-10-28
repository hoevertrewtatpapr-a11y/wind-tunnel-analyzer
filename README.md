# MECH 305 HW4
**Disclaimer**: This repository is part of the MECH 305 Homework 4 Github assignment. It is intended to be used to practise using the Github.

---
# Wind Tunnel Analyzer
This repository is part of AeroLab Dynamics computational toolkit. The **Wind Tunnel Analyzer** is a lightweight Python utility for performing quick aerodynamic calculations using simplified models and wind tunnel testing concepts. This tool provides estimates of aerodynamic quantities, validation of experimental trends and a simple analytical calculations alongside wind tunnel data. The current version of the tool includes a basic implementation of a linear lift model. However, several analysis features are still under development.

---
## Repository Structure

```text
wind-tunnel-analyzer/
├── data/             # Data folder
│   └── test1.csv     # Spreadsheet of collected data
├── main.py           # Entry point for running the analysis
├── analysis.py       # Aerodynamic calculations and solver functions
├── README.md         # Project documentation
└── environment.yml   # Python dependencies
```

---
## Experiment

The Wind Tunnel Analyzer is designed to support analysis of aerodynamic data obtained from controlled wind tunnel experiments. This section outlines the relationship between what is physically measured, what is recorded, and what is computed within the tool.

**Inputs (controlled variables)**

During a wind tunnel test, the controlled variables include:

- **Angle of attack** $(\alpha)$
- **Freestream velocity** $(V)$

For the current implementation, the analysis focuses on variations in angle of attack.

**Measurement system**

The wind tunnel setup includes a force balance system used to measure aerodynamic forces acting on the test article. The primary measured quantities are:

- **Lift force** $(L)$ — force perpendicular to the flow
- **Drag force** $(D)$ — force parallel to the flow

These measurements are obtained using load cells.

**Derived quantities**
Lift and drag coefficients can be calculated using:

$$ 
C_L = \frac{L}{\tfrac{1}{2} \rho V^2 A}, \quad  
C_D = \frac{D}{\tfrac{1}{2} \rho V^2 A}  
$$

where:

- $L$ = vertical lift force
- $D$ = horizontal drag force
- $\rho$ = air density
- $V$ = wind velocity
- $A$ = area

These coefficients allow results to be compared across different flow conditions and configurations.

---

## Analysis

A primary result of wind tunnel testing is the **lift curve**, which relates lift coefficient to angle of attack:

$$  
C_L\ \text{vs}\ \alpha  
$$

This relationship is used to determine operating conditions required to achieve a desired aerodynamic performance.


**Current approach**

In the current workflow, determining the angle of attack required to achieve a target lift coefficient is performed manually.

This involves:

1. performing a sweep over angle of attack during testing
2. plotting the resulting lift curve $(C_L$ vs $\alpha)$
3. estimating the angle of attack corresponding to a desired $C_L$

For simplified models, the relationship can also be evaluated analytically using:

$$  
C_L = C_{L0} + a \alpha  
\quad \longrightarrow \quad  
\alpha = \frac{C_{L,\text{target}} - C_{L0}}{a}  
$$

While effective in simple cases, these approaches rely on manual estimation or algebraic manipulation.

### Automated approach

To support a more consistent and extensible analysis workflow, the tool is being extended to compute the required angle of attack numerically.

Instead of solving the equation directly, the problem is expressed in residual form:

$$  
f(\alpha) = C_{L0} + a \alpha - C_{L,\text{target}}  
$$

The solution is obtained by finding the value of $\alpha$ such that:

$$  
f(\alpha) = 0  
$$

`analysis.solve_alpha` uses `scipy.optimize.fsolve` to find this root. It
checks the convergence flag and the residual before returning the angle
in degrees. A zero lift slope is rejected because it cannot give a unique
angle. The linear model is intended for pre-stall conditions; it does not
fit the measured data or describe the post-stall curve.

For the demonstration target $C_L=0.80$, with $C_{L0}=0.10$ and
$a=0.11$ per degree, the required angle is **6.363636 degrees**.

## Run the project

Create the environment from `environment.yml`, or install NumPy, SciPy,
Matplotlib, and Pandas in your existing environment. From the project folder:

```bash
python main.py
python -m unittest discover -s tests -v
```

When the project folder is next to the homework notebook, its existing cell
also runs the script:

```python
%run wind-tunnel-analyzer/main.py
```

Change `target_cl` in `main()` to analyze another target. The script prints
the required angle and the lift check, and displays the experimental lift
and drag curves. Data paths are relative to `main.py`, so running it from
the notebook does not depend on the current working directory.
