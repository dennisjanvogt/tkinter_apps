from ivy_app.database_tables import Order, Session


class OrderDatabase:
    def __init__(self):
        self.session = Session()
