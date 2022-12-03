"""Helper functions for the Taylor-Green vortices application."""

import numpy


def taylor_green_vortex(x, y, t, nu):
    """Return the solution of the Taylor-Green vortex at given time.

    Parameters
    ----------
    x : numpy.ndarray
        Gridline locations in the x direction as a 1D array of floats.
    y : numpy.ndarray
        Gridline locations in the y direction as a 1D array of floats.
    t : float
        Time value.
    nu : float
        Coefficient of viscosity.

    Returns
    -------
    numpy.ndarray
        x-component of the velocity field as a 2D array of floats.
    numpy.ndarray
        y-component of the velocity field as a 2D array of floats.
    numpy.ndarray
        pressure field as a 2D array of floats.

    """
    X, Y = numpy.meshgrid(x, y)
    F = numpy.exp(-2 * nu * t)
    u = -numpy.cos(X) * numpy.sin(Y) * F
    v = +numpy.sin(X) * numpy.cos(Y) * F
    p = -0.25 * (numpy.cos(2 * X) + numpy.cos(2 * Y)) * F**2
    return u, v, p
