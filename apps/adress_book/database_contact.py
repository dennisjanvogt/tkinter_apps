from apps.adress_book.database_tables import Contact, Session


class ContactDatabase:
    def __init__(self):
        self.session = Session()

    def add_contact(self, name, firstname, phone_number):
        contact = Contact(name=name, firstname=firstname, phone_number=phone_number)
        self.session.add(contact)
        self.session.commit()

    def get_all_contacts(self):
        return self.session.query(Contact).all()

    def update_contact(self, contact_id, name=None, firstname=None, phone_number=None):
        contact = self.session.query(Contact).get(contact_id)
        if name:
            contact.name = name
        if firstname:
            contact.firstname = firstname
        if phone_number:
            contact.phone_number = phone_number
        self.session.commit()

    def delete_contact(self, contact_id):
        contact = self.session.query(Contact).get(contact_id)
        self.session.delete(contact)
        self.session.commit()

    def close(self):
        self.session.close()
