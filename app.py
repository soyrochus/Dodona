# Dodona - Simple GUI for the OpenAI API, made with OpenAI - Copyright © 2023 Iwan van der Kleijn - See LICENSE.txt for conditions
import tkinter as tk
from PIL import Image, ImageTk

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.text_box = tk.Entry(self)
        self.text_box.pack(side="top")

        # Load an image file
        img = Image.open("python_logo.png")  # replace with your image path
        photo = ImageTk.PhotoImage(img)

        self.image_view = tk.Label(self, image=photo)
        self.image_view.image = photo  # keep a reference to the image
        self.image_view.pack(side="top")

        self.send_button = tk.Button(self)
        self.send_button["text"] = "Send"
        self.send_button["command"] = self.send
        self.send_button.pack(side="left")

        self.quit = tk.Button(self, text="Close", fg="red",
                              command=self.master.destroy)
        self.quit.pack(side="right")

    def send(self):
        pass  # do nothing for now

root = tk.Tk()
app = Application(master=root)
app.mainloop()
