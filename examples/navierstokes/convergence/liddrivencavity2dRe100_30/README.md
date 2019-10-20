# Convergence test of the Navier-Stokes solver

We use the 2D lid-driven cavity flow problem to compute the observed order of convergence on three consistently refined grids.

The present directory contains four folders (`30`, `90`, `270`, and `810`), which means that we can compute two observed orders of convergence (using the three first grids and using the three last grids).
The folder name corresponds to the number of cells in the x and y directions.

Run the cases from the present directory:

```shell
petibm-navierstokes -directory 30 -options_left -log_view ascii:30/view.log
petibm-navierstokes -directory 90 -options_left -log_view ascii:90/view.log
petibm-navierstokes -directory 270 -options_left -log_view ascii:270/view.log
petibm-navierstokes -directory 810 -options_left -log_view ascii:810/view.log
```

Computes the observed orders of convergence for the velocity components and
the pressure using three consistently refined grids:

```shell
python scripts/order_convergence.py
```
