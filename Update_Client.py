import Style_font
import os
import sqlite3
import xlsxwriter
from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Combobox

con = sqlite3.connect('DataBase/client_detail.db')
cur = con.cursor()

background_color = '#F9F1F9'


class client_delete():
    def __init__(self, frame):

        self.frame = frame
        self.heading_color = '#3c5b75'
        for widget in self.frame.winfo_children():
            widget.destroy()

        title = Label(self.frame, text='Update Client', font=("Helvetica", 30), fg=self.heading_color)
        title.pack(side=TOP)
        self.miniframe = Frame(self.frame)
        self.miniframe.pack()
        label2 = Label(self.miniframe, text="Enter client ID", bg=background_color)
        label2.pack()
        self.entry2 = Entry(self.miniframe, bg=background_color)
        self.entry2.pack()
        butt2 = Button(self.miniframe, text='Search', command=lambda: self.search())
        butt2.pack(anchor='w')
        delete_but = Button(self.miniframe, text='Delete', command=lambda: self.delete_student())
        delete_but.pack(anchor='e')

        self.downFrame = Frame(self.frame, bg='#3c5b75', height=25)
        self.downFrame.pack(side=BOTTOM, fill=X)

    def search(self):
        ID = self.entry2.get()

        try:
            self.miniFrame2.destroy()
        except:
            pass
        if ID == "":
            messagebox.showerror('Error', 'Plesase enter the Registration Number ')
        else:
            try:
                query2 = f"select * from 'client_detail' where ID='{ID}'"
                data = cur.execute(query2).fetchone()
                ID = data[0]
                client_name = data[1]
                client_email = data[2]
                client_phone = data[3]
                client_branch = data[4]
                client_course = data[5]

                self.miniFrame2 = Frame(self.frame)
                self.miniFrame2.pack()
                self.Fill_miniFrame2()
                self.reg_no_ent.insert(END, ID)
                self.ent1.insert(END, client_name)
                self.ent2.insert(END, client_email)
                self.phone_ent.insert(END, client_phone)
                self.branch.set(client_branch)
                self.course.set(client_course)
                for widget in self.downFrame.winfo_children():
                    widget.destroy()
                self.search_files()



            except:
                messagebox.showerror('Error', f'Student not found with \nRegistration Id:- {ID}')

    def Fill_miniFrame2(self):
        labelpadx = 10
        entrypady = 10
        atul = Style_font.Font_Style()

        reg_no = Label(self.miniFrame2, text='Registration No.', bg=background_color, font=atul.Label_Font)
        reg_no.grid(row=1, column=1, pady=(20, 0), padx=labelpadx, sticky='w')
        self.reg_no_ent = Entry(self.miniFrame2, bg=background_color)
        self.reg_no_ent.grid(row=1, column=2, pady=(20, 0), padx=entrypady)

        lab1 = Label(self.miniFrame2, text="enter name", bg=background_color, font=atul.Label_Font)
        lab1.grid(row=2, column=1, pady=5, padx=labelpadx, sticky='w')
        self.ent1 = Entry(self.miniFrame2, bg=background_color)
        self.ent1.grid(row=2, column=2, pady=5, padx=entrypady)

        lab2 = Label(self.miniFrame2, text="email", bg=background_color, font=atul.Label_Font)
        lab2.grid(row=3, column=1, pady=5, padx=labelpadx, sticky='w')
        self.ent2 = Entry(self.miniFrame2, bg=background_color)
        self.ent2.grid(row=3, column=2, pady=5, padx=entrypady)

        phone_no = Label(self.miniFrame2, text='Phone No.', bg=background_color, font=atul.Label_Font)
        phone_no.grid(row=4, column=1, pady=5, padx=labelpadx, sticky='w')
        self.phone_ent = Entry(self.miniFrame2, bg=background_color)
        self.phone_ent.grid(row=4, column=2, pady=5, padx=entrypady)

        branch_lab = Label(self.miniFrame2, text='Branch', bg=background_color, font=atul.Label_Font)
        branch_lab.grid(row=5, column=1, pady=5, padx=labelpadx, sticky='w')
        self.branch = Combobox(self.miniFrame2, height=5, width=15)  # ,values=v
        self.branch.bind("<Button-1>", self.fill_combobox)

        self.branch.set("Select Branch")
        self.branch.grid(row=5, column=2, pady=5, padx=entrypady)

        course_lab = Label(self.miniFrame2, text="Course", bg=background_color, font=atul.Label_Font)
        course_lab.grid(row=6, column=1, pady=5, padx=labelpadx, sticky='w')
        self.course = Combobox(self.miniFrame2, height=5, width=15)
        self.course.set("Select Course")
        self.course.grid(row=6, column=2, pady=5, padx=entrypady)
        self.course.bind("<Button-1>", self.fill_courses)

        button1 = Button(self.miniFrame2, text="Update", command=self.Update, font=atul.Label_Font)
        button1.grid(row=7, column=2, pady=30, ipadx=20)

    def fill_combobox(self, event):
        self.Branches = []
        self.con1 = sqlite3.connect('DataBase/extra.db')
        self.cur1 = self.con1.cursor()
        query_branch = "select * from 'extra_detail' "
        data = self.cur1.execute(query_branch)
        for dat in data:
            self.Branches.append(dat[1])
        self.branch['values'] = self.Branches
        print(self.Branches)

    def fill_courses(self, event):
        print(self.branch.get())
        query_courses = f"select * from 'extra_detail' where branch='{self.branch.get()}' "
        cour = self.cur1.execute(query_courses)
        for courses in cour:
            courses = courses[2]
        print(str(courses).split(","))
        self.course['values'] = str(courses).split(",")

    def Update(self):
        print('hllo')
        print(self.ent1.get(), self.entry2.get())
        update_query = "UPDATE 'client_detail' SET ID=? ,Name=?,Email_Id=?,Phone_no=?,Branch=?,Course=? WHERE ID=?"
        cur.execute(update_query, (
        int(self.reg_no_ent.get()), str(self.ent1.get()), str(self.ent2.get()), str(self.phone_ent.get()),
        str(self.branch.get()), str(self.course.get()), int(self.entry2.get())))

        if int(self.reg_no_ent.get()) != int(self.entry2.get()):
            os.rename(f'Student_base_attendance/{self.entry2.get()}.xlsx',
                      f'Student_base_attendance/{self.reg_no_ent.get()}.xlsx')
            os.rename(f'trainer/trainer{self.entry2.get()}.yml', f'trainer/trainer{self.reg_no_ent.get()}.yml')
            con.commit()
        messagebox.showinfo('Success', f'Update successfully\n'
                                       f'ID:- {str(self.reg_no_ent.get())}')

    def delete_student(self):
        ID = int(self.entry2.get())
        if ID == "":
            messagebox.showerror('Error', 'Plesase enter the Registration Number ')
        else:
            try:
                query2 = f"select * from 'client_detail' where ID='{ID}'"
                data = cur.execute(query2).fetchone()
                ID = data[0]
                client_name = data[1]
                comform = messagebox.askyesnocancel('comformation',
                                                    f'really want to delete clirnt data \n ID= {ID}\nName= {client_name}')
                if comform == True:
                    try:
                        delete_quiry = f"delete from 'client_detail' where ID='{ID}'"
                        cur.execute(delete_quiry)
                        con.commit()
                        messagebox.showinfo('Success',
                                            f'Successfully delete client data and trainer data of\nName:- {client_name}\nID:- {ID}')

                        try:
                            os.remove(f"trainer/trainer{ID}.yml")

                        except:
                            print('not found')
                        try:
                            os.remove(f'Student_base_attendance/{ID}.xlsx')
                        except:
                            print('not found')
                    except EXCEPTION as e:
                        print(e)
            except:
                messagebox.showerror('Error', f'Student not found with \nRegistration Id:- {ID}')

        try:
            self.miniFrame2.destroy()
        except:
            pass

    def search_files(self):
        if os.path.isfile(f'Student_base_attendance/{self.entry2.get()}.xlsx'):
            label = Label(self.downFrame, text="Attendance file Found", bg='#3c5b75', fg='white')
            label.pack(side=LEFT)
            absolute_path = os.path.abspath(f"Student_base_attendance/{self.entry2.get()}.xlsx")
            open_button = Button(self.downFrame, text='Open', command=lambda: os.startfile(absolute_path))
            open_button.pack(side=LEFT, padx=10)
        else:
            label = Label(self.downFrame, text='Attendance file Not found', bg='#3c5b75', fg='white')
            label.pack(side=LEFT)
            open_button = Button(self.downFrame, text='Create', command=lambda: self.create_xlsmFile())
            open_button.pack(side=LEFT)
        if os.path.isfile(f'trainer/trainer{self.entry2.get()}.yml'):
            label1 = Label(self.downFrame, text='Trainer file Found', bg='#3c5b75', fg='white')
            label1.pack(side=LEFT, padx=30)
        else:
            label1 = Label(self.downFrame, text='Trainer file Not found', bg='#3c5b75', fg='white')
            label1.pack(side=LEFT, padx=30)

    def create_xlsmFile(self):
        workbook = xlsxwriter.Workbook(f'Student_base_attendance/{self.entry2.get()}.xlsx')
        worksheet = workbook.add_worksheet()
        workbook.close()
