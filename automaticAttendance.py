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
import tkinter.ttk as tkk
import tkinter.font as font

haarcasecade_path = "haarcascade_frontalface_default.xml"
trainimagelabel_path = (
    "TrainingImageLabel/Trainner.yml"
)
trainimage_path = "TrainingImage"
studentdetail_path = (
    "StudentDetails/studentdetails.csv"
)
attendance_path = "Attendance"
# for choose subject and fill attendance
def subjectChoose(text_to_speech):
    def FillAttendance():
        sub = tx.get()
        now = time.time()
        future = now + 20
        print(now)
        print(future)
        if sub == "":
            t = "VUI LÒNG ĐIỀN TÊN MÔN HỌC!"
            text_to_speech(t)
        else:
            try:
                recognizer = cv2.face.LBPHFaceRecognizer_create()
                try:
                    recognizer.read(trainimagelabel_path)
                except:
                    e = "Không tìm thấy MODEL, vui lòng huấn luyện MODEL!"
                    Notifica.configure(
                        text=e,
                        bg="#24293E",
                        fg="#F4F5FC",
                        width=33,
                        font=("Be Vietnam Pro Bold", 15, "bold"),
                    )
                    Notifica.place(x=20, y=250)
                    text_to_speech(e)
                facecasCade = cv2.CascadeClassifier(haarcasecade_path)
                df = pd.read_csv(studentdetail_path)
                cam = cv2.VideoCapture(0)
                font = cv2.FONT_HERSHEY_SIMPLEX
                col_names = ["Enrollment", "Name"]
                attendance = pd.DataFrame(columns=col_names)
                while True:
                    ___, im = cam.read()
                    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
                    faces = facecasCade.detectMultiScale(gray, 1.2, 5)
                    for (x, y, w, h) in faces:
                        global Id

                        Id, conf = recognizer.predict(gray[y : y + h, x : x + w])
                        if conf < 70:
                            print(conf)
                            global Subject
                            global aa
                            global date
                            global timeStamp
                            Subject = tx.get()
                            ts = time.time()
                            date = datetime.datetime.fromtimestamp(ts).strftime(
                                "%Y-%m-%d"
                            )
                            timeStamp = datetime.datetime.fromtimestamp(ts).strftime(
                                "%H:%M:%S"
                            )
                            aa = df.loc[df["Enrollment"] == Id]["Name"].values
                            global tt
                            tt = str(Id) + "-" + aa
                            # En='1604501160'+str(Id)
                            attendance.loc[len(attendance)] = [
                                Id,
                                aa,
                            ]
                            cv2.rectangle(im, (x, y), (x + w, y + h), (0, 260, 0), 4)
                            cv2.putText(
                                im, str(tt), (x + h, y), font, 1, (255, 255, 0,), 4
                            )
                        else:
                            Id = "Unknown"
                            tt = str(Id)
                            cv2.rectangle(im, (x, y), (x + w, y + h), (0, 25, 255), 7)
                            cv2.putText(
                                im, str(tt), (x + h, y), font, 1, (0, 25, 255), 4
                            )
                    if time.time() > future:
                        break

                    attendance = attendance.drop_duplicates(
                        ["Enrollment"], keep="first"
                    )
                    cv2.imshow("Filling Attendance...", im)
                    key = cv2.waitKey(30) & 0xFF
                    if key == 27:
                        break

                ts = time.time()
                print(aa)
                # attendance["date"] = date
                # attendance["Attendance"] = "P"
                attendance[date] = 1
                date = datetime.datetime.fromtimestamp(ts).strftime("%Y-%m-%d")
                timeStamp = datetime.datetime.fromtimestamp(ts).strftime("%H:%M:%S")
                Hour, Minute, Second = timeStamp.split(":")
                path = os.path.join(attendance_path, Subject)
                os.makedirs(path, exist_ok=True)
                fileName = (
                    f"{path}/"
                    + Subject
                    + "_"
                    + date
                    + "_"
                    + Hour
                    + "-"
                    + Minute
                    + "-"
                    + Second
                    + ".csv"
                )
                attendance = attendance.drop_duplicates(["Enrollment"], keep="first")
                print(attendance)
                attendance.to_csv(fileName, index=False)

                m = "Hoàn thành điểm danh của môn " + Subject
                Notifica.configure(
                    text=m,
                    bg="#24293E",
                    fg="#F4F5FC",
                    width=33,
                    relief=RIDGE,
                    bd=5,
                    font=("Be Vietnam Pro Bold", 15, "bold"),
                )
                text_to_speech(m)

                Notifica.place(x=50, y=350)

                cam.release()
                cv2.destroyAllWindows()

                import csv
                import tkinter

                root = tkinter.Tk()
                root.title("Điểm danh của " + Subject)
                root.configure(background="#24293E")
                with open(fileName, newline="") as file:
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
                                font=("Be Vietnam Pro Bold", 15, " bold "),
                                bg="#24293E",
                                text=row,
                                relief=tkinter.RIDGE,
                            )
                            label.grid(row=r, column=c)
                            c += 1
                        r += 1
                root.mainloop()
                print(attendance)
            except Exception as e:
                print(f"Error occurred: {e}")
                f = "Không có khuôn mặt nào trong khung hình"
                text_to_speech(f)

    ###windo is frame for subject chooser
    subject = Tk()
    # windo.iconbitmap("AMS.ico")
    subject.title("Điểm danh")
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
    Notifica = tk.Label(
        subject,
        text="ĐIỀN THÀNH CÔNG",
        bg="#F4F5FC",
        fg="#24293E",
        width=33,
        height=2,
        font=("Be Vietnam Pro Bold", 15, "bold"),
    )

    def Attf():
        sub = tx.get()
        if sub == "":
            t = "VUI LÒNG ĐIỀN TÊN MÔN HỌC!!!"
            text_to_speech(t)
        else:
            import glob
            import os

            folder_path = f"Attendance/{sub}"
            csv_files = glob.glob(f"{folder_path}/*.csv")
            if not csv_files:
                t = f"Không có file tồn tại!"
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
        width=14,
        relief=RIDGE,
    )
    attf.place(x=400, y=200)

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
        text="ĐIỂM DANH",
        command=FillAttendance,
        bd=7,
        font=("Be Vietnam Pro Bold", 15),
        bg="#24293E",
        fg="#F4F5FC",
        height=2,
        width=12,
        relief=RIDGE,
    )
    fill_a.place(x=200, y=200)
    subject.mainloop()