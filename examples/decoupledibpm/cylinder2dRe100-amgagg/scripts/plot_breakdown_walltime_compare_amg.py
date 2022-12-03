"""Plot breakdown of stages by wall-time."""

import pathlib
from collections import OrderedDict

from matplotlib import pyplot

import petibmpy


simudir = pathlib.Path(__file__).absolute().parents[1]
maindir = simudir.parents[1]

cases = {
    'IBPM - Aggregation': {
        'directory': maindir / 'ibpm' / 'cylinder2dRe100',
        'xticklabel': 'IBPM\n(Aggregation)'
    },
    'Decoupled IBPM - Aggregation': {
        'directory': maindir / 'decoupledibpm' / 'cylinder2dRe100-amgagg',
        'xticklabel': 'Decoupled IBPM\n(Aggregation)'
    },
    'Decoupled IBPM - Classical': {
        'directory': maindir / 'decoupledibpm' / 'cylinder2dRe100',
        'xticklabel': 'Decoupled IBPM\n(Classical)'
    }
}

stage_labels = OrderedDict({
    'rhsVelocity': dict(label='Set RHS velocity', color='C2'),
    'solveVelocity': dict(label='Solve velocity', color='C1'),
    'rhsPoisson': dict(label='Set RHS Poisson', color='C3'),
    'solvePoisson': dict(label='Solve Poisson', color='C0'),
    'other': dict(label='Other', color='C5')
})

for name, config in cases.items():
    filepath = config['directory'] / 'view.log'
    logview = petibmpy.PETScLogView(filepath=filepath)
    stages = {}
    others = []
    for event, data in logview.events.items():
        if event in stage_labels:
            stages[event] = data
        else:
            others.append(data)
    stages['other'] = {key: 0.0 for key in others[0]}
    for other_i in others:
        for key, val in other_i.items():
            stages['other'][key] += val

    cases[name]['stages'] = stages

pyplot.rc('font', family='serif', size=14)
fig, ax = pyplot.subplots(figsize=(8.0, 6.0))
ax.set_ylabel('Wall-time (min)')
index = 1
for data in cases.values():
    bottom = 0.0
    stages = data['stages']
    for i, (key, plt_kwargs) in enumerate(stage_labels.items()):
        if key not in stages:
            continue
        walltime = stages[key]['wall-time (s)'] / 60
        ax.bar(index, walltime, bottom=bottom, width=0.25, **plt_kwargs)
        bottom += walltime
    if index == 1:
        walltime_ref = bottom
    else:
        speedup = walltime_ref / bottom
        s = f'${speedup:0.1f}x$'
        ax.text(index, bottom + 1, s,
                horizontalalignment='center',
                verticalalignment='center')
    index += 1

for loc in ('top', 'bottom', 'right'):
    ax.spines[loc].set_visible(False)

handles, labels = pyplot.gca().get_legend_handles_labels()
by_label = OrderedDict(zip(labels, handles))
ax.legend(by_label.values(), by_label.keys(), frameon=False, loc='upper right')

ax.set_xticks(range(1, len(cases) + 1))
ax.set_xticklabels([v['xticklabel'] for v in cases.values()])

ax.set_xlim(0.5, 3.5)
ax.set_ylim(0.0, 50.0)

fig.tight_layout()

# Save the figure as a PNG.
figdir = simudir / 'figures'
figdir.mkdir(parents=True, exist_ok=True)
filepath = figdir / 'breakdown_walltime_compare_amg.png'
fig.savefig(filepath, dpi=300, bbox_inches='tight')

pyplot.show()
