
import tkinter as tk
from tkinter import ttk
from ivy_app.database import Customer, Session

class CreateCustomerApp(ttk.Frame):
    title = "Kunden erstellen"

    def __init__(self, parent, *args):
        super().__init__(parent)

        self.session = Session()

        self.create_widgets()

    def create_widgets(self):
        ttk.Label(self, text="Name:").grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)
        self.name_entry = ttk.Entry(self)
        self.name_entry.grid(row=0, column=1, padx=10, pady=10, sticky=tk.W)

        ttk.Label(self, text="Telefon:").grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)
        self.phone_entry = ttk.Entry(self)
        self.phone_entry.grid(row=1, column=1, padx=10, pady=10, sticky=tk.W)

        ttk.Label(self, text="E-Mail:").grid(row=2, column=0, padx=10, pady=10, sticky=tk.W)
        self.email_entry = ttk.Entry(self)
        self.email_entry.grid(row=2, column=1, padx=10, pady=10, sticky=tk.W)

        self.save_button = ttk.Button(self, text="Kunde speichern", command=self.save_customer)
        self.save_button.grid(row=3, columnspan=2, pady=10)

    def save_customer(self):
        name = self.name_entry.get()
        phone = self.phone_entry.get()
        email = self.email_entry.get()

        customer = Customer(name=name, phone=phone, email=email)
        self.session.add(customer)
        self.session.commit()

        self.name_entry.delete(0, tk.END)
        self.phone_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)

        ttk.Label(self, text="Kunde erfolgreich gespeichert!", foreground="green").grid(row=4, columnspan=2, pady=10)
