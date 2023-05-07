import tkinter as tk
from tkinter import ttk
from apps.ivy_erp.database_customer import CustomerDatabase


class CreateCustomerApp(ttk.Frame):
    title = "Kunden erstellen"

    def __init__(self, parent, *args):
        super().__init__(parent)

        self.customer_db_instance = CustomerDatabase()

        self.create_widgets()

    def create_widgets(self):
        # Name
        self.name_label = ttk.Label(self, text="Name:")
        self.name_label.grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)
        self.name_entry = ttk.Entry(self)
        self.name_entry.grid(row=0, column=1, padx=10, pady=10, sticky=tk.W)

        # Telefonnummer
        self.phone_label = ttk.Label(self, text="Telefon:")
        self.phone_label.grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)
        self.phone_entry = ttk.Entry(self)
        self.phone_entry.grid(row=1, column=1, padx=10, pady=10, sticky=tk.W)

        # Email
        self.email_label = ttk.Label(self, text="E-Mail:")
        self.email_label.grid(row=2, column=0, padx=10, pady=10, sticky=tk.W)
        self.email_entry = ttk.Entry(self)
        self.email_entry.grid(row=2, column=1, padx=10, pady=10, sticky=tk.W)

        # Speichern-Button
        self.save_button = ttk.Button(
            self, text="Kunde speichern", command=self.save_customer
        )
        self.save_button.grid(row=3, columnspan=2, pady=10)

        # Status-Label
        self.status_label = ttk.Label(self, text="")
        self.status_label.grid(
            row=4, column=0, columnspan=2, padx=10, pady=(0, 10), sticky="w"
        )

    def save_customer(self):
        name = self.name_entry.get()
        phone = self.phone_entry.get()
        email = self.email_entry.get()

        if name and phone and email:
            self.customer_db_instance.add_customer(name, phone, email)

            self.name_entry.delete(0, tk.END)
            self.phone_entry.delete(0, tk.END)
            self.email_entry.delete(0, tk.END)

            # Zeige, dass die Daten gespeichert wurden
            self.status_label.config(text="Kunde gespeichert.", foreground="green")
        else:
            self.status_label.config(
                text="Bitte füllen Sie alle Felder aus.", foreground="red"
            )
