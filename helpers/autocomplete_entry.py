import tkinter as tk
from tkinter import ttk

class AutocompleteEntry(ttk.Entry):
    def __init__(self, master=None, options=None, **kwargs):
        super().__init__(master, **kwargs)
        self.var = tk.StringVar()
        self.options = options if options is not None else []
        self.configure(textvariable=self.var)
        
        # Bind the events for the AutocompleteEntry
        self.var.trace("w", self.update_list)
        self.bind("<FocusOut>", self.on_focus_out)

        # Create a listbox for displaying the autocomplete options
        self.listbox = tk.Listbox(master, height=0)
        self.listbox.bind("<Button-1>", self.on_listbox_click)
        
    def update_list(self, *args):
        self.listbox.delete(0, tk.END)
        search_term = self.var.get()
        matching_options = [
            option for option in self.options if option.lower().startswith(search_term.lower())
        ]
        
        # Update the listbox with the new matching options
        for option in matching_options:
            self.listbox.insert(tk.END, option)

        # Adjust the height of the listbox based on the number of matching options
        listbox_height = min(len(matching_options), 5)
        self.listbox.configure(height=listbox_height)

        if matching_options:
            self.listbox.place(x=self.winfo_x(), y=self.winfo_y() + self.winfo_height())
        else:
            self.listbox.place_forget()

    def on_focus_out(self, event):
        self.listbox.place_forget()

    def on_listbox_click(self, event):
        selected_option = self.listbox.get(self.listbox.curselection())
        self.var.set(selected_option)
        self.listbox.place_forget()
