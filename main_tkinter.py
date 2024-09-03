import tkinter as tk
from tkinter import (
        colorchooser as color,
        commondialog as cdialog,
        constants as const,
        dialog,
        dnd,
        filedialog as fdialog,
        font,
        messagebox as msgbox,
        scrolledtext as stext,
        simpledialog as sdialog,
        tix,
        ttk,
        Label,
        Entry,
        Button,
        StringVar,
        LabelFrame,
        RIDGE
    )

from functools import partial

from PIL import Image, ImageTk

import shutil, os
from modules.colordescriptor import ColorDescriptor
import argparse
import glob
import cv2
from modules.searcher import Searcher


import modules.users as users
import modules.vehicle_thefts as vehicle_thefts
import modules.vehicle_recoveries as vehicle_recoveries
import modules.criminals as criminals

superAdminPwd = 'india@top'
loginMode = False
loginGroup = ''
loggedUser = ''
loggedUserPwd = ''


def updateDatasetFeature() :
        

        cd = ColorDescriptor((8, 12, 3))
        output = open('dataset-features.csv', "w")
        # use glob to grab the image paths and loop over them
        for imagePath in glob.glob("dataset_images/*.jpg"):

                imageID = imagePath[imagePath.rfind("/") + 1:]
                image = cv2.imread(imagePath)
         
                # describe the image
                features = cd.describe(image)
         
                # write the features to file
                features = [str(f) for f in features]
                output.write("%s,%s\n" % (imageID, ",".join(features)))

        for imagePath in glob.glob("dataset_images/*.png"):

                imageID = imagePath[imagePath.rfind("/") + 1:]
                image = cv2.imread(imagePath)
         
                # describe the image
                features = cd.describe(image)
         
                # write the features to file
                features = [str(f) for f in features]
                output.write("%s,%s\n" % (imageID, ",".join(features)))
         
        # close the index file
        output.close()

def searchCriminalImage(query_image_path, frameResult) :

        cd = ColorDescriptor((8, 12, 3))

        # load the query image and describe it
        query = cv2.imread(query_image_path)
        features = cd.describe(query)
         
        # perform the search
        searcher = Searcher('dataset-features.csv')
        results = searcher.search(features)
         
        # display the query
        #cv2.imshow("Query", query)

        #print(results)
        criminal_data = criminals.list()

        for (score, resultID) in results:
            # load the result image and display it
            print("Image name: ",resultID)

            for criminal in criminal_data :
                print(criminal)
                if criminal['pic'] == resultID.replace('\\','/') :
                    img = Image.open(resultID).resize((200, 150))
                    photo = ImageTk.PhotoImage(img)
                    lblResultPic = Label(frameResult, image=photo, width=200, height=150)
                    lblResultPic.image = photo 

                    lblHeading = Label(frameResult, text="Match Found",font=("Arial", 20)).grid(row=0, column=0)
                    lblResultPic.grid(row=1,column=0)
                    lblName = Label(frameResult, text="Name:" + criminal['name'],font=("Arial", 10)).grid(row=2, column=0)
                    lblDob = Label(frameResult, text="Date of Birth:" + criminal['dob'],font=("Arial", 10)).grid(row=3, column=0)
                    lblAadhaar = Label(frameResult, text="Aadhaar:" + criminal['aadhaar_no'],font=("Arial", 10)).grid(row=4, column=0)
                    lblAdd = Label(frameResult, text="Add:" + criminal['address'],font=("Arial", 10)).grid(row=5, column=0)
                    
                    
                    return

            # result = cv2.imread('img' + "\\" + resultID)    
            # cv2.imshow('Results', result)
            # cv2.waitKey(0)





def Create_Toplevel():

        # THE CLUE
        root.wm_attributes("-disabled", True)

        # Creating the toplevel dialog
        toplevel_dialog = tk.Toplevel(root)
        #toplevel_dialog.minsize(300, 100)

        # Tell the window manager, this is the child widget.
        # Interesting, if you want to let the child window 
        # flash if user clicks onto parent
        toplevel_dialog.transient(root)



        # This is watching the window manager close button
        # and uses the same callback function as the other buttons
        # (you can use which ever you want, BUT REMEMBER TO ENABLE
        # THE PARENT WINDOW AGAIN)

        Close_ToplevelCallback = partial(Close_Toplevel, toplevel_dialog)
        toplevel_dialog.protocol("WM_DELETE_WINDOW", Close_ToplevelCallback)
        
        return toplevel_dialog

