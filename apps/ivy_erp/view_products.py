import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from apps.ivy_erp.database_tables import Order, Product, Session

from apps.ivy_erp.edit_product_dialog import EditProductDialog


class ViewProductsApp(ttk.Frame):
    title = "Produkte anzeigen"

    def __init__(self, parent, *args):
        super().__init__(parent)

        self.session = Session()

        self.products_tree = ttk.Treeview(
            self,
            columns=("Name", "Preis", "Kategorie", "Beschreibung"),
            show="headings",
        )
        self.products_tree.heading("Name", text="Name")
        self.products_tree.heading("Preis", text="Preis")
        self.products_tree.heading("Kategorie", text="Kategorie")
        self.products_tree.heading("Beschreibung", text="Beschreibung")
        self.products_tree.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)
        self.load_products()

    def load_products(self):
        for i in self.products_tree.get_children():
            self.products_tree.delete(i)

        for product in self.session.query(Product).all():
            self.products_tree.insert(
                "",
                tk.END,
                iid=product.id,
                values=(
                    product.name,
                    product.price,
                    product.category,
                    product.description,
                ),
            )

    def edit_product(self):
        product_id = self.products_tree.selection()[0]
        product = self.products_tree.item(product_id)

        name, price, category, description = product["values"]
        edit_dialog = EditProductDialog(
            self, product_id, name, price, category, description
        )
        self.wait_window(edit_dialog)  # Wait until the edit dialog window is closed
        self.load_products()  # Refresh the product list

    def delete_product(self):
        product_id = self.products_tree.selection()[0]

        response = messagebox.askyesno(
            title="Delete Product",
            message="Are you sure you want to delete this product?",
        )
        if response:
            customer = (
                self.session.query(Product).filter(Product.id == product_id).first()
            )

            self.session.query(Order).filter(Order.customer == customer).delete()

            customer = (
                self.session.query(Product).filter(Product.id == product_id).delete()
            )
            self.session.commit()
            self.load_products()
