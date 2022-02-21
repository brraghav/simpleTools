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

sg.theme("DarkTeal12")

SUCCESS = 0
FAILURE = -1

font = ("Franklin Gothic Book", 10)
small_font = ("Franklin Gothic Book", 8)

formats_list = ['png', 'pdf', 'jpg', 'canon', 'cmap', 'cmapx', 'cmapx_np', 'dia', 'dot', 'eps', \
                 'fig', 'gd', 'gd2', 'gif', 'hpgl', 'imap', 'imap_np', 'ismap',\
                 'jpe', 'jpeg', 'mif', 'mp', 'pcl', 'pic', \
                 'plain', 'plain-ext', 'ps', 'ps2', 'svg', 'svgz', \
                 'tk', 'vml', 'vmlz', 'vrml', 'vtx', 'wbmp', 'xdot', 'xlib']

form = sg.FlexForm('Generic Log Filter')

layout = [[sg.Text('Generate UML diagrams from Python Code')],
          [sg.Text('Select Python Module', size=(30, 1)),
           sg.Input(key="-MODULENAME-" ,change_submits=True, font=small_font),
           sg.FolderBrowse(font=small_font)],
          [sg.Text('Output Location', size=(30, 1)),
           sg.Input(key="-OUT1-" ,change_submits=True, font=small_font),
           sg.FolderBrowse(font=small_font)],
          [sg.Text('Output Format', size=(30, 1)), \
           sg.Combo(formats_list, default_value='png', enable_events=True, key="-FORMAT-")],
          [sg.Text('Colorized Output', size=(30, 1)), sg.Radio('Yes', "RADIO1", default=False, key="-RB1-"), sg.Radio('No', "RADIO2", default=True, key="-RB2-")],
          [sg.Button("Generate", font=font), sg.Button("View Output", font=font), \
           sg.Push(), sg.Button("Reset", font=font), sg.Button("Close", font=font)]
          ]

window=sg.Window('Generate UML from Python Code', layout, font=font)


def generate_UML_diagrams(input_location=None,  output_location=None, module_name='Test', preferred_format='png', colorized=False):
    '''
    This function is intended to generate UML Diagram as per the user request.
    The idea is to get input and output folders, run pyreverse and dot command.
    pyreverse creates dot file, which can be tranlated to the format the user
    requested.
    This is achived by putting all these command into a tmp bat or shell script
    Run the batch file or shell script & delete the batch or shell script file
    Delete the tmp batch/shell script
    Eg:
    Go to the folder which contains the module you want to generate UML for.
    In windows,
    if we need to generate UML Diagram for C:\simpleTools\simplePyreverseUI,
    we have to go till the folder which contains simplePyreverseUI, ie
    <prompt>cd C:\simpleTools
    <prompt>pyreverse simplePyreverseUI
    <prompt>dot -Tpdf classes_simplePyreverseUI.dot -o simplePyreverseUI.pdf
    The above commands will generate the UML diagrams in pdf format.
    '''
    status = SUCCESS
    try:
        with open('tmp.bat', "w") as t:
            cmd_str = '@echo off \n'
            cmd_str += 'cd {}\n'.format(input_location)
            if colorized:
                cmd_str += 'pyreverse {} -d {} --colorized\n'.format(module_name, output_location)
            else:
                cmd_str += 'pyreverse {} -d {}\n'.format(module_name, output_location)
            cmd_str += 'cd {}\n'.format(output_location)
            cmd_str += 'dot -T{} classes.dot -o {}_classes.{}\n'.format(preferred_format, module_name, preferred_format)
            cmd_str += 'dot -T{} packages.dot -o {}_packages.{}\n'.format(preferred_format, module_name, preferred_format)
            cmd_str += 'del classes.dot\n'
            cmd_str += 'del packages.dot\n'
            t.write(cmd_str)
        
        subprocess.call('tmp.bat')
        os.remove('tmp.bat')
    except Exception:
        status = FAILURE
        
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
        
        output_location = values["-OUT1-"]
        input_location = '/'.join(values["-MODULENAME-"].split('/')[:-1])
        module_name = values["-MODULENAME-"].split('/')[-1].strip()
        output_format = values["-FORMAT-"]
        colorized = True if values["-RB1-"] == True else False
        if len(module_name) < 1:
            sg.popup_error("Module not selected", line_width=80)
            continue
        if len(output_location) < 1:
            sg.popup_error("Output Location not specified", line_width=80)
            continue
        
        status = \
               generate_UML_diagrams(input_location, output_location, \
                                     module_name, output_format, colorized)
        if status == SUCCESS:
            sg.popup_ok("Done", line_width=80)
        else:
            sg.popup_error("Something went wrong", line_width=80)
            
        
    elif event == "Reset":
        window["-OUT1-"].update('')
        window["-MODULENAME-"].update('')
        window["-FORMAT-"].update('png')
        
    elif event == "View Output":
        folder = values["-OUT1-"]
        status = open_folder(folder)
        if status == FAILURE:
            window["-OUT1-"].update('')

window.Close() 


