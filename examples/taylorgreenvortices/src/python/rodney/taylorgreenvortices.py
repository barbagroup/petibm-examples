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
    a = 2 * numpy.pi
    u = -numpy.cos(a * X) * numpy.sin(a * Y) * numpy.exp(-2 * a**2 * nu * t)
    v = +numpy.sin(a * X) * numpy.cos(a * Y) * numpy.exp(-2 * a**2 * nu * t)
    p = (-0.25 * (numpy.cos(2 * a * X) + numpy.cos(2 * a * Y)) *
         numpy.exp(-4 * a**2 * nu * t))
    return u, v, p
