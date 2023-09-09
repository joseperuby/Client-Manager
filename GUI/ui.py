import Scripts.helpers as helpers
from tkinter.messagebox import askokcancel, WARNING
import DB.database as db
from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter.ttk import *

# Center UI
class CenterWidgetMixin:
    def center(self):
        self.update()
        w = self.winfo_width()
        h = self.winfo_height()
        ws = self.winfo_screenwidth()
        hs = self.winfo_screenheight()
        x = int(ws/2 - w/2)
        y = int(hs/2 - h/2)
        self.geometry(f"{w}x{h}+{x}+{y}")
        #self.geometry("WIDTHxHEIGHT+OFFSET_X+OFFSET_Y")

#UI CREATE CUSTOMER
class CreateCustomertWindow(Toplevel, CenterWidgetMixin):
    def __init__(self, father):
        super().__init__(father)
        self.title("Create customer")
        self.build()
        self.center()
        self.transient(father)
        self.grab_set()

    def build(self):
        frame = ttk.Frame(self)
        frame.pack(padx=20, pady=10)

        ttk.Label(frame, text="ID (2 ints and 1 upper char)").grid(row=0, column=0)
        ttk.Label(frame, text="Name (2 ints to 30 char)").grid(row=0, column=1)
        ttk.Label(frame, text="Lastname (2 ints to 30 char)").grid(row=0, column=2)

        id = tk.Entry(frame)
        id.grid(row=1, column=0)
        id.bind("<KeyRelease>", lambda event: self.validate(event, 0))
        name = tk.Entry(frame)
        name.grid(row=1, column=1)
        name.bind("<KeyRelease>", lambda event: self.validate(event, 1))
        lastname = tk.Entry(frame)
        lastname.grid(row=1, column=2)
        lastname.bind("<KeyRelease>", lambda event: self.validate(event, 2))

        frame = ttk.Frame(self)
        frame.pack(pady=10)

        create = ttk.Button(frame, text="Create", command=self.create_customer)
        #State of the button disabled
        create.configure(state=DISABLED)
        create.grid(row=0, column=0)
        ttk.Button(frame, text="Cancel", command=self.close).grid(row=0, column=1)

        self.validations = [0,0,0]
        self.create = create
        self.id = id
        self.name = name
        self.lastname = lastname


    def create_customer(self):
            self.master.treeview.insert(
                parent='', index='end', iid=self.id.get(),
                values=(self.id.get(), self.name.get(), self.lastname.get()))
            db.Customers.add(self.id.get(), self.name.get(), self.lastname.get())
            self.close()
            

    def close(self):
        self.destroy()
        self.update()

    def validate(self, event, index):
        value = event.widget.get()
        valid = helpers.valid_id(value, db.Customers.list) if index == 0 \
            else (value.isalpha() and len(value) >= 2 and len(value) <= 30)
        event.widget.configure({"background": "Green" if valid else "Red"})
        
        # Change the state of the button to normal
        self.validations[index] = valid
        self.create.config(state=NORMAL if self.validations == [1,1,1] else DISABLED)


#UI MODIFY CUSTOMER
class ModifyCustomertWindow(Toplevel, CenterWidgetMixin):
    def __init__(self, father):
        super().__init__(father)
        self.title("Modify customer")
        self.build()
        self.center()
        self.transient(father)
        self.grab_set()

    def build(self):
        frame = ttk.Frame(self)
        frame.pack(padx=20, pady=10)

        ttk.Label(frame, text="ID (no editable").grid(row=0, column=0)
        ttk.Label(frame, text="Name (2 ints to 30 char)").grid(row=0, column=1)
        ttk.Label(frame, text="Lastname (2 ints to 30 char)").grid(row=0, column=2)

        id = tk.Entry(frame)
        id.grid(row=1, column=0)
        name = tk.Entry(frame)
        name.grid(row=1, column=1)
        name.bind("<KeyRelease>", lambda event: self.validate(event, 0))
        lastname = tk.Entry(frame)
        lastname.grid(row=1, column=2)
        lastname.bind("<KeyRelease>", lambda event: self.validate(event, 1))

        customer = self.master.treeview.focus()
        items = self.master.treeview.item(customer, 'values')
        id.insert(0, items[0])
        id.config(state=DISABLED)
        name.insert(0, items[1])
        lastname.insert(0, items[2])

        frame = ttk.Frame(self)
        frame.pack(pady=10)

        update_button = ttk.Button(frame, text="Modify", command=self.update_customer)
        update_button.grid(row=0, column=0)
        ttk.Button(frame, text="Cancel", command=self.close).grid(row=0, column=1)

        self.validations = [0,0]
        self.update_button = update_button
        self.id = id
        self.name = name
        self.lastname = lastname


    def update_customer(self):
        customer = self.master.treeview.focus()
        self.master.treeview.item(customer, values=(self.id.get(), self.name.get(), self.lastname.get()))
        db.Customers.modify(self.id.get(), self.name.get(), self.lastname.get())
        self.close()
            

    def close(self):
        self.destroy()
        self.update()

    def validate(self, event, index):
        value = event.widget.get()
        valid = (value.isalpha() and len(value) >= 2 and len(value) <= 30)
        event.widget.configure({"background": "Green" if valid else "Red"})
        
        # Change the state of the button to normal
        self.validations[index] = valid
        self.update_button.config(state=NORMAL if self.validations == [1,1] else DISABLED)

        

# UI MAINWINDOW
class MainWindow(Tk, CenterWidgetMixin):
    def __init__(self):
        super().__init__()
        self.title("Customer Manager")
        self.build()
        self.center()

    def build(self):
        frame = ttk.Frame(self)
        frame.pack()

        treeview = ttk.Treeview(frame)
        treeview['columns'] = ('ID', 'NAME', 'LASTNAME')

        treeview.column("#0", width=0, stretch=NO)
        treeview.column("ID",anchor=CENTER)
        treeview.column("NAME",anchor=CENTER)
        treeview.column("LASTNAME",anchor=CENTER)

        treeview.heading("ID", text="ID", anchor=CENTER)
        treeview.heading("NAME", text="NAME", anchor=CENTER)
        treeview.heading("LASTNAME", text="LASTNAME", anchor=CENTER)

        scrollbar = ttk.Scrollbar(frame)
        scrollbar.pack(side=RIGHT, fill=Y)
        treeview["yscrollcommand"] = scrollbar.set

        for customer in db.Customers.list:
            treeview.insert(
                parent='', index='end', iid=customer.id,
                values=(customer.id, customer.name, customer.lastname)
            )

        treeview.pack()
        frame = ttk.Frame(self)
        frame.pack(pady=20)

        ttk.Button(frame, text="Create", command=self.UI_create).grid(row=0, column=0, padx=10)
        ttk.Button(frame, text="Modify", command=self.UI_modify).grid(row=0, column=1, padx=10)
        ttk.Button(frame, text="Remove", command=self.UI_delete).grid(row=0, column=2, padx=10)

        self.treeview = treeview

    def UI_delete(self):
        customer = self.treeview.focus()
        if customer:
            select = self.treeview.item(customer, "values")
            confirm = askokcancel(
                title="Remove",
                message=f"Do you want to remove {select[1]} {select[2]}?",
                icon = WARNING
            )

            if confirm:
                self.treeview.delete(customer)
                db.Customers.delete(select[0])

    def UI_create(self):
        CreateCustomertWindow(self)

    def UI_modify(self):
        if self.treeview.focus():
            ModifyCustomertWindow(self)


#__MAIN__
if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()