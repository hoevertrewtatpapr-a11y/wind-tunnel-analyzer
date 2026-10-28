# Wind Tunnel Analyzer

Plot the wind-tunnel data and find the angle of attack for a target lift
coefficient using `fsolve`.

The model is `CL = cl0 + lift_slope * alpha`. Angles are in degrees and the
lift slope is per degree. It applies before stall.

## Run

Install the dependencies in `environment.yml`, then run:

```bash
python main.py
```

Set `target_cl` in `main.py` to change the target. The default `CL = 0.80`
gives `alpha = 6.363636 deg`. The script also plots lift and drag from
`data/test1.csv`.

## Tests

```bash
python -m unittest discover -s tests -v
```

To run from the homework notebook, keep this project folder beside it and use:

```python
%run wind-tunnel-analyzer/main.py
```
