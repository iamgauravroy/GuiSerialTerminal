# Gui based Serial terminal program
# Written by Gaurav Roy
# Email: gauravoffice96@gmail.com
import time
import re
import csv
import serial
import pandas as pd
import shutil
from tempfile import NamedTemporaryFile
from datetime import date
import tkinter as tk
import tkinter.scrolledtext as tkscrolledtext
from tkinter import *
import _thread
from tkinter import messagebox
import tkinter.ttk as ttk
import serial.tools.list_ports
import requests
import json
import threading
import datetime
import os

connected     = False
serClosed     = 0
options       = []
def TestingWindow():
    # serial data callback function
    def OnReceiveSerialData(message,filename):
        #displaying data on terminal
        textbox.insert('1.0', message)
        str_message = str(message)
        str_message = str_message

        #Writing Logs in a File
        with open(filename,"a+") as f:                 
            f.writelines(str_message + '\n')

        #Write your own parsing function
        #to display in testvalue 1-12 entry box

    #reading data from uart
    def read_from_port(ser,filename):
        global connected
        global serClosed
        while connected:
            if serClosed == 0:
                reading = ser.readline()
                #print(reading)
                OnReceiveSerialData(reading,filename)
            if serClosed == 1:
                ser.close()
                connected = False
                break

    #commands associated with button presses
    #Open Port and Read Serial Data
    def OpenCommand():
        global connected
        global serClosed
        if button_openclose.cget("text") == 'Open COM Port' and ComPortList.get():
            serial_port = serial.Serial(ComPortList.get())
            serial_port.baudrate = baudrate_edit.get()
            serClosed = 0
            connected = True
            now = datetime.datetime.now()
            # directory (CWD)
            cwd = os.getcwd()
            #LogsFile Creation
            filename = now.strftime('myfile_%H_%M_%S_%d_%m_%Y.txt')
            filename = cwd+"\\"+filename
            #Creating thread for reading data from serial port
            thread = threading.Thread(target=read_from_port, args=(serial_port,filename))
            thread.start()
            button_openclose.config(text='Close COM Port',bg='red',foreground='white')  
            textbox.insert('1.0', "COM Port Opened\r\n")

        elif button_openclose.cget("text") == 'Close COM Port':
            serClosed = 1
            button_openclose.config(text='Open COM Port',bg='green',foreground='white')
            textbox.insert('1.0',"COM Port Closed\r\n")


    #clear Terminal
    def ClearDataCommand():
        textbox.delete('1.0',END)

    #display Testcase
    def DisplayAbout():
        tk.messagebox.showinfo(
        "Header---->Test Cases",
        "\r\n\r\n" 
        "------------------------Test Cases:------------------------------------\r\n\r\n" 
        "Step->1 -------Test Value 1 \r\n" 
        "Step->2 -------Test Value 2\r\n"
        "Step->3 -------Test Value 3\r\n" 
        "Step->4 -------Test Value 4 \r\n"
        "Step->5 -------Test Value 5\r\n"
        "Step->6 -------Test Value 6\r\r\n" 
        )

    #Exit the application
    def Exit():
        root.destroy()

    #Refresh the ComPort
    def Refresh():
        global options
        options.clear()
        ser=serial.tools.list_ports.comports(include_links=False)
        for i in ser:
            options.append(i.device)
        if len(options) == 0:
            tk.messagebox.showinfo(
            "Connect Device",
            "\r\n\r\n" 
            "***********************************************************\r\n\r\n"
            "                         No Device Found                     \r\n\r\n" 
            "***********************************************************\r\n")
        else:
            ComPortChoosen['values'] = (options)
           

    #run the main loop once each 200 ms
    def sdterm_main():
        root.after(200, sdterm_main)
    
