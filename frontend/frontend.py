import PySimpleGUI as sg

sg.theme('DarkAmber')  # Add a touch of color

# All the stuff inside your window.
layout = [[sg.Text('Assessment Toolkit')],
          [sg.Text('Enter the scenario to simulate'), sg.InputText()],
          [sg.Button('Ok'), sg.Button('Cancel')]]

# Create the Window
window = sg.Window('Assessment Toolkit', layout)
# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Cancel':  # if user closes window or clicks cancel
        break
    print('You entered ', values[0])

window.close()
