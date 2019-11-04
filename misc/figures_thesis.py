"""Gather figures (to be included in thesis)."""

import os
import pathlib
import shutil


rootdir = pathlib.Path(__file__).absolute().parents[1]
n_parts = len(rootdir.parts)

# Create the output directory.
figdir = rootdir / 'figures_thesis'
figdir.mkdir(parents=True, exist_ok=True)

# Load paths of figures to gather.
inpath = rootdir / 'misc' / 'figures_thesis.txt'
filepaths = []
with open(inpath, 'r') as infile:
    filepaths = [rootdir / line.strip() for line in infile.readlines()
                 if not line.startswith('#')]

# Define new names of the output figures.
filenames = []
for filepath in filepaths:
    filename, filedir = filepath.name, filepath.parent
    prefix = '_'.join([e for e in filedir.parts[n_parts + 2:]
                       if e != 'figures'])
    filenames.append('_'.join([prefix, filename]).lstrip('_'))

# Copy figures to output directory.
for filepath, filename in zip(filepaths, filenames):
    shutil.copy(filepath, figdir / filename)
