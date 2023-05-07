import tkinter as tk
from tkinter import ttk
from helpers.autocomplete_combobox import AutocompleteCombobox
from apps.ivy_erp.database_tables import Order, Customer, Product, Session
import re


class CreateOrderApp(ttk.Frame):
    title = "Bestellung erstellen"

    def __init__(self, parent, *args):
        super().__init__(parent)

        self.session = Session()

        self.customers = self.session.query(Customer).all()
        self.customer_names = [c.name for c in self.customers]

        self.products = self.session.query(Product).all()
        self.product_names = [p.name for p in self.products]

        self.create_widgets()

    def create_widgets(self):
        self.kunde_lable = ttk.Label(self, text="Kunde:")
        self.kunde_lable.grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)
        self.customer_entry = AutocompleteCombobox(self, self.customer_names)
        self.customer_entry.grid(row=0, column=1, padx=10, pady=10, sticky=tk.W)

        self.produkt_lable = ttk.Label(self, text="Produkt:")
        self.produkt_lable.grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)
        self.product_entry = AutocompleteCombobox(self, self.product_names)
        self.product_entry.grid(row=1, column=1, padx=10, pady=10, sticky=tk.W)

        self.status_lable = ttk.Label(self, text="Status:")
        self.status_lable.grid(row=2, column=0, padx=10, pady=10, sticky=tk.W)
        self.status_combobox = ttk.Combobox(
            self, values=["Pending", "Out for delivery", "Delivered"]
        )
        self.status_combobox.grid(row=2, column=1, padx=10, pady=10, sticky=tk.W)

        self.anmerkung_lable = ttk.Label(self, text="Anmerkung:")
        self.anmerkung_lable.grid(row=3, column=0, padx=10, pady=10, sticky=tk.W)
        self.note_entry = ttk.Entry(self)
        self.note_entry.grid(row=3, column=1, padx=10, pady=10, sticky=tk.W)

        self.save_button = ttk.Button(
            self, text="Bestellung speichern", command=self.save_order
        )
        self.save_button.grid(row=4, columnspan=2, pady=10)

        # Status-Label
        self.state_label = ttk.Label(self, text="")
        self.state_label.grid(
            row=5, column=0, columnspan=2, padx=10, pady=(0, 10), sticky="w"
        )

    def save_order(self):
        customer_name = self.customer_entry.get()
        product_name = self.product_entry.get()
        status = self.status_combobox.get()
        note = self.note_entry.get()

        customer = (
            self.session.query(Customer).filter(Customer.name == customer_name).first()
        )
        product = (
            self.session.query(Product).filter(Product.name == product_name).first()
        )

        if customer and product:
            order = Order(
                customer_id=customer.id, product_id=product.id, status=status, note=note
            )
            self.session.add(order)
            self.session.commit()
            self.customer_entry.delete(0, tk.END)
            self.product_entry.delete(0, tk.END)
            self.status_combobox.set("")
            self.note_entry.delete(0, tk.END)

            self.state_label.config(text="Bestellung gespeichert.", foreground="green")
        else:
            self.state_label.config(
                text="Bitte füllen Sie alle Felder aus.", foreground="red"
            )
