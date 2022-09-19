from ast import Pass
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import tkinter
import mysql.connector
import os
from datetime import *
from tkcalendar import Calendar
import hashlib


def loginToDBPopUp():
  loginWindow = Tk()
  loginWindow.geometry("300x200")
  loginWindow.resizable(False, False)
  loginWindow.title("Log In To Database.")
  loginWindow.configure(background='#6e72f9')
  w = loginWindow.winfo_reqwidth()
  h = loginWindow.winfo_reqheight()
  ws = loginWindow.winfo_screenwidth()
  hs = loginWindow.winfo_screenheight()
  x = (ws/2) - (w/2)
  y = (hs/2) - (h/2)
  loginWindow.geometry("+%d+%d" % (x, y)) 

  L1 = Label(loginWindow, text="Host:", bg = "#6e72f9", fg = "white")
  L1.pack()
  E1 = Entry(loginWindow, bd = 2, relief=FLAT)
  E1.pack()

  L2 = Label(loginWindow, text="User:", bg = "#6e72f9", fg = "white")
  L2.pack()
  E2 = Entry(loginWindow, bd = 2, relief=FLAT)
  E2.pack()
  L3 = Label(loginWindow, text="Password:", bg = "#6e72f9", fg = "white")
  L3.pack()
  E3 = Entry(loginWindow, bd = 2, show="*", relief=FLAT)
  E3.pack()

  B1 = Button(loginWindow, text="Log in", bg = "#6e72f9", activebackground="#9ea0f9", fg = "white", relief=GROOVE, padx=50, command=lambda: accessDB(E1.get(), E2.get(), E3.get(), loginWindow))
  B1.pack(side = LEFT)
  loginWindow.bind('<Return>', lambda x = None: accessDB(E1.get(), E2.get(), E3.get(), loginWindow))
  B2 = Button(loginWindow, text="Exit", bg = "#6e72f9", activebackground="#9ea0f9", fg = "white", relief=GROOVE, padx=50, command=lambda: loginWindow.destroy())
  B2.pack(side = RIGHT)
  
  loginWindow.mainloop()

def accessDB(hostname, username, password, DBLoginWindow):
  try:
    accessDB.mydb = mysql.connector.connect(
        host=hostname,
        user=username,
        password=password,
        database="crm_db"
        )  
    accessDB.mydb.autocommit = True
    DBLoginWindow.destroy()
  except Exception as e:
    print(e)
    messagebox.showerror("Error!", "Something went wrong. Please try again.")
#--------------------------------------------------------------------------------------------------------------------------------------------------------

def loginPopUp():
  loginWindow = Tk()
  loginWindow.geometry("300x200")
  loginWindow.resizable(False, False)
  loginWindow.title("Log In.")
  loginWindow.configure(background='#6e72f9')
  w = loginWindow.winfo_reqwidth()
  h = loginWindow.winfo_reqheight()
  ws = loginWindow.winfo_screenwidth()
  hs = loginWindow.winfo_screenheight()
  x = (ws/2) - (w/2)
  y = (hs/2) - (h/2)
  loginWindow.geometry("+%d+%d" % (x, y)) 

  L1 = Label(loginWindow, text="Username:", bg = "#6e72f9", fg = "white")
  L1.pack()
  E1 = Entry(loginWindow, bd = 2, relief=FLAT)
  E1.pack()

  L2 = Label(loginWindow, text="Password:", bg = "#6e72f9", fg = "white")
  L2.pack()
  E2 = Entry(loginWindow, bd = 2, show="*", relief=FLAT)
  E2.pack()

  B1 = Button(loginWindow, text="Log in", bg = "#6e72f9", activebackground="#9ea0f9", fg = "white", relief=GROOVE, padx=50, command=lambda: loginCheck(E1.get(), E2.get(), loginWindow))
  B1.pack(side = LEFT)
  loginWindow.bind('<Return>', lambda x = None: loginCheck(E1.get(), E2.get(), loginWindow))
  B2 = Button(loginWindow, text="Exit", bg = "#6e72f9", activebackground="#9ea0f9", fg = "white", relief=GROOVE, padx=50, command=lambda: loginWindow.destroy())
  B2.pack(side = RIGHT)
  
  loginWindow.mainloop()

def loginCheck(username, password, loginWindow):
  query = ("SELECT username, password, levelAccess, isActive FROM users WHERE username = %s AND password = %s")
  hash_pass = hashlib.md5(password.encode("utf-8")).hexdigest()
  dbCursor.execute(query, (username, hash_pass))
  c.append(dbCursor.fetchall())

  if c[0] and c[0][0][3] == 0:
    c.pop(0)
    messagebox.showerror("Error!", "User not active!")
  elif c[0] and c[0][0][3] == 1:
    loginWindow.destroy()
  else :
    c.pop(0)
    messagebox.showerror("Error!", "Invalid username or password!") 

#--------------------------------------------------------------------------------------------------------------------------------------------------------

def clearAllInnerFrames():
  for widget in dashboardWindow.innerFrame1.winfo_children():
        widget.destroy()
  for widget in dashboardWindow.innerFrame2.winfo_children():
        widget.destroy()

def clearInnerFrame1():
  for widget in dashboardWindow.innerFrame1.winfo_children():
        widget.destroy()

def clearInnerFrame2():
  for widget in dashboardWindow.innerFrame2.winfo_children():
        widget.destroy()

def delete_entries(frame):
  for widget in frame.winfo_children():
    if isinstance(widget, tkinter.Entry):
      widget.delete(0,END)
    elif isinstance(widget, tkinter.LabelFrame):
      for l_widget in widget.winfo_children():
        if isinstance(l_widget, tkinter.Radiobutton):
          l_widget.deselect()

#--------------------------------------------------------------------------------------------------------------------------------------------------------

