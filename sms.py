import time
from datetime import datetime
from itertools import count
from operator import length_hint, index
from re import search
from tkinter import *
from ttkthemes import ThemedTk
from tkinter import ttk,messagebox,filedialog
import mysql.connector
import pandas
from login import logoLabel

con = None
mycursor = None

#functionality section
#exit section
def iexit():
    result=messagebox.askyesno('Confirm','Do you want to exit?')
    if result:
        root.destroy()
    else:
        pass
    
#export section
def export_data():
    url=filedialog.asksaveasfilename(defaultextension='.csv')
    indexing=studentTable.get_children()
    newlist=[]
    for index in indexing:
        content=studentTable.item(index)
        datalist=content['values']
        newlist.append(datalist)

        table=pandas.DataFrame(newlist,columns=['id','Name','Mobile','Email','Address','Gender','DOB','Added Date','Added Time'])
        table.to_csv(url,index=False)
        messagebox.showinfo('Success','Data is saved successfully')
#update section
def update_student():
    # Get the current date and time
    currentdate = time.strftime('%d/%m/%Y')
    currenttime = time.strftime('%H:%M:%S')

    def update_data():
        try:
            # Ensure query matches the fields in your table and has the correct number of placeholders
            query = """
                UPDATE student 
                SET name = %s, mobile = %s, email = %s, address = %s, gender = %s, dob = %s, date = %s, time = %s
                WHERE id = %s
            """
            # Execute the query with the required parameters
            mycursor.execute(query, (
                nameEntry.get(), phoneEntry.get(), emailEntry.get(), addressEntry.get(),
                genderEntry.get(), dobEntry.get(), currentdate, currenttime, idEntry.get()
            ))

            # Commit the changes to the database
            con.commit()

            # Show success message and refresh the display
            messagebox.showinfo('Success', f'ID {idEntry.get()} has been successfully updated', parent=update_window)
            update_window.destroy()
            show_student()
        except mysql.connector.errors.ProgrammingError as e:
            messagebox.showerror('Error', f'Error updating data: {e}', parent=update_window)

    update_window = Toplevel()
    update_window.title('Update Student')
    update_window.grab_set()  # ensures one can't go to other window without finishing with current window
    update_window.resizable(False, False)

    idLabel = Label(update_window, text='Id', font=('times new roman', 20, 'bold'))
    idLabel.grid(row=0, column=0, padx=30, pady=15, sticky=W)
    idEntry = Entry(update_window, font=('times new roman', 15, 'bold'), width=24)
    idEntry.grid(row=0, column=1, pady=15, padx=10)

    nameLabel = Label(update_window, text='Name', font=('times new roman', 20, 'bold'))
    nameLabel.grid(row=1, column=0, padx=30, pady=15, sticky=W)
    nameEntry = Entry(update_window, font=('times new roman', 15, 'bold'), width=24)
    nameEntry.grid(row=1, column=1, pady=15, padx=10)

    phoneLabel = Label(update_window, text='Phone', font=('times new roman', 20, 'bold'))
    phoneLabel.grid(row=2, column=0, padx=30, pady=15, sticky=W)
    phoneEntry = Entry(update_window, font=('times new roman', 15, 'bold'), width=24)
    phoneEntry.grid(row=2, column=1, pady=15, padx=10)

    emailLabel = Label(update_window, text='Email', font=('times new roman', 20, 'bold'))
    emailLabel.grid(row=3, column=0, padx=30, pady=15, sticky=W)
    emailEntry = Entry(update_window, font=('times new roman', 15, 'bold'), width=24)
    emailEntry.grid(row=3, column=1, pady=15, padx=10)

    addressLabel = Label(update_window, text='Address', font=('times new roman', 20, 'bold'))
    addressLabel.grid(row=4, column=0, padx=30, pady=15, sticky=W)
    addressEntry = Entry(update_window, font=('times new roman', 15, 'bold'), width=24)
    addressEntry.grid(row=4, column=1, pady=15, padx=10)

    genderLabel = Label(update_window, text='Gender', font=('times new roman', 20, 'bold'))
    genderLabel.grid(row=5, column=0, padx=30, pady=15, sticky=W)
    genderEntry = Entry(update_window, font=('times new roman', 15, 'bold'), width=24)
    genderEntry.grid(row=5, column=1, pady=15, padx=10)

    dobLabel = Label(update_window, text='DOB', font=('times new roman', 20, 'bold'))
    dobLabel.grid(row=6, column=0, padx=30, pady=15, sticky=W)
    dobEntry = Entry(update_window, font=('times new roman', 15, 'bold'), width=24)
    dobEntry.grid(row=6, column=1, pady=15, padx=10)

    update_student_button =ttk.Button(update_window, text='Update student',command=update_data)
    update_student_button.grid(row=7, columnspan=2, pady=15)


    indexing=studentTable.focus()
    content=studentTable.item(indexing)
    listdata=content['values']
    idEntry.insert(0,listdata[0])
    nameEntry.insert(0,listdata[1])
    phoneEntry.insert(0,listdata[2])
    emailEntry.insert(0,listdata[3])
    addressEntry.insert(0,listdata[4])
    genderEntry.insert(0,listdata[5])
    dobEntry.insert(0,listdata[6])

