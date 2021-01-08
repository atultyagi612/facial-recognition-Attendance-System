import glob
import os
import re
import sqlite3
import time
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from tkinter.ttk import Combobox

import Style_font
import cv2
import numpy as np
import xlsxwriter
from PIL import Image

background_color = '#F9F1F9'
con = sqlite3.connect('DataBase/client_detail.db')
cur = con.cursor()
face_classifier = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
path = 'atul'
recognizer = cv2.face.LBPHFaceRecognizer_create()
detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml");
collapse_int = 0


class client_add():
    def __init__(self, frame):

        self.heading_color = '#3c5b75'
        self.frame = frame
        for widget in self.frame.winfo_children():
            widget.destroy()
        title = Label(self.frame, text='Add Client', font=("Helvetica", 30), fg=self.heading_color, bg=background_color)
        title.pack(side=TOP)
        self.frame1 = Frame(self.frame, bg='#3c5b75', height=25)
        self.frame1.pack(side=BOTTOM, fill=X)
        # Mini Frame ***************************************************************
        self.miniFrame = Frame(self.frame, bg=background_color, highlightbackground="#3c5b75", highlightthickness=3)
        self.miniFrame.pack(anchor='c', padx=(20, 0), pady=(40, 0))
        labelpadx = 10
        entrypady = 10
        atul = Style_font.Font_Style()
        reg_no = Label(self.miniFrame, text='Registration No.', bg=background_color, font=atul.Label_Font)
        reg_no.grid(row=1, column=1, pady=(20, 0), padx=labelpadx, sticky='w')
        self.reg_no_ent = Entry(self.miniFrame, bg=background_color)
        self.reg_no_ent.grid(row=1, column=2, pady=(20, 0), padx=entrypady)

        lab1 = Label(self.miniFrame, text="enter name", bg=background_color, font=atul.Label_Font)
        lab1.grid(row=2, column=1, pady=5, padx=labelpadx, sticky='w')
        self.ent1 = Entry(self.miniFrame, bg=background_color)
        self.ent1.grid(row=2, column=2, pady=5, padx=entrypady)

        lab2 = Label(self.miniFrame, text="email", bg=background_color, font=atul.Label_Font)
        lab2.grid(row=3, column=1, pady=5, padx=labelpadx, sticky='w')
        self.ent2 = Entry(self.miniFrame, bg=background_color)
        self.ent2.grid(row=3, column=2, pady=5, padx=entrypady)

        phone_no = Label(self.miniFrame, text='Phone No.', bg=background_color, font=atul.Label_Font)
        phone_no.grid(row=4, column=1, pady=5, padx=labelpadx, sticky='w')
        self.phone_ent = Entry(self.miniFrame, bg=background_color)
        self.phone_ent.grid(row=4, column=2, pady=5, padx=entrypady)

        branch_lab = Label(self.miniFrame, text='Branch', bg=background_color, font=atul.Label_Font)
        branch_lab.grid(row=5, column=1, pady=5, padx=labelpadx, sticky='w')
        self.branch = Combobox(self.miniFrame, height=5, width=15)  # ,values=v
        self.branch.bind("<Button-1>", self.fill_combobox)

        self.branch.set("Select Branch")
        self.branch.grid(row=5, column=2, pady=5, padx=entrypady)

        course_lab = Label(self.miniFrame, text="Course", bg=background_color, font=atul.Label_Font)
        course_lab.grid(row=6, column=1, pady=5, padx=labelpadx, sticky='w')
        self.course = Combobox(self.miniFrame, height=5, width=15)
        self.course.set("Select Course")
        self.course.grid(row=6, column=2, pady=5, padx=entrypady)
        self.course.bind("<Button-1>", self.fill_courses)

        button1 = Button(self.miniFrame, text="enter", command=self.verify_Input, font=atul.Label_Font)
        button1.grid(row=7, column=2, pady=30, ipadx=20)

        try:
            combostyle = ttk.Style()

            combostyle.theme_create('combostyle', parent='alt',
                                    settings={'TCombobox':
                                                  {'configure':
                                                       {'selectbackground': 'black',
                                                        'fieldbackground': background_color,
                                                        'background': '#3c5b75'
                                                        }}}
                                    )
            # ATTENTION: this applies the new style 'combostyle' to all ttk.Combobox
            combostyle.theme_use('combostyle')
        except:
            pass

    def verify_Input(self):
        regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
        query = f"select * from 'client_detail' where ID='{self.reg_no_ent.get()}'"
        cur.execute(query)
        result = cur.fetchone()
        if self.reg_no_ent.get() == "":
            messagebox.showerror('error', 'Enter Registration No.')
        elif result:
            messagebox.showerror('error', 'Registration no already present in database')
        elif self.ent1.get() == "":
            messagebox.showerror('error', 'Please enter the name')
        elif not re.search(regex, self.ent2.get()):
            messagebox.showerror('error', 'Invalid email Id')
        elif len(self.phone_ent.get()) != 10:
            messagebox.showerror('error', 'Invalid phone number')
        elif self.branch.get() == "Select Branch":
            messagebox.showerror('error', 'Select the branch')
        elif self.course.get() == "Select Course":
            messagebox.showerror('error', 'Select the course')
        else:
            messagebox.showinfo('succss', 'done')
            self.insert()

    def insert(self):
        self.create_xlsmFile()
        query = "insert into 'client_detail' (ID,Name,Email_Id,Phone_no,Branch,Course) values(?,?,?,?,?,?)"
        cur.execute(query, (
        int(self.reg_no_ent.get()), self.ent1.get(), self.ent2.get(), self.phone_ent.get(), self.branch.get(),
        self.course.get()))
        con.commit()
        messagebox.showinfo('done', 'done')

        self.Capture_faces(int(self.reg_no_ent.get()))

    def Capture_faces(self, id):
        face_id = id
        cam = cv2.VideoCapture(0)
        no_of_captures = 0
        while True:
            try:
                no_of_captures += 1
                is_captured, frame = cam.read()
                grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                f = self.croped_face(grey)

                cv2.imshow('face', f)

                cv2.imwrite("atul/User." + str(face_id) + '.' + str(no_of_captures) + ".jpg", f)
                cv2.waitKey(1)
            except:
                pass
            time.sleep(0.4)
            if cv2.waitKey(1) == 13 or no_of_captures == 20:
                break
        cam.release()
        cv2.destroyAllWindows()
        messagebox.showinfo('Done', 'capture done\nStart training')
        faces, ids = self.getImagesAndLabels(path)
        recognizer.train(faces, np.array(ids))

        # Save the model into trainer/trainer.yml
        recognizer.write(f'trainer/trainer{id}.yml')  # recognizer.save() worked on Mac, but not on Pi

        # Print the numer of faces trained and end program
        messagebox.showinfo('Congratulation', 'Face training complete')
        # deleting all the generated images
        directory = 'atul/'
        os.chdir(directory)
        files = glob.glob('*.jpg')
        for filename in files:
            os.unlink(filename)

        print("\n [INFO] {0} faces trained. Exiting Program".format(len(np.unique(ids))))

    def getImagesAndLabels(self, path):

        imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
        faceSamples = []
        ids = []

        for imagePath in imagePaths:

            PIL_img = Image.open(imagePath).convert('L')  # convert it to grayscale
            img_numpy = np.array(PIL_img, 'uint8')

            id = int(os.path.split(imagePath)[-1].split(".")[1])
            faces = detector.detectMultiScale(img_numpy)

            for (x, y, w, h) in faces:
                faceSamples.append(img_numpy[y:y + h, x:x + w])
                ids.append(id)

        return faceSamples, ids

    def croped_face(self, grey):
        face_coordinates = face_classifier.detectMultiScale(grey, 1.3, 5)
        if face_coordinates is ():
            return None

        for (x, y, w, h) in face_coordinates:
            croped_image = grey[y:y + h, x:x + w]
        return croped_image

    def create_xlsmFile(self):
        workbook = xlsxwriter.Workbook(f'Student_base_attendance/{self.reg_no_ent.get()}.xlsx')
        worksheet = workbook.add_worksheet()
        workbook.close()

    def fill_combobox(self, event):
        self.Branches = []
        self.con = sqlite3.connect('DataBase/extra.db')
        self.cur = self.con.cursor()
        query_branch = "select * from 'extra_detail' "
        data = self.cur.execute(query_branch)
        for dat in data:
            self.Branches.append(dat[1])
        self.branch['values'] = self.Branches
        print(self.Branches)

    def fill_courses(self, event):
        print(self.branch.get())
        query_courses = f"select * from 'extra_detail' where branch='{self.branch.get()}' "
        cour = self.cur.execute(query_courses)
        for courses in cour:
            courses = courses[2]
        print(str(courses).split(","))
        self.course['values'] = str(courses).split(",")
