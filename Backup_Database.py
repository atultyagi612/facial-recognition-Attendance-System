import smtplib
import sqlite3
import transfer
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox

from xlsxwriter.workbook import Workbook

Frame_Color = '#F9F1F9'


class brow():
    def __init__(self, frame):
        self.heading_color = '#3c5b75'

        self.frame = frame
        for widget in self.frame.winfo_children():
            widget.destroy()

        title = Label(self.frame, text='Backup into xl sheet', font=("Helvetica", 20), fg=self.heading_color)
        title.pack(side=TOP)
        self.frame4 = Frame(self.frame, bg='#3c5b75')
        self.frame4.pack(side=BOTTOM, fill=X)
        butt = Button(self.frame4, text='Transfer spreadsheet', command=self.transfer)
        butt.pack(side=RIGHT)

        self.frame0 = Frame(self.frame, bg=Frame_Color, highlightbackground="#3c5b75", highlightthickness=3)
        self.frame0.pack(side=LEFT, pady=(0, 200), padx=(50, 0))
        title_1 = Label(self.frame0, text="Backup to a location")
        title_1.pack(side=TOP, padx=40, pady=(10, 5))
        labe_text = Label(self.frame0, text='Enter File name')
        labe_text.pack()
        self.file_name = Entry(self.frame0)
        self.file_name.pack()
        location = Button(self.frame0, text="select location", command=self.backup)
        location.pack(pady=7)

        frame1 = Frame(self.frame, bg=Frame_Color, highlightbackground="#3c5b75", highlightthickness=3)
        frame1.pack(side=LEFT, pady=(0, 200), padx=(100, 0))
        title_2 = Label(frame1, text="sent student attendance to email")
        title_2.pack(side=TOP, padx=40, pady=(10, 5))
        id_label = Label(frame1, text="Enter Id")
        id_label.place(x=10, y=70)
        self.id = Entry(frame1)
        self.id.place(x=120, y=70)
        email_label = Label(frame1, text="Enter Email")
        email_label.place(x=10, y=90)
        self.email = Entry(frame1)
        self.email.place(x=120, y=90)
        sent = Button(frame1, text='sent', command=self.sent_email)
        sent.pack(side=BOTTOM, pady=(80, 0))

    def backup(self):
        try:
            directory = filedialog.askdirectory()
            self.backup2(directory, self.file_name.get())
            messagebox.showinfo('success',
                                f'Backup complete at location\n{directory}\nName:{self.file_name.get()}.xlsx')

        except:
            pass

    def backup2(self, directory, filename):
        workbook = Workbook(f'{directory}/{filename}.xlsx')
        worksheet = workbook.add_worksheet()

        conn = sqlite3.connect('DataBase/Login_data.db')
        c = conn.cursor()

        mysel = c.execute("select * from 'login_id' ")
        for i, row in enumerate(mysel):
            for j, value in enumerate(row):
                worksheet.write(i, j, value)
        workbook.close()

    def sent_email(self):
        fromaddr = "YOUR EMAIL ID"
        toaddr = self.email.get()


        msg = MIMEMultipart()


        msg['From'] = fromaddr


        msg['To'] = toaddr


        msg['Subject'] = "Backup "


        body = "Body_of_the_mail"


        msg.attach(MIMEText(body, 'plain'))


        filename = "back.xlsm"
        attachment = open(f"Student_base_attendance/{self.id.get()}.xlsx", "rb")


        p = MIMEBase('application', 'octet-stream')


        p.set_payload((attachment).read())


        encoders.encode_base64(p)

        p.add_header('Content-Disposition', "attachment; filename= %s" % filename)


        msg.attach(p)


        s = smtplib.SMTP('smtp.gmail.com', 587)

        s.starttls()

        # Authentication
        s.login(fromaddr, "YOUR EMAIL ID PASSWORD")

        text = msg.as_string()

        # sending the mail
        s.sendmail(fromaddr, toaddr, text)

        s.quit()
        # os.unlink(f'Student_base_attendance/{self.id.get()}.xlsx')
        messagebox.showinfo('Success', f"Email sent successfully to {toaddr}")

    def transfer(self):
        comform = messagebox.askyesno('Comformation',
                                      'do you really want to transfer google spreedsheet\n into folder:- Backup')
        if comform == True:
            transfer.trans()
