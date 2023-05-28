# Dodona - Simple GUI for the OpenAI API, made with OpenAI - Copyright © 2023 Iwan van der Kleijn - See LICENSE.txt for conditions

import openai
import requests
import os
import datetime
from utils import realize_current_subdir

openai.api_key = os.environ.get("OPENAI_API_KEY")

# set a directory to save DALL·E images to
image_dir = realize_current_subdir("images")

# set a directory to save whisper transcriptions to
transcript_dir = realize_current_subdir("transcriptions")

def get_whisper_translation(sound_path):
    #call openapi whisper api 
    
    audio_file= open(sound_path, "rb")
    translation = openai.Audio.translate("whisper-1", audio_file)
    #translation is a json object, get the text from it
    translation = translation["text"]
    store_data(transcript_dir, "translation", "txt", False, translation)  
    return translation


def get_whisper_transcription(sound_path):
    #call openapi whisper api 
    
    audio_file= open(sound_path, "rb")
    transcript = openai.Audio.transcribe("whisper-1", audio_file)
    transcript = transcript["text"]
    store_data(transcript_dir, "transcript", "txt", False, transcript)
    return transcript

def get_dalle_image(prompt):
    
    generation_response = openai.Image.create(
        prompt=prompt,
        n=1,
        size="1024x1024",
        response_format="url",
    )
    # print response
    print(generation_response)
    # save the image
    
    image_url = generation_response["data"][0]["url"]  # extract image URL from response
    image = requests.get(image_url).content 
    return store_data(image_dir, "dalle_image", "png", True, image)


def store_data(data_dir, file_name, file_ext, binary, data):

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