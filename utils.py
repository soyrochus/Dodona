# Dodona - Simple GUI for the OpenAI API, made with OpenAI - Copyright © 2023 Iwan van der Kleijn - See LICENSE.txt for conditions

import os

def realize_current_subdir(subdir_name):
    
    dir = os.path.join(os.curdir, subdir_name)

    # create the directory if it doesn't yet exist
    if not os.path.isdir(dir):
        os.mkdir(dir)
        
    return dir