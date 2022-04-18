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


import PySimpleGUI as sg
import os
import os.path
import subprocess
import platform
from pathlib import Path
import sys
import paramiko


sg.theme('TanBlue')
font = ("Calibri", 10)
small_font = ("Calibri", 9)

form = sg.FlexForm('Simple Paramiko UI')

SUCCESS = 0
FAILURE = -1
status = FAILURE


layout = [[sg.Push(), sg.Text('Simple Paramiko UI'), sg.Push()],
          [sg.Text('Linux Box IP', size=(20, 1), font=small_font),\
           sg.InputText(key="-LINUXIP-" ,change_submits=True, font=small_font),\
           sg.Text('Command(s) with args', size=(20, 1), font=small_font),\
           sg.Input(key="-ARGS-", do_not_clear=False, font=small_font),\
           sg.Button("Run Command", font=small_font)],
          [sg.Text('Username', size=(20, 1), font=small_font),\
          sg.InputText(key="-USERNAME-", font=small_font),\
          sg.Text('Password', size=(20, 1), font=small_font),\
           sg.InputText('', key='-PASSWORD-', password_char='*', font=small_font)],
          [sg.Text(' ', size=(20, 1), font=small_font)],
          
          [sg.Text('Script output....', size=(15, 1), font='Courier 8'), sg.Push()],
          [sg.Output(size=(130, 22), font='Courier 8', key="-SCRIPTOUTPUT-")],
          
          
          [sg.Push(), sg.Button("Reset", font=small_font), sg.Button("Close", font=small_font)],
          [sg.Push(), sg.Text("simpleTools/simpleParamiko", font='Arial 7'), sg.Push()],
          ]


def run_command_on_linux(username=None, password=None, ip=None, command=[]):
    cmd_list = command
    host = ip
    status = SUCCESS
    
    client = paramiko.client.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(host, username=username, password=password)
        for cmd in cmd_list:
            _stdin, _stdout,_stderr = client.exec_command(cmd)
            output = _stdout.read().decode()
            
            print(cmd)
            print(output)
    except Exception:
        print("Could not execute remote command..")
        status = FAILURE
            
    finally:
        client.close()
    return status

window = sg.Window('Simple Paramiko', layout)

while True:
    event, values = window.read()
    if event == 'Close'  or event == sg.WIN_CLOSED:
        break # exit button clicked
    
    elif event == 'Run Command':
        ip_address = values["-LINUXIP-"]
        cmd_str = values["-ARGS-"]
        username = values["-USERNAME-"]
        password = values["-PASSWORD-"]
        status = run_command_on_linux(username, password, ip_address, cmd_str.split(","))
        if status == FAILURE:
            sg.popup_error("Command did not execute..")
        
            
    elif event == "Reset":
        window["-LINUXIP-"].update('')
        window["-ARGS-"].update('')
        window["-SCRIPTOUTPUT-"].update('')
        
      
window.Close() 




            
            

