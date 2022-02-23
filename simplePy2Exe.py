# MIT License

# Copyright (c) 2022 Raghavendra Basvan

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# Author : Raghavendra Basvan <raghavendra.basvan@gmail.com>

import subprocess
import os
import platform
import PySimpleGUI as sg
from pathlib import Path

sg.theme("SystemDefault1")

SUCCESS = 0
FAILURE = -1
os_list = ['Windows', 'Linux']
font = ("Franklin Gothic Book", 10)
small_font = ("Franklin Gothic Book", 8)

form = sg.FlexForm('Exe Generator')

layout = [[sg.Text('Generate exe from Python Code')],
          [sg.Text('Select Python File', size=(20, 1)),
           sg.Input(key="-FILENAME-" ,change_submits=True, font=small_font),
           sg.FileBrowse(font=small_font)],
          [sg.Text('')],
          [sg.Push(), sg.Button("Generate", font=font, size=(8, 1)), sg.Push()],
          [sg.Push(), sg.Button("View", font=font, size=(8, 1)), sg.Push()],
          [sg.Push(), sg.Button("Reset", font=font, size=(8, 1)), sg.Push()],
          [sg.Push(), sg.Button("Close", font=font, size=(8, 1)), sg.Push()],
          ]

window=sg.Window('EXE from Python Code', layout, font=font)


def generate_executable(input_file=None):
    '''
    This function is intended to generate Executable as per the user request.
    The idea is to get input python file, desired output location and executable
    depending on the os type.
    run pyinstaller as follows:
    pyinstaller --onefile -w <python_file.py>
    '''
    status = SUCCESS
    input_location = '/'.join(input_file.split('/')[:-1])
                              
    file = input_file.split('/')[-1]
    if not file.endswith('.py'):
        status = FAILURE
        return status
    try:
        windows = False
        linux = False
        os = platform.system()
        
        if os == "Windows":
            with open('tmp.bat', 'w') as t:
                cmd_str = '@echo off \n'
                cmd_str += 'cd {}\n'.format(input_location)
                cmd_str += 'pyinstaller --onefile -w {}\n'.format(file)
                t.write(cmd_str)
            subprocess.call("tmp.bat")
            
        if os == "Linux":   
            with open("tmp.sh", "w") as t:
                cmd_str = 'exec 1>/dev/null \n'
                cmd_str += 'cd {}\n'.format(input_location)
                cmd_str += 'pyinstaller --onefile -w {}\n'.format(file)
                t.write(cmd_str)
            subprocess.call(['sh', './' + tmp_file])
            
            

    except Exception as e:
        status = FAILURE
        print(e)
        
    return status

    
def open_folder(folder='.'):
    '''
    Opens the folder of the output chosen by the user
    Compatible with Windows and Linux
    '''
    status = SUCCESS
    if len(folder) == 0:
        folder = '.'
        
    if os.path.isdir(folder):
        if platform.system() == "Windows":
            os.startfile(folder)
        else:
            subprocess.Popen(["xdg-open", path])
    else:
        sg.popup_error("Destination Folder does not exist")
        status = FAILURE
    return status


while True:
    event, values = window.read()
        
    if event == sg.WIN_CLOSED or event=="Close":
        break

    elif event == "Generate":
        input_file = values["-FILENAME-"]
        status = generate_executable(input_file)

        if status == SUCCESS:
            sg.popup_ok("Done", line_width=80)
        else:
            sg.popup_error("Something went wrong", line_width=80)
            
        
    elif event == "Reset":
        window["-FILENAME-"].update('')
        
    elif event == "View":
        output_location = '/'.join(values["-FILENAME-"].split('/')[:-1])
        output_location += '/dist'
        status = open_folder(output_location)
        if status == FAILURE:
            sg.popup_error("Output Location Corrupted", line_width=80)
            

window.Close() 


