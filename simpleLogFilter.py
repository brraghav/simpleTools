
import subprocess
import os
import platform
import PySimpleGUI as sg
from pathlib import Path

sg.theme("DarkTeal7")


keywords = ''
filename = ''
output_file = 'Filtered_Output.txt'

SUCCESS = 0
FAILURE = -1

font = ("Roboto", 10)
small_font = ("Roboto", 8)
        
form = sg.FlexForm('Generic Log Filter')

layout = [[sg.Text('Select a log file for filtering')],
          [sg.Text('Input Log file', size=(15, 1)),
           sg.Input(key="-IN2-" ,change_submits=True, font=small_font),
           sg.FileBrowse(file_types=(("TXT Files", "*.txt"), ("ALL Files", "*.*")), font=small_font)],
          [sg.Text('Output Location', size=(15, 1)),
           sg.Input(key="-FOLDER-" ,change_submits=True, font=small_font),
           sg.FolderBrowse(font=small_font)],
          
          [sg.Text('Output Filename', size=(15, 1)), sg.InputText('Filtered_Output.txt', key="-IN4-", do_not_clear=True, font=small_font)],
          [sg.Text('Keywords to Filter ', size=(15, 1)), sg.Input(key="-IN3-", do_not_clear=False, font=small_font), sg.Button("Add Keywords", font=small_font)],
          [sg.Text('Current Keywords List:', size=(20, 1), font=small_font)],
          [sg.Text('', size=(40, 3), key="-OUT1-", font=small_font)],
          [sg.Text('Keywords Suggestion:', size=(20, 1), font=small_font), sg.Button("Suggest", font=small_font)],
          [sg.Text('Separator', size=(20, 1), font=small_font), sg.Input(' ', s=5, key="-SEPARATOR-", do_not_clear=True, font=small_font), \
           sg.Text('Defaut separator " " (space)', size=(25, 1), font=small_font)],
          [sg.Listbox(values=[''], size=(40, 8), key="-OUT2-", font=small_font, select_mode='extended'), sg.Button("Select Keywords", font=small_font)],
          [sg.Button("Submit", font=font), sg.Button("Open Output File Location", font=font), sg.Button("Reset", font=font), sg.Button("Close", font=font)]
          ]

window=sg.Window('Generic Log Filter', layout, font=font)

def suggest_keywords(filename=filename, separator=' '):
    '''
    Parse the text or logfile and extract the keywords or tags as per
    decreasing order of frequency.
    Inputs: filename to parse, separator (default is empty space ' ')
    Output : List of predicted keywords or tags    
    '''
    predicted_keywords = []
    keywords_dict = {}          #Dictionary to maintain tags and its frequency
                
    if Path(filename).is_file():
        
        try:
            with open(filename, "rt", encoding='utf-8') as f:
                lines = f.readlines()
                for line in lines:
                    tmp_list = line.split(separator)
                    #Don't bother about lines which have less than 4 words
                    if len(tmp_list) < 4:
                        continue
                    
                    for i in range(len(tmp_list)):
                        tag = tmp_list[i]
                        tag_len = len(tag)
                        
                        if tag_len < 6 or tag_len > 28:
                            #Ignore the keywords whose length is less than 6
                            #or greater than 28
                            continue
                        
                        #Ignore keywords that have symbols or only numbers
                        #Avoid timestamps, key value pairs, rates (eg: kb/sec)
                        
                        if tag.count(':') > 1 or tag.find('.') != -1 or \
                           tag.find('=') != -1 or tag.find('\\') != -1 or \
                           tag.find('/') != -1 or tag[0] == "'" or \
                           tag[-1] == ']' or tag[0].isnumeric() or \
                           tag[-1].isnumeric() or tag.find(']') != -1 or \
                           tag.find(')') != -1 or tag.find('{') != -1:
                            continue

                        if tag not in keywords_dict:
                            keywords_dict[tag] = 0
                        keywords_dict[tag] += 1

            tmp_dict = dict(sorted(keywords_dict.items(), key=lambda x:x[1], reverse=True))
            tmp_count = 0
            for item in tmp_dict:
                predicted_keywords.append(item)
                tmp_count += 1
                if tmp_count > 100:  # Top 100 keywords by frequency
                    break
            #Create a list of unique keywords ordered alphabetically
            if predicted_keywords:
                predicted_keywords = list(sorted(set(predicted_keywords)))
            
                
        except Exception as e:
            print("Error: ", e)
            
    return predicted_keywords
    

