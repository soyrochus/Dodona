# Dodona - Simple GUI for the OpenAI API, made with OpenAI - Copyright © 2023 Iwan van der Kleijn - See LICENSE.txt for conditions

import datetime
import os

def realize_current_subdir(subdir_name):
    
    dir = os.path.join(os.curdir, subdir_name)

    # create the directory if it doesn't yet exist
    if not os.path.isdir(dir):
        os.mkdir(dir)
        
    return dir

def store_data_dump(data_dir, file_name, file_ext, binary, data):

    now = datetime.datetime.now()
    # Format the date and time as a string
    timestamp = now.strftime("%Y%m%d_%H%M%S")
    # Append the timestamp to the filename
    filename = f"{file_name}_{timestamp}.{file_ext}"
    #write data to file
    filepath = os.path.join(data_dir, filename)
  
    with open(filepath, f"w{'b' if binary else ''}") as data_file: 
        data_file.write(data)
    
    return filepath