import tkinter as tk
from tkinter import messagebox
import mysql.connector
from datetime import date
import matplotlib.pyplot as plt
from tkinter import ttk

db = mysql.connector.connect(host="localhost",user="root",password="mysql",database="attendance_system")
cursor = db.cursor()

def login():
    username = username_entry.get()
    password = password_entry.get()

    query = "SELECT * FROM tlogin WHERE name = %s AND password = %s"
    cursor.execute(query, (username, password))
    result = cursor.fetchone()

    if result:
        messagebox.showinfo("Login Successful", "Welcome, " + username)
        show_options()
         
    else:
        messagebox.showerror("Login Failed", "Invalid username or password")

def register():
    name = reg_name_entry.get()
    class_val = reg_class_entry.get()
    email = reg_email_entry.get()
    password = reg_password_entry.get()

    query = "INSERT INTO tlogin (name, class, email, password) VALUES (%s, %s, %s, %s)"
    cursor.execute(query, (name, class_val, email, password))
    db.commit()
    messagebox.showinfo("Registration Successful", "You are now registered.")

def att_trends():
    import matplotlib.pyplot as plt
    import mysql.connector as mc
    import pandas as pd

    c = mc.connect(host="localhost", user="root", password="mysql", database="attendance_system")
    cr = c.cursor()

    cr.execute("SELECT class, COUNT(attendance)/2 FROM dailyatt WHERE date=curdate() and attendance in ('present','pstar') and shift in('1','2') GROUP BY class")
    rows = cr.fetchall()

    # Create a DataFrame from the fetched data
    df = pd.DataFrame(rows, columns=['Class', 'No of students Present'])

    # Convert 'No of students Present' column to integers
    df['No of students Present'] = df['No of students Present'].astype(int)

    # Plotting
    plt.figure(figsize=(10, 6))  # Adjust the figure size as needed
    plt.bar(df['Class'], df['No of students Present'])
    plt.xlabel('Class')
    plt.ylabel('No of students Present')
    plt.title('Attendance per Class')
    plt.xticks(rotation=45)  # Rotate x-axis labels for better visibility

    # Set y-axis ticks to specific values
    plt.yticks(range(1, df['No of students Present'].max() + 1))  # Set y-axis ticks from 1 to the maximum present value

    plt.tight_layout()  # Adjust layout for better appearance
    plt.show()

    # Close the connection
    c.close()


def daily_attendancenext(c_var,d_var):
    root1.destroy()
    root2=Tk()
    root2.title("Attendance System")
    root2.geometry('700x530')
    
    import mysql.connector as mc
    from tkinter import ttk
    c=mc.connect(host="localhost",user="root",password="mysql",database="attendance_system")
    cr=c.cursor()
    

    frame=Frame(root2)
    frame.grid(row=3,column=3)
    
    tree=ttk.Treeview(frame)
    tree["columns"]=("","","","","")
    
    tree.heading("0",text="USN",anchor=CENTER)
    tree.heading("1",text="RollNo",anchor=CENTER)
    tree.heading("2",text="Name",anchor=CENTER)
    tree.heading("3",text="Attendance",anchor=CENTER)
    tree.heading("4",text="Shift",anchor=CENTER)
                                    
    tree.column("#0",width=0)
    tree.column("0",anchor=CENTER,width=100)
    tree.column("1",anchor=CENTER,width=100)
    tree.column("2",anchor=CENTER,width=100)
    tree.column("3",anchor=CENTER,width=100)
    tree.column("4",anchor=CENTER,width=100)
    
    q="select usn,rollno,name,attendance,shift from dailyatt where class=%s and date=%s order by rollno"

    cr.execute(q,[c_var,d_var])
    d=cr.fetchall()
    
    for x in d:
        tree.insert(parent="",index="end",values=x)
        
    tree.pack()
    c.close()
    root1.mainloop()
