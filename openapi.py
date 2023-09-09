# Dodona - Simple GUI for the OpenAI API, made with OpenAI - Copyright © 2023 Iwan van der Kleijn - See LICENSE.txt for conditions

import openai
import requests
import os
import datetime

from utils import realize_current_subdir, store_data_dump

openai.api_key = os.environ.get("OPENAI_API_KEY")

conversation_history = ["This is a conversation between user and AI:\n"]

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
    store_data_dump(transcript_dir, "translation", "txt", False, translation)  
    return translation

def get_whisper_transcription(sound_path):
    #call openapi whisper api 
    
    audio_file= open(sound_path, "rb")
    transcript = openai.Audio.transcribe("whisper-1", audio_file)
    transcript = transcript["text"]
    store_data_dump(transcript_dir, "transcript", "txt", False, transcript)
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
    return store_data_dump(image_dir, "dalle_image", "png", True, image)


def get_chat_response(prompt_text: str) -> str:
    
    global conversation_history
    prompt = "\n\n".join(conversation_history + ["User: " + prompt_text])
    
    response = openai.Completion.create(
#        engine="davinci",
        engine="text-davinci-003",
        prompt=prompt_text,
        max_tokens=200,
        n=1,
        stop=None,
        temperature=0,
    )

    message = response.choices[0].text.strip()
    conversation_history.append("User: " + prompt_text )
    conversation_history.append("AI: " + message)
    
    return message