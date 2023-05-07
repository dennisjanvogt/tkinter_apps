import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

from apps.adress_book.database_contact import ContactDatabase
from apps.adress_book.edit_contact_dialog import EditContactDialog


class ViewContactApp(ttk.Frame):
    title = "Kontakte anzeigen"

    def __init__(self, parent, *args):
        super().__init__(parent)

        self.address_book = ContactDatabase()

        self.contacts_tree = ttk.Treeview(
            self, columns=("Name", "Vorname", "Telefonnummer"), show="headings"
        )
        self.contacts_tree.heading("Name", text="Name")
        self.contacts_tree.heading("Vorname", text="Vorname")
        self.contacts_tree.heading("Telefonnummer", text="Telefonnummer")
        self.contacts_tree.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)
        self.load_contacts()

        self.contacts_tree.bind(
            "<Double-1>", self.on_double_click
        )  # Doppelklick-Funktion hinzufügen

        edit_button = ttk.Button(
            self, text="Kontakt bearbeiten", command=self.edit_contact
        )
        edit_button.pack(side=tk.LEFT, padx=(10, 5), pady=(0, 10))

        delete_button = ttk.Button(
            self, text="Kontakt löschen", command=self.delete_contact
        )
        delete_button.pack(side=tk.RIGHT, padx=(5, 10), pady=(0, 10))

    def load_contacts(self):
        for i in self.contacts_tree.get_children():
            self.contacts_tree.delete(i)

        for contact in self.address_book.get_all_contacts():
            self.contacts_tree.insert(
                "",
                tk.END,
                iid=contact.id,
                values=(contact.name, contact.firstname, contact.phone_number),
            )

    def edit_contact(self):
        contact_id = self.contacts_tree.selection()[0]
        contact = self.contacts_tree.item(contact_id)

        name, firstname, phone_number = contact["values"]
        edit_dialog = EditContactDialog(self, contact_id, name, firstname, phone_number)
        self.wait_window(
            edit_dialog
        )  # Warten, bis das Bearbeitungsdialogfenster geschlossen wird
        self.load_contacts()  # Kontaktliste aktualisieren

    def delete_contact(self):
        contact_id = self.contacts_tree.selection()[0]

        response = messagebox.askyesno(
            title="Kontakt löschen",
            message="Möchten Sie diesen Kontakt wirklich löschen?",
        )
        if response:
            self.address_book.delete_contact(contact_id)
            self.contacts_tree.delete(contact_id)

    def on_double_click(self, event):
        self.edit_contact()