#===================================================================================================
#SecondWindow Created.
    SecondWindow = Toplevel()
    SecondWindow.title("Automation Tool")
    SecondWindow.geometry('1350x750+0+0')


    frame2 = tk.Frame(SecondWindow,bg='#3EB5FE')
    frame2.pack(side='left',fill=Y)

    ButtonFrame = LabelFrame(frame2,width=220,padx=10,bg='#3EB5FE')
    ButtonFrame.pack(side='left')

    textbox = tkscrolledtext.ScrolledText(master=frame2,wrap='word',width=140, height=45) #width=characters, height=lines
    textbox.pack(side='bottom', fill='y', anchor="ne",expand=True, padx=0, pady=0)
    textbox.config(background='black',foreground='white')


    ComPortList = tk.StringVar()
    ComPortChoosen = ttk.Combobox(frame2, width = 12, textvariable = ComPortList)
    ser=serial.tools.list_ports.comports(include_links=False)
    for i in ser:
        options.append(i.device)
    ComPortChoosen['values'] = (options)

    ComPortChoosen.place(x=100,y=88)
    ComPortChoosen.current()


    # COM Port open/close button
    RefreshButton = Button(master=frame2,text="Refresh",width=16,borderwidth=5,command=Refresh)
    RefreshButton.config(font="bold",bg='gray60',foreground='black')
    RefreshButton.place(x=18,y=5)

    # COM Port open/close button
    button_openclose = Button(master=frame2,text="Open COM Port",width=16,borderwidth=5,command=OpenCommand)
    button_openclose.config(font="bold",bg='forest green',foreground='white')
    button_openclose.place(x=18,y=45)

    #Test Case button
    button_about = Button(master=frame2,text="Test Case",width=16,borderwidth=5,bg='gray50',foreground='black',command=DisplayAbout)
    button_about.config(font="bold")
    button_about.place(x=18,y=630)

    #Clear Rx Data button
    button_cleardata = Button(master=frame2,text="Clear Rx",width=6,borderwidth=5,bg='gray50',foreground='black',command=ClearDataCommand)
    button_cleardata.config(font="bold")
    button_cleardata.place(x=117,y=670)

    #Exit
    button_about = Button(master=frame2,text="Exit",width=7,borderwidth=5,bg='gray50',foreground='black',command=Exit)
    button_about.config(font="bold")
    button_about.place(x=18,y=670)

    #COM Port label
    label_comport = Label(master=frame2,width=8,text="COM Port",bg='#3EB5FE',foreground='black')
    label_comport.place(x=20,y=90)             #x=10 y=100
    label_comport.config(font=('helvetica',11,'bold'))

    #Baud Rate label
    label_baud = Label(master=frame2,width=8,text="Baud Rate",bg='#3EB5FE',foreground='black')
    label_baud.config(font=('helvetica',11,'bold'))
    label_baud.place(x=20,y=118)

    # Combobox creation
    baudrate_edit = tk.StringVar()
    BaudrateChoosen = ttk.Combobox(frame2, width = 12, textvariable = baudrate_edit)

    BaudrateChoosen['values'] = (' 110', 
                          ' 300',
                          ' 600',
                          ' 1200',
                          ' 2400',
                          ' 4800',
                          ' 9600',
                          ' 14400',
                          ' 19200',
                          ' 38400',
                          ' 57600',
                          ' 115200',
                          ' 230400',
                          ' 460800',
                          ' 921600')
    BaudrateChoosen.place(x=100,y=118)
    BaudrateChoosen.current()


    #Label For TestID
    label_testId = Label(master=frame2,width=19,text="Test ID",bg='dark orange',foreground='black')
    label_testId.config(font="bold")
    label_testId.place(x=20,y=145)

    #Entry Box TestID
    entrybox_testId = Entry(master=frame2,width=19)
    entrybox_testId.place(x=20,y=175)
    entrybox_testId.config(font="bold")


    #Label of Test Value 1
    label_testVal_1 = Label(master=frame2,width=8,text="Test Val-1",bg='#3EB5FE',foreground='black')
    label_testVal_1.config(font=('helvetica',13,'bold'))
    label_testVal_1.place(x=0,y=200)

    #Entry Box for Test Value-1
    entrybox_testVal_1 = Entry(master=frame2,width=10)
    entrybox_testVal_1.place(x=100,y=200)
    entrybox_testVal_1.config(font="bold")


    #Label for Test Value -2
    label_testVal_2 = Label(master=frame2,width=8,text="Test Val-2",bg='#3EB5FE',foreground='black')
    label_testVal_2.config(font=('helvetica',13,'bold'))
    label_testVal_2.place(x=0,y=230)

    #Entry Box for Test Val-2 
    entrybox_testVal_2 = Entry(master=frame2,width=10)
    entrybox_testVal_2.place(x=100,y=230)
    entrybox_testVal_2.config(font="bold")


    #Label for Test Value-3
    label_testVal_3 = Label(master=frame2,width=8,text="Test Val-3 ",bg='#3EB5FE',foreground='black')
    label_testVal_3.config(font=('helvetica',13,'bold'))
    label_testVal_3.place(x=0,y=260)

    #Entry Box for Test Value-3 
    entrybox_testVal_3 = Entry(master=frame2,width=10)
    entrybox_testVal_3.config(font="bold")
    entrybox_testVal_3.place(x=100,y=260)


    #Label for Test-Val-4
    label_testVal_4 = Label(master=frame2,width=10,text="Test Val-4 ",bg='#3EB5FE',foreground='black')
    label_testVal_4.config(font=('helvetica',13,'bold'))
    label_testVal_4.place(x=0,y=290)

    #Entry Box for testVal_4 
    entrybox_testVal_4 = Entry(master=frame2,width=10)
    entrybox_testVal_4.place(x=100,y=290)
    entrybox_testVal_4.config(font="bold")


    #Label for Test Val-5
    label_testVal_5 = Label(master=frame2,width=10,text="Test Val-5 ",bg='#3EB5FE',foreground='black')
    label_testVal_5.config(font=('helvetica',13,'bold'))
    label_testVal_5.place(x=0,y=320)

    #Entry Box for Test Val-5 
    entrybox_testVal_5 = Entry(master=frame2,width=10)
    entrybox_testVal_5.place(x=100,y=320)
    entrybox_testVal_5.config(font="bold")

    #Label for Test Val-6
    label_testVal_6 = Label(master=frame2,width=8,text="Test Val-6 ",bg='#3EB5FE',foreground='black')
    label_testVal_6.config(font=('helvetica',13,'bold'))
    label_testVal_6.place(x=0,y=350)

    #Entry Box for Test Val-6 
    entrybox_testVal_6 = Entry(master=frame2,width=10)
    entrybox_testVal_6.place(x=100,y=350)
    entrybox_testVal_6.config(font="bold")

    #Label for Test Val-7
    label_testVal_7 = Label(master=frame2,width=8,text="Test Val-7 ",bg='#3EB5FE',foreground='black')
    label_testVal_7.config(font=('helvetica',13,'bold'))
    label_testVal_7.place(x=0,y=380)

    #Entry Box for Test Val-7  
    entrybox_testVal_7 = Entry(master=frame2,width=10)
    entrybox_testVal_7.place(x=100,y=380)
    entrybox_testVal_7.config(font="bold")


    #Label for Test Val-8 
    label_testVal_8 = Label(master=frame2,width=8,text="Test Val-8",bg='#3EB5FE',foreground='black')
    label_testVal_8.config(font=('helvetica',13,'bold'))
    label_testVal_8.place(x=0,y=410)

    #Entry Box for Test Val-8
    entrybox_testVal_8 = Entry(master=frame2,width=10)
    entrybox_testVal_8.place(x=100,y=410)
    entrybox_testVal_8.config(font="bold")


    #Label for Test Val-9  
    label_testVal_9 = Label(master=frame2,width=8,text="Test Val-9",bg='#3EB5FE',foreground='black')
    label_testVal_9.config(font=('helvetica',13,'bold'))
    label_testVal_9.place(x=0,y=440)

    #Entry Box Test Val-9
    entrybox_testVal_9 = Entry(master=frame2,width=10)
    entrybox_testVal_9.place(x=100,y=440)
    entrybox_testVal_9.config(font="bold")


    #Label for Test Val-10  
    label_testVal_10 = Label(master=frame2,width=0,text="Test Val-10",bg='#3EB5FE',foreground='black')
    label_testVal_10.config(font=('helvetica',11,'bold'))
    label_testVal_10.place(x=0,y=470)

    #Entry Box for Test Val-10
    entrybox_testVal_10 = Entry(master=frame2,width=10)
    entrybox_testVal_10.place(x=100,y=470)
    entrybox_testVal_10.config(font="bold")

    #Label for Test Val-11
    label_testVal_11 = Label(master=frame2,width=10,text="Test Val-11",bg='#3EB5FE',foreground='black')
    label_testVal_11.config(font=('helvetica',13,'bold'))
    label_testVal_11.place(x=0,y=500)

    #Entry Box for Test Val-11 
    entrybox_testVal_11 = Entry(master=frame2,width=10)
    entrybox_testVal_11.place(x=100,y=500)
    entrybox_testVal_11.config(font="bold")


    label_testVal_12 = Label(master=frame2,width=0,text="Test Val-12",bg='#3EB5FE',foreground='black')
    label_testVal_12.config(font=('helvetica',11,'bold'))
    label_testVal_12.place(x=0,y=535)

    #Entry Box for Test Val-12 
    entrybox_testVal_12 = Entry(master=frame2,width=10)
    entrybox_testVal_12.place(x=100,y=535)
    entrybox_testVal_12.config(font="bold")
    root.after(200, sdterm_main)

