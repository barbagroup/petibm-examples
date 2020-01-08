"""Plot the isosurfaces of the Q-criterion at save time steps.

The isosurfaces are colored with the streamwise vorticity.
"""

import numpy
import os
import pathlib
import sys

moduledir = os.path.join(os.environ.get('PETIBMPY_DIR'), 'misc')
if moduledir not in sys.path:
    sys.path.insert(0, moduledir)
from visitplot import *


simudir = pathlib.Path(__file__).absolute().parents[1]
datadir = simudir / 'output'
xdmfpath = datadir / 'postprocessing' / 'qcrit_wx_cc.xmf'
config_view = simudir / 'scripts' / 'visit_view3d.yaml'
figdir = simudir / 'figures'
prefix = 'qcrit_wx_wake3d_'

visit_plot_qcrit_wx_3d_direct(xdmfpath,
                              wx_range=(-5.0, 5.0),
                              q_value=0.05,
                              config_view=config_view,
                              out_dir=figdir, out_prefix=prefix,
                              figsize=(880, 372))
