# Dodona - Simple GUI for the OpenAI API, made with OpenAI - Copyright © 2023 Iwan van der Kleijn - See LICENSE.txt for conditions

import tkinter as tk
from PIL import Image, ImageTk

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
        self.send_button.grid(row=3, column=1, sticky="e")

        self.quit = tk.Button(self, text="Close", fg="red",
                              command=self.master.destroy)
        self.quit.grid(row=3, column=0, sticky="e", padx=5)

    def send(self):
        # Load an image file
        img = Image.open("python_logo.png")  # replace with your image path
        photo = ImageTk.PhotoImage(img)

        self.image_view = tk.Label(self, image=photo)
        self.image_view.image = photo  # keep a reference to the image
        self.image_view.grid(row=2, column=0, padx=5, pady=5)  # Add padding

root = tk.Tk()
app = Application(master=root)
app.mainloop()
