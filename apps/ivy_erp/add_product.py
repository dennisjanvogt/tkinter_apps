# create_product_app.py
import tkinter as tk
from tkinter import ttk
from apps.ivy_erp.database_tables import Product, Session


class CreateProductApp(ttk.Frame):
    title = "Produkt erstellen"

    def __init__(self, parent, *args):
        super().__init__(parent)

        self.session = Session()

        self.create_widgets()

    def create_widgets(self):
        ttk.Label(self, text="Name:").grid(
            row=0, column=0, padx=10, pady=10, sticky=tk.W
        )
        self.name_entry = ttk.Entry(self)
        self.name_entry.grid(row=0, column=1, padx=10, pady=10, sticky=tk.W)

        ttk.Label(self, text="Preis:").grid(
            row=1, column=0, padx=10, pady=10, sticky=tk.W
        )
        self.price_entry = ttk.Entry(self)
        self.price_entry.grid(row=1, column=1, padx=10, pady=10, sticky=tk.W)

        ttk.Label(self, text="Kategorie:").grid(
            row=2, column=0, padx=10, pady=10, sticky=tk.W
        )
        self.category_entry = ttk.Entry(self)
        self.category_entry.grid(row=2, column=1, padx=10, pady=10, sticky=tk.W)

        ttk.Label(self, text="Beschreibung:").grid(
            row=3, column=0, padx=10, pady=10, sticky=tk.W
        )
        self.description_entry = ttk.Entry(self)
        self.description_entry.grid(row=3, column=1, padx=10, pady=10, sticky=tk.W)

        self.save_button = ttk.Button(
            self, text="Produkt speichern", command=self.save_product
        )
        self.save_button.grid(row=4, columnspan=2, pady=10)

        # Status-Label
        self.state_label = ttk.Label(self, text="")
        self.state_label.grid(
            row=5, column=0, columnspan=2, padx=10, pady=(0, 10), sticky="w"
        )

    def save_product(self):
        name = self.name_entry.get()
        price = self.price_entry.get()
        category = self.category_entry.get()
        description = self.description_entry.get()

        try:
            if name and price and category:
                product = Product(
                    name=name,
                    price=float(price),
                    category=category,
                    description=description,
                )
                self.session.add(product)
                self.session.commit()

                self.name_entry.delete(0, tk.END)
                self.price_entry.delete(0, tk.END)
                self.category_entry.delete(0, tk.END)
                self.description_entry.delete(0, tk.END)

                self.state_label.config(
                    text="Produkt erfolgreich gespeichert!", foreground="green"
                )

            else:
                self.state_label.config(
                    text="Bitte füllen Sie alle Felder aus.", foreground="red"
                )
        except ValueError:
            self.state_label.config(text="Preis muss eine Zahl sein.", foreground="red")
