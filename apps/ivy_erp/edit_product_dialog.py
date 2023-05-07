from tkinter import ttk
import tkinter as tk


class EditProductDialog(tk.Toplevel):
    def init(self, parent, product_id, name, description, price):
        super().init(parent)

        self.product_id = product_id
        self.title("Produkt bearbeiten")
        self.geometry("400x250")

        ttk.Label(self, text="Name:").grid(
            row=0, column=0, padx=10, pady=10, sticky=tk.W
        )
        self.name_entry = ttk.Entry(self)
        self.name_entry.insert(0, name)
        self.name_entry.grid(row=0, column=1, padx=10, pady=10, sticky=tk.W)

        ttk.Label(self, text="Beschreibung:").grid(
            row=1, column=0, padx=10, pady=10, sticky=tk.W
        )
        self.description_entry = ttk.Entry(self)
        self.description_entry.insert(0, description)
        self.description_entry.grid(row=1, column=1, padx=10, pady=10, sticky=tk.W)

        ttk.Label(self, text="Preis:").grid(
            row=2, column=0, padx=10, pady=10, sticky=tk.W
        )
        self.price_entry = ttk.Entry(self)
        self.price_entry.insert(0, price)
        self.price_entry.grid(row=2, column=1, padx=10, pady=10, sticky=tk.W)

        save_button = ttk.Button(self, text="Speichern", command=self.save_product)
        save_button.grid(row=3, columnspan=2, pady=10)

    def save_product(self):
        name = self.name_entry.get()
        description = self.description_entry.get()
        price = self.price_entry.get()

        self.master.product_app.update_product(
            self.product_id, name, description, price
        )
        self.master.load_products()
        self.destroy()
