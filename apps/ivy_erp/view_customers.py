import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from apps.ivy_erp.database_tables import Customer, Order, Session
from apps.ivy_erp.edit_customer_dialog import EditCustomerDialog


class ViewCustomersApp(ttk.Frame):
    title = "Kunde anzeigen"

    def __init__(self, parent, *args):
        super().__init__(parent)

        self.session = Session()

        self.customer_tree = ttk.Treeview(
            self, columns=("Name", "Telefon", "E-Mail"), show="headings"
        )
        self.customer_tree.heading("Name", text="Name")
        self.customer_tree.heading("Telefon", text="Telefon")
        self.customer_tree.heading("E-Mail", text="E-Mail")
        self.customer_tree.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)
        self.load_customer()

        self.customer_tree.bind(
            "<Double-1>", self.on_double_click
        )  # Doppelklick-Funktion hinzufügen

        edit_button = ttk.Button(
            self, text="Kontakt bearbeiten", command=self.edit_contact
        )
        edit_button.pack(side=tk.LEFT, padx=(10, 5), pady=(0, 10))

        delete_button = ttk.Button(
            self, text="Kontakt löschen", command=self.delete_contact
        )
        delete_button.pack(side=tk.RIGHT, padx=(5, 10), pady=(0, 10))

    def load_customer(self):
        for i in self.customer_tree.get_children():
            self.customer_tree.delete(i)

        for customer in self.session.query(Customer).all():
            self.customer_tree.insert(
                "",
                tk.END,
                iid=customer.id,
                values=(customer.name, customer.phone, customer.email),
            )

    def edit_contact(self):
        customer_id = self.customer_tree.selection()[0]
        customer = self.customer_tree.item(customer_id)

        name, phone, email = customer["values"]
        edit_dialog = EditCustomerDialog(self, customer_id, name, phone, email)
        self.wait_window(edit_dialog)  # Wait until the edit dialog window is closed
        self.load_customer()  # Refresh the customer list

    def delete_contact(self):
        customer_id = self.customer_tree.selection()[0]

        response = messagebox.askyesno(
            title="Kontakt löschen",
            message="Möchten Sie diesen Kontakt wirklich löschen?",
        )
        if response:
            customer = (
                self.session.query(Customer).filter(Customer.id == customer_id).first()
            )

            self.session.query(Order).filter(Order.customer == customer).delete()

            customer = (
                self.session.query(Customer).filter(Customer.id == customer_id).delete()
            )
            self.session.commit()
            self.load_customer()

    def on_double_click(self, event):
        self.edit_contact()
