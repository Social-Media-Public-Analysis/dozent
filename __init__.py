from .dozent import Dozent
from .catch_thread_exceptions import install as _catch_thread_exceptions

_catch_thread_exceptions()

__all__ = ['Dozent', ]