from tkinter import *
from tkcalendar import DateEntry
def daily_attendance():
    options_window.destroy()
    global root1
    root1 = Tk()
    root1.title("Attendance System")
    root1.geometry('700x530')

    global classsec
    global datee

    classseclabel = Label(root1, text="Class and Section")
    classseclabel.grid(row=2, column=2)
    classsec = Entry(root1)
    classsec.grid(row=2, column=3)

    l_date = tk.Label(root1, text="Select Date:")
    l_date.grid(row=3,column=2)
    e_date = DateEntry(root1, width=12, background='darkblue', foreground='white', borderwidth=2)
    e_date.grid(row=3,column=3)
  
    b1 = Button(root1, text="Show attendance", fg="red", command=lambda:daily_attendancenext(classsec.get(),e_date.get_date()))
    b1.grid(row=4, column=2)

    root1.mainloop()

def monthly_attendancenext(class__sec,month):
    root3.destroy()
    root4=Tk()
    root4.title("Attendance System")
    root4.geometry('700x530')
    
    import mysql.connector as mc
    from tkinter import ttk
    c=mc.connect(host="localhost",user="root",password="mysql",database="attendance_system")
    cr=c.cursor()

    lbl = Label(root4, text = "Class:"+class__sec.get())
    lbl.grid(column=2,row=1)
    lbl.config(font=('Helvetica bold',15))
    lb2 = Label(root4, text = "Month:"+month.get())
    lb2.grid(column=3,row=1)
    lb2.config(font=('Helvetica bold',15))
    
    frame=Frame(root4)
    frame.grid(row=3,column=3)
    
    tree=ttk.Treeview(frame)
    tree["columns"]=("","","","")
    
    tree.heading("0",text="USN",anchor=CENTER)
    tree.heading("1",text="RollNo",anchor=CENTER)
    tree.heading("2",text="Name",anchor=CENTER)
    tree.heading("3",text="No of days present",anchor=CENTER)
    
    tree.column("#0",width=0)
    tree.column("0",anchor=CENTER,width=150)
    tree.column("1",anchor=CENTER,width=100)
    tree.column("2",anchor=CENTER,width=150)
    tree.column("3",anchor=CENTER,width=200)
    
    q="SELECT usn, rollno, name, round((COUNT(attendance)/2),2) FROM dailyatt WHERE attendance in ('present','pstar') and shift in('1','2') AND class = %s AND MONTH(date) = %s GROUP BY usn, rollno, name ORDER BY rollno"

    cr.execute(q,[class__sec.get(),month.get()])
    d=cr.fetchall()
    for x in d:
        tree.insert(parent="",index="end",values=x)
        
    tree.pack()
    c.close()
    root4.mainloop()
    
from tkinter import *
def monthly_attendance():
    options_window.destroy()
    global root3
    root3=Tk()
    root3.title("Attendance System")
    root3.geometry('700x530')
    
    class__seclabel=Label(root3,text="Enter class and Section").grid(row=2,column=2)
    class__sec=StringVar()
    class__secentry=Entry(root3,textvariable=class__sec).grid(row=2,column=3)
    
    dateelabel=Label(root3,text="Enter month number").grid(row=3,column=2)
    month=StringVar()
    dateeentry=Entry(root3,textvariable=month).grid(row=3,column=3)
    
    b1=Button(root3,text="Show attendance",fg="red",command=lambda:monthly_attendancenext(class__sec,month))
    b1.grid(row=4,column=2)

    root3.mainloop()

def take_attendance():
    options_window.destroy()
        
    import tkinter as tk
    from tkinter import messagebox
    from tkcalendar import DateEntry  
    import mysql.connector

    # Establish MySQL connection
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="mysql",
        database="attendance_system"
    )
    mycursor = mydb.cursor()

    std = None

    student_radios = {}
    global root7
    # Create Tkinter window
    root7 = tk.Tk()
    root7.geometry('700x530')
    root7.title("Attendance System")

    # Date selection with calendar
    label_date = tk.Label(root7, text="Select Date:")
    label_date.pack()
    entry_date = DateEntry(root7, width=12, background='darkblue', foreground='white', borderwidth=2)
    entry_date.pack()

    label_std = tk.Label(root7, text="Class:")
    label_std.pack()
    entry_std = tk.Entry(root7)
    entry_std.pack()

    label_shift = tk.Label(root7, text="Shift:")
    label_shift.pack()
    entry_shift = tk.Entry(root7)
    entry_shift.pack()

    button = tk.Button(root7, text="Enter Attendance", command=lambda: enter(entry_date, entry_std, entry_shift, student_radios, mycursor))
    button.pack()

    root7.mainloop()
