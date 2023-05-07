import tkinter as tk
from tkinter import ttk
from apps.adress_book.database_contact import ContactDatabase


class ContactApp(ttk.Frame):
    title = "Kontakt-App"

    def __init__(self, parent, *args):
        super().__init__(parent)

        self.contact_db_instance = ContactDatabase()

        self.create_widgets()

    def create_widgets(self):
        # Name
        self.name_label = ttk.Label(self, text="Name:")
        self.name_label.grid(row=0, column=0, padx=(10, 5), pady=10, sticky="w")
        self.name_entry = ttk.Entry(self)
        self.name_entry.grid(row=0, column=1, padx=(5, 10), pady=10, sticky="ew")

        # Vorname
        self.firstname_label = ttk.Label(self, text="Vorname:")
        self.firstname_label.grid(row=1, column=0, padx=(10, 5), pady=10, sticky="w")
        self.firstname_entry = ttk.Entry(self)
        self.firstname_entry.grid(row=1, column=1, padx=(5, 10), pady=10, sticky="ew")

        # Telefonnummer
        self.phone_number_label = ttk.Label(self, text="Telefonnummer:")
        self.phone_number_label.grid(row=2, column=0, padx=(10, 5), pady=10, sticky="w")
        self.phone_number_entry = ttk.Entry(self)
        self.phone_number_entry.grid(
            row=2, column=1, padx=(5, 10), pady=10, sticky="ew"
        )

        # Speichern-Button
        self.save_button = ttk.Button(self, text="Speichern", command=self.save_contact)
        self.save_button.grid(row=3, column=0, columnspan=2, pady=(10, 20))

        # Status-Label
        self.status_label = ttk.Label(self, text="")
        self.status_label.grid(
            row=4, column=0, columnspan=2, padx=10, pady=(0, 10), sticky="w"
        )

    def save_contact(self):
        name = self.name_entry.get()
        firstname = self.firstname_entry.get()
        phone_number = self.phone_number_entry.get()

        if name and firstname and phone_number:
            self.contact_db_instance.add_contact(name, firstname, phone_number)

            # Leeren Sie die Eingabefelder
            self.name_entry.delete(0, tk.END)
            self.firstname_entry.delete(0, tk.END)
            self.phone_number_entry.delete(0, tk.END)

            # Zeige, dass die Daten gespeichert wurden
            self.status_label.config(text="Kontakt gespeichert.", foreground="green")
        else:
            self.status_label.config(
                text="Bitte füllen Sie alle Felder aus.", foreground="red"
            )
