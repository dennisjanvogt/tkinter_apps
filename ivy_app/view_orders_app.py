import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from ivy_app.database import Order, Session
from ivy_app.edit_order_dialog import EditOrderDialog


class ViewOrdersApp(ttk.Frame):
    title = "Bestellungen anzeigen"

    def __init__(self, parent, *args):
        super().__init__(parent)

        self.session = Session()

        self.orders_tree = ttk.Treeview(
            self,
            columns=("Kundenname", "Produktname", "Status", "Notiz"),
            show="headings",
        )
        self.orders_tree.heading("Kundenname", text="Kundenname")
        self.orders_tree.heading("Produktname", text="Produktname")
        self.orders_tree.heading("Status", text="Status")
        self.orders_tree.heading("Notiz", text="Notiz")
        self.orders_tree.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)
        self.load_orders()

    def load_orders(self):
        for i in self.orders_tree.get_children():
            self.orders_tree.delete(i)

        for order in self.session.query(Order).all():
            self.orders_tree.insert(
                "",
                tk.END,
                iid=order.id,
                values=(
                    order.customer.name,
                    order.product.name,
                    order.status,
                    order.note,
                ),
            )

    def edit_order(self):
        order_id = self.orders_tree.selection()[0]
        order = self.orders_tree.item(order_id)

        customer_id, product_id, status, note = order["values"]
        edit_dialog = EditOrderDialog(
            self, order_id, customer_id, product_id, status, note
        )
        self.wait_window(edit_dialog)  # Wait until the edit dialog window is closed
        self.load_orders()  # Refresh the order list

    def delete_order(self):
        order_id = self.orders_tree.selection()[0]

        response = messagebox.askyesno(
            title="Delete Order",
            message="Are you sure you want to delete this order?",
        )
        if response:
            self.session.query(Order).filter(Order.id == order_id).delete()
            self.session.commit()
            self.load_orders()
