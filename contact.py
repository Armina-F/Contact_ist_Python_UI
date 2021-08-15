from tkinter import * 
from tkinter import  messagebox
import pyodbc 
# re module provides support
# for regular expressions
import re
 
# Make a regular expression
# for validating an Email
regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

def xstr(s):
    return '' if s is None else str(s)

def sql_commandSelect(CommandText):
    conx_string = "DRIVER={ODBC Driver 17 for SQL Server}; server=(LocalDB)\MSSQLLocalDB; database=python_contact_list; trusted_connection=YES;"
    conx = pyodbc.connect(conx_string)
    cursor = conx.cursor()
    listInfo = cursor.execute(CommandText).fetchall() #array of tuples(rows of result SQL querly)
    conx.close()
    return listInfo

def sql_commandExecute(CommandText):
    conx_string = "DRIVER={ODBC Driver 17 for SQL Server}; server=(LocalDB)\MSSQLLocalDB; database=python_contact_list; trusted_connection=YES;"
    conx = pyodbc.connect(conx_string)
    cursor = conx.cursor()
    cursor.execute(CommandText)
    conx.commit() 
    conx.close()



#get id than selete * from tableBla where id = id
def Add_contact():
    if first_name_txt.get() == '':
        messagebox.showerror(title=" Warning" ,message='FirstName is Empty!')
        return
    if last_name_txt.get() == '':
        messagebox.showerror(title=" Warning", message='Last_name is Empty!')
        return
    if email_txt.get() != '' and not (re.fullmatch(regex, email_txt.get())):
        messagebox.showerror(title=" Warning", message='Invalid Email!')
        return
    phone_no = 0
    try:
        phone_no = int(phone_no_txt.get())
    except:
        messagebox.showerror(title=" Warning", message='Incorrect phone number!')
        return
    if phone_no < 10 :
        messagebox.showerror(title=" Warning", message='Incorrect phone number!')
        return  

    query = f"INSERT INTO contact_info (First_name,Last_name,Phone_no,Address,Email)  VALUES ('{first_name_txt.get()}','{last_name_txt.get()}', {phone_no},'{address_txt.get()}','{email_txt.get()}')"
    sql_commandExecute(query)
    View_all()
    


def Edit():
    if len(listbox.curselection()) == 0:
        messagebox.showerror(title=" Warning", message='Select one contact !')
        return
    selectedRow = str(listbox.get(listbox.curselection()))
    id = selectedRow[:selectedRow.find(':')]

    if first_name_txt.get() == '':
        messagebox.showerror(title=" Warning" ,message='FirstName is Empty!')
        return
    if last_name_txt.get() == '':
        messagebox.showerror(title=" Warning", message='Last_name is Empty!')
        return
    if email_txt.get() != '' and not (re.fullmatch(regex, email_txt.get())):
        messagebox.showerror(title=" Warning", message='Invalid Email!')
        return
    phone_no = 0
    try:
        phone_no = int(phone_no_txt.get())
    except:
        messagebox.showerror(title=" Warning", message='Incorrect phone number!')
        return
    if phone_no < 10 :
        messagebox.showerror(title=" Warning", message='Incorrect phone number!')
        return  

    query = f"UPDATE contact_info SET First_name='{first_name_txt.get()}', Last_name='{last_name_txt.get()}', Phone_no ={phone_no} ,Address='{address_txt.get()}' , Email= '{email_txt.get()}'   Where id={id}"
    sql_commandExecute(query)
    View_all()

def Sort_all():
    query = "SELECT * FROM contact_info ORDER BY First_name, Last_name"
    contact_list = sql_commandSelect(query)
    listbox.delete(0,END)
    for item in contact_list:
        listbox.insert(END,f"{item[0]}: {item[1]}: {item[2]}")
    #Clear UI
    first_name_txt.delete(0,END)
    last_name_txt.delete(0,END)
    phone_no_txt.delete(0,END)
    address_txt.delete(0,END)
    email_txt.delete(0,END)



def View_all():
    query = "SELECT * FROM contact_info ORDER BY ID"
    contact_list = sql_commandSelect(query)
    listbox.delete(0,END)
    for item in contact_list:
        listbox.insert(END,f"{item[0]}: {item[1]}: {item[2]}")
    #Clear UI
    first_name_txt.delete(0,END)
    last_name_txt.delete(0,END)
    phone_no_txt.delete(0,END)
    address_txt.delete(0,END)
    email_txt.delete(0,END)


def View_One(self):
    if len(listbox.curselection()) == 0:
        messagebox.showerror(title=" Warning", message='Select one contact !')
        return
    selectedRow = str(listbox.get(listbox.curselection()))
    id = selectedRow[:selectedRow.find(':')]
    query = f" SELECT TOP(1) * FROM contact_info WHERE id = {id} ORDER BY ID    "
    contact_info = sql_commandSelect(query)[0]  #first tuple of sql array of results
 
    first_name_txt.delete(0,END)
    first_name_txt.insert(0,xstr(contact_info[1]))
    
    last_name_txt.delete(0,END)
    last_name_txt.insert(0,xstr(contact_info[2]))

    phone_no_txt.delete(0,END)
    phone_no_txt.insert(0,xstr(contact_info[3]))

    address_txt.delete(0,END)
    address_txt.insert(0,xstr(contact_info[4]))

    email_txt.delete(0,END)
    email_txt.insert(0,xstr(contact_info[5]))
    

