from .production_settings import *

try:
    from .local_dev_settings import *
except ImportError:
    pass