def dashboardOptions(bCode):

  dashboardOptions.var = IntVar()

  if bCode == 0:
    clearAllInnerFrames()
    displayLatestMessage()

  elif bCode == 1:
    clearInnerFrame1()
    labelFrameC = LabelFrame(dashboardWindow.innerFrame1, text='Choose an option', bg= innerFrameColor)
    labelFrameC.grid(row=1, column=0, rowspan = 3, sticky = NSEW, padx=20, pady=(dashboardWindow.homeButton.winfo_height() + 10,0))
    customerRB1 = Radiobutton(labelFrameC, text="Insert new customer", variable=dashboardOptions.var, value=1, bg=innerFrameColor)
    customerRB1.grid(row = 0, column = 0, sticky = W)
    customerRB2 = Radiobutton(labelFrameC, text="Edit customer", variable=dashboardOptions.var, value=2, bg=innerFrameColor)
    customerRB2.grid(row = 1, column = 0, sticky = W)
    customerRB3 = Radiobutton(labelFrameC, text="Show customer list", variable=dashboardOptions.var, value=3, bg=innerFrameColor)
    customerRB3.grid(row = 2, column = 0, sticky = W)
    
    dashboardWindow.goButtonC = Button(dashboardWindow.innerFrame1, text = "GO!", relief=GROOVE, bg = "#4acfab", activebackground="#4acfab", command = lambda: [clearInnerFrame2(), customerMethods(dashboardOptions.var.get())])
    dashboardWindow.goButtonC.grid(row = 1, column = 1, sticky = E, padx=10, pady=(dashboardWindow.homeButton.winfo_height() + dashboardWindow.homeButton.winfo_height()/4,0))

  elif bCode == 2:
    clearInnerFrame1()
    labelFrameM = LabelFrame(dashboardWindow.innerFrame1, text='Choose an option', bg=innerFrameColor)
    labelFrameM.grid(row=1, column=0, padx=20, pady=(dashboardWindow.homeButton.winfo_height()*2 + 10,0), rowspan = 3, sticky = NSEW)
    messageRB1 = Radiobutton(labelFrameM, text="Insert new message", variable=dashboardOptions.var, value=1, bg=innerFrameColor)
    messageRB1.grid(row = 1, column = 0, sticky = W)
    messageRB2 = Radiobutton(labelFrameM, text="Edit message", variable=dashboardOptions.var, value=2, bg=innerFrameColor)
    messageRB2.grid(row = 2, column = 0, sticky = W)
    messageRB3 = Radiobutton(labelFrameM, text="Archived messages", variable=dashboardOptions.var, value=3, bg=innerFrameColor)
    messageRB3.grid(row = 3, column = 0, sticky = W)
    
    dashboardWindow.goButtonM = Button(dashboardWindow.innerFrame1, text = "GO!", relief=GROOVE, bg = "#4acfab", activebackground="#4acfab", command = lambda: [clearInnerFrame2(), messageMethods(dashboardOptions.var.get())])
    dashboardWindow.goButtonM.grid(row = 2, column = 1, sticky = E,  padx=10, pady=(dashboardWindow.homeButton.winfo_height()*2 + dashboardWindow.homeButton.winfo_height()/4,0))

  else:
    clearInnerFrame1()
    labelFrameU = LabelFrame(dashboardWindow.innerFrame1, text='Choose an option', bg=innerFrameColor)
    labelFrameU.grid(row=1, column=0, padx=20, pady=(dashboardWindow.homeButton.winfo_height()*3 + 10,0), rowspan = 3, sticky = NSEW)
    userRB1 = Radiobutton(labelFrameU, text="Insert new user", variable=dashboardOptions.var, value=1, bg=innerFrameColor)
    userRB1.grid(row = 1, column = 0, sticky = W)
    userRB2 = Radiobutton(labelFrameU, text="Edit user", variable=dashboardOptions.var, value=2, bg=innerFrameColor)
    userRB2.grid(row = 2, column = 0, sticky = W)
    userRB3 = Radiobutton(labelFrameU, text="Show user list", variable=dashboardOptions.var, value=3, bg=innerFrameColor)
    userRB3.grid(row = 3, column = 0, sticky = W)
    
    dashboardWindow.goButtonU = Button(dashboardWindow.innerFrame1, text = "GO!", relief=GROOVE, bg = "#4acfab", activebackground="#4acfab", command = lambda:[clearInnerFrame2(), userMethods(dashboardOptions.var.get())])
    dashboardWindow.goButtonU.grid(row = 2, column = 1, sticky = E, padx=10, pady=(dashboardWindow.homeButton.winfo_height()*3 + dashboardWindow.homeButton.winfo_height()/4,0))

#--------------------------------------------------------------------------------------------------------------------------------------------------------

def selectItem(tree):
  curItem = tree.item(tree.selection())
  val_list = curItem['values']
  return val_list

#--------------------------------------------------------------------------------------------------------------------------------------------------------

def customerMethods(radioVar):
  if radioVar == 1:
    return insertCustomer()
  elif radioVar == 2:
    return editCustomer()
  elif radioVar == 3:
    return showCustomerList()
  else:
    messagebox.showerror("Error!", "Feature not impemented yet...")

def insertCustomer():

  ctr_mid = Frame(dashboardWindow.innerFrame2, bg=innerFrameColor)
  ctr_mid.pack(side='left', fill=BOTH, expand=True) 

  L1 = Label(ctr_mid, text = "Company Name:", bg = innerFrameColor)
  L1.grid(row=0, column=0, padx=10, pady=10)
  L2 = Label(ctr_mid, text = "E-mail:", bg = innerFrameColor)
  L2.grid(row=1, column=0, padx=10, pady=10)
  L3 = Label(ctr_mid, text = "Phone number:", bg = innerFrameColor)
  L3.grid(row=2, column=0, padx=10, pady=10)
  L4 = Label(ctr_mid, text = "Tax ID:", bg = innerFrameColor)
  L4.grid(row=3, column=0, padx=10, pady=10)
  L5 = Label(ctr_mid, text = "Street:", bg = innerFrameColor)
  L5.grid(row=4, column=0, padx=10, pady=10)
  L6 = Label(ctr_mid, text = "Street number:", bg = innerFrameColor)
  L6.grid(row=5, column=0, padx=10, pady=10)
  L7 = Label(ctr_mid, text = "Postcode:", bg = innerFrameColor)
  L7.grid(row=6, column=0, padx=10, pady=10)
  L8 = Label(ctr_mid, text = "City:", bg = innerFrameColor)
  L8.grid(row=7, column=0, padx=10, pady=10)
  L9 = Label(ctr_mid, text = "Firstname:", bg = innerFrameColor)
  L9.grid(row=8, column=0, padx=10, pady=10)
  L10 = Label(ctr_mid, text = "Lastname:", bg = innerFrameColor)
  L10.grid(row=9, column=0, padx=10, pady=10)
  L11 = Label(ctr_mid, text = "Customer type:", bg = innerFrameColor)
  L11.grid(row=10, column=0, padx=10, pady=10)

  customer_Type = IntVar(ctr_mid, 0)

  E1 = Entry(ctr_mid, width=30)
  E1.grid(row=0, column=1, ipadx="100")
  E2 = Entry(ctr_mid, width=30)
  E2.grid(row=1, column=1, ipadx="100")
  E3 = Entry(ctr_mid, width=30)
  E3.grid(row=2, column=1, ipadx="100")
  E4 = Entry(ctr_mid, width=30)
  E4.grid(row=3, column=1, ipadx="100")
  E5 = Entry(ctr_mid, width=30)
  E5.grid(row=4, column=1, ipadx="100")
  E6 = Entry(ctr_mid, width=30)
  E6.grid(row=5, column=1, ipadx="100")
  E7 = Entry(ctr_mid, width=30)
  E7.grid(row=6, column=1, ipadx="100")
  E8 = Entry(ctr_mid, width=30)
  E8.grid(row=7, column=1, ipadx="100")
  E9 = Entry(ctr_mid, width=30)
  E9.grid(row=8, column=1, ipadx="100")
  E10 = Entry(ctr_mid, width=30)
  E10.grid(row=9, column=1, ipadx="100")
  E11 = LabelFrame(ctr_mid, bg = innerFrameColor)
  E11.grid(row=10, column=1, ipadx="100")
  E11RB1 = Radiobutton(E11, text = "Retail", variable=customer_Type, value=1, padx= 10, bg = innerFrameColor)
  E11RB1.pack(ipady = 5)
  E11RB2 = Radiobutton(E11, text = " Wholesail", variable=customer_Type, value=2, padx= 10, bg = innerFrameColor)
  E11RB2.pack(ipady = 5)

  query = ("INSERT INTO `customers` ( `companyName`, `email`, `phoneNumber`, `taxId`, `street`, `streetNumber`, `postCode`, `town`, `name`, `lastname`, `customerType`) VALUES( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);")

  B1 = Button(ctr_mid, text="Submit", relief=GROOVE, width= 50, padx=30, pady=15, bg = "#4acfab", activebackground="#4acfab", command=lambda: [dbCursor.execute(query, (E1.get(), E2.get(), E3.get(), E4.get(), E5.get(), E6.get(), E7.get(), E8.get(), E9.get(), E10.get(), customer_Type.get())), messagebox.showinfo("Success!", "Customer inserted successfully.") ,ctr_mid.destroy()])
  B1.grid(row=11, column=1, padx=10, pady=10)
  B2 = Button(ctr_mid, text="Clear", relief=GROOVE, width= 50,  padx=30, pady=15, bg = "#f06262", activebackground="#f06262", command=lambda: delete_entries(ctr_mid))
  B2.grid(row=12, column=1, padx=10, pady=10, sticky=E)