def enter(entry_date, entry_std, entry_shift, student_radios, mycursor):
    std = entry_std.get()
    mycursor.execute("SELECT name, rollno, usn FROM students WHERE class=%s", [std])
    students = mycursor.fetchall()

    for student in students:
        frame = tk.Frame(root7)
        frame.pack()

        student_name = student[0]
        label1 = tk.Label(frame, text=student_name)
        label1.pack(side=tk.LEFT, padx=5)

        student_rollno = student[1]
        label2 = tk.Label(frame, text=student_rollno)
        label2.pack(side=tk.LEFT, padx=5)

        student_usn = student[2]
        label3 = tk.Label(frame, text=student_usn)
        label3.pack(side=tk.LEFT, padx=5)

        var = tk.StringVar(value="Present")
        radio_present = tk.Radiobutton(frame, text="Present", variable=var, value="Present")
        radio_present.pack(side=tk.LEFT, padx=5)
        radio_absent = tk.Radiobutton(frame, text="Absent", variable=var, value="Absent")
        radio_absent.pack(side=tk.LEFT, padx=5)
        radio_pstar = tk.Radiobutton(frame, text="Special permission", variable=var, value="Pstar")
        radio_pstar.pack(side=tk.LEFT, padx=5)

        student_radios[(student_name, student_rollno, student_usn)] = var  # Store Radiobutton variable in the dictionary



    button = tk.Button(root7, text="Save Attendance", command=lambda: save_attendance(entry_date, entry_std, entry_shift, student_radios, mycursor))
    button.pack()

def save_attendance(entry_date, entry_std, entry_shift, student_radios, mycursor):
    date = entry_date.get_date()  # Get selected date from DateEntry widget
    class1 = entry_std.get()
    sh = entry_shift.get()
    attendance_data = []
    import mysql.connector
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="mysql",
        database="attendance_system"
    )
    mycursor = mydb.cursor()
    for (student_name, student_rollno, student_usn), var in student_radios.items():
        attendance_status = var.get()  # Get the value of the RadioButton for each student
        attendance_data.append((student_name, student_rollno, student_usn, attendance_status, date, class1, sh))


    insert_query = "INSERT INTO dailyatt (name, rollno, usn, attendance, date, class, shift) VALUES (%s,%s,%s, %s, %s,%s,%s)"
    mycursor.executemany(insert_query, attendance_data)
    mydb.commit()
    messagebox.showinfo("Take attendance", "Attendance saved successfully!")


import mysql.connector
import numpy as np
import matplotlib.pyplot as plt

def schart():
    mydb = mysql.connector.connect(host="localhost", user="root", password="mysql", database="attendance_system")
    mycursor = mydb.cursor()

    mycursor.execute("SELECT usn, COUNT(*)/2 FROM dailyatt WHERE attendance IN ('present', 'pstar') AND shift IN ('1', '2') GROUP BY usn")
    result = mycursor.fetchall()

    Names = []
    pre = []

    for i in result:
        Names.append(i[0])
        pre.append(float(i[1]))  # Convert to float here

    mycursor.execute('SELECT COUNT(*) FROM dailyatt WHERE rollno=120101')
    total_days = mycursor.fetchone()[0]  # Fetch the count directly

    # Calculate percentages
    total_days = int(total_days)
    percentages = [(count / total_days) * 100 for count in pre]

    # Visualizing Data using Matplotlib
    plt.figure(figsize=(10, 6))  # Adjust figure size as needed
    plt.bar(Names, pre)
    
    max_value = max(pre) + 5  # Add a margin to the maximum value for better visualization
    plt.ylim(0, max_value)  # Set y-axis limits based on the maximum value
    
    plt.xlabel("Usn of Students")
    plt.ylabel("Number of days present")
    plt.title("Student's Information")

    # Display percentages above the chart
    for i, percentage in enumerate(percentages):
        plt.text(i, pre[i] + 0.1, f"{percentage:.2f}%", ha='center', va='bottom', fontsize=8)

    plt.xticks(rotation=90)  # Rotate x-axis labels for better readability if needed
    plt.tight_layout()  # Adjust layout for better spacing
    plt.show()


