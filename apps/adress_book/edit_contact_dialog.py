from tkinter import ttk
import tkinter as tk


class EditContactDialog(tk.Toplevel):
    def __init__(self, parent, contact_id, name, firstname, phone_number):
        super().__init__(parent)

        self.contact_id = contact_id
        self.title("Kontakt bearbeiten")
        self.geometry("400x200")

        ttk.Label(self, text="Name:").grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)
        self.name_entry = ttk.Entry(self)
        self.name_entry.insert(0, name)
        self.name_entry.grid(row=0, column=1, padx=10, pady=10, sticky=tk.W)

        ttk.Label(self, text="Vorname:").grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)
        self.firstname_entry = ttk.Entry(self)
        self.firstname_entry.insert(0, firstname)
        self.firstname_entry.grid(row=1, column=1, padx=10, pady=10, sticky=tk.W)

        ttk.Label(self, text="Telefonnummer:").grid(row=2, column=0, padx=10, pady=10, sticky=tk.W)
        self.phone_number_entry = ttk.Entry(self)
        self.phone_number_entry.insert(0, phone_number)
        self.phone_number_entry.grid(row=2, column=1, padx=10, pady=10, sticky=tk.W)

        save_button = ttk.Button(self, text="Speichern", command=self.save_contact)
        save_button.grid(row=3, columnspan=2, pady=10)

    def save_contact(self):
        name = self.name_entry.get()
        firstname = self.firstname_entry.get()
        phone_number = self.phone_number_entry.get()

        self.master.address_book.update_contact(self.contact_id, name, firstname, phone_number)
        self.master.load_contacts()
        self.destroy()