def Close_Toplevel(toplevel_dialog):
    # IMPORTANT!
    root.wm_attributes("-disabled", False) # IMPORTANT!

    toplevel_dialog.destroy()

    # Possibly not needed, used to focus parent window again
    root.deiconify()

def deleteRecordButton_click(tree, model) :
    answer = "no"
        
    selected_row = False
    for selected_item in tree.selection():
        if answer == "no":
            answer = msgbox.askquestion(title='confirmation', message='Are you sure that you want to delete?')

        if answer=="no":
            return
        selected_row = True
        
        item = tree.item(selected_item)
        #print(item)
        record = item['values']
        #print(record)
        id_for_delete = record[0]

        if id_for_delete == 1 :
            msgbox.showerror(title='System Error', message='First Record not allowed to delete with ID:' + str(id_for_delete))
            continue;
        
        #print(id_for_delete)

        result = model.deleteByID(str(id_for_delete))
        if result :
            tree.delete(selected_item)
            msgbox.showinfo(title='System Delete Information', message='Record successfully deleted from DB for ID:' + str(id_for_delete))
        else :
            msgbox.showerror(title='System Error', message='Record could not deleted from DB for ID:' + str(id_for_delete))

    if not selected_row :
        msgbox.showerror(title='System Error', message='Something Need to Select')    


def clearTxtBox(txtbox) :
    txtbox.delete(0, "end")

def saveButton_click(model, params, tree) :
    update_dataset_required = False
    paramsval = []
    for param in params :
        pval = param.get();
        print(pval)
        if 'img_path:' in pval :
                pval = pval.replace('img_path:','')
                #print(pval)
                shutil.copy(pval, './dataset_images')
                basename = os.path.basename(pval)
                #print(basename)
                pval = 'dataset_images/' + basename
                #print(pval)
                update_dataset_required = True
        paramsval.append(pval)


    result = model.add(*paramsval)
    res = bool(model.response_msg)
    if res and result :
        msgbox.showinfo(title='System Save Information', message= model.response_msg['msg'])
        for param in params :
            clearTxtBox(param)

        #Prepare List to insert in Tree
        newData = []
        for key in model.response_msg['item_inserted'] :
            newData.append(model.response_msg['item_inserted'][key])

        tree.insert('', 'end', value=newData) #insert newData in Tree

        updateDatasetFeature()
        print(model.response_msg)
        return True
    elif res and not result :
        msgbox.showerror(title='System Error', message= model.response_msg['msg'])
        return False
    else :
        msgbox.showerror(title='System Error', message= 'Unknow Error while saving')
        return False
        #printMsg("SYSTEM " + vehicle_thefts.response_msg['status'].upper() + " : " + vehicle_thefts.response_msg['msg'])
    

