import ctypes
import inspect

def extract(source=None):
    """Copies the variables of the caller up to iPython. Useful for debugging.
    
    .. code-block:: python
    
        def f():
            x = 'hello world'
            extract()
        
        f() # raises an error
    
        print(x) # prints 'hello world'
        
    """
    import inspect
    import ctypes 
    
    if source is None:
        frames = inspect.stack()
        caller = frames[1].frame
        name, ls, gs = caller.f_code.co_name, caller.f_locals, caller.f_globals
    elif hasattr(source, '__func__'):
        func = source.__func__
        name, ls, gs = func.__qualname__, (func.__closure__ or {}), func.__globals__
    elif hasattr(source, '__init__'):
        func = source.__init__.__func__
        name, ls, gs = func.__qualname__, (func.__closure__ or {}), func.__globals__
    else:
        raise ValueError(f'Don\'t support source {source}')

    ipython = [f for f in inspect.stack() if f.filename.startswith('<ipython-input')][-1].frame
    
    ipython.f_locals.update({k: v for k, v in gs.items() if k[:2] != '__'})
    ipython.f_locals.update({k: v for k, v in ls.items() if k[:2] != '__'})
    
    # Magic call to make the updates to f_locals 'stick'.
    # More info: http://pydev.blogspot.co.uk/2014/02/changing-locals-of-frame-frameflocals.html
    ctypes.pythonapi.PyFrame_LocalsToFast(ctypes.py_object(ipython), ctypes.c_int(0))
    
    message = 'Copied {}\'s variables to {}'.format(name, ipython.f_code.co_name)
    raise RuntimeError(message)