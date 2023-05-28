# Dodona - Simple GUI for the OpenAI API, made with OpenAI - Copyright © 2023 Iwan van der Kleijn - See LICENSE.txt for conditions

import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import sounddevice as sd
import soundfile as sf
import threading
import random
import numpy
from utils import realize_current_subdir

import os
import threading
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
from PIL import Image, ImageTk
import sounddevice as sd
import numpy as np
import soundfile as sf
import queue

class RecordAudio(tk.Frame):
    def __init__(self, master=None, root_dir="."):
        super().__init__(master)
        self.root_dir = root_dir
        self.master = master
        self.master.title("Audio Recorder")
        self.grid()

        # Images for buttons
        self.record_img = tk.PhotoImage(file='icons/record.png')
        self.play_img = tk.PhotoImage(file='icons/play.png')
        self.stop_img = tk.PhotoImage(file='icons/stop.png')
        self.delete_img = tk.PhotoImage(file='icons/delete.png')

        self.record_button = tk.Button(self, image=self.record_img, command=self.start_recording)
        self.play_button = tk.Button(self, image=self.play_img, command=self.play_selected)
        self.stop_button = tk.Button(self, image=self.stop_img, command=self.stop_recording)
        self.delete_button = tk.Button(self, image=self.delete_img, command=self.delete_selected)
        self.close_button = tk.Button(self, text="Close", command=self.master.destroy)

        self.file_list = tk.Listbox(self)

        self.record_button.grid(row=0, column=0)
        self.play_button.grid(row=0, column=1)
        self.stop_button.grid(row=0, column=2)
        self.delete_button.grid(row=0, column=3)
        self.file_list.grid(row=1, column=0, columnspan=4)
        self.close_button.grid(row=2, column=0, columnspan=4)

        self.recording = False
        self.q = queue.Queue()

    def start_recording(self):
        if self.recording:
            return
        self.recording = True
        self.record_button.config(image=self.stop_img)
        self.stream = sd.InputStream(callback=self.audio_callback)
        self.stream.start()

    def stop_recording(self):
        if not self.recording:
            return
        self.recording = False
        self.record_button.config(image=self.record_img)
        self.stream.stop()
        self.stream.close()

        filename = f"recording_{np.random.randint(1000)}.wav"
        filepath = os.path.join(self.root_dir, filename)

        # Make sure directory exists
        os.makedirs(os.path.dirname(filepath), exist_ok=True)

        qsize = self.q.qsize()
        if qsize > 0:
            complete_recording = np.concatenate([self.q.get() for _ in range(qsize)])
            sf.write(filepath, complete_recording, 44100)
            self.file_list.insert(tk.END, filename)

    def audio_callback(self, indata, frames, time, status):
        if self.recording:
            self.q.put(indata.copy())

    def play_selected(self):
        if self.recording or len(self.file_list.curselection()) == 0:
            return
        filename = self.file_list.get(self.file_list.curselection()[0])
        threading.Thread(target=self.play_thread, args=(os.path.join(self.root_dir, filename),), daemon=True).start()

    def play_thread(self, filename):
        try:
            data, fs = sf.read(filename, dtype='float32')  
            sd.play(data, fs)
            status = sd.wait()  
        finally:
            pass

    def delete_selected(self):
        if len(self.file_list.curselection()) == 0:
            return
        filename = self.file_list.get(self.file_list.curselection()[0])
        filepath = os.path.join(self.root_dir, filename)
        os.remove(filepath)
        self.file_list.delete(self.file_list.curselection()[0])

   

if __name__ == "__main__":
    
    # set a directory to save DALL·E images to
    audio_dir = realize_current_subdir("audio")
    root = tk.Tk()
    app = RecordAudio(master=root, root_dir=audio_dir)
    app.mainloop()