#show section
def show_student():
    query='select * from student'
    mycursor.execute(query)
    fetched_data = mycursor.fetchall()
    studentTable.delete(*studentTable.get_children())
    for data in fetched_data:
        studentTable.insert('', END, values=data)
#delete section
def delete_student():
    indexing=studentTable.focus()
    print(indexing)
    content=studentTable.item(indexing)
    content_id=content['values'][0]
    query='delete from student where id=%s'
    mycursor.execute(query,(content_id,))
    con.commit()
    messagebox.showinfo('Deleted',f'Id {content_id} is deleted successfully')
    query='select * from student'
    mycursor.execute(query)
    fetched_data=mycursor.fetchall()
    studentTable.delete(*studentTable.get_children())
    for data in fetched_data:
        studentTable.insert('',END,values=data)
#search section
def search_student():
    #how to such for data in db
    def search_data():
        query='select * from student where id=%s or name=%s or email=%s or mobile=%s or address=%s or gender=%s or dob=%s'
        mycursor.execute(query,(idEntry.get(),nameEntry.get(),emailEntry.get(),phoneEntry.get(),addressEntry.get(),genderEntry.get(),dobEntry.get()))
        studentTable.delete(*studentTable.get_children())
        fetched_data = mycursor.fetchall()
        for data in fetched_data:
            studentTable.insert('',END, values=data)


    search_window = Toplevel()
    search_window.title('Search Student')
    search_window.grab_set()  # ensures one can't go to other window without finishing with current window
    search_window.resizable(False, False)

    idLabel = Label(search_window, text='Id', font=('times new roman', 20, 'bold'))
    idLabel.grid(row=0, column=0, padx=30, pady=15, sticky=W)
    idEntry = Entry(search_window, font=('times new roman', 15, 'bold'), width=24)
    idEntry.grid(row=0, column=1, pady=15, padx=10)

    nameLabel = Label(search_window, text='Name', font=('times new roman', 20, 'bold'))
    nameLabel.grid(row=1, column=0, padx=30, pady=15, sticky=W)
    nameEntry = Entry(search_window, font=('times new roman', 15, 'bold'), width=24)
    nameEntry.grid(row=1, column=1, pady=15, padx=10)

    phoneLabel = Label(search_window, text='Phone', font=('times new roman', 20, 'bold'))
    phoneLabel.grid(row=2, column=0, padx=30, pady=15, sticky=W)
    phoneEntry = Entry(search_window, font=('times new roman', 15, 'bold'), width=24)
    phoneEntry.grid(row=2, column=1, pady=15, padx=10)

    emailLabel = Label(search_window, text='Email', font=('times new roman', 20, 'bold'))
    emailLabel.grid(row=3, column=0, padx=30, pady=15, sticky=W)
    emailEntry = Entry(search_window, font=('times new roman', 15, 'bold'), width=24)
    emailEntry.grid(row=3, column=1, pady=15, padx=10)

    addressLabel = Label(search_window, text='Address', font=('times new roman', 20, 'bold'))
    addressLabel.grid(row=4, column=0, padx=30, pady=15, sticky=W)
    addressEntry = Entry(search_window, font=('times new roman', 15, 'bold'), width=24)
    addressEntry.grid(row=4, column=1, pady=15, padx=10)

    genderLabel = Label(search_window, text='Gender', font=('times new roman', 20, 'bold'))
    genderLabel.grid(row=5, column=0, padx=30, pady=15, sticky=W)
    genderEntry = Entry(search_window, font=('times new roman', 15, 'bold'), width=24)
    genderEntry.grid(row=5, column=1, pady=15, padx=10)

    dobLabel = Label(search_window, text='DOB', font=('times new roman', 20, 'bold'))
    dobLabel.grid(row=6, column=0, padx=30, pady=15, sticky=W)
    dobEntry = Entry(search_window, font=('times new roman', 15, 'bold'), width=24)
    dobEntry.grid(row=6, column=1, pady=15, padx=10)

    search_window_button =ttk.Button(search_window, text='Search student', command=search_data)
    search_window_button.grid(row=7, columnspan=2, pady=15)

