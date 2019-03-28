import pandas as pd
import numpy as np

class dotdict(dict):
    
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__
    
    def __dir__(self):
        return sorted(set(super().__dir__() + list(self.keys())))

    def __getattr__(self, k):
        if k in self:
            return self[k]
        raise KeyError(k)
    
    def __str__(self):
        key_length = max(map(len, map(str, self.keys()))) if self.keys() else 0
        max_spaces = 4 + key_length
        val_length = 119 - max_spaces
        
        d = {}
        for k, v in self.items():
            rep = repr(v)
            has_short_repr = (len(rep.splitlines()) == 1) and (len(rep) < val_length)
            if has_short_repr:
                d[k] = repr(v)
            elif type(v) in (pd.Series, pd.DataFrame, pd.Panel, np.ndarray):                    
                d[k] = f'{v.shape}-{type(v).__name__}'
            elif type(v) in (list, set, dict):
                d[k] = f'({len(v)},)-{type(v).__name__}'
            elif type(v) in (dotdict,):
                d[k] = str(v)
            elif repr(v):
                d[k] = f'{repr(v).splitlines()[0][:val_length]} ...'
            else:
                d[k] = f'{type(v).__name__}()'

        s = []
        for k, v in d.items():
            lines = v.splitlines() or ['']
            s.append(str(k) + ' '*(max_spaces - len(k)) + lines[0])
            for l in lines[1:]:
                s.append(' '*max_spaces + l)
            if len(lines) > 1:
                s.append('\n')

        return '\n'.join(s)
    
    def __repr__(self):
        return self.__str__()

    def __getstate__(self):
        return self

    def __setstate__(self, state):
        self.update(state)
    
    def copy(self):
        return dotdict(super().copy()) 
    
    def pipe(self, f, *args, **kwargs):
        return f(self, *args, **kwargs)