def editCustomer():

  ctr_mid = Frame(dashboardWindow.innerFrame2, bg=innerFrameColor)
  ctr_mid.pack(side='top', fill=BOTH, expand=True) 
  ctr_mid2 = Frame(dashboardWindow.innerFrame2, bg=innerFrameColor)
  ctr_mid2.pack(side='bottom', fill=BOTH, expand=True)

  cols = ('ID', 'Company Name', 'E-mail', 'Phone Number', 'Tax id', 'Street', 'Street Number','Post Code', 'City', 'Firstname', 'Lastname', 'Costumer Type')
  customer_tree = ttk.Treeview(ctr_mid, columns = cols, show='headings', selectmode="browse")
  customer_tree.column('ID', anchor = W, stretch = TRUE, width = 40)
  customer_tree.column('Street Number', anchor = W, stretch = TRUE, width = 40)
  customer_tree.column('Costumer Type', anchor = W, stretch = TRUE, width = 40)
  for col in cols:
    customer_tree.heading(col, text=col, anchor=W)
    if col != 'ID' and col !='Street Number' and col !='Costumer Type':
      customer_tree.column(col, anchor = W, stretch = TRUE, width = 100)
  customer_tree.pack(side='left', fill=BOTH, expand=True) 

  vsb = ttk.Scrollbar(ctr_mid, orient="vertical", command=customer_tree.yview)
  vsb.pack(side='right', fill='y')
  customer_tree.configure(yscrollcommand=vsb.set)

  customer_tree.bind('<ButtonRelease-1>', selectItem(customer_tree))

  dbCursor.execute("SELECT * FROM customers;")
  resultSet = dbCursor.fetchall()
  for dt in resultSet: 
    customer_tree.insert("", 'end',iid=dt[0], text=dt[0],
               values =(dt[0],dt[1],dt[2],dt[3],dt[4],dt[5],dt[6],dt[7],dt[8],dt[9],dt[10],dt[11]))

  select_label = Label(ctr_mid2, text = "Select the customer you wish to edit.", pady=20, bg=innerFrameColor)
  select_label.pack()
  B1 = Button(ctr_mid2, text="Edit Info", relief=GROOVE, width = 50, padx=50, pady=25, bg = "#4acfab", activebackground="#4acfab", command=lambda: editCustomerInfo(selectItem(customer_tree)))
  B1.pack(pady=10)
  B2 = Button(ctr_mid2, text="Delete customer", relief=GROOVE, width = 50, padx=50, pady=25, bg = "#f06262", activebackground="#f06262", command=lambda: deleteCustomer(selectItem(customer_tree)))
  B2.pack()

