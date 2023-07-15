import tkinter as tk
from tkinter import *
from tkinter import filedialog
import glob
from PIL import ImageTk, Image
from io import BytesIO
from tkinter import messagebox
import win32clipboard
import os
import shutil

root = tk.Tk()
root.geometry("500x500")
root.title("PicEmo")

path = "src/img"
files = glob.glob(path + "/*.jpg")
photolist = list()
photolist_clipboard = list()
page = 1
PageInfo = Label(root, text="test")
PageInfo.place(x=185, y=472.5)

pathwindow = None

def refreshpath() :
    global files, photolist, photolist_clipboard, path, PageInfo
    files = glob.glob(path + "/*.jpg") + glob.glob(path + "/*.png") + glob.glob(path + "/*.jpeg") + glob.glob(path + "/*.gif")
    photolist = list()
    photolist_clipboard = list()
    try :
        files.sort(key=lambda fname: int(fname.split('/')[-1].split('.')[0]))
    except :
        pass
    for i in range(0, len(files)):
        files[i] = files[i].replace("\\", "/")
        photolist.append(ImageTk.PhotoImage(Image.open(files[i]).resize((100, 100))))
        photolist_clipboard.append(Image.open(files[i]))
    #print(len(files))
    PageInfo.config(text="Page " + str(page) + " / " + str(int(len(files)/20) + 1) + " (" + str(len(files)) + " files)")

refreshpath()

def addtofavorites(num) :
    global files
    imsi = glob.glob("src/img" + "/*.jpg") + glob.glob("src/img" + "/*.png") + glob.glob("src/img" + "/*.jpeg") + glob.glob("src/img" + "/*.gif")
    shutil.copy2(files[num], "src/img/" + str(len(imsi)+1) + "." +  os.path.basename(files[num]).split('.')[-1])

def deletefavorites(num) :
    global files, photolist, photolist_clipboard
    photolist.pop(num)
    photolist_clipboard.pop(num)
    destroybuttons()
    os.remove(files[num])
    refreshpath()
    makebuttons()

def copypath(num) :
    global files
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardText(os.path.abspath(files[num]))
    win32clipboard.CloseClipboard()

def copyname(num) :
    global files
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardText(os.path.basename(files[num]))
    win32clipboard.CloseClipboard()

def popup_menu(event, number) :
    ButtonMenu = tk.Menu(root, tearoff=0)
    if path != 'src/img' :
        ButtonMenu.add_command(label="Add to Favorites", command=lambda: addtofavorites(number))
        ButtonMenu.add_command(label="Copy File Name", command=lambda: copyname(number))
        ButtonMenu.add_command(label="Copy File Path", command=lambda: copypath(number))
    else :
        ButtonMenu.add_command(label="Remove from Favorites", command=lambda: deletefavorites(number))
    try :
        ButtonMenu.tk_popup(event.x_root, event.y_root)
    finally :
        ButtonMenu.grab_release()


def makebuttons() :
    global page, files, photolist, buttons
    buttons = [[tk.Button() for j in range(5)] for i in range(4)]
    num = -1
    for i in range(0, 4):
        for j in range(0, 5):
            num = num  + 1
            try :
                photo = photolist[num + (page-1) * 20]
                buttons[i][j] = tk.Button(root, image=photo, padx=1, pady=1)
                buttons[i][j].bind("<Button-1>", lambda e, c = num: on_click(c + (page-1) * 20))
                buttons[i][j].bind("<Button-3>", lambda e, c = num: popup_menu(e, c + (page-1) * 20))
                buttons[i][j].place(x=photo.width() * j, y=photo.height() * i + 70)

            except :
                buttons[i][j] = tk.Button(root, bg="gray")
                buttons[i][j].place(x= 100 * j, y= 100 * i + 70, width=100, height=100)
                buttons[i][j].config(state=DISABLED)


def askdirectory():
    global path, PageInfo
    path = filedialog.askdirectory()
    Directory.config(state=NORMAL)
    Directory.delete(0, END)
    Directory.insert(0, path)
    Directory.config(state=DISABLED)
    #print(path)
    refreshpath()
    makebuttons()

Directory = Entry(font=("Arial", 10))
if path != "src/img" :
    Directory.insert(0, os.path.abspath(path))
else :
    Directory.insert(0, "(Favorites)")
Directory.config(state=DISABLED)
Directory.place(x=10, y=15, width=400, height=20)

BrowseDirectory = tk.Button(root, text="Browse", padx=1, pady=1, command= askdirectory)
BrowseDirectory.place(x=420, y=15, width=70, height=20)

