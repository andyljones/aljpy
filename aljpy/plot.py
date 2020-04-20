import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
from pathlib import Path

def si_suffix(x):
    #TODO: merge with suffix_axis
    suffixes = np.array(['', 'k', 'm', 'b', 't'])

    order = np.log10(max(abs(x), 1))
    index = min(int(order//3), len(suffixes)-1)
    suffix = suffixes[index]

    significand = x / (10**(3*(order//3)))
    rounded = float(f'{significand:.2g}')
    head = str(int(rounded) if rounded % 1 == 0 else rounded)

    return head + suffix

def percent_axis(ax=None, axis='x'):
    ax = (ax or plt.gca())
    axis = getattr(ax, f'{axis}axis')
    axis.set_major_formatter(FuncFormatter(lambda x, _: f'{x:.0%}')) 

def suffix_axis(ax=None, axis='x', prefix=''):
    ax = (ax or plt.gca())
    axis = getattr(ax, f'{axis}axis')

    magnitude = np.fabs(axis.get_ticklocs()).max()
    order = np.log10(max(abs(magnitude), 1))
    scale = 3*(order//3)

    suffixes = ('', 'k', 'm', 'bn', 'tn')
    index = int(np.clip(order//3, 0, len(suffixes)-1))
    suffix = suffixes[index]

    def formatter(x, pos):
        if x == 0:
            return f'{prefix}{x:.0f}'
        else:
            return f'{prefix}{x/10**scale:.0f}{suffix}'

    axis.set_major_formatter(FuncFormatter(formatter)) 
    
def save(name, fig=None):
    if set('./') & set(name):
        path = Path(name)
    else:
        path = Path(f'./output/plots/{name}.png')
    path.parent.mkdir(exist_ok=True, parents=True)

    fig = (fig or plt.gcf())
    fig.savefig(path, bbox_inches='tight')

def array(fig=None):
    fig = (fig or plt.gcf())
    fig.canvas.draw()
    data = np.frombuffer(fig.canvas.tostring_rgb(), dtype=np.uint8)
    data = data.reshape(fig.canvas.get_width_height()[::-1] + (3,))