def editCustomerInfo(selectedItem):

  updateQuery = ("UPDATE `customers` SET `companyName` = %s, `email` = %s, `phoneNumber` = %s, `taxId` = %s, `street` = %s, `streetNumber` = %s, `postCode` = %s, `town` = %s, `name` = %s, `lastname` = %s, `customerType` = %s WHERE `id` = %s;")
  try:
    if selectedItem:
      editWindow = Tk()
      editWindow.title('Edit info.')
      editWindow.config(bg=innerFrameColor)
      winWidth = 600
      winHeight = 700
      screenWidth = editWindow.winfo_screenwidth()
      screenHeight = editWindow.winfo_screenheight()
      x = (screenWidth / 2) - (winWidth / 2)
      y = (screenHeight / 2) - (winHeight / 2)
      editWindow.geometry(f"{winWidth}x{winHeight}+{int(x)}+{int(y)}")

      L1 = Label(editWindow, text = "Company Name:", bg = innerFrameColor)
      L1.grid(row=0, column=0, padx=10, pady=10)
      L2 = Label(editWindow, text = "E-mail:", bg = innerFrameColor)
      L2.grid(row=1, column=0, padx=10, pady=10)
      L3 = Label(editWindow, text = "Phone number:", bg = innerFrameColor)
      L3.grid(row=2, column=0, padx=10, pady=10)
      L4 = Label(editWindow, text = "Tax ID:", bg = innerFrameColor)
      L4.grid(row=3, column=0, padx=10, pady=10)
      L5 = Label(editWindow, text = "Street:", bg = innerFrameColor)
      L5.grid(row=4, column=0, padx=10, pady=10)
      L6 = Label(editWindow, text = "Street number:", bg = innerFrameColor)
      L6.grid(row=5, column=0, padx=10, pady=10)
      L7 = Label(editWindow, text = "Postcode:", bg = innerFrameColor)
      L7.grid(row=6, column=0, padx=10, pady=10)
      L8 = Label(editWindow, text = "City:", bg = innerFrameColor)
      L8.grid(row=7, column=0, padx=10, pady=10)
      L9 = Label(editWindow, text = "Firstname:", bg = innerFrameColor)
      L9.grid(row=8, column=0, padx=10, pady=10)
      L10 = Label(editWindow, text = "Lastname:", bg = innerFrameColor)
      L10.grid(row=9, column=0, padx=10, pady=10)
      L11 = Label(editWindow, text = "Customer type:", bg = innerFrameColor)
      L11.grid(row=10, column=0, padx=10, pady=10)

      customer_Type = IntVar(editWindow, selectedItem[11])

      E1 = Entry(editWindow, width=30)
      E1.grid(row=0, column=1, ipadx="100")
      E1.insert(0, selectedItem[1])
      E2 = Entry(editWindow, width=30)
      E2.grid(row=1, column=1, ipadx="100")
      E2.insert(0, selectedItem[2])
      E3 = Entry(editWindow, width=30)
      E3.grid(row=2, column=1, ipadx="100")
      E3.insert(0, selectedItem[3])
      E4 = Entry(editWindow, width=30)
      E4.grid(row=3, column=1, ipadx="100")
      E4.insert(0, selectedItem[4])
      E5 = Entry(editWindow, width=30)
      E5.grid(row=4, column=1, ipadx="100")
      E5.insert(0, selectedItem[5])
      E6 = Entry(editWindow, width=30)
      E6.grid(row=5, column=1, ipadx="100")
      E6.insert(0, selectedItem[6])
      E7 = Entry(editWindow, width=30)
      E7.grid(row=6, column=1, ipadx="100")
      E7.insert(0, selectedItem[7])
      E8 = Entry(editWindow, width=30)
      E8.grid(row=7, column=1, ipadx="100")
      E8.insert(0, selectedItem[8])
      E9 = Entry(editWindow, width=30)
      E9.grid(row=8, column=1, ipadx="100")
      E9.insert(0, selectedItem[9])
      E10 = Entry(editWindow, width=30)
      E10.grid(row=9, column=1, ipadx="100")
      E10.insert(0, selectedItem[10])
      E11 = LabelFrame(editWindow, bg = innerFrameColor)
      E11.grid(row=10, column=1, ipadx="100")
      E11RB1 = Radiobutton(E11, text = "Retail", variable=customer_Type, value=1, padx= 10, bg = innerFrameColor)
      E11RB1.pack(ipady = 5)
      E11RB2 = Radiobutton(E11, text = " Wholesail", variable=customer_Type, value=2, padx= 10, bg = innerFrameColor)
      E11RB2.pack(ipady = 5)

      B1 = Button(editWindow, text="Submit", relief=GROOVE, padx=30, pady=15, bg = "#4acfab", activebackground="#4acfab", command=lambda: [dbCursor.execute(updateQuery, (E1.get(), E2.get(), E3.get(), E4.get(), E5.get(), E6.get(), E7.get(), E8.get(), E9.get(), E10.get(), customer_Type.get(), selectedItem[0])), messagebox.showinfo("Success!", "Customer updated successfully."), editWindow.destroy()])
      B1.grid(row=11, column=0, padx=10, pady=(10,0))
      B2 = Button(editWindow, text="Cancel", relief=GROOVE,  padx=30, pady=15, bg = "#f06262", activebackground="#f06262", command=lambda: editWindow.destroy())
      B2.grid(row=11, column=1, padx=10, pady=(10,0), sticky=E)

      editWindow.mainloop()
    else:
      messagebox.showerror("Error!", "You have not selected a customer.")
  except Exception as e:
    print(e)
    editWindow.destroy()
    messagebox.showerror("Error!", "Something went wrong. Please try again.")

def deleteCustomer(selectedItem):
  
  query = ("DELETE FROM `customers` WHERE `id` = %s;")
  try:
    dbCursor.execute(query, (selectedItem[0],))
    messagebox.showinfo("Success!", "Customer deleted successfully.")
  except:
    messagebox.showerror("Error!", "Something went wrong. Please try again.")

def showCustomerList():

  query = ("SELECT * FROM customers;")
  dbCursor.execute(query)
  resultSet = dbCursor.fetchall()
  
  cols = ('ID', 'Company Name', 'E-mail', 'Phone Number', 'Tax id', 'Street', 'Street Number','Post Code', 'City', 'Firstname', 'Lastname', 'Costumer Type')

  customer_tree = ttk.Treeview(dashboardWindow.innerFrame2, columns = cols, show='headings')
  customer_tree.column('ID', anchor = W, stretch = TRUE, width = 40)
  customer_tree.column('Street Number', anchor = W, stretch = TRUE, width = 40)
  customer_tree.column('Costumer Type', anchor = W, stretch = TRUE, width = 40)
  for col in cols:
    customer_tree.heading(col, text=col, anchor=W)
    if col != 'ID' and col !='Street Number' and col !='Costumer Type':
      customer_tree.column(col, anchor = W, stretch = TRUE, width = 100)
  customer_tree.pack(side='left', fill=BOTH, expand=True) 

  vsb = ttk.Scrollbar(dashboardWindow.innerFrame2, orient="vertical", command=customer_tree.yview)
  vsb.pack(side='right', fill='y')
  customer_tree.configure(yscrollcommand=vsb.set)
 
  for dt in resultSet: 
    customer_tree.insert("", 'end',iid=dt[0], text=dt[0],
               values =(dt[0],dt[1],dt[2],dt[3],dt[4],dt[5],dt[6],dt[7],dt[8],dt[9],dt[10],dt[11]))

#--------------------------------------------------------------------------------------------------------------------------------------------------------

def messageMethods(radioVar):
  if radioVar == 1:
    return insertMessage()
  elif radioVar == 2:
    return editMessage()
  elif radioVar == 3:
    return showArchivedMessages()
  else:
    messagebox.showerror("Error!", "Feature not impemented yet...")

def insertMessage():

  ctr_mid = Frame(dashboardWindow.innerFrame2, bg=innerFrameColor)
  ctr_mid.pack(side='left', fill=BOTH, expand=True) 

  L1 = Label(ctr_mid, text="Message:", bg = innerFrameColor)
  L1.pack(pady=10)
  E1 = Text(ctr_mid, bd = 2)
  E1.pack(ipadx=ctr_mid.winfo_width(), ipady=10)

  message_source_list = ["1 (Email)", "2 (Phone)", "3 (Meeting)", "4 (Letter)"]
  message_source = StringVar()
  message_source_menu = ttk.OptionMenu(ctr_mid, message_source, message_source_list[0], *message_source_list)
  message_source_menu.pack(pady=5)

  L2 = Label(ctr_mid, text="Date of the message:", bg = innerFrameColor)
  L2.pack(pady=5)

  cal = Calendar(ctr_mid, selectmode = 'day', date_pattern="y-mm-dd")
  cal.pack(pady = 5)
  def selected_Date():
    selected_date = cal.get_date()
    return selected_date
  cal.bind("<<DateEntrySelected>>", selected_Date())

  query = ("INSERT INTO `messages` ( `content`, `messagedate`, `messagesource`) VALUES( %s, %s, %s);")
  
  B1 = Button(ctr_mid, text="Submit", relief=GROOVE, width=50, padx=50, pady=20, bg = "#4acfab", activebackground="#4acfab", command=lambda: [dbCursor.execute(query, (E1.get("1.0",'end-1c'), selected_Date(), message_source.get())), ctr_mid.destroy(), messagebox.showinfo("Success!", "Message inserted successfully.")])
  B1.pack()
  B2 = Button(ctr_mid, text="Cancel", relief=GROOVE, width=50, padx=50, pady=20, bg = "#f06262", activebackground="#f06262", command=lambda: ctr_mid.destroy())
  B2.pack()

