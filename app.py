# Dodona - Simple GUI for the OpenAI API, made with OpenAI - Copyright © 2023 Iwan van der Kleijn - See LICENSE.txt for conditions

import datetime
import tkinter as tk
import os
from PIL import Image, ImageTk
import openai
import requests
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

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.grid(padx=5, pady=5)  # Add padding around the frame
        self.create_widgets()

    def create_widgets(self):
        self.prompt_label = tk.Label(self, text="Prompt")
        self.prompt_label.grid(row=0, column=0, sticky="w")

        self.text_box = tk.Entry(self, width=50)  # Set width of the text box
        self.text_box.grid(row=1, column=0, sticky="w", padx=5, pady=5)  # Align to left and add padding

        self.send_button = tk.Button(self)
        self.send_button["text"] = "Send"
        self.send_button["command"] = self.send
        self.send_button.grid(row=2, column=1, sticky="e")

        self.quit = tk.Button(self, text="Close", fg="red",
                              command=self.master.destroy)
        self.quit.grid(row=2, column=0, sticky="e", padx=5)

    def send(self):
        # Load an image file
        #img = Image.open("python_logo.png")  # replace with your image path
        
        prompt_text = self.text_box.get()
        file_path = get_dalle_image(prompt_text)  # n=4, size="1024x1024")
        img = Image.open(file_path)
        image = ImageTk.PhotoImage(img)

        self.image_view = tk.Label(self, image=image)
        self.image_view.image = image  # keep a reference to the image
        self.image_view.grid(row=2, column=0, padx=5, pady=5)  # Add padding

root = tk.Tk()
app = Application(master=root)
app.mainloop()
