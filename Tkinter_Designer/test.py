from tkinter import *
win = Tk()
a=Scrollbar(win)
a.pack(side=RIGHT, fill=Y)
Label(a,text=123).pack()
win.mainloop()