def editMessage():

  ctr_mid = Frame(dashboardWindow.innerFrame2, bg=innerFrameColor)
  ctr_mid.pack(side='top', fill=BOTH, expand=True) 
  ctr_mid2 = Frame(dashboardWindow.innerFrame2, bg=innerFrameColor)
  ctr_mid2.pack(side='bottom', fill=BOTH, expand=True)

  cols = ('ID', 'Content', 'Message Date', 'Message Source')

  message_tree = ttk.Treeview(ctr_mid, columns = cols, show='headings')
  message_tree.column('ID', anchor = W, stretch = TRUE, width = 20)
  message_tree.column('Content', anchor = W, stretch = TRUE, width = 400)
  message_tree.column('Message Date', anchor = W, stretch = TRUE, width = 40)
  message_tree.column('Message Source', anchor = W, stretch = TRUE, width = 40)
  for col in cols:
    message_tree.heading(col, text=col, anchor=W)
  message_tree.pack(side='left', fill=BOTH, expand=True) 

  vsb = ttk.Scrollbar(ctr_mid, orient="vertical", command=message_tree.yview)
  vsb.pack(side='right', fill='y')
  message_tree.configure(yscrollcommand=vsb.set)

  message_tree.bind('<ButtonRelease-1>', selectItem(message_tree))  

  dbCursor.execute("SELECT * FROM messages;")
  resultSet = dbCursor.fetchall()
  for dt in resultSet: 
    message_tree.insert("", 'end',iid=dt[0], text=dt[0],
               values =(dt[0],dt[1],dt[2],dt[3]))

  select_label = Label(ctr_mid2, text = "Select a message you wish to edit.", pady=20, bg=innerFrameColor)
  select_label.pack()
  B1 = Button(ctr_mid2, text="Edit message", relief=GROOVE, width = 50, padx=50, pady=25, bg = "#4acfab", activebackground="#4acfab", command=lambda: editMessageInfo(selectItem(message_tree)))
  B1.pack(pady=10)
  B2 = Button(ctr_mid2, text="Delete message", relief=GROOVE, width = 50, padx=50, pady=25, bg = "#f06262", activebackground="#f06262", command=lambda: deleteMessage(selectItem(message_tree)))
  B2.pack()

def editMessageInfo(selectedItem):
  updateQuery = ("UPDATE `messages` SET `content` = %s, `messagedate` = %s, `messagesource` = %s WHERE `id` = %s;")
  try:
    if selectedItem:
      editWindow = Tk()
      editWindow.title('Edit info.')
      editWindow.config(bg=innerFrameColor)
      winWidth = 800
      winHeight = 900
      screenWidth = editWindow.winfo_screenwidth()
      screenHeight = editWindow.winfo_screenheight()
      x = (screenWidth / 2) - (winWidth / 2)
      y = (screenHeight / 2) - (winHeight / 2)
      editWindow.geometry(f"{winWidth}x{winHeight}+{int(x)}+{int(y)}") 

      L1 = Label(editWindow, text="Message:", bg = innerFrameColor)
      L1.pack(pady=10)
      E1 = Text(editWindow, bd = 2)
      E1.pack(ipadx=editWindow.winfo_width(), ipady=10)
      E1.insert(INSERT, selectedItem[1])

      message_source_list = ["1 (Email)", "2 (Phone)", "3 (Meeting)", "4 (Letter)"]
      message_source = StringVar(editWindow)
      message_source_menu = ttk.OptionMenu(editWindow, message_source, selectedItem[3], *message_source_list)
      message_source_menu.pack(pady=5)
      
      L2 = Label(editWindow, text="Date of the message:", bg = innerFrameColor)
      L2.pack(pady=5)

      cal = Calendar(editWindow, selectmode = 'day', date_pattern="y-mm-dd")
      cal.pack(pady = 5)
      cal.selection_set(selectedItem[2])
      def selected_Date():
        selected_date = cal.get_date()
        return selected_date
      cal.bind("<<DateEntrySelected>>", selected_Date())
      
      B1 = Button(editWindow, text="Submit", relief=GROOVE, width=50, padx=50, pady=20, bg = "#4acfab", activebackground="#4acfab", command=lambda: [dbCursor.execute(updateQuery, (E1.get("1.0",'end-1c'), selected_Date(), message_source.get(), selectedItem[0])), editWindow.destroy(), messagebox.showinfo("Success!", "Message updated successfully.")])
      B1.pack(pady=10)
      B2 = Button(editWindow, text="Cancel", relief=GROOVE, width=50, padx=50, pady=20, bg = "#f06262", activebackground="#f06262", command=lambda: editWindow.destroy())
      B2.pack()

      editWindow.mainloop()
    else:
      messagebox.showerror("Error!", "You have not selected a message.")
    mainloop()
  except Exception as e:
    print(e)
    editWindow.destroy()
    messagebox.showerror("Error!", "Something went wrong. Please try again.")

def deleteMessage(selectedItem):
  query = ("DELETE FROM `messages` WHERE `id` = %s;")
  try:
    dbCursor.execute(query, (selectedItem[0],))
    messagebox.showinfo("Success!", "Message deleted successfully.")
  except:
    messagebox.showerror("Error!", "Something went wrong. Please try again.")

def showArchivedMessages():

  query = ("SELECT * FROM messages;")
  dbCursor.execute(query)
  resultSet = dbCursor.fetchall()
  
  cols = ('ID', 'Content', 'Message Date', 'Message Source')

  message_tree = ttk.Treeview(dashboardWindow.innerFrame2, columns = cols, show='headings')
  message_tree.column('ID', anchor = W, stretch = TRUE, width = 20)
  message_tree.column('Content', anchor = W, stretch = TRUE, width = 400)
  message_tree.column('Message Date', anchor = W, stretch = TRUE, width = 40)
  message_tree.column('Message Source', anchor = W, stretch = TRUE, width = 40)
  for col in cols:
    message_tree.heading(col, text=col, anchor=W)
  message_tree.pack(side='left', fill=BOTH, expand=True) 

  vsb = ttk.Scrollbar(dashboardWindow.innerFrame2, orient="vertical", command=message_tree.yview)
  vsb.pack(side='right', fill='y')
  message_tree.configure(yscrollcommand=vsb.set)
 
  for dt in resultSet: 
    message_tree.insert("", 'end',iid=dt[0], text=dt[0],
               values =(dt[0],dt[1],dt[2],dt[3]))

#--------------------------------------------------------------------------------------------------------------------------------------------------------

def userMethods(radioVar):
  if radioVar == 1:
    return insertUser()
  elif radioVar == 2:
    return editUser()
  elif radioVar == 3:
    return showAllUsers()
  else:
    messagebox.showerror("Error!", "Feature not impemented yet...") 

