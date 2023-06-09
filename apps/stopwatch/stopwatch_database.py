from .database_tables import Stopwatches, Entrys, Projekte, Session_Stopwatch
from sqlalchemy.orm.exc import NoResultFound


class StopwatchDB:
    def __init__(self):
        self.session = Session_Stopwatch()

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()

    def close(self):
        self.session.close()


class StopwatchTable(StopwatchDB):
    def add_stopwatch(self, stopwatch_data):
        new_stopwatch = Stopwatches(
            project_id=stopwatch_data["project_id"],
            first_start_time=stopwatch_data["first_start_time"],
            latest_start_time=stopwatch_data["latest_start_time"],
            state=stopwatch_data["state"],
            actual_time=stopwatch_data["actual_time"],
            note=stopwatch_data["note"],
        )
        self.session.add(new_stopwatch)
        self.session.commit()
        return new_stopwatch.id

    def get_stopwatch(self, id):
        return self.session.query(Stopwatches).filter_by(id=id).one()

    def get_all_stopwatches(self):
        return self.session.query(Stopwatches).all()

    def update_stopwatch(self, id, **kwargs):
        stopwatch = self.get_stopwatch(id)
        for key, value in kwargs.items():
            setattr(stopwatch, key, value)
        self.session.commit()

    def delete_stopwatch(self, id):
        stopwatch = self.get_stopwatch(id)
        self.session.delete(stopwatch)
        self.session.commit()


class EntryTable(StopwatchDB):
    def add_entry(self, project_id, time, first_start_time, note=""):
        entry = Entrys(
            project_id=project_id,
            time=time,
            first_start_time=first_start_time,
            note=note,
        )
        self.session.add(entry)
        self.session.commit()
        return entry

    def get_entry(self, id):
        return self.session.query(Entrys).filter_by(id=id).one()

    def get_all_entries(self):
        return self.session.query(Entrys).all()

    def update_entry(self, id, **kwargs):
        entry = self.get_entry(id)
        for key, value in kwargs.items():
            setattr(entry, key, value)
        self.session.commit()

    def delete_entry(self, id):
        entry = self.get_entry(id)
        self.session.delete(entry)
        self.session.commit()


class ProjectTable(StopwatchDB):
    def add_project(self, project_data):
        new_project = Projekte(
            name=project_data["name"],
            description=project_data["description"],
        )
        self.session.add(new_project)
        self.session.commit()

    def get_project(self, id):
        return self.session.query(Projekte).filter_by(id=id).one()

    def get_all_projects(self):
        return self.session.query(Projekte).all()

    def update_project(self, id, **kwargs):
        project = self.get_project(id)
        for key, value in kwargs.items():
            setattr(project, key, value)
        self.session.commit()

    def delete_project(self, id):
        project = self.get_project(id)
        self.session.delete(project)
        self.session.commit()

    def get_project_by_name(self, name):
        try:
            return self.session.query(Projekte).filter_by(name=name).one()
        except NoResultFound:
            return None

    def get_project_id_by_name(self, project_name):
        return self.session.query(Projekte).filter_by(name=project_name).one().id