#creates the popup for adding studying information
def add_student():

    def add_data():
        if idEntry.get()== '' or nameEntry.get()== '' or phoneEntry.get()== '' or emailEntry.get()== '' or addressEntry.get()== '' or genderEntry.get()== '' or dobEntry.get()== '':
            messagebox.showerror('Error','All the fields are required.',parent=add_window)
        try:
            currentdate = time.strftime('%d/%m/%Y')
            currenttime = time.strftime('%H:%M:%S')
            query='insert into student values(%s,%s,%s,%s,%s,%s,%s,%s,%s)'
            mycursor.execute(query,(idEntry.get(),nameEntry.get(),phoneEntry.get(),
                                            emailEntry.get(),addressEntry.get(),genderEntry.get(),dobEntry.get(),currentdate,currenttime))
            #con variable is used to commit changes
            con.commit()
            result=messagebox.askyesno('Confirm','Data added successfully. Dou you want to clean the form?',parent=add_window)
            if result:
                idEntry.delete(0,END)
                nameEntry.delete(0,END)
                phoneEntry.delete(0,END)
                emailEntry.delete(0,END)
                addressEntry.delete(0,END)
                genderEntry.delete(0,END)
                dobEntry.delete(0,END)
            else:
                pass
        except:
            messagebox.showerror('Error',' Id cannot be repeated',parent=add_window)
            return

            #fetches data from db
            query='select * from student'
            mycursor.execute(query)
            fetched_data=mycursor.fetchall()
            #deletes everything in data so to avoid repetition in display
            studentTable.delete(*studentTable.get_children())
            for data in fetched_data:
                studentTable.insert('',END,values=data)# displays data


    add_window=Toplevel()
    add_window.grab_set() #ensures one can't go to other window without finishing with current window
    add_window.resizable(False,False)

    idLabel=Label(add_window,text='Id',font=('times new roman',20,'bold'))
    idLabel.grid(row=0,column=0,padx=30,pady=15,sticky=W)
    idEntry=Entry(add_window,font=('times new roman',15,'bold'),width=24)
    idEntry.grid(row=0, column=1,pady=15,padx=10)

    nameLabel = Label(add_window, text='Name', font=('times new roman', 20, 'bold'))
    nameLabel.grid(row=1, column=0, padx=30, pady=15,sticky=W)
    nameEntry = Entry(add_window, font=('times new roman', 15, 'bold'), width=24)
    nameEntry.grid(row=1, column=1, pady=15, padx=10)

    phoneLabel = Label(add_window, text='Phone', font=('times new roman', 20, 'bold'))
    phoneLabel.grid(row=2, column=0, padx=30, pady=15,sticky=W)
    phoneEntry = Entry(add_window, font=('times new roman', 15, 'bold'), width=24)
    phoneEntry.grid(row=2, column=1, pady=15, padx=10)

    emailLabel = Label(add_window, text='Email', font=('times new roman', 20, 'bold'))
    emailLabel.grid(row=3, column=0, padx=30, pady=15,sticky=W)
    emailEntry = Entry(add_window, font=('times new roman', 15, 'bold'), width=24)
    emailEntry.grid(row=3, column=1, pady=15, padx=10)

    addressLabel = Label(add_window, text='Address', font=('times new roman', 20, 'bold'))
    addressLabel.grid(row=4, column=0, padx=30, pady=15,sticky=W)
    addressEntry = Entry(add_window, font=('times new roman', 15, 'bold'), width=24)
    addressEntry.grid(row=4, column=1, pady=15, padx=10)

    genderLabel = Label(add_window, text='Gender', font=('times new roman', 20, 'bold'))
    genderLabel.grid(row=5, column=0, padx=30, pady=15,sticky=W)
    genderEntry = Entry(add_window, font=('times new roman', 15, 'bold'), width=24)
    genderEntry.grid(row=5, column=1, pady=15, padx=10)

    dobLabel = Label(add_window, text='DOB', font=('times new roman', 20, 'bold'))
    dobLabel.grid(row=6, column=0, padx=30, pady=15,sticky=W)
    dobEntry = Entry(add_window, font=('times new roman', 15, 'bold'), width=24)
    dobEntry.grid(row=6, column=1, pady=15, padx=10)

    add_student_button=ttk.Button(add_window, text='ADD STUDENT', command=add_data)
    add_student_button.grid(row=7, columnspan=2,pady=15)


