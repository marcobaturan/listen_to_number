
# !/usr/bin/python3
from tkinter import *

def sel():
   selection = "You selected the option " + str(var.get())
   label.config(text = selection)

root = Tk()
var = IntVar()
R1 = Radiobutton(root, text = "Option 1", variable = var, value = 1,
                  command = sel).grid(row=0, column=0)


R2 = Radiobutton(root, text = "Option 2", variable = var, value = 2,
                  command = sel).grid(row=1, column=0)


R3 = Radiobutton(root, text = "Option 3", variable = var, value = 3,
                  command = sel).grid(row=3, column=0)


label = Label(root, text='espero')
label.grid(row=4, column=0)
root.mainloop()