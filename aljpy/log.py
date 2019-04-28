import sys
import inspect
import logging
from contextlib import contextmanager

logging.basicConfig(
            stream=sys.stdout, 
            level=logging.INFO, 
            format='%(asctime)s %(levelname)s %(name)s: %(message)s', 
            datefmt=r'%Y-%m-%d %H:%M:%S')
logging.getLogger('parso').setLevel('WARN')  # Jupyter's autocomplete spams the output if this isn't set

def logger(**kwargs):
    """A logger named after the module it's called in."""
    caller = inspect.stack()[1]
    name = caller.frame.f_globals.get('__name__', 'UNKNOWN')
    return logging.getLogger(name, **kwargs)

loggers = {}
def modulelogger(method):
    #TODO: Holy hell, the stack inspection here is much slower than I expected

    def g(*args, **kwargs):
        caller = inspect.stack()[1]
        name = caller.frame.f_globals.get('__name__', 'UNKNOWN')
        log = loggers.setdefault(name, logging.getLogger(name)) 
        return getattr(log, method)(*args, **kwargs)

    return g

@contextmanager
def suppress(name):
    try:
        logger = logging.getLogger(name)
        level = logger.getEffectiveLevel()
        logger.setLevel('ERROR')
        yield
    finally:
        logger.setLevel(level)

debug = modulelogger('debug')
info = modulelogger('info')
warn = modulelogger('warn')
error = modulelogger('error')
exception = modulelogger('exception')