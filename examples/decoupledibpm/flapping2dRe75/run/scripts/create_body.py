"""Create an ellipse."""

import numpy
import pathlib

import petibmpy


def ellipse(a, b, center=(0.0, 0.0), num=50):
    """Return the coordinates of an ellipse.

    Parameters
    ----------
    a : float
        The semi-major axis of the ellipse.
    b : float
        The semi-minor axis of the ellipse.
    center : 2-tuple of floats, optional
        The position of the center of the ellipse;
        default: (0.0, 0.0)
    num : integer, optional
        The number of points on the upper side of the ellipse.
        The number includes the leading and trailing edges.
        Thus, the total number of points will be 2 * (num - 1);
        default: 50.

    Returns
    -------
    x : numpy.ndarray
        The x-coordinates of the ellipse as a 1D array of floats.
    y: numpy.ndarray
        The y-coordinates of the ellipse as a 1D array of floats.

    """
    xc, yc = center
    x_upper = numpy.linspace(xc + a, xc - a, num=num)
    y_upper = b / a * numpy.sqrt(a**2 - x_upper**2)
    x_lower = numpy.linspace(xc - a, xc + a, num=num)[1:-1]
    y_lower = -b / a * numpy.sqrt(a**2 - x_lower**2)
    x = numpy.concatenate((x_upper, x_lower))
    y = numpy.concatenate((y_upper, y_lower))
    return x, y


# Set parameters of the ellipse.
c = 1.0  # chord of the ellipse (major axis)
r = 0.10  # ratio between minor and major axis
a, b = c / 2.0, r * c / 2.0
x0, y0 = ellipse(a, b, center=(0.0, 0.0), num=100)

# Regularize the boundary given a resolution.
ds = 0.025  # target distance between two consecutive points.
x, y = petibmpy.regularize2d(x0, y0, ds=ds)

# Save coordinates into a file.
simudir = pathlib.Path(__file__).absolute().parents[1]
filepath = simudir / 'ellipse.body'
petibmpy.write_body(filepath, x, y)
