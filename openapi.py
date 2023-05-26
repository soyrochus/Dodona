# Dodona - Simple GUI for the OpenAI API, made with OpenAI - Copyright © 2023 Iwan van der Kleijn - See LICENSE.txt for conditions

import openai
import requests
import os
import datetime

openai.api_key = os.environ.get("OPENAI_API_KEY")

# set a directory to save DALL·E images to
image_dir_name = "images"
image_dir = os.path.join(os.curdir, image_dir_name)

# create the directory if it doesn't yet exist
if not os.path.isdir(image_dir):
    os.mkdir(image_dir)

# print the directory to save to
print(f"{image_dir=}")

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
    # Get the current date and time
    now = datetime.datetime.now()

    # Format the date and time as a string
    timestamp = now.strftime("%Y%m%d_%H%M%S")

    # Append the timestamp to the filename
    filename = f"dalle_image_{timestamp}.png"

    image_filepath = os.path.join(image_dir, filename)
    image_url = generation_response["data"][0]["url"]  # extract image URL from response
    image = requests.get(image_url).content  # download the image

    with open(image_filepath, "wb") as image_file:
        image_file.write(image)  # write the image to the file
    
    return image_filepath