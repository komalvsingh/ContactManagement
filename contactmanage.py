from tkinter import *
from tkinter import ttk, messagebox
import sqlite3
import subprocess

# Database setup
con = sqlite3.connect(database='info.db')
cur = con.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS contact (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                contact TEXT,
                email TEXT)""")
con.commit()
con.close()

class supplierClass:

    def __init__(self, root):
        self.root = root
        self.root.title("Contacts")
        self.root.geometry("1350x700")
        self.root.configure(bg="#fff")
        # self.root.state('zoomed')

        # Header label
        Manage_suppliers_tag = Label(self.root, text="Manage Contacts", bg="#fff", fg="black", font=('Microsoft YaHei UI Bold', 28, 'bold'))
        Manage_suppliers_tag.place(x=40, y=20)

        # Form entry fields
        lbl_name = Label(self.root, text="Name", bg="#fff", fg="#548678", font=('Microsoft YaHei UI Light', 21))
        lbl_name.place(x=120, y=140)
        self.name_entry = Entry(self.root, width=25, fg='black', border=0, bg='#fff', font=('Microsoft YaHei UI semi bold', 14))
        self.name_entry.place(x=120, y=190)
        Frame(self.root, width=280, height=2, bg='black').place(x=120, y=220)

        lbl_contact = Label(self.root, text="Phone No.", bg="#fff", fg="#548678", font=('Microsoft YaHei UI Light', 21))
        lbl_contact.place(x=120, y=260)
        self.contact_entry = Entry(self.root, width=25, fg='black', border=0, bg='#fff', font=('Microsoft YaHei UI semi bold', 14))
        self.contact_entry.place(x=120, y=310)
        Frame(self.root, width=400, height=2, bg='black').place(x=120, y=340)

        lbl_email = Label(self.root, text="Email id", bg="#fff", fg="#548678", font=('Microsoft YaHei UI Light', 21))
        lbl_email.place(x=120, y=380)
        self.email_entry = Entry(self.root, width=25, fg='black', border=0, bg='#fff', font=('Microsoft YaHei UI semi bold', 14))
        self.email_entry.place(x=120, y=430)
        Frame(self.root, width=400, height=2, bg='black').place(x=120, y=450)

        # Supplier table
        sup_table_frame = Frame(self.root, width=500, height=400)
        sup_table_frame.place(x=700, y=240)

        tree_scroll_x = Scrollbar(sup_table_frame, orient=HORIZONTAL)
        tree_scroll_y = Scrollbar(sup_table_frame, orient=VERTICAL)

        self.tree_table = ttk.Treeview(sup_table_frame, yscrollcommand=tree_scroll_y.set, xscrollcommand=tree_scroll_x.set, selectmode="extended")
        tree_scroll_y.pack(side=RIGHT, fill=Y)
        tree_scroll_x.pack(side=BOTTOM, fill=X)
        tree_scroll_x.config(command=self.tree_table.xview)
        tree_scroll_y.config(command=self.tree_table.yview)
        self.tree_table.pack()

        self.tree_table["columns"] = ('id', 'name', 'contact', 'email')
        self.tree_table.column("#0", width=0, stretch=NO)
        self.tree_table.column("id", anchor=W, width=100)
        self.tree_table.column("name", anchor=W, width=140)
        self.tree_table.column("contact", anchor=W, width=140)
        self.tree_table.column("email", anchor=W, width=160)
        self.tree_table.bind("<ButtonRelease-1>", self.select_record)
        self.tree_table.tag_configure('oddrow', background='white')
        self.tree_table.tag_configure('evenrow', background='#D8FCF1')

        self.tree_table.heading("id", anchor=W, text="Id")
        self.tree_table.heading("name", anchor=W, text="Name")
        self.tree_table.heading("contact", anchor=W, text="Contact")
        self.tree_table.heading("email", anchor=W, text="Email")

        add_btn = Button(self.root, text="Save", command=self.add, width=10, bg='#548678', fg='#fff', border=0, font=('Microsoft YaHei UI Light', 10, 'bold'))
        add_btn.place(x=720, y=570)
        update_btn = Button(self.root, text="Update", command=self.update_record, width=10, bg='#548678', fg='#fff', border=0, font=('Microsoft YaHei UI Light', 10, 'bold'))
        update_btn.place(x=860, y=570)
        delete_btn = Button(self.root, text="Delete", command=self.delete_record, width=10, bg='#548678', fg='#fff', border=0, font=('Microsoft YaHei UI Light', 10, 'bold'))
        delete_btn.place(x=1000, y=570)
        clear_btn = Button(self.root, text="Clear", command=self.clear_entry, width=10, bg='#548678', fg='#fff', border=0, font=('Microsoft YaHei UI Light', 10, 'bold'))
        clear_btn.place(x=1140, y=570)
       

        self.query_db()

    def query_db(self):
        con = sqlite3.connect('info.db')
        c = con.cursor()

        c.execute("SELECT * FROM contact")
        records = c.fetchall()

        global count
        count = 0

        for row in records:
            if count % 2 == 0:
                self.tree_table.insert(parent='', index='end', iid=count, text='', values=(row[0], row[1], row[2], row[3]), tags=('evenrow',))
            else:
                self.tree_table.insert(parent='', index='end', iid=count, text='', values=(row[0], row[1], row[2], row[3]), tags=('oddrow',))

            count += 1

        con.commit()
        con.close()

    def clear_entry(self):
        self.name_entry.delete(0, END)
        self.contact_entry.delete(0, END)
        self.email_entry.delete(0, END)

    def add(self):
        con = sqlite3.connect('info.db')
        cur = con.cursor()
        try:
            if self.name_entry.get() == "":
                messagebox.showerror("Error", "Name is required.", parent=self.root)
            else:
                cur.execute("""INSERT INTO contact (name, contact, email) VALUES (?, ?, ?)""",
                            (self.name_entry.get(), self.contact_entry.get(), self.email_entry.get()))
                con.commit()
                con.close()
                messagebox.showinfo("Success", "Record Added Successfully", parent=self.root)
                self.tree_table.delete(*self.tree_table.get_children())
                self.query_db()
                self.clear_entry()
        except Exception as e:
            messagebox.showerror("Error", f"Error due to: {str(e)}", parent=self.root)

    def select_record(self, ev):
        selected = self.tree_table.focus()
        content = self.tree_table.item(selected)
        row = content['values']

        self.clear_entry()

        self.name_entry.insert(0, row[1])
        self.contact_entry.insert(0, row[2])
        self.email_entry.insert(0, row[3])

    def update_record(self):
        selected = self.tree_table.focus()
        content = self.tree_table.item(selected)
        row = content['values']

        con = sqlite3.connect('info.db')
        cur = con.cursor()
        try:
            if self.name_entry.get() == "":
                messagebox.showerror("Error", "Name is required.", parent=self.root)
            else:
                cur.execute("""UPDATE contact SET name = ?, contact = ?, email = ? WHERE id = ?""",
                            (self.name_entry.get(), self.contact_entry.get(), self.email_entry.get(), row[0]))
                con.commit()
                con.close()
                messagebox.showinfo("Success", "Record Updated Successfully", parent=self.root)
                self.tree_table.delete(*self.tree_table.get_children())
                self.clear_entry()
                self.query_db()
        except Exception as e:
            messagebox.showerror("Error", f"Error due to: {str(e)}", parent=self.root)

    def delete_record(self):
        selected = self.tree_table.focus()
        content = self.tree_table.item(selected)
        row = content['values']

        con = sqlite3.connect('info.db')
        cur = con.cursor()
        try:
            if not row:
                messagebox.showerror("Error", "Please select a record to delete.", parent=self.root)
            else:
                cur.execute("DELETE FROM contact WHERE id=?", (row[0],))
                con.commit()
                con.close()
                messagebox.showinfo("Success", "Record Deleted Successfully", parent=self.root)
                self.tree_table.delete(*self.tree_table.get_children())
                self.clear_entry()
                self.query_db()
        except Exception as e:
            messagebox.showerror("Error", f"Error due to: {str(e)}", parent=self.root)

    

if __name__ == "__main__":
    root = Tk()
    obj = supplierClass(root)
    root.mainloop()
