import sys
import os

import numpy as np
import threading
import shutil
import queue

from typing import Dict, Callable, Tuple
from collections import namedtuple

Task = namedtuple('Task', 'id progress_callback progress prefix suffix line_length')


class ProgressTracker(threading.Thread):
    """It is assumed that no other printing to stdout will occur while running this ProgressTracker thread.
    """

    def __init__(self):
        threading.Thread.__init__(self)

        self.tasks: Dict[int, Task] = {}
        self.message_queue = queue.Queue()
        self.sum_progress = 0
        self.next_task = 0

        self.terminal_size = None

        resized = self.refresh_terminal_size()
        assert(resized)  # This won't work if we couldn't read the terminal size

        self.lock = threading.Lock()
        self.tasks_pending = False
        self.running = True

    def refresh_terminal_size(self) -> bool:
        """
        Records any change in the terminal size.
        :returns: True if a change is detected, else False
        """

        old_size = self.terminal_size
        try:
            self.terminal_size = os.get_terminal_size()[0]
        except OSError:
            self.terminal_size = shutil.get_terminal_size()[0]

        return old_size != self.terminal_size

    def join(self):
        self.message_queue.join()
        self.stop()

    def stop(self):
        self.running = False
        self.update(0)

    def update(self, task_id: int):
        self.message_queue.put(task_id)

    def register_task(self, name: str, progress_callback: Callable[[], Tuple[float, str, str]]) -> int:
        """Register a new task with the given progress callback.

        :param name: A unique name for this task.
        :param progress_callback: A function, which will report a tuple of:
                                    a progress percentage in [0,100],
                                    a string prefix to be output before the progress bar,
                                    and a string suffix to be output after the progress bar.
        :return: The ID of the registered task.
        """

        task_id = self.next_task
        self.next_task += 1

        # Perform operation in helper function on own thread, so that this function does not block
        thread = threading.Thread(target=self._register_task_helper, args=(name, task_id, progress_callback))
        thread.daemon = True
        thread.start()

        return task_id

    def _register_task_helper(self, name: str, task_id: int, progress_callback: Callable[[], Tuple[float, str]]):
        with self.lock:
            # Create the task, with initial progress 0
            self.tasks[task_id] = (Task(id=task_id,
                                        progress_callback=progress_callback,
                                        progress=0,
                                        prefix=None,
                                        suffix=None,
                                        line_length=0))
            self.tasks_pending = True
            self._delete_progress_bars()
            print(f"Queueing tweet download {task_id}: {name}", flush=True)

    def _delete_progress_bars(self, starting_id: int = 0):
        if self.tasks:
            sys.stdout.write('\b' * (np.sum([self.tasks[i].line_length for i in range(starting_id, len(self.tasks))])))

    def _update_task_progress(self, task_id: int, draw: bool = True):
        """Update the progress bar for the given task

        :param task_id: Identifier of the task to update.
        :param draw: Whether to draw the updated progress bar, defaults to True
        """

        # Update the progress value
        task = self.tasks[task_id]
        assert(task.id == task_id)

        progress, prefix, suffix = task.progress_callback()
        assert(0 <= progress <= 100)

        self.sum_progress += progress - task.progress
        task = Task(id=task_id,
                    progress_callback=task.progress_callback,
                    progress=progress,
                    prefix=prefix,
                    suffix=suffix,
                    line_length=task.line_length)
        self.tasks[task_id] = task

        if draw:
            # Redraw all bars if the terminal size changes
            if self.refresh_terminal_size():
                task_id = 0

            # Return to start of the progress bar for task_id
            self._delete_progress_bars(starting_id=task_id)
            self._draw_task_progress(task_id)

    def _draw_task_progress(self, task_id: int):
        """Updates the progress bar for task_id and after.

        Assumes the console begins at the end of any previously drawn progress bars.
        """

        # We re-write the progress for all tasks, in order to finish at the end of all progress bars (our assumption)
        for task in [self.tasks[i] for i in range(task_id, len(self.tasks))]:
            if task.prefix is None or task.suffix is None:
                continue

            prefix = f"{task.id:3.0f}: "

            bar = ' '*len(prefix)
            bar_width = self.terminal_size - len(prefix) - 2
            assert(bar_width > 0)

            num_dashes = int(task.progress * bar_width / 100.0)
            bar += f"[{'-' * num_dashes}{' ' * (bar_width - num_dashes)}]"

            prefix += task.prefix[:int(self.terminal_size/2)]
            suffix = task.suffix[:int(self.terminal_size/3)]
            spaces = ' ' * (self.terminal_size - len(suffix) - len(prefix))

            line = f"{prefix}{spaces}{suffix}{bar}"

            assert(self.tasks[task.id] == task)
            self.tasks[task.id] = Task(id=task.id,
                                       progress_callback=task.progress_callback,
                                       progress=task.progress,
                                       prefix=task.prefix,
                                       suffix=task.suffix,
                                       line_length=len(line))

            sys.stdout.write(line)

        sys.stdout.flush()

    def _run_task(self):
        task_id = self.message_queue.get(True)

        try:
            with self.lock:
                if self.tasks_pending:
                    self._update_task_progress(0, draw=False)
                    self.tasks_pending = False

                else:
                    self._update_task_progress(task_id, draw=True)

        finally:
            self.message_queue.task_done()

    def run(self):
        while self.running:
            self._run_task()

        self._delete_progress_bars()
        print('')
