import time
import tkinter as tk
from datetime import datetime
from .stopwatch_database import StopwatchTable, EntryTable


class Stopwatch:
    def __init__(
        self,
        id,
        project_id,
        state,
        first_start_time=None,
        latest_start_time=None,
        actual_time=0.0,
        note=None,
    ):
        self.id = id
        self.project_id = project_id
        self.state = state
        self.first_start_time = first_start_time
        self.latest_start_time = latest_start_time
        self.actual_time = actual_time
        self.note = note
        self.stopwatchtable_instance = StopwatchTable()

    def toggle(self):
        if self.state == "paused":
            if self.first_start_time is None:
                self.first_start_time = datetime.now()
                self.stopwatchtable_instance.update_stopwatch(
                    self.id, first_start_time=datetime.now()
                )

            self.latest_start_time = time.time()
            self.state = "running"
            self.stopwatchtable_instance.update_stopwatch(
                self.id, state="running", latest_start_time=time.time()
            )
        else:
            self.actual_time = self.actual_time + time.time() - self.latest_start_time
            self.state = "paused"
            self.stopwatchtable_instance.update_stopwatch(
                self.id, state="paused", latest_start_time=None, actual_time = self.actual_time
            )

    def reset(self):
        self.actual_time = 0.0
        self.first_start_time = None
        self.latest_start_time = None
        self.state = "paused"
        self.stopwatchtable_instance.update_stopwatch(
                self.id, state="paused", latest_start_time=None, actual_time = 0.0,
        first_start_time = None
            )

    def elapsed_time(self):
        if self.state == "running":
            return self.actual_time + time.time() - self.latest_start_time
        return 0

    def save_time(self, note=""):
        if self.latest_start_time is not None:
            entry_table = EntryTable()
            entry_table.add_entry(
                project_id=self.project_id,
                time=self.get_elapsed_time_str(),
                first_start_time=self.first_start_time,
                note=note.get(),
            )
            note.set("")
            self.reset()
            return True

    def remove(self):
        self.stopwatchtable_instance.delete_stopwatch(self.id)

    def get_elapsed_time_str(self):
        if self.state == "running":
            if self.latest_start_time == None:
                elapsed_time = self.actual_time
            else:
                elapsed_time = self.actual_time + time.time() - self.latest_start_time
        elif self.state == "paused":
            if self.first_start_time is None:
                elapsed_time = 0.0
            else:
                elapsed_time = self.actual_time
        else:
            raise ValueError(f"Ungültiger Stoppuhrzustand: {self.state}")

        elapsed_time_str = time.strftime("%H:%M:%S", time.gmtime(elapsed_time))
        return elapsed_time_str