def insertUser():

  ctr_mid = Frame(dashboardWindow.innerFrame2, bg=innerFrameColor)
  ctr_mid.pack(side='left', fill=BOTH, expand=True) 

  L1 = Label(ctr_mid, text = "Firstname:", bg = innerFrameColor)
  L1.grid(row=0, column=0, padx=10, pady=10)
  L2 = Label(ctr_mid, text = "Lastname:", bg = innerFrameColor)
  L2.grid(row=1, column=0, padx=10, pady=10)
  L3 = Label(ctr_mid, text = "Username:", bg = innerFrameColor)
  L3.grid(row=2, column=0, padx=10, pady=10)
  L4 = Label(ctr_mid, text = "Password:", bg = innerFrameColor)
  L4.grid(row=3, column=0, padx=10, pady=10)
  L5 = Label(ctr_mid, text = "E-mail:", bg = innerFrameColor)
  L5.grid(row=4, column=0, padx=10, pady=10)
  L6 = Label(ctr_mid, text = "Access level:", bg = innerFrameColor)
  L6.grid(row=5, column=0, padx=10, pady=10)
  L7 = Label(ctr_mid, text = "Active:", bg = innerFrameColor)
  L7.grid(row=6, column=0, padx=10, pady=10)

  access_Level = IntVar()
  activity_Flag = IntVar()

  E1 = Entry(ctr_mid, width=30)
  E1.grid(row=0, column=1, ipadx="100")
  E2 = Entry(ctr_mid, width=30)
  E2.grid(row=1, column=1, ipadx="100")
  E3 = Entry(ctr_mid, width=30)
  E3.grid(row=2, column=1, ipadx="100")
  E4 = Entry(ctr_mid, width=30)
  E4.grid(row=3, column=1, ipadx="100")
  E5 = Entry(ctr_mid, width=30)
  E5.grid(row=4, column=1, ipadx="100")
  E6 = LabelFrame(ctr_mid, bg = innerFrameColor)
  E6.grid(row=5, column=1, ipadx="100")
  E6RB1 = Radiobutton(E6, text = "1 (Administrator)", variable=access_Level, value=1, bg = innerFrameColor, width=20)
  E6RB1.pack(ipady = 5)
  E6RB2 = Radiobutton(E6, text = "2 (Editor)", variable=access_Level, value=2, bg = innerFrameColor, width=20)
  E6RB2.pack(ipady = 5)
  E7 = LabelFrame(ctr_mid, bg = innerFrameColor)
  E7.grid(row=6, column=1, ipadx="100")
  E7RB1 = Radiobutton(E7, text = "1 (Active)", variable=activity_Flag, value=1, bg = innerFrameColor, width=20)
  E7RB1.pack(ipady = 5)
  E7RB2 = Radiobutton(E7, text = "0 (Inactive)", variable=activity_Flag, value=0, bg = innerFrameColor, width=20)
  E7RB2.pack(ipady = 5)

  query = ("INSERT INTO `users` ( `name`, `lastname`, `username`,`password`,`email`,`levelAccess`,`isActive`) VALUES( %s, %s, %s, %s, %s, %s, %s);")

  B1 = Button(ctr_mid, text="Submit", relief=GROOVE, width=50, padx=30, pady=15, bg = "#4acfab", activebackground="#4acfab", command=lambda: [dbCursor.execute(query, (E1.get(), E2.get(), E3.get(), hashlib.md5(E4.get().encode("utf-8")).hexdigest(), E5.get(), access_Level.get(), activity_Flag.get())), messagebox.showinfo("Success!", "User inserted successfully."), ctr_mid.destroy()])
  B1.grid(row=7, column=1, padx=10, pady=10)
  B2 = Button(ctr_mid, text="Clear", relief=GROOVE, width=50, padx=30, pady=15, bg = "#f06262", activebackground="#f06262", command=lambda: delete_entries(ctr_mid))
  B2.grid(row=8, column=1, padx=10, pady=10, sticky=E)

def editUser():
  ctr_mid = Frame(dashboardWindow.innerFrame2, bg=innerFrameColor)
  ctr_mid.pack(side='top', fill=BOTH, expand=True) 
  ctr_mid2 = Frame(dashboardWindow.innerFrame2, bg=innerFrameColor)
  ctr_mid2.pack(side='bottom', fill=BOTH, expand=True)

  cols = ('ID', 'First Name', 'Last Name', 'Username', 'Password', 'Email', 'levelAccess', 'isActive')

  user_tree = ttk.Treeview(ctr_mid, columns = cols, show='headings')
  user_tree.column('ID', anchor = W, stretch = TRUE, width = 40)
  user_tree.column('First Name', anchor = W, stretch = TRUE, width = 100)
  user_tree.column('Last Name', anchor = W, stretch = TRUE, width = 100)
  user_tree.column('Username', anchor = W, stretch = TRUE, width = 100)
  user_tree.column('Password', anchor = W, stretch = TRUE, width = 100)
  user_tree.column('Email', anchor = W, stretch = TRUE, width = 100)
  user_tree.column('levelAccess', anchor = W, stretch = TRUE, width = 40)
  user_tree.column('isActive', anchor = W, stretch = TRUE, width = 40)
  for col in cols:
    user_tree.heading(col, text=col, anchor=W)
  user_tree.pack(side='left', fill=BOTH, expand=True) 

  vsb = ttk.Scrollbar(ctr_mid, orient="vertical", command=user_tree.yview)
  vsb.pack(side='right', fill='y')
  user_tree.configure(yscrollcommand=vsb.set)
  user_tree.bind('<ButtonRelease-1>', selectItem(user_tree))
  dbCursor.execute("SELECT * FROM users;")
  resultSet = dbCursor.fetchall()
  for dt in resultSet: 
    user_tree.insert("", 'end',iid=dt[0], text=dt[0],
               values =(dt[0],dt[1],dt[2],dt[3],dt[4],dt[5],dt[6],dt[7]))
  
  select_label = Label(ctr_mid2, text = "Select the user you wish to edit.", pady=20, bg=innerFrameColor)
  select_label.pack()
  B1 = Button(ctr_mid2, text="Edit Info", relief=GROOVE, width = 50, padx=50, pady=25, bg = "#4acfab", activebackground="#4acfab", command=lambda: editUserInfo(selectItem(user_tree)))
  B1.pack(pady=10)
  B2 = Button(ctr_mid2, text="Delete user", relief=GROOVE, width = 50, padx=50, pady=25, bg = "#f06262", activebackground="#f06262", command=lambda: deleteUser(selectItem(user_tree)))
  B2.pack(pady=10)
  B3 = Button(ctr_mid2, text="Activate/Deactivate user", relief=GROOVE, width = 50, padx=50, pady=25, bg = "#649edd", activebackground="#f06262", command=lambda: userActivityEdit(selectItem(user_tree)))
  B3.pack(pady=10)