def prepareTree(window, model) :
    #Get data From Function
    list_data = model.list()
    #print(list_data)
    
    col = []
    values=[]
    tree_list_data = []
    for row in list_data :
        col = []
        values = []
        i=0
        for key in row :
            col.append(key)
            values.append(str(row[key]))
            i +=1
        tree_list_data.append(values)
    
    #columns = ('first_name', 'last_name', 'email')
    columns = tuple(col) # Dynamic col

    tree = ttk.Treeview(window, columns=columns, show='headings')

    for val in columns :
        tree.heading(val, text= val.upper().replace('_',' '))
        if val == 'id' :
            tree.column(val, minwidth=0, width=50, stretch="no")
        else:
            tree.column(val, minwidth=0, width=160, stretch="no")
    
    # add data to the treeview
    for data_row in tree_list_data:
        tree.insert('', tk.END, values=data_row)

    #print(contacts)
    
    tree.grid(row=2, column=0, padx=20, pady=20, sticky='nsew', rowspan=10)

    #tree.bind('<<TreeviewSelect>>', item_selected)    
    # add a scrollbar
    scrollbar = ttk.Scrollbar(window, orient=tk.VERTICAL, command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.grid(row=2, column=1, sticky='ns', rowspan=10)
    return tree

def logout() :
        global loginMode, loginGroup, loggedUser, loggedUserPwd, superAdminPwd, btnDashboardLogin
        print("logout")
        loginMode = False
        loginGroup = ''
        loggedUser = ''
        loggedUserPwd = ''
        btnDashboardLogin.configure(text = "Login", command=loginForm)
        #btnDashboardLogin['text'] = 'Login'
        #btnDashboardLogin['command'] = ''


def validateLogin(username, password, btn, window):
    global loginMode, loginGroup, loggedUser, loggedUserPwd, superAdminPwd, btnDashboardLogin
    user = username.get().strip()
    pwd = password.get().strip()
    error = ''

    if len(user) <= 2 :
        error = 'Username required with minimum 3 character'
    elif not user.isalnum():
        error = 'Username can only contain alphanumeric characters'

    elif len(pwd) <5 :
        error = 'password required with minimum 6 character'

    if len(error) >=1 :
        return msgbox.showerror( "Error", error)

    if btn == 'register_btn_click' :
        print("under construction")
        #saveResult = saveUser(user, pwd)
    elif btn == 'login_btn_click' :
        #print(user.strip())
        #print(pwd.strip())
        if user.strip() == 'superadmin' and pwd.strip() == superAdminPwd :
            msgbox.showinfo(title="Login Success", message= "You have successfully login in system")
            btnDashboardLogin.configure(text = "Logout", command=logout)
            #btnDashboardLogin.place_forget()
            loginMode = True
            loginGroup = 'superadmin'
            Close_Toplevel(window)
            return True
        else :
            result = users.isValidUser(user.strip(), pwd.strip())
            if not result :
                if users.response_msg != '' :
                    msgbox.showerror(title='Login Error', message= users.response_msg['msg'])
            else :
                msgbox.showinfo(title="Login Success", message= "You have successfully login in system")
                btnDashboardLogin.configure(text = "Logout", command=logout)
                #btnDashboardLogin.place_forget()
                loginMode = True
                loginGroup = 'admin'
                loggedUser = username
                loggedUserPwd = pwd
                Close_Toplevel(window)
                return True

    return

def loginForm():
    #tkWindow = tk.Toplevel(root)
    tkWindow = Create_Toplevel();
    frmc = ttk.Frame(tkWindow, padding=10)
    frmc.grid()

    #tkWindow.geometry('400x150')  
    tkWindow.title('Login')
    Label(frmc, text="Login Form",font=("Arial", 14)).grid(row=0, column=0)
    #username label and text entry box
    usernameLabel = Label(frmc, text="User Name").grid(row=1, column=0)
    username = StringVar()
    usernameEntry = Entry(frmc, textvariable=username).grid(row=1, column=1)  

    #password label and password entry box
    passwordLabel = Label(frmc,text="Password").grid(row=2, column=0)  
    password = StringVar()
    passwordEntry = Entry(frmc, textvariable=password, show='*').grid(row=2, column=1)  
    validateLoginCallback = partial(validateLogin, username, password, 'login_btn_click', tkWindow)

    #login button
    loginButton = Button(frmc, text="Login", command=validateLoginCallback).grid(row=3, column=0)

    '''
    registerFormCallback = partial(registerForm, tkWindow) #passing login window to close in register form
    #Register button
    registerButton = Button(frmc, text="Create New Account", command=registerFormCallback).grid(row=3, column=1)
    '''


def fileDialog(frameAddNew, input5_Entry):

        filename = fdialog.askopenfilename(initialdir =  "./", title = "Select A File", filetype =
        (("jpeg files","*.jpg"),("all files","*.*")) )
        '''
        label = ttk.Label(frameAddNew, text = "")
        label.grid(row=4, column=2 )
        label.configure(text = filename)
        '''
        img = Image.open(filename)
        photo = ImageTk.PhotoImage(img)

        label2 = Label(frameAddNew, image=photo, width=100, height=100)
        label2.image = photo 
        label2.grid(row=4,column=2)

        input5_Entry.configure(state='normal')
        input5_Entry.insert('end', 'img_path:' + filename)
        input5_Entry.configure(state='disabled')


def fileDialogFindCriminal(frameAddNew, filename_input_box, frameSearchResult) :
        filename = fdialog.askopenfilename(initialdir =  "./", title = "Select A File", filetype =
        (("jpeg files","*.jpg"),("all files","*.*")) )
        img = Image.open(filename).resize((200, 150))
        photo = ImageTk.PhotoImage(img)

        label2 = Label(frameAddNew, image=photo, width=200, height=150)
        label2.image = photo 
        label2.grid(row=1,column=0, columnspan=2)

        searchCriminalImageCallback = partial(searchCriminalImage, filename, frameSearchResult)

        btnStartSearching=tk.Button(frameAddNew,
                              text="Start Search",
                                width=10,
                              command=searchCriminalImageCallback)
        btnStartSearching.grid(row=0, column=1, padx=10, pady=2)
        
        filename_input_box.insert('end', 'img_path:' + filename)
        



def prepare_window(model, title) :
    global loginMode, loginGroup

    if not loginMode and (title == 'FIND CRIMINAL' or title == 'USERS') :
            loginForm()
            return
    
    #print(model)
    #print(title)
    #window = tk.Tk()
    window = Create_Toplevel();

    if title == 'FIND CRIMINAL' :
            window.geometry("600x400")
    else :
            window.geometry("%dx%d" % (width, height/2))

    window.title(title)
    label = tk.Label(window, text=title,font=('verdana',20,'bold'),fg="#248aa2")

    label.grid(row=0, column=0, columnspan=2)


    if title == 'FIND CRIMINAL' :
            findCriminalForm(window)
            return


    
    tree = prepareTree(window, model)
    
    ####BUTTONS

    if loginMode :
        deleteData = partial(deleteRecordButton_click, tree, model)
        btnDelete=tk.Button(window,
                      text="Delete",
                      width=10,
                      command=deleteData)
        btnDelete.grid(row=1, column=0, padx=20, pady=2, sticky='w')

    if title == 'FIR LIST' or (loginMode and loginGroup == 'admin' and title != 'USERS') or (loginMode and loginGroup == 'superadmin') :

        frameAddNew = LabelFrame(window,text="Add New Record",width=150,height=200,font=('verdana',10,'bold'),borderwidth=3,relief=RIDGE,highlightthickness=4,bg="white",highlightcolor="white",highlightbackground="white",fg="#248aa2")
        frameAddNew.grid(row=2,column=3, columnspan=2, rowspan=10, sticky='n')

        addNewRecordLabel1 = 'Vehicle No.  :'
        addNewRecordLabel2 = 'Vehicle Type :'

        if title == 'USERS':
            addNewRecordLabel1 = 'User:'
            addNewRecordLabel2 = 'Pwd :'

        elif title == 'CRIMINALS':
            addNewRecordLabel1 = 'Name:'
            addNewRecordLabel2 = 'AAdhaar No.:'
            
        label = tk.Label(frameAddNew, text=addNewRecordLabel1,font=('verdana',10,'bold'))
        label.grid(row=0, column=1, padx=10, pady=10)

        
        input_text_1 = StringVar()
        input1_Entry = Entry(frameAddNew, textvariable=input_text_1)
        input1_Entry.grid(row=0, column=2, padx=10, pady=10)
        
        label = tk.Label(frameAddNew, text=addNewRecordLabel2,font=('verdana',10,'bold'))
        label.grid(row=1, column=1, padx=10, pady=10)

        
        input_text_2 = StringVar()
        input2_Entry = Entry(frameAddNew, textvariable=input_text_2)
        input2_Entry.grid(row=1, column=2, padx=10, pady=10)

        if title == 'CRIMINALS' :

            label = tk.Label(frameAddNew, text='Date of Birth:',font=('verdana',10,'bold'))
            label.grid(row=2, column=1, padx=10, pady=10)
            input_text_3 = StringVar()
            input3_Entry = Entry(frameAddNew, textvariable=input_text_3)
            input3_Entry.grid(row=2, column=2, padx=10, pady=10)

            label = tk.Label(frameAddNew, text='Address:',font=('verdana',10,'bold'))
            label.grid(row=3, column=1, padx=10, pady=10)
            input_text_4 = StringVar()
            input4_Entry = Entry(frameAddNew, textvariable=input_text_4)
            input4_Entry.grid(row=3, column=2, padx=10, pady=10)

            '''
            label = tk.Label(frameAddNew, text='Photo:',font=('verdana',10,'bold'))
            label.grid(row=4, column=1, padx=10, pady=10)
            input_text_5 = StringVar()
            '''

            input5_Entry = Entry(frameAddNew, state="readonly")
            input5_Entry.grid(row=5, column=2, padx=10, pady=10)


            fileDialogCallback = partial(fileDialog, frameAddNew, input5_Entry)
            btnBrowse = tk.Button(frameAddNew, text = "Photo",command = fileDialogCallback)
            btnBrowse.grid(row=4, column=1,padx=10, pady=10)


            
            
            saveData = partial(saveButton_click, model, [input1_Entry, input2_Entry, input3_Entry, input4_Entry, input5_Entry], tree)
            
            btnAddNew=tk.Button(frameAddNew,
                              text="Save",
                                width=10,
                              command=saveData)
            btnAddNew.grid(row=6, column=1, padx=10, pady=2, sticky='w', columnspan=2)


        else :

            saveData = partial(saveButton_click, model, [input1_Entry, input2_Entry], tree)
            
            btnAddNew=tk.Button(frameAddNew,
                              text="Save",
                                width=10,
                              command=saveData)
            btnAddNew.grid(row=2, column=1, padx=10, pady=2, sticky='w', columnspan=2)
        
    




def findCriminalForm(window) :
        
        frameAddNew = LabelFrame(window,text="Search Photo",width=300,height=300,font=('verdana',10,'bold'),borderwidth=3,relief=RIDGE,highlightthickness=4,bg="white",highlightcolor="white",highlightbackground="white",fg="#248aa2")
        frameAddNew.grid(row=1,column=0, sticky='e')

        btnBrowse = tk.Button(frameAddNew, text = "Select Photo")
        btnBrowse.grid(row=0, column=0,padx=10, pady=10)

        label2 = Label(frameAddNew, text="photo", width=30, height=15)
        label2.grid(row=1,column=0, columnspan=2)

        
        input5_Entry = Entry(frameAddNew)

        frameResult = LabelFrame(window,text="Searching",width=300,height=300,font=('verdana',10,'bold'),borderwidth=3,relief=RIDGE,highlightthickness=4,bg="white",highlightcolor="white",highlightbackground="white",fg="#248aa2")
        frameResult.grid(row=1,column=1, sticky='w')
        
        fileDialogCallback = partial(fileDialogFindCriminal, frameAddNew, input5_Entry, frameResult)
        btnBrowse = tk.Button(frameAddNew, text = "Select Photo",command = fileDialogCallback)
        btnBrowse.grid(row=0, column=0,padx=10, pady=10)

        


#############MAIN TINKER###############################
app_title = "Online Crime Record Management System"
root = tk.Tk()
#frame = tk.Frame(root)
#frame.pack()
width= root.winfo_screenwidth() 
height= root.winfo_screenheight()
root.geometry("%dx%d" % (width, height))
#root.geometry('1080x720')
root.title(app_title)
root.maxsize(width,height)
root.minsize(700,300)
root['bg'] = "white"

heading = Label(root,text=app_title,font=('verdana',20,'bold'),fg="#248aa2",bg="white")
heading.pack()
#heading.place(x=60,y=5)

style1 = Label(root,bg="#248aa2",height=1,width=100)
style1.pack()

prepareFIRWindowCallback = partial(prepare_window, vehicle_thefts, 'FIR LIST')

btnDashboardFIR = tk.Button(root,
                   text="FIRs",
                   fg="blue",
                    width=30,
                    height=15,
                    font=('verdana',8,'bold'),
                    command=prepareFIRWindowCallback)
btnDashboardFIR.place(x=50, y=100)
#button1.pack()

prepareRecoveriesWindowCallback = partial(prepare_window, vehicle_recoveries, 'RECOVERIES')
btnDashboardRecoveries = tk.Button(root,
                    text="Recoveris",
                    width=30,
                    height=15,
                    font=('verdana',8,'bold'),
                    command=prepareRecoveriesWindowCallback)
btnDashboardRecoveries.place(x=300, y=100)

btnDashboardLogin = tk.Button(root,
                    text="Login",
                    width=30,
                    height=15,
                    font=('verdana',8,'bold'),
                    command=loginForm)
btnDashboardLogin.place(x=550, y=100)

prepareUsersWindowCallback = partial(prepare_window, users, 'USERS')
btnDashboardUsers = tk.Button(root,
                    text="Users",
                    width=30,
                    height=15,
                    font=('verdana',8,'bold'),
                    command=prepareUsersWindowCallback)
btnDashboardUsers.place(x=800, y=100)

prepareCriminalsWindowCallback = partial(prepare_window, criminals, 'CRIMINALS')
btnDashboardCriminals = tk.Button(root,
                    text="Criminals",
                    width=30,
                    height=15,
                    font=('verdana',8,'bold'),
                    command=prepareCriminalsWindowCallback)
btnDashboardCriminals.place(x=1050, y=100)

prepareFindCriminalWindowCallback = partial(prepare_window, criminals, 'FIND CRIMINAL')
btnDashboardFindCriminal = tk.Button(root,
                    text="Find Criminal",
                    width=30,
                    height=15,
                    font=('verdana',8,'bold'),
                    command=prepareFindCriminalWindowCallback)
btnDashboardFindCriminal.place(x=50, y=400)

#button2.pack()

root.mainloop()