#===========================================Second Window==============================
def LoginSystem():
    global username
    global password
    username = Username.get()
    password = Password.get()

    try:
        #Post Username and Password to get from server
        #payload = {'userid': username, 'password': password}
        #url = ''
        #response = requests.post(url)
        #responseJson = response.json()
        #print("responseJson ", responseJson)
        if(username):
            print('Login success')
            #print('userid = '+responseJson['userid'])
            Username.config(state='disabled')
            Password.config(state='disabled')
            root.withdraw()
            TestingWindow()
        else:
            tk.messagebox.showinfo(
                "Error",
                "Enter Correct Password"
                )
    except requests.exceptions.HTTPError as errh:
        tk.messagebox.showinfo(
                "Error Connecting",
                "Login Error",
                )
    except requests.exceptions.ConnectionError as errc:
        tk.messagebox.showinfo(
                "Error Connecting",
                "Login Error",
                )
        print ("Error Connecting:",errc)
    except requests.exceptions.Timeout as errt:
        tk.messagebox.showinfo(
                "Error Connecting",
                "Login Error",
                )
    except requests.exceptions.RequestException as err:
        tk.messagebox.showinfo(
                "Error Connecting",
                "Login Error",
                )    

def Exit():
    root.destroy()
#============================================================================================================
#Reset Useername and Pawword
def ResetUserPass():
    global username
    global password
    Username.delete(0,END)
    Password.delete(0,END)
    username = 0
    password = 0
