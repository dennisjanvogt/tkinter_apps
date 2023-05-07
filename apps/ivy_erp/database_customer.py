from apps.ivy_erp.database_tables import Customer, Session


class CustomerDatabase:
    def __init__(self):
        self.session = Session()

    def add_customer(self, name, phone, email):
        customer = Customer(name=name, phone=phone, email=email)
        self.session.add(customer)
        self.session.commit()

    def get_all_customers(self):
        return self.session.query(Customer).all()

    def update_customer(self, customer_id, name=None, phone=None, email=None):
        customer: Customer = self.session.query(Customer).get(customer_id)
        if name:
            customer.name = name
        if phone:
            customer.phone = phone
        if email:
            customer.email = email
        self.session.commit()

    def delete_customer(self, customer_id):
        customer = self.session.query(Customer).get(customer_id)
        self.session.delete(customer)
        self.session.commit()

    def close(self):
        self.session.close()
