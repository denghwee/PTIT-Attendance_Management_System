import tkinter as tk
from tkinter import *
import os, cv2
import shutil
import csv
import numpy as np
from PIL import ImageTk, Image
import pandas as pd
import datetime
import time
import tkinter.font as font
import pyttsx3

# project module
import show_attendance
import takeImage
import trainImage
import automaticAttendance

# engine = pyttsx3.init()
# engine.say("Welcome!")
# engine.say("Please browse through your options..")
# engine.runAndWait()


def text_to_speech(user_text):
    engine = pyttsx3.init()
    engine.say(user_text)
    engine.runAndWait()


haarcasecade_path = "haarcascade_frontalface_default.xml"
trainimagelabel_path = (
    "TrainingImageLabel/Trainner.yml"
)
trainimage_path = "TrainingImage"
if not os.path.exists(trainimage_path):
    os.makedirs(trainimage_path)

studentdetail_path = (
    "StudentDetails/studentdetails.csv"
)
attendance_path = "Attendance"

def frm_mainMenu():
    # Create Main Window
    window = tk.Tk()
    window.geometry('1920x1080')
    window.state('zoomed')
    window.title('Hệ thống nhận diện khuôn mặt')

    # Set background color
    window.configure(bg='#24293E')

    # Create a frame for the text
    text_frame = tk.Frame(window, bg='#24293E')
    text_frame.pack(side='left', padx=50, pady=50, anchor='w')

    # Create a frame for the placeholder image
    image_frame = tk.Frame(window, bg='#24293E')
    image_frame.pack(side='right', padx=50, pady=50)

    # Create the heading label
    heading_label = tk.Label(text_frame,
                             text="HỆ THỐNG NHẬN DIỆN KHUÔN MẶT",
                             font=('Be Vietnam Pro ExtraBold', 30),
                             fg='#F4F5FC',
                             bg='#24293E',
                             anchor='w',
                             justify='left')
    heading_label.pack(fill='x', padx=0, pady=40)

    # Create the description label
    description_label = tk.Label(text_frame,
                                 text=
                                 "Hệ thống cho phép:\n"
                                 "1) ĐĂNG KÝ khuôn mặt vào hệ thống điểm danh\n"
                                 "2) HUẤN LUYỆN mô hình để học các khuôn mặt đăng ký trong hệ thống\n"
                                 "3) ĐIỂM DANH các sinh viên tham gia buổi học của một môn học cụ thể\n"
                                 "4) KIỂM TRA thống kê điểm danh các sinh viên trong từng môn học\n",
                                 font=("Be Vietnam Pro", 12),
                                 fg='#F4F5FC',
                                 bg='#24293E',
                                 anchor='w',
                                 justify='left')
    description_label.pack(fill='x', padx=5, pady=15)

    # Create the button
    button = tk.Button(text_frame,
                       text='Continue',
                       font=('Be Vietnam Pro', 16), 
                       fg='#F4F5FC',  # Text color (foreground)
                       bg='#8EBBFF',   # Background color
                       activebackground='#8EBBFF',  # Color when button is clicked
                       activeforeground='#F4F5FC',
                       command=lambda: transition(window, frm_functionMenu))
    button.pack(fill='x', padx=5, pady=10)

    # Create the placeholder image
    mainMenu_image = tk.PhotoImage(file='data/images/mainMenu.png')
    image_label = tk.Label(image_frame, image=mainMenu_image, width=1920, height=1080)
    image_label.pack()

    # Set background color
    window.configure(bg='#24293E')

    window.mainloop()

