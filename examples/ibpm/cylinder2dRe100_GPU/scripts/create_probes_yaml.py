"""Write the YAML configuration file for the probes."""

import pathlib

import petibmpy


# Create configuration for a volume probe.
probe = petibmpy.ProbeVolume('probe-p', 'p',
                             box=((-0.75, 0.75), (-0.75, 0.75)),
                             viewer='hdf5', path='probe-p.h5',
                             n_sum=1000)
# Save configuration into YAML file.
simudir = pathlib.Path(__file__).absolute().parents[1]
filepath = simudir / 'probes.yaml'
petibmpy.probes_yaml_dump(probe, filepath)