#connection to database function
def connect_database():
    # connection to mysql
    def connect():
        global mycursor,con #enables variable to be used in another function
        try:
            con = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                port="3306",
            )

            mycursor=con.cursor()

            #create a new database if it doesn't exist
            mycursor.execute("CREATE DATABASE IF NOT EXISTS student_management_system")

            con.database = 'student_management_system'

            #student tables
            query = (
                'create table student(id int not null primary key, name varchar(30),mobile varchar(10),email varchar(30),'
                'address varchar(100),gender varchar(20),dob varchar(20),date varchar(50),time varchar(50)) ')

            mycursor.execute(query)

            messagebox.showinfo('Success', 'Database Connection is Successful',parent=connectWindow)

        except mysql.connector.Error as err:
            messagebox.showerror('Error', f'Error: {err}', parent=connectWindow)
            print(f"Detailed error: {err}")  # Print specific error to console for debugging

            connectWindow.destroy()

        addstudentButton.config(state=NORMAL)
        searchButton.config(state=NORMAL)
        updatestudentButton.config(state=NORMAL)
        showstudentButton.config(state=NORMAL)
        exportstudentButton.config(state=NORMAL)
        deletestudentButton.config(state=NORMAL)



    connectWindow=Toplevel()
    connectWindow.grab_set()
    connectWindow.geometry('470x250+730+250')
    connectWindow.title('Database Connection')
    connectWindow.resizable(False,False)


    hostnameLabel=Label(connectWindow,text='Host name:',font=('arial',20,'bold'))
    hostnameLabel.grid(row=0,column=0,padx=20)

    hostEntry=Entry(connectWindow,font=('roman',15,'bold'),bd=2)
    hostEntry.grid(row=0,column=1,padx=40,pady=20)

    usernameLabel = Label(connectWindow, text='User Name:', font=('arial', 20, 'bold'))
    usernameLabel.grid(row=1, column=0, padx=20)

    usernameEntry = Entry(connectWindow, font=('roman', 15, 'bold'), bd=2)
    usernameEntry.grid(row=1, column=1, padx=40, pady=20)

    passwordLabel = Label(connectWindow, text='Password:', font=('arial', 20, 'bold'))
    passwordLabel.grid(row=2, column=0, padx=20)

    passwordEntry = Entry(connectWindow, font=('roman', 15, 'bold'), bd=2)
    passwordEntry.grid(row=2, column=1, padx=40, pady=20)

    connectButton=ttk.Button(connectWindow,text='CONNECT',command=connect)
    connectButton.grid(row=3,columnspan=2)


#clock and date function
def clock():
    date=time.strftime('%d/%m/%Y')
    currenttime = time.strftime('%H:%M:%S')
    datetimeLabel.config(text=f'    Date:{date} \nTime:{currenttime}')
    datetimeLabel.after(1000, clock) #updates the seconds in the clock

#slider name function
count=0
text=''
def slider():
    global text,count
    if count==len(s):
        count=0
        text=''

    text=text+s[count] #S
    sliderLabel.config(text=text)
    count+=1
    sliderLabel.after(200, slider)


 #GUI section
root=ThemedTk()

root.get_themes()