def filter_lines(filename='', output_folder='.', output_file='', keywords=keywords):
    '''
    This function filter the text file or log according to the keyword chosen
    by the user. The user can either enter the keywords manually or select from
    the list of suggested keywords.
    Inputs:
    filename : name of the log or text file,
    output_file : desired name of the output file
    keywords : keywords that will be used for filtering
    Output: Returns a file with only filtered lines as per keywords
    '''
    status = SUCCESS
    if len(filename) < 1:
        sg.popup("Empty file received.. Returning..", text_color = 'red')
        return
    
    if Path(filename).is_file():
        try:
            with open(filename, "rt", encoding='utf-8') as f:
                #Go through each word of each line, match against
                #keywords chosen and write it to a file
                if not os.path.isdir(folder):
                    sg.popup_error("Output Folder does not exist")
                    status = FAILURE
                else:
                    out = '{}/{}'.format(output_folder, output_file)
                    with open(out, "w", encoding='utf-8') as o:
                        lines = f.readlines()
                        for line in lines:
                            for m in keywords:
                                for l in line.split(" "):
                                    if l.find(m) != -1:
                                        o.write(line)
        except Exception as e:
            print("Error: ", e)
            sg.popup_error("Error: {}".format(e))
            status = FAILURE
    else:
        sg.popup_error("Input file not found")
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

    elif event == "Submit":
    
        if len(keywords) < 1:
            sg.popup("No keywords/tags selected", text_color='red')
            
        else:
            input_filename = values["-IN2-"]
            output_filename = values["-IN4-"] if values["-IN4-"] else 'Filtered_Output.txt'

            #Output file folder location
            folder = values["-FOLDER-"]  if values["-FOLDER-"] else '.'
            if folder == '.':
                window["-FOLDER-"].update('.')
            status = filter_lines(input_filename, folder, output_filename, keywords)
            if status == SUCCESS:
                sg.popup("Done. Open Result File")
            
    elif event == "Add Keywords":
        if len(values["-IN3-"]) < 1:
            sg.popup_error("No keywords added")
        else:
            if keywords:
                keywords.extend(values["-IN3-"].split(' '))
            else:
                keywords = values["-IN3-"].split(' ')
                
        #Unique sorted keywords entered by user
        keywords = list(sorted(set(keywords)))
        window["-OUT1-"].update(', '.join(keywords))
        
    elif event == "Suggest":
        #Suggest user with keywords in a file, based on separator
        input_filename = values["-IN2-"]
        separator = values["-SEPARATOR-"]
        suggestion = suggest_keywords(input_filename, separator)
        window['-OUT2-'].update(suggestion)
 
    elif event == "Select Keywords":
        #User selected keywords added to the keyword list for filtering
        if values['-OUT2-']:
            if keywords:
                keywords.extend(values["-OUT2-"])
            else:
                keywords = values["-OUT2-"]
            keywords = list(sorted(set(keywords)))
            window["-OUT1-"].update(', '.join(keywords))
        
    elif event == "Reset":
        keywords = []
        predicted_keywords = []
        output_file = "Output.txt"
        window["-OUT1-"].update(', '.join(keywords))
        window["-OUT2-"].update(', '.join(predicted_keywords))
        window["-IN2-"].update('')
        window["-IN4-"].update('')
        window["-FOLDER-"].update('')
        
    elif event == "Open Output File Location":
        if len(values["-FOLDER-"]) < 1:
            open_folder()
        else:
            folder = values["-FOLDER-"]
            status = open_folder(folder)
            if status == FAILURE:
                window["-FOLDER-"].update('')

window.Close() 

quit()
