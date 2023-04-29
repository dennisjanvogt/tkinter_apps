import tkinter as tk
from tkinter import ttk
from ivy_app.autocomplete_combobox import AutocompleteCombobox
from ivy_app.database import Order, Customer, Product, Session
import re

class CreateOrderApp(ttk.Frame):
    title = "Bestellung erstellen"

    def __init__(self, parent, *args):
        super().__init__(parent)

        self.session = Session()
        
        self.customers = self.session.query(Customer).all()
        self.products = self.session.query(Product).all()
        self.customer_names = [c.name for c in self.customers]
        self.product_names = [p.name for p in self.products]

        self.create_widgets()

    def create_widgets(self):
        ttk.Label(self, text="Kunde:").grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)
        self.customer_entry = AutocompleteCombobox(self, self.customer_names)
        self.customer_entry.grid(row=0, column=1, padx=10, pady=10, sticky=tk.W)

        ttk.Label(self, text="Produkt:").grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)
        self.product_entry = AutocompleteCombobox(self, self.product_names)
        self.product_entry.grid(row=1, column=1, padx=10, pady=10, sticky=tk.W)

        ttk.Label(self, text="Status:").grid(row=2, column=0, padx=10, pady=10, sticky=tk.W)
        self.status_combobox = ttk.Combobox(self, values=["Pending", "Out for delivery", "Delivered"])
        self.status_combobox.grid(row=2, column=1, padx=10, pady=10, sticky=tk.W)

        ttk.Label(self, text="Anmerkung:").grid(row=3, column=0, padx=10, pady=10, sticky=tk.W)
        self.note_entry = ttk.Entry(self)
        self.note_entry.grid(row=3, column=1, padx=10, pady=10, sticky=tk.W)

        self.save_button = ttk.Button(self, text="Bestellung speichern", command=self.save_order)
        self.save_button.grid(row=4, columnspan=2, pady=10)


    def save_order(self):
        customer_name = self.customer_entry.get()
        product_name = self.product_entry.get()
        status = self.status_combobox.get()
        note = self.note_entry.get()

        customer = self.session.query(Customer).filter(Customer.name == customer_name).first()
        product = self.session.query(Product).filter(Product.name == product_name).first()

        if customer and product:
            order = Order(customer_id=customer.id, product_id=product.id, status=status, note=note)
            self.session.add(order)
            self.session.commit()
            self.customer_entry.delete(0, tk.END)
            self.product_entry.delete(0, tk.END)
            self.status_combobox.set('')
            self.note_entry.delete(0, tk.END)

            ttk.Label(self, text="Bestellung erfolgreich gespeichert!", foreground="green").grid(row=5, columnspan=2, pady=10)
        else:
            ttk.Label(self, text="Kunde oder Produkt nicht gefunden. Bitte überprüfen Sie Ihre Eingabe.", foreground="red").grid(row=5, columnspan=2, pady=10)
