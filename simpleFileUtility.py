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


import os.path
import subprocess
import os
import platform
import PySimpleGUI as sg
from pathlib import Path
import pandas as pd

sg.theme("DarkTeal12")


keywords = ''
filename = ''
output_file = 'Filtered_Output.txt'

SUCCESS = 0
FAILURE = -1
status = FAILURE

font = ("Roboto", 10)
small_font = ("Roboto", 8)
        
form = sg.FlexForm('Simple File Utility')

layout = [[sg.Push(), sg.Text('Perform Simple File Operations'), sg.Push()],
          [sg.Text('File Splitter')],
          [sg.Text('Input file', size=(15, 1)),
           sg.Input(key="-IN2-" ,change_submits=True, font=small_font),
           sg.FileBrowse(file_types=(("CSV Files", "*.csv"), ("ALL Files", "*.*")), font=small_font)],
          [sg.Text('Split Size', size=(15, 1)), sg.Input(key="-SPLITSIZE-" ,change_submits=True, font=small_font)],
          [sg.Text('Output Location', size=(15, 1)),
           sg.Input(key="-OUTPUTFOLDER-" ,change_submits=True, font=small_font),
           sg.FolderBrowse(font=small_font)],
          [sg.Text('')],
          [sg.Text('Stitch the files')],
          [sg.Text('Input Location', size=(15, 1)),
           sg.Input(key="-INPUTFOLDER-" ,change_submits=True, font=small_font),
           sg.FolderBrowse(font=small_font)],
          [sg.Text('File Extension', size=(15, 1)), sg.InputText('csv', key="-EXTENSION-", do_not_clear=True, font=small_font)],
          [sg.Text('')],
          
          [sg.Button("Submit", font=font), sg.Button("Open Output File Location", font=font), sg.Button("Reset", font=font), sg.Button("Close", font=font)]
          ]

window=sg.Window('Simple File Utility', layout, font=font)


#####################################################################################
# Get All Files of a given extension
#####################################################################################

def get_all_files_of_type(folder='.', file_type='.csv'):
    files = []
    path = folder
    # r=root, d=directories, f = files
    for r, d, f in os.walk(path):
        for file in f:
            if file_type in file:
                files.append(os.path.join(r, file))
                
    return files



#####################################################################################
# Stitch All Files.
# By default stitches CSV files
#####################################################################################
def stitch_all_files(source_folder='.', extension='csv', file_name='COMBINED.csv'):
    status = SUCCESS
    files = get_all_files_of_type(folder=source_folder, file_type=extension)
    if extension == 'csv' or extension == 'CSV':
        combined_csv = pd.concat([pd.read_csv(f) for f in files], sort=False)
        combined_file = source_folder + '/' + file_name
        combined_csv.to_csv( combined_file, index=False, encoding='utf-8-sig')
    else:
        print("Not supported yet")
        status = FAILURE
    return status

def split_file(filename=None, output_folder=None, header_present=True, chunk_size=100000):
    status = SUCCESS
    header = ''
    if header_present:
        with open(filename, "r", encoding='windows-1252') as file:
            header = file.readline()

    split_filename = filename.split('/')[-1].split('.')[0].strip()
    file_extension = filename.split('/')[-1].split('.')[1].strip()
    chunk_number = 1
    
    with open(filename, "r", encoding='windows-1252') as file:
        next_line = "line"
        while next_line:
            outfile_name = output_folder + '/' + split_filename + '-' + str(chunk_number) + '.' + file_extension
            chunk_number += 1

            with open(outfile_name, "w") as outfile:
                if header_present:
                    outfile.writelines(header)
                for _ in range(chunk_size):
                    next_line = file.readline()
                    outfile.writelines(next_line)
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

    elif event == "Submit":
        if values["-INPUTFOLDER-"] is None and values["-IN2-"] is None:
            sg.popup_error("No input file or folder selected..")
            
        input_filename = values["-IN2-"]
        if input_filename:
            split_size = values["-SPLITSIZE-"]
            #Output file folder location
            folder = values["-OUTPUTFOLDER-"]  if values["-OUTPUTFOLDER-"] else '.'
            if folder == '.':
                window["-OUTPUTFOLDER-"].update('.')
            file_extension = input_filename.split('/')[-1].split('.')[1].strip()
            if file_extension == 'csv' or file_extension == 'CSV':
                header_present = True
            else:
                header_present = False
            status = split_file(input_filename, output_folder=folder, header_present=header_present, chunk_size=int(split_size))

        
        input_folder = values["-INPUTFOLDER-"]
        if input_folder:
            extension = values["-EXTENSION-"] if values["-EXTENSION-"] else 'csv'
            status = stitch_all_files(input_folder, extension)
        
        if status == SUCCESS:
            sg.popup("Done. Open Result File")
        else:
            sg.popup_error("Something went wrong..")
            
    elif event == "Reset":
        window["-SPLITSIZE-"].update('')
        window["-IN2-"].update('')
        window["-OUTPUTFOLDER-"].update('')
        
    elif event == "Open Output File Location":
        if len(values["-OUTPUTFOLDER-"]) < 1:
            open_folder()
        else:
            folder = values["-OUTPUTFOLDER-"]
            status = open_folder(folder)
            if status == FAILURE:
                window["-OUTPUTFOLDER-"].update('')

window.Close()

