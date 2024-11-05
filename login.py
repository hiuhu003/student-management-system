from tkinter import *
from tkinter import messagebox
from PIL import ImageTk

#function to ensure user doesn't enter null values
def login():
    if usernameEntry.get()=='' or passwordEntry.get()=='':
        messagebox.showerror('Error','Fields cannot be empty!')
    elif usernameEntry.get()=='Ursula' and passwordEntry.get()=='1234':
       messagebox.showinfo('Success','Welcome!')

       window.destroy()  # closes the previous login window
       import sms


    else:
       messagebox.showerror('Error','Please enter correct credentials!')


window=Tk()

window.geometry('1280x700+0+0')
window.title('Login System of Student Management System')

window.resizable(False,False)

backgroundImage=ImageTk.PhotoImage(file='background.jpg')

bgLabel=Label(window,image=backgroundImage)
bgLabel.place(x=0,y=0)

loginFrame=Frame(window,bg='gainsboro')
loginFrame.place(x=400,y=150)

logoImage=PhotoImage(file='logo.png')

logoLabel=Label(loginFrame,image=logoImage)
logoLabel.grid(row=0,column=0,columnspan=2)

#username section
usernameImage=PhotoImage(file='user.png')
usernameLabel=Label(loginFrame,image=usernameImage,text='Username:',compound=LEFT,
                    font=('times new roman',20,'bold'),bg='gainsboro')
usernameLabel.grid(row=1,column=0,pady=10,padx=20)

usernameEntry=Entry(loginFrame,font=('times new roman',20,'bold'),bd=5)
usernameEntry.grid(row=1,column=1,padx=10,pady=20)

#password section
passwordImage=PhotoImage(file='password.png')
passwordLabel=Label(loginFrame,image=passwordImage,text='Password:',compound=LEFT,
                    font=('times new roman',20,'bold'),bg='gainsboro')
passwordLabel.grid(row=2,column=0,pady=10,padx=20)

passwordEntry=Entry(loginFrame,font=('times new roman',20,'bold'),bd=5)
passwordEntry.grid(row=2,column=1,padx=10,pady=20)


#button
loginButton=Button(loginFrame,text='Login',font=('times new roman',15,'bold'),width=15
                   ,fg='white',bg='cornflowerblue',activebackground='gainsboro',
                   activeforeground='white',cursor='hand2',command=login)
loginButton.grid(row=3,column=1,pady=10,padx=10)


window.mainloop()