def frm_functionMenu():
    # Create window
    window = tk.Tk()
    window.geometry('1920x1080')
    window.state('zoomed')
    window.title('Hệ thống nhận diện khuôn mặt')

    # Set background color
    window.configure(bg='#24293E')

    # Create a frame for the text
    text_frame = tk.Frame(window, bg='#24293E')
    text_frame.pack(side='left', padx=50, pady=50, anchor='w')

    # Create a frame for the buttons in the right
    button_frame = tk.Frame(window, bg='#24293E')
    button_frame.pack(side='right', padx=50, pady=50, anchor='e')

    # Create the heading label
    heading_label = tk.Label(text_frame,
                             text="HỆ THỐNG NHẬN DIỆN KHUÔN MẶT",
                             font=('Be Vietnam Pro ExtraBold', 30),
                             fg='#F4F5FC',
                             bg='#24293E',
                             anchor='w',
                             justify='left')
    heading_label.pack(fill='x', padx=0, pady=40)

    # Create the description label
    description_label = tk.Label(text_frame,
                                 text=
                                 "Chọn 'ĐĂNG KÝ' để đăng ký khuôn mặt vào hệ thống điểm danh                               \n\n"
                                 "Chọn 'ĐIỂM DANH' để điểm danh các sinh viên tham gia buổi học                            \n\n"
                                 "Chọn 'THỐNG KÊ' để thống kê tỉ lệ tham gia các buổi học của các sinh viên của một môn học\n\n",
                                 font=('Be Vietnam Pro', 12),
                                 fg='#F4F5FC',
                                 bg='#24293E',
                                 anchor='w',
                                 justify='left')
    description_label.pack(fill='x', padx=5, pady=15)

    # Create the buttons
        # Register button
    register_button = tk.Button(button_frame,
                       text='ĐĂNG KÝ',
                       font=('Be Vietnam Pro', 16), 
                       fg='#F4F5FC',  # Text color (foreground)
                       bg='#8EBBFF',   # Background color
                       activebackground='#8EBBFF',  # Color when button is clicked
                       activeforeground='#F4F5FC',
                       command=TakeImageUI)
    register_button.pack(fill='x', padx=5, pady=10)

        # Attendance button
    attendance_button = tk.Button(button_frame,
                       text='ĐIỂM DANH',
                       font=('Be Vietnam Pro', 16), 
                       fg='#F4F5FC',  # Text color (foreground)
                       bg='#8EBBFF',   # Background color
                       activebackground='#8EBBFF',  # Color when button is clicked
                       activeforeground='#F4F5FC',
                       command=automatic_attendance)
    attendance_button.pack(fill='x', padx=5, pady=10)

        # STATS button
    stats_button = tk.Button(button_frame,
                       text='THỐNG KÊ',
                       font=('Be Vietnam Pro', 16), 
                       fg='#F4F5FC',  # Text color (foreground)
                       bg='#8EBBFF',   # Background color
                       activebackground='#8EBBFF',  # Color when button is clicked
                       activeforeground='#F4F5FC',
                       command=view_attendance)
    stats_button.pack(fill='x', padx=5, pady=10)

    window.mainloop()

# to destroy screen
def del_sc1():
    sc1.destroy()

# error message for name and no
def err_screen():
    global sc1
    sc1 = tk.Tk()
    sc1.geometry("400x110")
    sc1.iconbitmap("AMS.ico")
    sc1.title("Warning!!")
    sc1.configure(background="#24293E")
    sc1.resizable(0, 0)
    tk.Label(
        sc1,
        text="Vui lòng điền đẩy đủ thông tin!!!",
        fg="#F4F5FC",
        bg="#24293E",
        font=("Be Vietnam Pro Bold", 20, " bold "),
    ).pack()
    tk.Button(
        sc1,
        text="OK",
        command=del_sc1,
        fg="#F4F5FC",
        bg="#24293E",
        width=9,
        height=1,
        activebackground="Red",
        font=("Be Vietnam Pro Bold", 20, " bold "),
    ).place(x=110, y=50)


def testVal(inStr, acttyp):
    if acttyp == "1":  # insert
        if not inStr.isdigit():
            return False
    return True

def take_image(txt1, txt2, message):
    l1 = txt1.get()
    l2 = txt2.get()
    takeImage.TakeImage(
        l1,
        l2,
        haarcasecade_path,
        trainimage_path,
        message,
        err_screen,
        text_to_speech,
    )
    txt1.delete(0, "end")
    txt2.delete(0, "end")