root.set_theme('elegance')

root.geometry('1174x850+0+0')
root.resizable(False,False)
root.title('Student Management System')




datetimeLabel=Label(root,font=('times new roman',18,'bold'))
datetimeLabel.place(x=5,y=5)
clock()

s='Student Management System' #s[count]=S when count is 0
sliderLabel=Label(root,font=('arial',28,'italic bold'),width=40)
sliderLabel.place(x=200,y=0)
slider()

connectButton=ttk.Button(root,text='Connect To Database',command=connect_database)
connectButton.place(x=1000,y=1)

leftFrame=Frame(root)
leftFrame.place(x=50,y=80,width=300,height=600)

logo_image=PhotoImage(file='student.png')
logoLabel=Label(leftFrame,image=logo_image)
logoLabel.grid(row=0,column=0)

addstudentButton=ttk.Button(leftFrame,text='Add Student',width=25,state=DISABLED,command=add_student)
addstudentButton.grid(row=1,column=0,pady=20)

searchButton=ttk.Button(leftFrame,text='Search Student',width=25,state=DISABLED,command=search_student)
searchButton.grid(row=2,column=0,pady=20)

deletestudentButton=ttk.Button(leftFrame,text='Delete Student',width=25,state=DISABLED,command=delete_student)
deletestudentButton.grid(row=3,column=0,pady=20)

updatestudentButton=ttk.Button(leftFrame,text='Update Student',width=25,state=DISABLED,command=update_student)
updatestudentButton.grid(row=4,column=0,pady=20)

showstudentButton=ttk.Button(leftFrame,text='Show Student',width=25,state=DISABLED,command=show_student)
showstudentButton.grid(row=5,column=0,pady=20)

exportstudentButton=ttk.Button(leftFrame,text='Export data',width=25,state=DISABLED,command=export_data)
exportstudentButton.grid(row=6,column=0,pady=20)

exitButton=ttk.Button(leftFrame,text='Exit',width=25,command=iexit)
exitButton.grid(row=7,column=0,pady=20)

rightFrame=Frame(root,bg='grey')
rightFrame.place(x=350,y=80,width=820,height=600)

#scrollbar
scrollBarX=Scrollbar(rightFrame,orient=HORIZONTAL)
scrollBarY=Scrollbar(rightFrame,orient=VERTICAL)

studentTable=ttk.Treeview(rightFrame,columns=('Id','Name','Mobile','Email',
                                 'Address','Gender','D.O.B',
                                 'Added Date','Added Time'),
                          xscrollcommand=scrollBarX.set,yscrollcommand=scrollBarY.set)

scrollBarX.config(command=studentTable.xview)
scrollBarY.config(command=studentTable.yview)

scrollBarX.pack(side=TOP,fill=X)
scrollBarY.pack(side=RIGHT,fill=Y)

studentTable.pack(fill=BOTH,expand=1)

studentTable.heading('Id',text='Id')
studentTable.heading('Name',text='Name')
studentTable.heading('Mobile',text='Mobile No')
studentTable.heading('Email',text='Email')
studentTable.heading('Address',text='Address')
studentTable.heading('Gender',text='Gender')
studentTable.heading('D.O.B',text='D.O.B')
studentTable.heading('Added Date',text='Added Date')
studentTable.heading('Added Time',text='Added Time')

#styles format display
studentTable.column('Id', width=50,anchor=CENTER)
studentTable.column('Name', width=150,anchor=CENTER)
studentTable.column('Email', width=250,anchor=CENTER)
studentTable.column('Mobile', width=100,anchor=CENTER)
studentTable.column('Address', width=250,anchor=CENTER)
studentTable.column('Gender', width=100,anchor=CENTER)
studentTable.column('D.O.B', width=100,anchor=CENTER)
studentTable.column('Added Date', width=200,anchor=CENTER)
studentTable.column('Added Time', width=200,anchor=CENTER)


#backgound color for table
style=ttk.Style()

style.configure('Treeview',rowheight=40,font=('arial',15,'bold'),foreground='black',background='grey',fieldbackground='grey')
style.configure('Treeview.Heading',font=('arial',14,'bold'))
# to ensure id appears as the first column tab
studentTable.config(show='headings')



root.mainloop()