def Search_By_Names():
    query = f" SELECT * FROM contact_info WHERE 1=1  "
    if first_name_txt.get() != '':
        query = query + f" AND First_name='{first_name_txt.get()}'   "
    if last_name_txt.get() != '':
        query = query + f" AND Last_name='{last_name_txt.get()}'  "
   
    query = query + f" ORDER BY ID "
    contact_list = sql_commandSelect(query)
    listbox.delete(0,END)
    for item in contact_list:
        listbox.insert(END,f"{item[0]}: {item[1]}: {item[2]}")
    #Clear UI
    first_name_txt.delete(0,END)
    last_name_txt.delete(0,END)
    phone_no_txt.delete(0,END)
    address_txt.delete(0,END)
    email_txt.delete(0,END)
    
def Exit():
    root.destroy()


def Delete():   

    if len(listbox.curselection()) == 0:
        messagebox.showerror(title=" Warning", message='Select one contact !')
        return
    selectedRow = str(listbox.get(listbox.curselection()))
    id = selectedRow[:selectedRow.find(':')]
    query = f"DELETE FROM contact_info WHERE id = {id}"
    sql_commandExecute(query)
    View_all()
    

    
root = Tk()
root.geometry('900x400')
root.resizable(1,1)
root.config(bg='linen')
root.title("contact list")

#contact_list=[]
##list of lists
#first_name=str()
#last_name=str()
#phone_no=str()
#address=str()
#email=str()
#print(type(first_name))
MainFrame = Frame(root)
MainFrame.grid(row=0, column=0) 

InfoFrame = Frame(MainFrame)
InfoFrame.grid(row=0, column= 1, padx=15, pady=15)

ListFrame = Frame(MainFrame)
ListFrame.grid(row=0, column= 2)

scroll = Scrollbar(ListFrame,orient=VERTICAL)
scroll.pack(side=RIGHT,fill=BOTH)

listbox = Listbox(ListFrame)
listbox.bind('<<ListboxSelect>>', View_One)
listbox.pack(side = RIGHT, fill = BOTH)
select = listbox.config(yscrollcommand=scroll.set)
scroll.config(command=listbox.yview)

    


font = ("b nazanin" , 12, 'bold') 
widthButton = 20
widthLable = 15
widthTextBox = 25
padX = 5
padY = 5

first_name_lbl = Label(InfoFrame,text="first name" , font=font , bg ="MediumPurple1",width = widthLable)
first_name_lbl.grid(row=3,column=2, padx =padX , pady =padY)

last_name_lbl = Label(InfoFrame,text="last name" , font=font , bg ="MediumPurple1",width = widthLable)
last_name_lbl.grid(row=5,column=2, padx =padX , pady =padY)

phone_no_lbl = Label(InfoFrame,text="phone no" , font=font , bg ="MediumPurple1",width = widthLable)
phone_no_lbl.grid(row=7,column=2, padx =padX , pady =padY)


address_lbl = Label(InfoFrame,text="address" , font=font , bg ="MediumPurple1",width = widthLable)
address_lbl.grid(row=9,column=2, padx =padX , pady =padY)

email_lbl = Label(InfoFrame,text="email" , font=font , bg ="MediumPurple1",width = widthLable)
email_lbl.grid(row=11,column=2, padx =padX , pady =padY)


first_name_txt = Entry(InfoFrame,font=font , bg="light grey",width = widthTextBox)
first_name_txt.grid(row=3,column=4, padx =padX , pady =padY)

last_name_txt = Entry(InfoFrame,font=font , bg="light grey",width = widthTextBox)
last_name_txt.grid(row=5,column=4, padx =padX , pady =padY)

phone_no_txt = Entry(InfoFrame,font=font , bg="light grey",width = widthTextBox)
phone_no_txt.grid(row=7,column=4, padx =padX , pady =padY)

address_txt = Entry(InfoFrame,font=font , bg="light grey",width = widthTextBox)
address_txt.grid(row=9,column=4, padx =padX , pady =padY)

email_txt = Entry(InfoFrame,font=font , bg="light grey",width = widthTextBox)
email_txt.grid(row=11,column=4, padx =padX , pady =padY)

add_btn = Button(InfoFrame,text="add new contact",font=font , bg="LightBlue1" ,width = widthButton, command=Add_contact)
add_btn.grid(row=3,column=0, padx =padX , pady =padY)

edit_btn = Button(InfoFrame,text="edit existing contact",font=font , bg="LightBlue1",width = widthButton, command=Edit)
edit_btn.grid(row=5,column=0, padx =padX , pady =padY)

view_all_btn = Button(InfoFrame,text="view all contacts",font=font , bg="LightBlue1",width = widthButton, command = View_all)
view_all_btn.grid(row=7,column=0, padx =padX , pady =padY)

sort_all_btn = Button(InfoFrame,text="sort all contacts ",font=font , bg="LightBlue1",width = widthButton, command=Sort_all)
sort_all_btn.grid(row=9,column=0, padx =padX , pady =padY)

view_btn = Button(InfoFrame,text="search contact by names",font=font , bg="LightBlue1",width = widthButton, command=Search_By_Names)
view_btn.grid(row=11,column=0, padx =padX , pady =padY)

delete_btn = Button(InfoFrame,text="delete existing contact",font=font , bg="LightBlue1",width = widthButton, command=Delete)
delete_btn.grid(row=13,column=0, padx =padX , pady =padY)

exit_btn = Button(InfoFrame,text="exit",font=font , bg="LightBlue1",width = widthButton, command=Exit)
exit_btn.grid(row=15,column=0, padx =padX , pady =padY)

   

root.mainloop()
