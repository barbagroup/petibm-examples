"""Module to read force coefficients from different sources."""

import numpy
import pathlib

import petibmpy


rootdir = pathlib.Path(__file__).absolute().parents[5]
datadir = rootdir / 'data' / 'flapping2dRe75'


class Flapping(object):
    """Contain information about the flapping kinematics."""

    def __init__(self):
        """Initialize parameters of the flapping kinematics."""
        self.Re = 75.0  # Reynolds number
        self.rho = 1.0  # density
        self.c = 1.0  # chord-length
        self.r = 0.10  # thickness-to-chord ratio
        self.A0 = 2.8 * self.c  # stroke amplitude
        self.f = 0.25  # flapping frequency
        self.Umax = self.A0 * numpy.pi * self.f  # max translational velocity
        self.alpha0 = numpy.pi / 2  # initial angle of attack
        self.beta = numpy.pi / 4  # amplitude of the pitching
        self.phi = 0.0  # phase difference between translation and rotation

    def orientation_angle(self, t):
        """Return the orientation angle (in radians) at a given time t."""
        w = 2 * numpy.pi * self.f
        alpha = self.alpha0 + self.beta * numpy.sin(w * t + self.phi)
        return alpha

    def displacement(self, t):
        """Return the displacement of the wing at a given time t."""
        w = 2 * numpy.pi * self.f
        xd = self.A0 / 2 * numpy.cos(w * t)
        yd = 0.0
        return xd, yd

    def position(self, t, x0, y0):
        """Return the coordinates of the wing a given time t."""
        xd, yd = self.displacement(t)
        alpha = self.orientation_angle(t)
        x, y = x0 + xd, y0 + yd
        x, y = petibmpy.rotate2d(x, y, center=(xd, yd),
                                 angle=alpha, mode='rad')
        return x, y

    def translational_velocity(self, t):
        """Return the translational velocity of the wing at a given time t."""
        w = 2 * numpy.pi * self.f
        ux = -self.Umax * numpy.sin(w * t)
        uy = 0.0 if isinstance(t, float) else numpy.zeros_like(t)
        return ux, uy

    def angular_velocity(self, t):
        """Return the angular velocity of the wing at a given time t."""
        w = 2 * numpy.pi * self.f
        omega = w * self.beta * numpy.cos(w * t + self.phi)
        return omega

    def velocity(self, t, x, y, xc, yc):
        """Return the velocity of the wing at a given time t."""
        U0, V0 = self.translational_velocity(t)
        W0 = self.angular_velocity(t)
        ux = U0 - W0 * (y - yc)
        uy = V0 + W0 * (x - xc)
        return ux, uy

    def quasi_steady_coefficients(self, t):
        """Compute the quasi-steady force coefficients at a given time t."""
        alpha = self.orientation_angle(t)
        U0, _ = self.translational_velocity(t)
        if isinstance(t, float):
            alpha = numpy.pi - alpha if U0 <= 0.0 else alpha
        else:
            mask = numpy.where(U0 <= 0.0)
            alpha[mask] = numpy.pi - alpha[mask]
        CD = 1.4 - numpy.cos(2 * alpha)
        CL = 1.2 * numpy.sin(2 * alpha)
        return CD, CL

    def quasi_steady_forces(self, t, x, y, xc, yc, rho=1.0):
        """Compute the quasi-steady forces at a given time t."""
        CD, CL = self.quasi_steady_coefficients(t)
        ux, uy = self.velocity(t, x, y, xc, yc)
        u = numpy.sqrt(ux**2 + uy**2)
        D = 0.5 * rho * u**2 * CD
        L = 0.5 * rho * u**2 * CL
        return D, L

    def get_CD_CL(self, filepath, bodypath):
        """Load the forces from file and return the force coefficients."""
        t, fx, fy = petibmpy.read_forces(filepath)
        # Non-dimensionalize time by the period.
        t_nodim = self.f * t
        # Reverse sign of force in x-direction when the body moving
        # in the positive x-direction.
        U0, _ = self.translational_velocity(t)
        fx *= -U0 / numpy.abs(U0)
        # Normalize the forces by the maximum quasi-steady force on the wing.
        D, L = [], []
        x0 = petibmpy.read_body(bodypath, skiprows=1, usecols=0)
        y0 = numpy.zeros_like(x0)
        for ti in t:
            alpha = self.orientation_angle(ti)
            x, y = petibmpy.rotate2d(x0, y0, center=(0.0, 0.0),
                                     angle=alpha, mode='rad')
            Di, Li = self.quasi_steady_forces(ti, x, y, 0.0, 0.0, rho=1.0)
            D.append(numpy.max(Di))
            L.append(numpy.max(Li))
        D, L = numpy.array(D), numpy.array(L)
        cd, cl = fx / numpy.max(D), fy / numpy.max(L)
        return {'CD': (t_nodim, cd), 'CL': (t_nodim, cl)}


def get_CD_CL(label, *args):
    """Load/Compute the force coefficients."""
    dispatcher = {'petibm': Flapping().get_CD_CL,
                  'Li et al. (2015)': get_CD_CL_li_et_al_2015,
                  'Wang et al. (2004)': get_CD_CL_wang_et_al_2004,
                  'Eldredge (2007)': get_CD_CL_eldredge_2007}
    if label not in dispatcher.keys():
        raise ValueError(f'Label should be in {list(dispatcher.keys())}')
    return dispatcher[label](*args)


def get_CD_CL_li_et_al_2015():
    """Get the force coefficients from Li et al. (2015)."""
    filepath = datadir / 'CD_current.dat'
    with open(filepath, 'r') as infile:
        t1, cd = numpy.loadtxt(infile, unpack=True)
    filepath = datadir / 'CL_current.dat'
    with open(filepath, 'r') as infile:
        t2, cl = numpy.loadtxt(infile, unpack=True)
    return {'CD': (t1, cd), 'CL': (t2, cl)}


def get_CD_CL_wang_et_al_2004():
    """Get the force coefficients from Wang et al. (2004)."""
    filepath = datadir / 'CD_EXP.dat'
    with open(filepath, 'r') as infile:
        t1, cd = numpy.loadtxt(infile, unpack=True)
    filepath = datadir / 'CL_EXP.dat'
    with open(filepath, 'r') as infile:
        t2, cl = numpy.loadtxt(infile, unpack=True)
    return {'CD': (t1, cd), 'CL': (t2, cl)}


def get_CD_CL_eldredge_2007():
    """Get the force coefficients from Eldredge (2007)."""
    filepath = datadir / 'CD_VVPM.dat'
    with open(filepath, 'r') as infile:
        t1, cd = numpy.loadtxt(infile, unpack=True)
    filepath = datadir / 'CL_VVPM.dat'
    with open(filepath, 'r') as infile:
        t2, cl = numpy.loadtxt(infile, unpack=True)
    return {'CD': (t1, cd), 'CL': (t2, cl)}