def editUserInfo(selectedItem):
  try:
    if selectedItem:

      oldPass = selectedItem[4]

      editWindow = Tk()
      editWindow.title('Edit info.')
      editWindow.config(bg=innerFrameColor)
      winWidth = 800
      winHeight = 900
      screenWidth = editWindow.winfo_screenwidth()
      screenHeight = editWindow.winfo_screenheight()
      x = (screenWidth / 2) - (winWidth / 2)
      y = (screenHeight / 2) - (winHeight / 2)
      editWindow.geometry(f"{winWidth}x{winHeight}+{int(x)}+{int(y)}")

      L1 = Label(editWindow, text = "Firstname:", bg = innerFrameColor)
      L1.grid(row=0, column=0, padx=10, pady=10)
      L2 = Label(editWindow, text = "Lastname:", bg = innerFrameColor)
      L2.grid(row=1, column=0, padx=10, pady=10)
      L3 = Label(editWindow, text = "Username:", bg = innerFrameColor)
      L3.grid(row=2, column=0, padx=10, pady=10)
      L4 = Label(editWindow, text = "Password:", bg = innerFrameColor)
      L4.grid(row=3, column=0, padx=10, pady=10)
      L5 = Label(editWindow, text = "E-mail:", bg = innerFrameColor)
      L5.grid(row=4, column=0, padx=10, pady=10)
      L6 = Label(editWindow, text = "Access level:", bg = innerFrameColor)
      L6.grid(row=5, column=0, padx=10, pady=10)
      L7 = Label(editWindow, text = "Active:", bg = innerFrameColor)
      L7.grid(row=6, column=0, padx=10, pady=10)

      access_Level = IntVar(editWindow, selectedItem[6])
      activity_Flag = IntVar(editWindow, selectedItem[7])

      E1 = Entry(editWindow, width=30)
      E1.grid(row=0, column=1, ipadx="100")
      E1.insert(0, selectedItem[1])
      E2 = Entry(editWindow, width=30)
      E2.grid(row=1, column=1, ipadx="100")
      E2.insert(0, selectedItem[2])
      E3 = Entry(editWindow, width=30)
      E3.grid(row=2, column=1, ipadx="100")
      E3.insert(0, selectedItem[3])
      E4 = Entry(editWindow, width=30)
      E4.grid(row=3, column=1, ipadx="100")
      E4.insert(0, selectedItem[4])
      E5 = Entry(editWindow, width=30)
      E5.grid(row=4, column=1, ipadx="100")
      E5.insert(0, selectedItem[5])
      E6 = LabelFrame(editWindow, bg = innerFrameColor)
      E6.grid(row=5, column=1, ipadx="100")
      E6RB1 = Radiobutton(E6, text = "1 (Administrator)", variable=access_Level, value=1, bg = innerFrameColor, width=20)
      E6RB1.pack(ipady = 5)
      E6RB2 = Radiobutton(E6, text = "2 (Editor)", variable=access_Level, value=2, bg = innerFrameColor, width=20)
      E6RB2.pack(ipady = 5)
      E7 = LabelFrame(editWindow, bg = innerFrameColor)
      E7.grid(row=6, column=1, ipadx="100")
      E7RB1 = Radiobutton(E7, text = "1 (Active)", variable=activity_Flag, value=1, bg = innerFrameColor, width=20)
      E7RB1.pack(ipady = 5)
      E7RB2 = Radiobutton(E7, text = "0 (Inactive)", variable=activity_Flag, value=0, bg = innerFrameColor, width=20)
      E7RB2.pack(ipady = 5)

      def updateQueryCheck(oldPass):
        if oldPass == E4.get():
          updateQuery = ("UPDATE `users` SET `name` = %s, `lastname` = %s, `username` = %s, `email` = %s, `levelAccess` = %s, `isActive` = %s  WHERE `id` = %s;")
          dbCursor.execute(updateQuery, (E1.get(), E2.get(), E3.get(), E5.get(), access_Level.get(), activity_Flag.get(), selectedItem[0]))
        else:
          updateQuery = ("UPDATE `users` SET `name` = %s, `lastname` = %s, `username` = %s, `password` = %s, `email` = %s, `levelAccess` = %s, `isActive` = %s  WHERE `id` = %s;")
          dbCursor.execute(updateQuery, (E1.get(), E2.get(), E3.get(), hashlib.md5(E4.get().encode("utf-8")).hexdigest(), E5.get(), access_Level.get(), activity_Flag.get(), selectedItem[0]))

      B1 = Button(editWindow, text="Submit", relief=GROOVE, width=50, padx=30, pady=15, bg = "#4acfab", activebackground="#4acfab", command=lambda: [updateQueryCheck(oldPass), messagebox.showinfo("Success!", "User updated successfully."), editWindow.destroy()])
      B1.grid(row=7, column=1, padx=10, pady=10)
      B2 = Button(editWindow, text="Cancel", relief=GROOVE, width=50, padx=30, pady=15, bg = "#f06262", activebackground="#f06262", command=lambda: editWindow.destroy())
      B2.grid(row=8, column=1, padx=10, pady=10, sticky=E)
    else:
      messagebox.showerror("Error!", "You have not selected a user.")
    editWindow.mainloop()
  except Exception as e:
    print(e)
    editWindow.destroy()
    messagebox.showerror("Error!", "Something went wrong. Please try again.")

def deleteUser(selectedItem):
  query = ("DELETE FROM `users` WHERE `id` = %s;")
  try:
    dbCursor.execute(query, (selectedItem[0],))
    messagebox.showinfo("Success!", "User deleted successfully.")
  except:
    messagebox.showerror("Error!", "Something went wrong. Please try again.")

def userActivityEdit(selectedItem):
  try:
    if selectedItem:
      if selectedItem[7] == 0:
        query = "UPDATE `users` SET  `isActive` = 1  WHERE `id` = %s;"
        val = (selectedItem[0],)
        dbCursor.execute(query, val)
        messagebox.showinfo("Success!", "User activated successfully.")
      else:
        query = "UPDATE `users` SET  `isActive` = 0  WHERE `id` = %s;"
        val = (selectedItem[0],)
        dbCursor.execute(query, val)
        messagebox.showinfo("Success!", "User deactivated successfully.") 
    else:
      messagebox.showerror("Error!","You have not selected a user.")
  except Exception as e:
    print(e)
    messagebox.showerror("Error!", "Something went wrong. Please try again.")

