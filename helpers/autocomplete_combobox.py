import tkinter as tk
from tkinter import ttk


class AutocompleteCombobox(ttk.Entry):
    MAX_VISIBLE_ITEMS = 3

    def __init__(self, parent, autocomplete_list):
        super().__init__(parent)
        self.autocomplete_list = autocomplete_list
        self.listbox = None
        self.bind("<KeyRelease>", self.check_key_release)
        # self.bind('<FocusOut>', self.on_focus_out) #Kann theoretisch weg, aber weiß noch nicht

    def check_key_release(self, event):
        if event.keysym in ("Down", "Up", "Return", "Tab", "ISO_Left_Tab"):
            self.handle_special_keys(event)
            return

        if event.keysym in ("Delete"):
            self.destroy_listbox()
            return

        input_text = self.get()
        if len(input_text) < 1:
            self.destroy_listbox()
            return

        if not self.listbox:
            self.listbox = tk.Listbox(self.master, height=self.MAX_VISIBLE_ITEMS)
            self.listbox.place(x=self.winfo_x(), y=self.winfo_y() + self.winfo_height())
            self.listbox.bind(
                "<Button-1>", self.on_listbox_click
            )  # Bind the left mouse click event

        values = [
            item
            for item in self.autocomplete_list
            if input_text.lower() in item.lower()
        ][: self.MAX_VISIBLE_ITEMS]
        print(values)
        if not values:
            self.destroy_listbox()
            return

        self.listbox.delete(0, tk.END)
        for value in values:
            self.listbox.insert(tk.END, value)

    def on_focus_out(self, event):
        if event.widget == self:
            self.after(200000, self.destroy_listbox)

    def on_listbox_click(self, event):
        if self.listbox and self.listbox.curselection():
            selected_value = self.listbox.get(self.listbox.curselection())
            self.delete(0, tk.END)
            self.insert(0, selected_value)
            self.destroy_listbox()

    def handle_special_keys(self, event):
        if not self.listbox:
            return

        if event.keysym == "Down":
            self.listbox.focus()
            self.listbox.selection_set(0)
            self.listbox.activate(0)
            self.listbox.bind("<Return>", self.on_return_key)
            self.listbox.bind("<Up>", self.handle_listbox_keys)
            self.listbox.bind("<Down>", self.handle_listbox_keys)
        elif event.keysym == "Up":
            current_selection = self.listbox.curselection()
            if current_selection:
                index = current_selection[0]
                if index > 0:
                    self.listbox.selection_clear(index)
                    self.listbox.selection_set(index - 1)
                    self.listbox.activate(index - 1)
        elif event.keysym == "Return":
            self.on_return_key()

    def handle_listbox_keys(self, event):
        if event.keysym == "Up":
            current_selection = self.listbox.curselection()
            if current_selection:
                index = current_selection[0]
                if index > 0:
                    self.listbox.selection_clear(index)
                    self.listbox.selection_set(index)
                    self.listbox.activate(index)
        elif event.keysym == "Down":
            current_selection = self.listbox.curselection()
            if current_selection:
                index = current_selection[0]
                if index < self.listbox.size() - 1:
                    self.listbox.selection_clear(index)
                    self.listbox.selection_set(index)
                    self.listbox.activate(index)

    def on_return_key(self, event=None):
        if self.listbox and self.listbox.curselection():
            selected_value = self.listbox.get(self.listbox.curselection())
            self.delete(0, tk.END)
            self.insert(0, selected_value)
            self.destroy_listbox()

    def destroy_listbox(self):
        if self.listbox:
            self.listbox.unbind("<FocusOut>")
            self.listbox.destroy()
            self.listbox = None
