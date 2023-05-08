import time
from datetime import datetime
from apps.stopwatch.stopwatch_database import StopwatchTable, EntryTable


class Stopwatch:
    def __init__(self, id, project_id, state, start_time=None, note=None):
        self.id = id
        self.project_id = project_id
        self.state = state
        self.start_time = start_time
        self.paused_time = 0.0  # Setzen Sie den Standardwert für "paused_time" auf 0.0
        self.note = note
        self.stopwatchtable_instance = StopwatchTable()

    def toggle(self):
        if self.state == "paused":
            if (
                self.start_time is None
            ):  # Wenn die Stoppuhr zum ersten Mal gestartet wird
                self.start_time = time.time()
                self.paused_time = self.start_time
                self._start_timestamp = time.time()
            else:
                self.start_time = time.time() - (self.paused_time - self.start_time)
            self.state = "running"
            self.stopwatchtable_instance.update_stopwatch(self.id, state="running")

        else:
            self.paused_time = (
                time.time()
            )  # Aktualisieren Sie das Attribut "paused_time"
            self.state = "paused"
            self.stopwatchtable_instance.update_stopwatch(self.id, state="running")

        return True

    def start(self):
        if self.state == "paused":
            self._start_timestamp = time.time()
            self.start_time = self.start_time or time.time()
            self.state = "running"
            self.stopwatchtable_instance.update_stopwatch(self.id, state="running")
            return True
        return False

    def pause(self):
        if self.state == "running":
            self.state = "paused"
            self.stopwatchtable_instance.update_stopwatch(self.id, state="paused")
            return True
        return False

    def reset(self):
        if self.state == "paused":
            self.start_time = None
            self._start_timestamp = None
            return True
        return False

    def elapsed_time(self):
        if self.state == "running":
            return time.time() - self._start_timestamp
        return 0

    def save_time(self, note=""):
        if self.state == "paused" and self.start_time is not None:
            entry_table = EntryTable()
            duration = time.time() - self.start_time
            entry_table.add_entry(
                stopwatch_id=self.id,
                project_id=self.project_id,
                time=duration,
                start_time=datetime.fromtimestamp(self._start_timestamp),
                note=note or self.note,
            )
            self.reset()
            return True
        return False

    def remove(self):
        self.stopwatchtable_instance.delete_stopwatch(self.id)

    def get_elapsed_time_str(self):
        if self.state == "running":
            elapsed_time = time.time() - self.start_time
        elif self.state == "paused":
            if self.start_time is None:
                elapsed_time = 0.0
            else:
                elapsed_time = self.paused_time - self.start_time
        else:
            raise ValueError(f"Ungültiger Stoppuhrzustand: {self.state}")

        elapsed_time_str = time.strftime("%H:%M:%S", time.gmtime(elapsed_time))
        return elapsed_time_str