def showAllUsers():

  query = ("SELECT * FROM users;")
  dbCursor.execute(query)
  resultSet = dbCursor.fetchall()
  
  cols = ('ID', 'First Name', 'Last Name', 'Username', 'Password', 'Email', 'levelAccess', 'isActive')

  user_tree = ttk.Treeview(dashboardWindow.innerFrame2, columns = cols, show='headings')
  user_tree.column('ID', anchor = W, stretch = TRUE, width = 40)
  user_tree.column('First Name', anchor = W, stretch = TRUE, width = 100)
  user_tree.column('Last Name', anchor = W, stretch = TRUE, width = 100)
  user_tree.column('Username', anchor = W, stretch = TRUE, width = 100)
  user_tree.column('Password', anchor = W, stretch = TRUE, width = 100)
  user_tree.column('Email', anchor = W, stretch = TRUE, width = 100)
  user_tree.column('levelAccess', anchor = W, stretch = TRUE, width = 40)
  user_tree.column('isActive', anchor = W, stretch = TRUE, width = 40)
  for col in cols:
    user_tree.heading(col, text=col, anchor=W)
  user_tree.pack(side='left', fill=BOTH, expand=True) 

  vsb = ttk.Scrollbar(dashboardWindow.innerFrame2, orient="vertical", command=user_tree.yview)
  vsb.pack(side='right', fill='y')
  user_tree.configure(yscrollcommand=vsb.set)
 
  for dt in resultSet: 
    user_tree.insert("", 'end',iid=dt[0], text=dt[0],
               values =(dt[0],dt[1],dt[2],dt[3],dt[4],dt[5],dt[6],dt[7]))

#--------------------------------------------------------------------------------------------------------------------------------------------------------

def dashboardWindow():
  dashboardWindow.dashboard = Tk()
  dashboardWindow.dashboard.title('CRM - Dashboard')
  dashboardWindow.dashboard.config(bg="#f4f4f4")
  appWidth = 1600
  appHeight = 900
  screenWidth = dashboardWindow.dashboard.winfo_screenwidth()
  screenHeight = dashboardWindow.dashboard.winfo_screenheight()
  x = (screenWidth / 2) - (appWidth / 2)
  y = (screenHeight / 2) - (appHeight / 2)
  dashboardWindow.dashboard.geometry(f"{appWidth}x{appHeight}+{int(x)}+{int(y)}")

  photoHome = PhotoImage(file = r"%s\icons\home-page.png" % (os.getcwd())).subsample(5,5)
  photoCostumer = PhotoImage(file = r"%s\icons\customers.png" % (os.getcwd())).subsample(5,5)
  photoMessage = PhotoImage(file = r"%s\icons\envelope.png" % (os.getcwd())).subsample(5,5)
  photoUser = PhotoImage(file = r"%s\icons\user.png" % (os.getcwd())).subsample(5,5)
  photoExit = PhotoImage(file = r"%s\icons\logout.png" % (os.getcwd())).subsample(5,5)

  dashboardWindow.homeButton = Button(dashboardWindow.dashboard, text = "Home", font= ("Helvetica 12 bold"),
    bg = "#6e72f9", activebackground="#9ea0f9", relief=FLAT, image = photoHome, compound = TOP, command = lambda: dashboardOptions(0))
  dashboardWindow.homeButton.grid(row = 1, column = 0, rowspan = 3, sticky = NSEW)

  dashboardWindow.customerButton = Button(dashboardWindow.dashboard, text = "Customers", font= ("Helvetica 12 bold"), 
    bg = "#6e72f9", activebackground="#9ea0f9", relief=FLAT, image = photoCostumer, compound = TOP, command = lambda: dashboardOptions(1))
  dashboardWindow.customerButton.grid(row = 4, column = 0, rowspan = 3, sticky = NSEW)

  dashboardWindow.messageButton = Button(dashboardWindow.dashboard, text = "Messages", font= ("Helvetica 12 bold"),
    bg = "#6e72f9", activebackground="#9ea0f9", relief=FLAT, image = photoMessage, compound = TOP, command = lambda: dashboardOptions(2))
  dashboardWindow.messageButton.grid(row = 7, column = 0, rowspan = 3, sticky = NSEW)

  dashboardWindow.userButton = Button(dashboardWindow.dashboard, text = "Users", font= ("Helvetica 12 bold"), 
    bg = "#6e72f9", activebackground="#9ea0f9", relief=FLAT, image = photoUser, compound = TOP, command = lambda: dashboardOptions(3))
  dashboardWindow.userButton.grid(row = 10, column = 0, rowspan = 3, sticky = NSEW)

  dashboardWindow.dashboard.rowconfigure(13, weight = 1)
  spacer1 = Label(dashboardWindow.dashboard, bg = "#6e72f9")  
  spacer1.grid(row = 13, column = 0, rowspan = 3, sticky = NSEW)  

  exitButton = Button(dashboardWindow.dashboard, text = "Exit", font= ("Helvetica 12 bold"), 
    bg = "#6e72f9", activebackground="#9ea0f9", relief=FLAT, image = photoExit, compound = TOP, command=lambda: dashboardWindow.dashboard.destroy())
  exitButton.grid(row = 14, column = 0,  sticky = SW) 
  
  dashboardWindow.clock = Label(dashboardWindow.dashboard, fg="white", height = 2, anchor = W, bg="#6e72f9", font=("helvetica 8"))
  dashboardWindow.clock.grid(row = 0, column = 0, columnspan = 5, sticky = NSEW)
  
  dashboardWindow.dashboard.grid_columnconfigure(1, weight=1, minsize = 250)
  dashboardWindow.innerFrame1 = Frame(dashboardWindow.dashboard, bg = innerFrameColor) 
  dashboardWindow.innerFrame1.grid(row = 1, column = 1, columnspan = 1, rowspan = 100, sticky = NSEW)

  dashboardWindow.dashboard.grid_columnconfigure(2, weight=4)
  dashboardWindow.innerFrame2 = Frame(dashboardWindow.dashboard, bg = innerFrameColor, padx=10, pady=10)   
  dashboardWindow.innerFrame2.grid(row = 1, column = 2, columnspan = 1, rowspan = 100, sticky = NSEW)
  
  displayLatestMessage()

  if userAcessLvl == 2:
    dashboardWindow.userButton['state'] = DISABLED

  tick()
  dashboardWindow.dashboard.mainloop()

def getLatestMessage():
  dbCursor.execute("SELECT `content`,`messagedate` FROM `messages` WHERE `id` = (SELECT MAX(id) FROM `messages`);")
  resultSet = dbCursor.fetchall()
  return resultSet

def displayLatestMessage():
  latestMessage = Label(dashboardWindow.innerFrame2, text = ("Latest message: " + str(getLatestMessage()[0][0]) + "\n\n Recieved on: " + str(getLatestMessage()[0][1])), bg = "#6e72f9",fg ='white', height=10, width=50, relief= RIDGE, bd=10)
  latestMessage.pack(side=BOTTOM, anchor=E)

def tick():
  now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
  dashboardWindow.clock.config(text=now)
  dashboardWindow.clock.after(200, tick)

#--------------------------------------------------------------------------------------------------------------------------------------------------------

innerFrameColor = "#dbddee"
test_color = "black"

now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

loginToDBPopUp()

c = []

try:
  dbCursor = accessDB.mydb.cursor()
  loginPopUp()
except:
  pass

if c:
  userAcessLvl = (c[0][0][2])
  dashboardWindow()

try:
  accessDB.mydb.close()
except:
  pass