import tkinter as tk
from tkinter import messagebox
import mysql.connector
from datetime import date
from tkinter import ttk
from tkinter import Label, Entry, StringVar

db = mysql.connector.connect(host="localhost",user="root",password="mysql",database="attendance_system")
cursor = db.cursor()

def registers2():
    nameeg = namee.get()
    class1g = class1.get()
    Rg = R.get()
    usnng = usnn.get()

    query = "INSERT INTO students (name, class, usn, rollno) VALUES (%s, %s, %s, %s)"
    cursor.execute(query, (nameeg,class1g,usnng,Rg))
    db.commit()
    messagebox.showinfo("Registration Successful", "Student registered.")

def register_new_student():
    options_window.destroy()
    global root5
    root5=tk.Tk()
    root5.title("Register student")
    root5.geometry("700x530")
    global usnn
    global namee
    global R
    global class1
    
    usnnlabel=Label(root5,text="Enter usn").grid(row=2,column=2)
    usnn=StringVar()
    usnnentry=Entry(root5,textvariable=usnn).grid(row=2,column=3)
    
    nameelabel=Label(root5,text="Enter name").grid(row=3,column=2)
    namee=StringVar()
    nameeentry=Entry(root5,textvariable=namee).grid(row=3,column=3)
    
    Rlabel=Label(root5,text="Enter rollno").grid(row=4,column=2)
    R=StringVar()
    Rentry=Entry(root5,textvariable=R).grid(row=4,column=3)

    class1label=Label(root5,text="Enter class").grid(row=5,column=2)
    class1=StringVar()
    class1entry=Entry(root5,textvariable=class1).grid(row=5,column=3)
    
    sr_attendance_btn = tk.Button(root5, text="Register", command=registers2)
    sr_attendance_btn.grid(row=6,column=3)

    root5.mainloop()


import csv
import mysql.connector as mc
from tkinter import *    
def exportcsv():
    
    options_window.destroy()
    root6 = Tk()
    root6.title("Export data")
    root6.geometry('700x530')

    def export():
        c = mc.connect(host="localhost", user="root", password="mysql", database="attendance_system")
        cr = c.cursor()

        rget = R1.get()
        filename = rget + '.csv'
        with open(filename, 'w', newline="") as f:
            wo = csv.writer(f)
            wo.writerow(['date', 'attendance', 'shift'])
            q = 'SELECT date, attendance, shift FROM dailyatt WHERE rollno=%s'
            cr.execute(q, [rget])
            data = cr.fetchall()
            for row in data:
                wo.writerow(row)
        messagebox.showinfo("Export successful", "Data stored in csv file")

        cr.close()
        c.close()

    R1label = Label(root6, text="Enter rollno")
    R1label.grid(row=1, column=1)
    R1 = StringVar()
    R1entry = Entry(root6, textvariable=R1)
    R1entry.grid(row=1, column=2)

    export_btn = Button(root6, text="Export data", command=export, width=10)
    export_btn.grid(row=4, column=1)
    
    root6.mainloop()

def show_options():
    root.destroy()
    global options_window
    options_window = tk.Tk()
    options_window.geometry('700x530')
    options_window.title("Attendance Management System")
    image1 = Image.open("class1.png")
    photo = ImageTk.PhotoImage(image1)

# Create a canvas with the image as the background
    canvas = tk.Canvas(options_window, width=image1.width, height=image1.height)
    canvas.pack()

    canvas.create_image(0, 0, anchor=tk.NW, image=photo)

