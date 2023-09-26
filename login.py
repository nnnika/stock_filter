# Import packages
import tkinter
import tkinter.messagebox
from tkinter import *
from PIL import ImageTk
# Create database
import sqlite3
import subprocess
con = sqlite3.connect('test.db')
cursor = con.cursor()
cursor.execute('''
                CREATE TABLE IF NOT EXISTS user_info(
                username int(10) PRIMARY KEY,
                password int(10))
                ''')
cursor.close()
con.close()


# Define login function
def event_login():
    con = sqlite3.connect('test.db')
    cursor = con.cursor()
    cursor.execute('select * from user_info')
    all_user_information = cursor.fetchall()
    cursor.close()
    con.close()
    if username_entry.get() == '' or password_entry.get() == '':
        tkinter.messagebox.showwarning('Reminder', 'Please input your username and password!')
    elif username_entry.get().isdigit() == False or password_entry.get().isdigit() == False:
        tkinter.messagebox.showwarning('Reminder', 'Both the username and password can only be composed of digits. Please try again!')
        username_entry.delete(0, 'end')
        password_entry.delete(0, 'end')
    else:
        user_information = int(username_entry.get()), int(password_entry.get())
        if user_information in all_user_information:
            tkinter.messagebox.showinfo(title = 'Reminder', message = 'Log in successfully!')
            username_entry.delete(0, 'end')
            password_entry.delete(0, 'end')
            subprocess.Popen(["python", "filter.py"])
            login_window.iconify()
        else:
            tkinter.messagebox.showwarning(title = 'Reminder', message = 'Error in username or password!')
            username_entry.delete(0, 'end')
            password_entry.delete(0, 'end')


# Define register function
def event_register():
    register = Tk()
    register.title('Register interface')
    register.geometry('400x400')

    frame_one = Frame(register, height = 50, width = 500)
    label_one = Label(frame_one, text = 'Username:')
    entry_one = Entry(frame_one)
    label_one.pack(side = 'left')
    entry_one.pack()
    frame_one.pack(pady = 10)
 
    frame_two = Frame(register)
    label_two = Label(frame_two, text = 'Password:')
    entry_two = Entry(frame_two)
    label_two.pack(side = 'left')
    entry_two.pack(side = 'right')
    frame_two.pack()
 
    def event_insert():
        if entry_one.get() == '' or entry_two.get() == '':
            tkinter.messagebox.showwarning('Reminder', 'Please input your username and password!')
        elif entry_one.get().isdigit() == False or entry_two.get().isdigit() == False:
            tkinter.messagebox.showwarning('Reminder', 'Both the username and password can only be composed of digits. Please try again!')
            entry_one.delete(0, 'end')
            entry_two.delete(0, 'end')
        else:
            con1 = sqlite3.connect('test.db')
            cursor1 = con1.cursor()
            cursor1.execute('select * from user_info where username = ?', (int(entry_one.get()),))
            if cursor1.fetchone() is not None:
                tkinter.messagebox.showwarning('Reminder', 'This username has already been registered!')
                register.destroy()
                entry_one.delete(0, 'end')
                entry_two.delete(0, 'end')
            else:
                values = (int(entry_one.get()), int(entry_two.get()))
                con1.execute('insert into user_info values(?,?)', values)
                tkinter.messagebox.showinfo('Reminder', 'Register successfully!')
                register.destroy()
                cursor1.close()
                con1.commit()
                con1.close()
 
    button_one = Button(register, text = 'Confirm', command = event_insert)
    button_one.pack(pady = 30)

# Create root page

# Step1: Create login window
login_window = Tk()
login_window.title('Login interface')
login_window.geometry('800x600')
canvas = Canvas(login_window, width = 600, height = 400, bg = 'white')
canvas.pack(expand = YES, fill = BOTH)
# Create image label
image = ImageTk.PhotoImage(file = r'background.png')
canvas.create_image(0, 0, image = image, anchor = NW)

# Step2: Create username text input box
username_frame = Frame(login_window, height = 50, width = 500)
username_label = Label(username_frame, text = 'Username:')
username_entry = Entry(username_frame)
username_label.pack(side = 'left')
username_entry.pack()
username_frame.pack(pady = 10)

# Step3: Create password text input box
password_frame = Frame(login_window)
password_label = Label(password_frame, text = "Password:")
password_entry = Entry(password_frame, show = "*")
password_label.pack(side = 'left')
password_entry.pack(side = 'right')
password_frame.pack()

# Step4: Create login button
login_frame = Frame(login_window)
login_button = Button(login_frame, text = "Log in", command = event_login)
register_button = Button(login_frame, text = "Register", command = event_register)
login_button.pack(side = 'left', pady = 30)
register_button.pack(side = 'right', padx = 30, pady = 30)
login_frame.pack()

canvas.pack()
login_window.mainloop()

