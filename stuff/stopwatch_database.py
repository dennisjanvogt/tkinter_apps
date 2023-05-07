import sqlite3


class StopWatchDatabase:
    def create_database(self):
        conn = sqlite3.connect("stopwatch_data.db")
        c = conn.cursor()
        c.execute(
            """CREATE TABLE IF NOT EXISTS stopwatch_data
                (id INTEGER PRIMARY KEY,
                project_id INTEGER,
                elapsed_time REAL,
                first_start INTEGER,
                FOREIGN KEY(project_id) REFERENCES projekte(id))"""
        )
        c.execute(
            """CREATE TABLE IF NOT EXISTS stopwatch_data
                    (id INTEGER PRIMARY KEY, description TEXT, elapsed_time REAL, first_start REAL, project_id INTEGER, 
                    FOREIGN KEY (project_id) REFERENCES projekte (id) ON DELETE CASCADE)"""
        )
        conn.commit()
        conn.close()

    def load_projects(self, projekte: list):
        conn = sqlite3.connect("stopwatch_data.db")
        c = conn.cursor()
        c.execute("SELECT * FROM projekte")
        rows = c.fetchall()
        for row in rows:
            projekte.append(row[1])
        conn.close()
