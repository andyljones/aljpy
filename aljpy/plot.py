import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

def percent_axis(ax=None, axis='x'):
    ax = (ax or plt.gca())
    axis = getattr(ax, f'{axis}axis')
    axis.set_major_formatter(FuncFormatter(lambda x, _: f'{x:.0%}')) 

def suffix_axis(ax=None, axis='x'):
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
            return f'{x}'
        else:
            return f'{x/10**scale}{suffix}'

    axis.set_major_formatter(FuncFormatter(formatter)) 
    