from tkinter import ttk
import tkinter as tk


class EditOrderDialog(tk.Toplevel):
    def __init__(self, parent, order_id, customer_id, product_id, status, note):
        super().__init__(parent)

        self.order_id = order_id
        self.title("Bestellung bearbeiten")
        self.geometry("400x300")

        ttk.Label(self, text="Kunden-ID:").grid(
            row=0, column=0, padx=10, pady=10, sticky=tk.W
        )
        self.customer_id_entry = ttk.Entry(self)
        self.customer_id_entry.insert(0, customer_id)
        self.customer_id_entry.grid(row=0, column=1, padx=10, pady=10, sticky=tk.W)

        ttk.Label(self, text="Produkt-ID:").grid(
            row=1, column=0, padx=10, pady=10, sticky=tk.W
        )
        self.product_id_entry = ttk.Entry(self)
        self.product_id_entry.insert(0, product_id)
        self.product_id_entry.grid(row=1, column=1, padx=10, pady=10, sticky=tk.W)

        ttk.Label(self, text="Status:").grid(
            row=2, column=0, padx=10, pady=10, sticky=tk.W
        )
        self.status_entry = ttk.Entry(self)
        self.status_entry.insert(0, status)
        self.status_entry.grid(row=2, column=1, padx=10, pady=10, sticky=tk.W)

        ttk.Label(self, text="Notiz:").grid(
            row=3, column=0, padx=10, pady=10, sticky=tk.W
        )
        self.note_entry = ttk.Entry(self)
        self.note_entry.insert(0, note)
        self.note_entry.grid(row=3, column=1, padx=10, pady=10, sticky=tk.W)

        save_button = ttk.Button(self, text="Speichern", command=self.save_order)
        save_button.grid(row=4, columnspan=2, pady=10)

    def save_order(self):
        customer_id = self.customer_id_entry.get()
        product_id = self.product_id_entry.get()
        status = self.status_entry.get()
        note = self.note_entry.get()

        self.master.order_app.update_order(
            self.order_id, customer_id, product_id, status, note
        )
        self.master.load_orders()
        self.destroy()
