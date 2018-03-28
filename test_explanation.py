# test_explanation.py
import tkinter
window =tkinter.Tk()


list_voice = [1,2,3] # correct
list_compare=[1,4,3] # incorrect

for i in list_voice:
    label_voice = tkinter.Label(window, text=i)
    label_voice.grid(row=0, column= i )

for ii in list_compare:
    # list for compare
    if ii not in list_voice:
        color ='red'
    else:
        color='grey'
    
    label_entry = tkinter.Label(window, text=ii ,background=color)
    label_entry.grid(row=1, column= ii )

window.mainloop()