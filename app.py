# Dodona - Simple GUI for the OpenAI API, made with OpenAI - Copyright © 2023 Iwan van der Kleijn - See LICENSE.txt for conditions

import datetime
import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
from tkinter import filedialog
import os
from PIL import Image, ImageTk

from openapi import get_dalle_image, get_whisper_transcription

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        master.title('Dodona')
        master.columnconfigure(0, weight=1) # Configure
        self.grid(padx=5, pady=5)  # Add padding around the frame
        self.pack(fill=tk.BOTH, expand=True)  # Add padding around the frame
        self.create_widgets()

    def create_widgets(self):
        s = ttk.Style()
        s.configure('TNotebook.Tab', background='#f2f2f2', foreground='black')
        s.configure('TButton', background='#f2f2f2', foreground='black')

        self.tabControl = ttk.Notebook(self)  # Create Tab Control

        # Creating the Dall-e tab
        self.tab1 = ttk.Frame(self.tabControl)
        self.tabControl.add(self.tab1, text='Dall-e')

        # Creating widgets for the Dall-e tab
        #self.prompt = tk.StringVar()
        self.prompt_entry = tk.Text(self.tab1, height=3)
        self.prompt_entry.grid(row=0, column=0, pady=5, padx=5, sticky="ew")

        self.send_button1 = ttk.Button(self.tab1, text="Send", command=self.send_dall_e)
        self.send_button1.grid(row=1, column=0, pady=5, padx=5)

        self.image_area = tk.Canvas(self.tab1, bg="#ffffff")
        self.image_area.grid(row=2, column=0, pady=5, padx=5, sticky="nsew")

        # Creating the Speech to text tab
        self.tab2 = ttk.Frame(self.tabControl)
        self.tabControl.add(self.tab2, text='Speech to text')

        # Creating widgets for the Speech to text tab
        self.select_file_button = ttk.Button(self.tab2, text="Select sound file", command=self.open_file_dialog)
        self.select_file_button.grid(row=0, column=0, pady=5, padx=5)

        self.send_button2 = ttk.Button(self.tab2, text="Send", command=self.send_sound_to_text)
        self.send_button2.grid(row=0, column=1, pady=5, padx=5)

        self.file_path_label = tk.StringVar()
        self.label = ttk.Label(self.tab2, textvariable=self.file_path_label)
        self.label.grid(row=1, column=0, columnspan=2)

        self.transcription_field = scrolledtext.ScrolledText(self.tab2, wrap=tk.WORD, width=30, height=10, bg="#ffffff")
        self.transcription_field.grid(row=2, column=0, columnspan=2, pady=5, padx=5, sticky="nsew")

        # Configure columns and rows for expanding
        self.tab1.columnconfigure(0, weight=1)
        self.tab1.rowconfigure(2, weight=1)
        self.tab2.columnconfigure(0, weight=1)
        self.tab2.columnconfigure(1, weight=1)
        self.tab2.rowconfigure(2, weight=1)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        # Display the tab control
        self.tabControl.grid(row=0, column=0, sticky="nsew", pady=5, padx=5)

        # Add close button under the tabs
        self.close_button = ttk.Button(self, text="Close", command=self.master.destroy)
        self.close_button.grid(row=1, column=0, pady=5, padx=5)

    def open_file_dialog(self):
        file_path = filedialog.askopenfilename()
        self.file_path_label.set(file_path)
        print(f"Selected file: {file_path}")  # print the selected file path


    def send_sound_to_text(self):
        
        text = get_whisper_transcription(self.file_path_label.get())
        self.transcription_field.delete('1.0', tk.END)
        self.transcription_field.insert(tk.END, text)

    
    def send_dall_e(self):
        # Load an image file
        #img = Image.open("python_logo.png")  # replace with your image path
        
        prompt_text = self.prompt_entry.get("1.0", tk.END)
        file_path = get_dalle_image(prompt_text)  # n=4, size="1024x1024")
        img = Image.open(file_path)
        image = ImageTk.PhotoImage(img)
        
        # Save the image reference (prevent GC from disposing it)
        self.image_area.image = image  

        # Clear the canvas and draw the new image
        self.image_area.delete("all")
        self.image_area.create_image(0, 0, anchor=tk.NW, image=image)

root = tk.Tk()
app = Application(master=root)
app.mainloop()
