import sqlite3
from tkinter import *
from tkinter.font import Font

import Add_Client
import Backup_Database
import Show_Client
import Update_Client

con = sqlite3.connect('DataBase/client_detail.db')
cur = con.cursor()
collapse_int = 0
background_color = '#F9F1F9'


class Main_():
    def __init__(self):
        self.heading_color = '#3c5b75'

        root = Tk()
        self.label_font = Font(family="Courier", size=44, weight='bold')
        self.font = Font(family="kalam", size=10, weight="bold")
        self.hover_font = Font(family="kalam", size=11, weight="bold")
        root.geometry('900x500')

        self.top_frame = Frame(root, bg='#3c5b75')
        self.top_frame.pack(side=LEFT, fill=Y)

        self.lab = Label(self.top_frame, text='≡', bg='#3c5b75', font=self.label_font, fg='white', padx=60)
        self.lab.pack(side=TOP, fill=X)
        self.lab.bind("<Button-1>", self.collapse)

        self.button = Button(self.top_frame, text="Add client",
                             command=lambda: [self.Add_Client(), self.Manage_Border(self.button)], font=self.font,
                             bg='#3c5b75', fg='white', borderwidth=2)
        self.button.pack(side=TOP, padx=(10, 0))
        self.button.bind('<Enter>', lambda event: self.button.config(font=self.hover_font))
        self.button.bind('<Leave>', lambda event: self.button.config(font=self.font))

        self.button2 = Button(self.top_frame, text="Update client",
                              command=lambda: [self.delete_client(), self.Manage_Border(self.button2)], font=self.font,
                              bg='#3c5b75', fg='white', borderwidth=0)
        self.button2.pack(side=TOP, padx=10)
        self.button2.bind('<Enter>', lambda event: self.button2.config(font=self.hover_font))
        self.button2.bind('<Leave>', lambda event: self.button2.config(font=self.font))

        self.button3 = Button(self.top_frame, text="Clients", font=self.font, bg='#3c5b75', fg='white', borderwidth=0,
                              command=lambda: [self.clients(), self.Manage_Border(self.button3)])
        self.button3.pack(side=TOP, padx=10)
        self.button3.bind('<Enter>', lambda event: self.button3.config(font=self.hover_font))
        self.button3.bind('<Leave>', lambda event: self.button3.config(font=self.font))

        self.button4 = Button(self.top_frame, text="Backup",
                              command=lambda: [self.backup(), self.Manage_Border(self.button4)], font=self.font,
                              bg='#3c5b75', fg='white', borderwidth=0)
        self.button4.pack(side=TOP, padx=(10, 0))
        self.button4.bind('<Enter>', lambda event: self.button4.config(font=self.hover_font))
        self.button4.bind('<Leave>', lambda event: self.button4.config(font=self.font))

        self.frame = Frame(root, bg='#F9F1F9')
        self.frame.pack(side=TOP, fill=BOTH, expand=1)
        self.Add_Client()

        root.mainloop()

    def Add_Client(self):
        add = Add_Client.client_add(self.frame)

    def delete_client(self):
        dell = Update_Client.client_delete(self.frame)

    def clients(self):
        cle = Show_Client.client_detail(self.frame)

    def backup(self):
        at = Backup_Database.brow(self.frame)

    def collapse(self, event):
        global collapse_int
        if int(collapse_int) == 0:
            self.lab.config(padx=14)
            self.button.config(text="+")
            self.button2.config(text="✘")
            self.button3.config(text="i")
            self.button4.config(text='B')
            self.label_font.config(size=20)
            collapse_int = 1

        elif int(collapse_int) == 1:
            self.lab.config(padx=50)
            self.button.config(text="Add Client")
            self.button2.config(text="delete client")
            self.button3.config(text="Clients")
            self.button4.config(text='Backup')
            self.label_font.config(size=44)
            collapse_int = 0

    def Manage_Border(self, button_name, event=None):
        self.button.config(borderwidth=0)
        self.button2.config(borderwidth=0)
        self.button4.config(borderwidth=0)
        self.button3.config(borderwidth=0)
        button_name.config(borderwidth=2)


#atul = Main_()