def destroybuttons() :
    global buttons
    for i in range(0, 4):
        for j in range(0, 5):
            buttons[i][j].destroy()

def on_click(num):
    global photolist_clipboard
    #print(num)
    output = BytesIO()
    photolist_clipboard[num].convert('RGB').save(output, 'BMP')
    data = output.getvalue()[14:]
    output.close()

    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)
    win32clipboard.CloseClipboard()

def prevpage():
    global page, PageInfo
    if page > 1 :
        page = page - 1
    PageInfo.config(text="Page " + str(page) + " / " + str(int(len(files)/20) + 1) + " (" + str(len(files)) + " files)")
    destroybuttons()
    makebuttons()

def aftpage():
    global page, PageInfo
    if int(len(files)/20) + 1 > page :
        page = page + 1
    PageInfo.config(text="Page " + str(page) + " / " + str(int(len(files)/20) + 1) + " (" + str(len(files)) + " files)")
    destroybuttons()
    makebuttons()

tk.Button(root, text="<", padx=1, pady=1, command= prevpage) .place(x=100, y=470)
tk.Button(root, text=">", padx=1, pady=1, command= aftpage) .place(x=380, y=470)

def favoritebutton() :
    global path
    if path != "src/img" :
        path = "src/img"
        Directory.config(state=NORMAL)
        Directory.delete(0, END)
        Directory.insert(0, "(Favorites)")
        Directory.config(state=DISABLED)
        refreshpath()
        destroybuttons()
        makebuttons()

def selectpath(path1) :
    global path
    path = path1.split(" ")[1].replace("\n", "").replace("(", "").replace(")", "")
    Directory.config(state=NORMAL)
    Directory.delete(0, END)
    Directory.insert(0, path)
    Directory.config(state=DISABLED)
    refreshpath()
    destroybuttons()
    makebuttons()

def deletepath(path1) :
    with open('path.txt', 'r') as f:
        pathlist = f.readlines()
    pathlist.remove(path1+'\n')
    with open('path.txt', 'w') as f:
        f.write("\n".join(pathlist))
    listrefresh()

def listrefresh() :
    global pathwindow, listbox, path
    with open('path.txt', 'r') as f:
        pathlist = f.readlines()
    for i in range(0, len(pathlist)) :
        pathlist[i] = pathlist[i].replace("\n", "")
    listbox = tk.Listbox(pathwindow)
    listbox.insert(END, *pathlist)
    listbox.place(x=0, y=50, width=300, height=350)

def deleteallpath() :
    warning = messagebox.askokcancel("Delete All Path", "Are you sure you want to delete all path?")
    if warning :
        with open('path.txt', 'w') as f:
            f.write("")
        listrefresh()

def addpath() :
    global path
    if path != 'src/img' :
        with open('path.txt', 'r') as f:
            pathlist = f.readlines()
        if path not in pathlist :
            pathname = path.split("/")[-1]
            pathlist.append(pathname + ' (' + path+')\n')
            print(pathlist)
            with open('path.txt', 'w') as f:
                f.writelines(pathlist)
        listrefresh()

def pathlistbutton() :
    global pathwindow, listbox
    if not pathwindow :
        pathwindow = tk.Toplevel(root)
        pathwindow.title("Path List")
        x = root.winfo_x()
        y = root.winfo_y()
        pathwindow.geometry("300x500")
        pathwindow.geometry("+%d+%d" % (x + 500, y))
        listrefresh()
        selectbutton = Button(pathwindow, text="Select", padx=1, pady=1, command=lambda: selectpath(listbox.get(listbox.curselection())))
        selectbutton.place(x=0, y=400, width=300, height=50)
        addbutton = Button(pathwindow, text="Add", padx=1, pady=1, command=lambda: addpath())
        addbutton.place(x=0, y=450, width=150, height=50)
        deletebutton = Button(pathwindow, text="Delete", padx=1, pady=1, command=lambda: deletepath(listbox.get(listbox.curselection())))
        deletebutton.place(x=150, y=450, width=150, height=25)
        deletallbutton = Button(pathwindow, text="Delete All", padx=1, pady=1, command=deleteallpath)
        deletallbutton.place(x=150, y=475, width=150, height=25)

tk.Button(root, text="Favorites", padx=1, pady=1, command= favoritebutton).place(x=0, y=40, width=250, height=30)
tk.Button(root, text="Path Lists", padx=1, pady=1, command=pathlistbutton).place(x=250, y=40, width=250, height=30)

makebuttons()
root.mainloop()