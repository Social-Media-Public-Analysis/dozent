import threading
import sys
import traceback
import os
import signal

"""
usage: install()

Once installed, all exceptions caught from within threads will cause the program to end.
"""


def sendKillSignal(etype, value, tb):
    lines = traceback.format_exception(etype, value, tb)
    for line in lines:
        print(line, flush=True)

    os.kill(os.getpid(), signal.SIGTERM)


original_init = threading.Thread.__init__


def patched_init(self, *args, **kwargs):
    original_init(self, *args, **kwargs)
    original_run = self.run

    def patched_run(*args, **kw):
        try:
            original_run(*args, **kw)
        except Exception:
            sys.excepthook(*sys.exc_info())
    self.run = patched_run


def install():
    sys.excepthook = sendKillSignal
    threading.Thread.__init__ = patched_init
