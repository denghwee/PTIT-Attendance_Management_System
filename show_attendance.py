import pandas as pd
from glob import glob
import os
import tkinter
import csv
import tkinter as tk
from tkinter import *

def subjectchoose(text_to_speech):
    def calculate_attendance():
        Subject = tx.get()
        if Subject=="":
            t='Vui lòng điền tên môn học.'
            text_to_speech(t)
        filename = f"Attendance/{Subject}/attendance.csv"
        filenames = glob(
            f"Attendance/{Subject}/{Subject}*.csv"
        )
        print(filenames)
        df = [pd.read_csv(f) for f in filenames]
        newdf = df[0]
        for i in range(1, len(df)):
            newdf = newdf.merge(df[i], how="outer")
        newdf.fillna(0, inplace=True)
        newdf["Attendance"] = 0
        for i in range(len(newdf)):
            newdf['Attendance'] = newdf['Attendance'].astype('object')
            for i in range(len(newdf)):
                attendance_percentage = str(int(round(newdf.iloc[i, 2:-1].mean() * 100))) + '%'
                newdf.loc[i, "Attendance"] = attendance_percentage
        original_dir = os.getcwd()
        os.chdir(f"Attendance/{Subject}")
        newdf.to_csv("attendance.csv", index=False)
        os.chdir(original_dir)

        root = tkinter.Tk()
        root.title("Attendance of "+Subject)
        root.configure(background="#24293E")
        with open(filename) as file:
            reader = csv.reader(file)
            r = 0
            for col in reader:
                c = 0
                for row in col:

                    label = tkinter.Label(
                        root,
                        width=10,
                        height=1,
                            fg="#F4F5FC",
                        font=("times", 15, " bold "),
                        bg="#24293E",
                        text=row,
                        relief=tkinter.RIDGE,
                    )
                    label.grid(row=r, column=c)
                    c += 1
                r += 1
        root.mainloop()
        print(newdf)

    subject = Tk()
    # windo.iconbitmap("AMS.ico")
    subject.title("Thống kê")
    subject.geometry("780x480")
    subject.resizable(0, 0)
    subject.configure(background="#24293E")
    # subject_logo = Image.open("UI_Image/0004.png")
    # subject_logo = subject_logo.resize((50, 47), Image.ANTIALIAS)
    # subject_logo1 = ImageTk.PhotoImage(subject_logo)
    titl = tk.Label(subject, bg="#24293E", relief=RIDGE, bd=10, font=("Be Vietnam Pro Bold", 30))
    titl.pack(fill=X)
    # l1 = tk.Label(subject, image=subject_logo1, bg="#24293E",)
    # l1.place(x=100, y=10)
    titl = tk.Label(
        subject,
        text="ĐIỀN TÊN MÔN HỌC",
        bg="#24293E",
        fg="#F4F5FC",
        font=("Be Vietnam Pro Bold", 25),
    )
    titl.place(x=220, y=12)

    def Attf():
        sub = tx.get()
        if sub == "":
            t = "VUI LÒNG ĐIỀN TÊN MÔN HỌC!!!"
            text_to_speech(t)
        else:
            import glob
            import os

            folder_path = f"Attendance/{sub}"
            csv_files = glob.glob(f"{folder_path}/attendance.csv")
            if not csv_files:
                t = f"No attendance files found for {sub}!"
                text_to_speech(t)
            else:
                latest_file = max(csv_files, key=os.path.getctime)
                os.startfile(latest_file)


    attf = tk.Button(
        subject,
        text="XEM TRANG TÍNH",
        command=Attf,
        bd=7,
        font=("Be Vietnam Pro Bold", 15),
        bg="#24293E",
        fg="#F4F5FC",
        height=2,
        width=15,
        relief=RIDGE,
    )
    attf.place(x=420, y=200)

    sub = tk.Label(
        subject,
        text="Môn học",
        width=10,
        height=2,
        bg="#24293E",
        fg="#F4F5FC",
        bd=5,
        relief=RIDGE,
        font=("Be Vietnam Pro Bold", 15),
    )
    sub.place(x=50, y=100)

    tx = tk.Entry(
        subject,
        width=15,
        bd=5,
        bg="#24293E",
        fg="#F4F5FC",
        relief=RIDGE,
        font=("Be Vietnam Pro Bold", 30, "bold"),
    )
    tx.place(x=200, y=100)

    fill_a = tk.Button(
        subject,
        text="XEM THỐNG KÊ",
        command=calculate_attendance,
        bd=7,
        font=("Be Vietnam Pro Bold", 15),
        bg="#24293E",
        fg="#F4F5FC",
        height=2,
        width=14,
        relief=RIDGE,
    )
    fill_a.place(x=200, y=200)
    subject.mainloop()
