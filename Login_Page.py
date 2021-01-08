import sqlite3
from tkinter import *
from tkinter import messagebox
from tkinter.font import Font
import Admin_side


con = sqlite3.connect('DataBase/Login_data.db')
cur = con.cursor()


def clear_text(text, entry, event=None):
    if text == "User name":
        entry.delete(0, END)
    elif text == "Password":
        entry.delete(0, END)


def reset_text(fill_text, text, entry, event=None):
    if text == "":
        entry.insert(END, fill_text)


def Login():
    user_name = username.get()
    pass_word = password.get()
    query = f"Select * from 'login_id'where User_Name='{user_name}'"
    try:
        data = con.execute(query)
        for dat in data:
            print(dat[2])
        if dat[2] == pass_word:
            messagebox.showinfo('Success', 'Login successfull')
            top.destroy()

            at = Admin_side.Main_()

        else:
            messagebox.showerror('Error', 'Incorrect Password')
    except:
        messagebox.showerror('Error', 'Account not found')


if __name__ == '__main__':
    top = Tk()
    background_color = '#F9F1F9'
    text_color = '#A31284'
    top.geometry('1000x600')
    top.resizable(0, 0)
    top.config(bg=background_color)

    filename = PhotoImage(file="frame_060_delay-0.04s.gif")
    background_label = Label(top, image=filename)
    background_label.place(x=-130, y=0)

    # Fonts
    font = Font(family="kalam", size=11, weight="bold")
    login_font = Font(family="kalam", size=30, weight="bold", slant='italic')

    login_label = Label(top, text='login ', font=login_font, fg=text_color, bg=background_color)
    login_label.place(x=630, y=110)
    username = Entry(top, width=30, highlightbackground='#4508A2', highlightthickness=1, bg=background_color,
                     fg=text_color, font=font)
    username.insert(END, 'User name')
    username.place(x=590, y=200)
    password = Entry(top, width=30, highlightbackground='#4508A2', highlightthickness=1, bg=background_color,
                     fg=text_color, font=font)
    password.insert(END, 'Password')
    password.place(x=590, y=250)
    Login = Button(top, text="Login", command=Login)
    Login.place(x=590, y=300)

    # Bind Functions
    username.bind("<FocusIn>", lambda event: clear_text(username.get(), username, event))
    username.bind("<FocusOut>", lambda event: reset_text('User name', username.get(), username, event))
    password.bind("<FocusIn>", lambda event: clear_text(password.get(), password, event))
    password.bind("<FocusOut>", lambda event: reset_text('Password', password.get(), password, event))
    # top.wm_attributes('-alpha', 0.7)
    top.mainloop()
