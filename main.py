# import
import PySimpleGUI as sg
import pyttsx3
import random


# variables
engine = pyttsx3.init()


# functions
def generate_random_number(length):
    minimum = 10 ** (int(length) - 1)
    maximum = (10 ** int(length)) - 1
    return random.randint(minimum, maximum)


# main window
sg.theme('DarkAmber')
# Create a list of numbers from 1 to 50
numbers = [str(i) for i in range(1, 51)]
layout = [[sg.Titlebar('Listen the numbers')],
          [sg.Text('Select the length of the number')],
          [sg.DropDown(numbers, default_value='1')],
          [sg.Text('Select the rate of reading')],
          [sg.DropDown([100, 50, 25], default_value='1')],
          [sg.Button('Read')],
          [sg.Text('Write the number after listening')],
          [sg.Input(tooltip='Only numbers')],
          [sg.Button('Compare'), sg.Exit()],
          ]

window = sg.Window('Window that stays open', layout)

# The Event Loop
while True:
    event, values = window.read()
    # drive by events
    if event == sg.WIN_CLOSED or event == 'Exit':
        engine.stop()
        break

    if numbers is not None and event == 'Compare':
        if sg.Window("Comparator", [[sg.Text(str(numbers))],
                                    [sg.Text(str(values[2]))],
                                    [sg.Yes(), sg.No()]]).read(close=True)[0] == "Yes":
            engine.stop()

    if numbers is not None and event == 'Read':
        numbers = generate_random_number(length=values[0])
        rate = engine.getProperty('rate')
        engine.setProperty('rate', rate - values[1])
        for number in str(numbers):
            engine.say(str(number))
        engine.runAndWait()

window.close()
