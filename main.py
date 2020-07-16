from ttkthemes import ThemedTk
from tkinter import *
import os , subprocess, imagesaver, time, threading
from tkinter import filedialog, messagebox
from PIL import ImageTk, Image

def expandBox():
    global expand
    root.withdraw()
    if not(expand):
        root.geometry('450x400+%d+%d' % (root.winfo_screenwidth()//2-225, root.winfo_screenheight()//2-200))
        expand = True
    else:
        root.geometry('450x100+%d+%d' % (root.winfo_screenwidth()//2-225, root.winfo_screenheight()//2-50))
        expand = False
    root.deiconify()

def getFrontBack():
    if topBTN.get() == 1:
        root.attributes('-topmost', 1)
    else:
        root.attributes('-topmost', 0)

def runFile(filepath):
    root.protocol('WM_DELETE_WINDOW', lambda: rootdestroy(False))
    try:
        outputbox.delete('1.0', 'end')
        outputbox.insert('end', '\n • on : '+time.ctime())
        outputbox.insert('end', '\n • file : '+str(os.path.split(filepath)[1]))
        outputbox.insert('end', '\n • outputs ↓\n')
        outputbox.insert('end', '_'*47+'\n')
        root.update()

        process = subprocess.Popen(str(os.path.split(filepath)[1]), cwd=os.path.split(filepath)[0], stdin=subprocess.DEVNULL, stderr=subprocess.STDOUT, shell=True, stdout=subprocess.PIPE)
        for line in process.stdout:
            outputbox.insert('end', line)
            root.update()

        outputbox.insert('end', '\n'+'_'*47+'\n')
        root.update()

    except OSError as error:
        messagebox.showerror('Run on Py', error)
    except:
        messagebox.showerror('Run on Py', "Something went wrong with run on file.")
    root.protocol('WM_DELETE_WINDOW', lambda: rootdestroy(True))

def RunonPy():
    if len(pathENT.get()) > 0:
        thread = threading.Thread(target=lambda: runFile(pathENT.get()))
        thread.run()
    else:
        messagebox.showinfo('Run on Py', 'No any Python file selected.')

def openPYfile():
    pathENT.set('')
    path = filedialog.askopenfile(title='Select a python file', filetypes=[('Python files', '*.py *.pyw *.pyx *.py3')])
    if path != None:
        pathENT.set(path.name)

def rootdestroy(destroy):
    if destroy:
        root.destroy()
    else:
        pass

#GLOBAL variables
expand = False

root = ThemedTk(theme='breeze')
root.geometry('450x100+%d+%d' % (root.winfo_screenwidth()//2-225, root.winfo_screenheight()//2-50))
imagesaver.iconbit()
root.iconbitmap('icon.ico')
os.remove('icon.ico')
root.title('Run on Py')
root.configure(background='white')
root.resizable(False, False)
root.minsize(450, 80)
root.maxsize(450, 400)

imagesaver.saveOpenFileImage()
image = PhotoImage(file='icon_open_file.png')
Button(root, image=image, background='white', border=0, relief=FLAT, command=openPYfile).place(x=280, y=21)
os.remove('icon_open_file.png')

pathENT = StringVar()
ttk.Entry(root, textvariable=pathENT, width=35).pack(padx=15, pady=20, anchor=W)
ttk.Button(root, text='Run', command=RunonPy).place(x=340, y=20)

style_configure = ttk.Style()
style_configure.configure('checkbox.TCheckbutton', background='white', font=('ubuntu', 10))
ttk.Checkbutton(root, text="Outputs", style='checkbox.TCheckbutton', takefocus=False, command=expandBox).place(x=80, y=65)

topBTN = IntVar()
ttk.Checkbutton(root, text='Always on top', style='checkbox.TCheckbutton', takefocus=False, variable=topBTN, onvalue=1, offvalue=0, command=getFrontBack).place(x=230, y=65)

outputbox = Text(root, background='black', padx=2, height=15, width=47, foreground='white', font='consolas')
outputbox.place(x=10, y=100)

root.mainloop()
