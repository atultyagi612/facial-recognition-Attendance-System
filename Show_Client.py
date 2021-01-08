import sqlite3
from tkinter import *
from tkinter import ttk

con = sqlite3.connect('DataBase/client_detail.db')
cur = con.cursor()

background_color = '#F9F1F9'


class client_detail():
    def __init__(self, frame):
        self.frame = frame
        self.heading_color = '#3c5b75'
        for widget in self.frame.winfo_children():
            widget.destroy()
        title = Label(self.frame, text='client details', font=("Helvetica", 30), fg=self.heading_color)
        title.pack(side=TOP)
        columns_name = ('Id', 'Name', 'Email Id', 'Phone No.', 'Branch', 'Course')
        self.listBox = ttk.Treeview(self.frame, columns=columns_name, show='headings')

        self.listBox.column("0", width=20)
        self.listBox.column("1", width=120)
        self.listBox.column("2", width=170)
        self.listBox.column("3", width=120)
        self.listBox.column("4", width=120)
        self.listBox.column("5", width=120)

        # set column headings
        for col in columns_name:
            self.listBox.heading(col, text=col)

        self.listBox.pack(fill=BOTH, expand=1)
        self.show()

    def show(self):
        query = "select * from 'client_detail'"
        data = cur.execute(query)
        for dat in data:
            self.listBox.insert("", "end",
                                values=(str(dat[0]), str(dat[1]), str(dat[2]), str(dat[3]), str(dat[4]), str(dat[5])))
