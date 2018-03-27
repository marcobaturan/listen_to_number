from tkinter import *
import tkinter as tk
# import
import pyttsx3
import random
# Info
__dedicated_to__="Elenuchy"
__author__ ="Marco Baturan Garcia"
__date__ ="2018/03/23"
__license__="GNU, Open Source"
__collaborator__="Reset Reboot"
__description__=""" Listen to number.
                It's an Open SOurce software for training
                auditive memory by listening
                of random integers series."""


class Program:
    # Main class
    def __init__(self):
        # Elements  of main window
        self.master = Tk()
        self.master.title("Listen to number. 2.0") # Title main window.
        # variables of all program
        self.how_many_numbers = 0
        self.entry_number_to_compare = []
        self.lista = []
        self.v = IntVar()
        self.v.set(1)
        self.basic = 0
        self.e1 = 0
        self.e2 = 0
        self.lista_I = 0
        self.list_compare = 0

    def random_numbers_list(self):
         """ Generate a list of random integer numbers."""
         self.how_many_numbers = int(self.e1.get())
         if self.how_many_numbers == 0:
            engine = pyttsx3.init()
            engine.say("The field is empty. Please, enter a digit.")
            engine.runAndWait()
         else:
             for i in range(self.how_many_numbers):
                 self.lista.append(random.randint(1, 99))
         self.lista_I = self.lista

    def voice(self):
        # generate digital voy from list of numbers =
        if self.v.get() == 1:
            speed = -100
        else:
            speed = 200

        self.random_numbers_list()

        voice_list = self.lista_I
        engine = pyttsx3.init()
        engine.setProperty('rate', speed)
        engine.say(voice_list)
        engine.runAndWait()

    def compare_voice_list_write_list(self):
        # Compare voice list vs a write list by user
        # And raise a matrix composed by two list
        # And put in red the diference.
        self.window = Toplevel(self.master) # Title second window
        self.window.title('Compare the list:')
        self.lista.reverse()
        list_voice = self.lista
        self.entry_number_to_compare.reverse()
        list_compare = self.entry_number_to_compare
        Label(self.window, text="List from voice: ").grid(row=0, column=0)
        for i in list_voice:
            label_voice = Label(self.window, text=i)
            label_voice.grid(row=0, column= i + 1)
            
        Label(self.window, text="List from entry: ").grid(row=1, column=0)
        for ii in list_compare:
            # list comprehension for compare
            comparation = [item for item in list_voice if item in list_compare]
            if len(comparation) > 0:
                for item in comparation: color ="white"
            else:
                color="red"
                # to resolve, fuck
            label_entry = Label(self.window, text=ii ,background=color)
            label_entry.grid(row=1, column= ii + 1)
        Button(self.window, text='Close', command=self.close).grid(row=2, column=0)
        
    def close(self):
        # It's close and destroy the window: COmpare the list
        self.window.destroy()
        self.lista.clear()
        self.entry_number_to_compare.clear()
        
    def introduce(self):
        # read de entry of number of numbers
        # append to list
        # and delete de entry, wait for the next input
        for value in self.e2.get().split():
            self.entry_number_to_compare.append(int(value))
        self.e2.delete(0,'end')
        
    def run(self):
        # Labels
        Label(self.master, text="Enter number of numbers:").grid(row=0) # label one
        Label(self.master, text="Speed of voice: ").grid(row=1) #label speed
        Label(self.master, text="Introduce the result: ").grid(row=3) #label speed
        # input elements
        self.e1 = Entry(self.master) # entry number of integers
        self.e1.insert(0,self.basic) # Insert value in entry
        self.e2 = Entry(self.master) # Insert values for comparation
        self.e2.insert(0, self.basic)
        r1 = Radiobutton(self.master, text="Slow", variable=self.v, value=1) # option of 1,2,3 seconds
        r2 = Radiobutton(self.master, text="Fast", variable=self.v, value=2)
        # grid section for input
        self.e1.grid(row=0, column=1)
        self.e2.grid(row=3, column=1)
        r1.grid(row=1, column=1)
        r2.grid(row=2, column=1)
        # grid section of buttons
        Button(self.master, text='Introduce', command=self.introduce).grid(row=3, column=2, sticky=E, pady=4)
        Button(self.master, text='Quit', command=self.master.quit).grid(row=4, column=0, sticky=W, pady=4)
        Button(self.master, text='Say numbers', command=self.voice).grid(row=4, column=1, sticky=W, pady=4)
        Button(self.master, text='Compare lists', command=self.compare_voice_list_write_list).grid(row=4, column=2, sticky=W, pady=4)
        self.master.mainloop()

if __name__=='__main__': # call the main program
    program = Program()
    program.run() # remember, any terminal function has () for run