# Create a frame inside the canvas
    frame1 = tk.Frame(canvas, bg='white')
    frame1.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

# Create buttons inside the frame
    take_attendance_btn = tk.Button(frame1, text="Take Attendance", command=take_attendance, width=30)
    take_attendance_btn.grid(row=0, column=0)
    
    daily_attendance_btn = tk.Button(frame1, text="Daily Attendance", command=daily_attendance, width=30)
    daily_attendance_btn.grid(row=1, column=0)
    
    monthly_attendance_btn = tk.Button(frame1, text="Monthly Attendance", command=monthly_attendance, width=30)
    monthly_attendance_btn.grid(row=2, column=0)

    register_new_student_btn = tk.Button(frame1, text="Register new student", command=register_new_student, width=30)
    register_new_student_btn.grid(row=3, column=0)

    schartt_btn = tk.Button(frame1, text="Student chart", command=schart, width=30)
    schartt_btn.grid(row=4, column=0)
    
    att_trends_btn=tk.Button(frame1,text="Attendance trends", command=att_trends, width=30)
    att_trends_btn.grid(row=5, column=0)
    
    export_btn=tk.Button(frame1,text="Export into csv", command=exportcsv, width=30)
    export_btn.grid(row=6, column=0)

    
    
    options_window.mainloop()

# Create main login window
import tkinter as tk
from PIL import Image, ImageTk

# Create the main window
root = tk.Tk()
root.geometry('700x530')
root.title("Login Window")

# Load the image
image1 = Image.open("class1.png")
photo = ImageTk.PhotoImage(image1)

# Create a canvas with the image as the background
canvas = tk.Canvas(root, width=image1.width, height=image1.height)
canvas.pack()

# Place the image on the canvas
canvas.create_image(0, 0, anchor=tk.NW, image=photo)

# Create the login frame
login_frame = tk.Frame(canvas, bg='white')  # Set the background color of the frame
login_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

# Add labels, entry widgets, and button to the login frame
username_label = tk.Label(login_frame, text="Username")
username_label.grid(row=0, column=0)
username_entry = tk.Entry(login_frame)
username_entry.grid(row=0, column=1)

password_label = tk.Label(login_frame, text="Password")
password_label.grid(row=1, column=0)
password_entry = tk.Entry(login_frame, show="*")
password_entry.grid(row=1, column=1)


login_btn = tk.Button(login_frame, text="Login", command=login)
login_btn.grid(row=2, columnspan=2, pady=10)

# Register Frame
register_frame = tk.Frame(root)
register_frame.pack(padx=20, pady=20)

reg_name_label = tk.Label(register_frame, text="Name")
reg_name_label.grid(row=0, column=0)
reg_name_entry = tk.Entry(register_frame)
reg_name_entry.grid(row=0, column=1)

reg_class_label = tk.Label(register_frame, text="Class")
reg_class_label.grid(row=1, column=0)
reg_class_entry = tk.Entry(register_frame)
reg_class_entry.grid(row=1, column=1)

reg_email_label = tk.Label(register_frame, text="Email")
reg_email_label.grid(row=2, column=0)
reg_email_entry = tk.Entry(register_frame)
reg_email_entry.grid(row=2, column=1)

reg_password_label = tk.Label(register_frame, text="Password")
reg_password_label.grid(row=3, column=0)
reg_password_entry = tk.Entry(register_frame, show="*")
reg_password_entry.grid(row=3, column=1)

register_btn = tk.Button(register_frame, text="Register", command=register)
register_btn.grid(row=4, columnspan=2, pady=10)

# Hide register frame initially
register_frame.pack_forget()

# Function to toggle between login and register frames
def toggle_frame():
    if login_frame.winfo_ismapped():
        login_frame.pack_forget()
        register_frame.pack()
    else:
        register_frame.pack_forget()
        login_frame.pack()

# Button to toggle between login and register frames
toggle_btn = tk.Button(root, text="New Teacher? Register here", command=toggle_frame)
toggle_btn.pack()

root.mainloop()
db.close()