def TakeImageUI():
    ImageUI = Tk()
    ImageUI.title("Chụp hình ảnh..")
    ImageUI.geometry("780x480")
    ImageUI.configure(background="#24293E")
    ImageUI.resizable(0, 0)
    titl = tk.Label(ImageUI,
                    bg="#24293E",
                    relief=RIDGE,
                    bd=10,
                    font=("Be Vietnam Pro Bold", 35))
    titl.pack(fill=X)
    # image and title
    titl = tk.Label(
        ImageUI, text="ĐĂNG KÝ NHẬN DIỆN KHUÔN MẶT", bg="#24293E", fg="#F4F5FC", font=("Be Vietnam Pro Bold", 20), justify='center',
    )
    titl.place(x=180, y=12)

    # heading
    a = tk.Label(
        ImageUI,
        text="ĐIỀN THÔNG TIN",
        bg="#24293E",
        fg="#F4F5FC",
        bd=10,
        font=("Be Vietnam Pro Bold", 24),
    )
    a.place(x=270, y=75)

    # ER no
    lbl1 = tk.Label(
        ImageUI,
        text="MSV",
        width=10,
        height=2,
        bg="#24293E",
        fg="#F4F5FC",
        bd=5,
        relief=RIDGE,
        font=("Be Vietnam Pro Bold", 12),
    )
    lbl1.place(x=120, y=140)
    txt1 = tk.Entry(
        ImageUI,
        width=17,
        bd=5,
        validate="key",
        bg="#24293E",
        fg="#F4F5FC",
        relief=RIDGE,
        font=("Be Vietnam Pro Bold", 25, "bold"),
    )
    txt1.place(x=250, y=140)
    txt1["validatecommand"] = (txt1.register(testVal), "%P", "%d")

    # name
    lbl2 = tk.Label(
        ImageUI,
        text="Họ tên",
        width=10,
        height=2,
        bg="#24293E",
        fg="#F4F5FC",
        bd=5,
        relief=RIDGE,
        font=("Be Vietnam Pro Bold", 12),
    )
    lbl2.place(x=120, y=210)
    txt2 = tk.Entry(
        ImageUI,
        width=17,
        bd=5,
        bg="#24293E",
        fg="#F4F5FC",
        relief=RIDGE,
        font=("Be Vietnam Pro Bold", 25, "bold"),
    )
    txt2.place(x=250, y=210)

    lbl3 = tk.Label(
        ImageUI,
        text="Thông báo",
        width=10,
        height=2,
        bg="#24293E",
        fg="#F4F5FC",
        bd=5,
        relief=RIDGE,
        font=("Be Vietnam Pro Bold", 12),
    )
    lbl3.place(x=120, y=280)

    message = tk.Label(
        ImageUI,
        text="",
        width=39,
        height=2,
        bd=5,
        bg="#24293E",
        fg="#F4F5FC",
        relief=RIDGE,
        font=("Be Vietnam Pro Bold", 12, "bold"),
    )
    message.place(x=250, y=280)

    def take_image():
        l1 = txt1.get()
        l2 = txt2.get()
        takeImage.TakeImage(
            l1,
            l2,
            haarcasecade_path,
            trainimage_path,
            message,
            err_screen,
            text_to_speech,
        )
        txt1.delete(0, "end")
        txt2.delete(0, "end")

    # take Image button
    # image
    takeImg = tk.Button(
        ImageUI,
        text="CHỤP ẢNH",
        command=take_image,
        bd=10,
        font=("Be Vietnam Pro Bold", 18),
        bg="#24293E",
        fg="#F4F5FC",
        height=2,
        width=12,
        relief=RIDGE,
    )
    takeImg.place(x=130, y=355)

    def train_image():
        trainImage.TrainImage(
            haarcasecade_path,
            trainimage_path,
            trainimagelabel_path,
            message,
            text_to_speech,
        )

    # train Image function call
    trainImg = tk.Button(
        ImageUI,
        text="CẬP NHẬT",
        command=train_image,
        bd=10,
        font=("Be Vietnam Pro Bold", 18),
        bg="#24293E",
        fg="#F4F5FC",
        height=2,
        width=12,
        relief=RIDGE,
    )
    trainImg.place(x=410, y=355)

def automatic_attendance():
    automaticAttendance.subjectChoose(text_to_speech)

def view_attendance():
    show_attendance.subjectchoose(text_to_speech)

def transition(window, next_window, sentence = ''):
    if sentence != '':
        print(sentence)
    window.destroy()
    next_window()


if __name__ == '__main__':
    frm_mainMenu()