#============================================================================================================

# create a Tk root window
root = tk.Tk() 
root.title( "Testing Tool" )
#fullscreen for windows
root.geometry('1350x750+0+0')
root.config(bg='#54DFF8')
#==================================Label and Entry===========================================================

UsernameLabel = Label(root,text='Username',bg='#54DFF8',font=('arial',20,'bold'))
UsernameLabel.place(x=430,y=290)

Username = Entry(root,font=('arial',15,'bold'))
Username.place(x=600,y=295)

PasswordLabel = Label(root,text='Password',bg='#54DFF8',font=('arial',20,'bold'))
PasswordLabel.place(x=430,y=330)

Password = Entry(root,font=('arial',15,'bold'))
Password.config(show="*")
Password.place(x=600,y=330)

#Login Button
LoginButton = Button(root,text="Login Button",width=10,borderwidth=4,bg='gray30',foreground='white',command=LoginSystem)
LoginButton.config(font="bold")
LoginButton.place(x=600,y=380)

#Reset Button
ResetButton = Button(root,text="Reset Button",width=10,borderwidth=4,bg='gray30',foreground='white',command=ResetUserPass)
ResetButton.config(font="bold")
ResetButton.place(x=730,y=380)

#Exit Button
ExitButton = Button(root,text="Exit Button",width=19,borderwidth=4,bg='gray30',foreground='white',command=Exit)
ExitButton.config(font="bold")
ExitButton.place(x=620,y=430)    

# The main loop
root.mainloop()
