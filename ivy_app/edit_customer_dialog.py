from tkinter import ttk
import tkinter as tk


class EditCustomerDialog(tk.Toplevel):
    def __init__(self, customer_app, customer_id, name, phone, email):
        super().__init__(customer_app)

        self.customer_app = customer_app
        self.customer_id = customer_id
        self.title("Kunde bearbeiten")
        self.geometry("400x200")

        ttk.Label(self, text="Name:").grid(
            row=0, column=0, padx=10, pady=10, sticky=tk.W
        )
        self.name_entry = ttk.Entry(self)
        self.name_entry.insert(0, name)
        self.name_entry.grid(row=0, column=1, padx=10, pady=10, sticky=tk.W)

        ttk.Label(self, text="Telefon:").grid(
            row=1, column=0, padx=10, pady=10, sticky=tk.W
        )
        self.phone_entry = ttk.Entry(self)
        self.phone_entry.insert(0, phone)
        self.phone_entry.grid(row=1, column=1, padx=10, pady=10, sticky=tk.W)

        ttk.Label(self, text="E-Mail:").grid(
            row=2, column=0, padx=10, pady=10, sticky=tk.W
        )
        self.email_entry = ttk.Entry(self)
        self.email_entry.insert(0, email)
        self.email_entry.grid(row=2, column=1, padx=10, pady=10, sticky=tk.W)

        save_button = ttk.Button(self, text="Speichern", command=self.save_customer)
        save_button.grid(row=3, columnspan=2, pady=10)

    def save_customer(self):
        name = self.name_entry.get()
        phone = self.phone_entry.get()
        email = self.email_entry.get()

        self.customer_app.update_customer(self.customer_id, name, phone, email)
        self.master.update_customer()
        self.destroy()
