"""Helper functions to plot the solution fields."""

from matplotlib import pyplot


def plot_contourf_field(grid, field, name, figsize=(8.0, 8.0),
                        levels=None, axis_lim=(0.0, 1.0, 0.0, 1.0),
                        ref=None, body=None):
    """Plot the filled contour of the a given 2D field.

    Parameters
    ----------
    grid : tuple of numpy.ndarray objects
        Gridline locations in each direction.
    field : numpy.ndarray
        Solution field to plot, given as a 2D array of floats.
    name : str
        Name of the field.
    figsize : tuple of floats
        The size of the Matplotlib figure.
    levels : list or numpy.ndarray, optional
        Levels of the contours to plot; default is None.
    axis_lim : tuple of floats, optional
        Limits of the x- and y-axes ('xmin', 'xmax', 'ymin', 'ymax');
        default is (0.0, 1.0, 0.0, 1.0).
    ref : numpy.ndarray, optional
        Reference solution to plot on separate Matplotlib axes;
        default is None (i.e., does not plot the reference solution).
    body : tuple of numpy.ndarray objects, optional
        The coordinates of the immersed body to plot, given tuple of two
        elements (array with x coordinates followed by array with y
        coordinates); default is None (i.e., does not plot the body).

    Returns
    -------
    matplotlib.figure.Figure
        The Matplotlib Figure object.
    matplotlib.axes.Axes
        The Matplotlib Axes object or array of Axes objects.

    """
    fig = pyplot.figure(figsize=figsize)
    if ref is not None:
        ax = fig.add_subplot(121)
        ax2 = fig.add_subplot(122)
    else:
        ax = fig.add_subplot(111)
    ax.set_title(name)
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.contourf(*grid, field, levels=levels, extend='both')
    if body is not None:
        ax.plot(*body, color='C3')
    ax.axis('scaled', adjustable='box')
    ax.axis(axis_lim)
    if ref is not None:
        ax2.set_title(name + ' (ref)')
        ax2.set_xlabel('x')
        ax2.set_ylabel('y')
        ax2.contourf(*grid, ref, levels=levels, extend='both')
        ax2.axis('scaled', adjustable='box')
        ax2.axis(axis_lim)
    fig.tight_layout()
    return fig, ax
