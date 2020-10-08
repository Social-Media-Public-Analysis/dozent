from .dozent import Dozent
from .catch_thread_exceptions import install as _catch_thread_exceptions

_catch_thread_exceptions()
from .command_line_utils import text_renderer

__all__ = ['Dozent', 'text_renderer']
