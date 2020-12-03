import unittest

from typing import Tuple
import time

from dozent.progress_tracker import ProgressTracker, Task


class ProgressTrackerTestCase(unittest.TestCase):
    def sync_tracker(self, tracker: ProgressTracker):
        time.sleep(.01)
        with tracker.lock:
            pass

    def setUp(self):
        self.progress = []

    def progress_callback(self, i: int = None) -> Tuple[float, str, str]:
        progress = 0 if i is None else self.progress[i]
        prefix = f"{i}:"
        suffix = ''
        return progress, prefix, suffix

    def test_register_task(self):
        tracker = ProgressTracker()
        self.assertEqual(len(tracker.tasks), 0)

        for new_id in range(20):
            task_id = tracker.register_task(f'{new_id}', self.progress_callback)
            self.assertEqual(task_id, new_id)
            self.sync_tracker(tracker)

            self.assertEqual(len(tracker.tasks), new_id + 1)
            self.assertEqual(tracker.tasks_pending, True)
            self.assertEqual(tracker.tasks[task_id], Task(id=task_id,
                                                          progress_callback=self.progress_callback,
                                                          progress=0,
                                                          prefix=None,
                                                          suffix=None,
                                                          line_length=0))

    def test_update_task_progress(self):
        tracker = ProgressTracker()

        callbacks = [(lambda task_id: lambda: self.progress_callback(task_id))(i) for i in range(20)]
        for task_id in range(20):
            tracker.register_task(f'{task_id}', callbacks[task_id])
            self.sync_tracker(tracker)

        for task_id in range(20):
            self.progress.append(task_id)
            tracker._update_task_progress(task_id, draw=False)
            self.assertEqual(tracker.tasks[task_id], Task(id=task_id,
                                                          progress_callback=callbacks[task_id],
                                                          progress=task_id,
                                                          prefix=f"{task_id}:",
                                                          suffix='',
                                                          line_length=0))

        for task_id in reversed(range(20)):
            for i in range(101):
                self.progress[task_id] = i
                tracker._update_task_progress(task_id, draw=False)
                self.assertEqual(tracker.tasks[task_id], Task(id=task_id,
                                                              progress_callback=callbacks[task_id],
                                                              progress=i,
                                                              prefix=f"{task_id}:",
                                                              suffix='',
                                                              line_length=0))

        self.progress[0] = 101
        with self.assertRaises(AssertionError):
            tracker._update_task_progress(0, draw=False)

        self.progress[0] = -1
        with self.assertRaises(AssertionError):
            tracker._update_task_progress(0, draw=False)


if __name__ == "__main__":
    unittest.main()
