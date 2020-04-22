import os
import time
import tkinter.messagebox
from tkinter import *
from tkinter import ttk
from ttkthemes import themed_tk as tk
from pygame import mixer
from concurrent.futures import ThreadPoolExecutor
from generate import  SongGenerator
import uuid

# root Tk element
root = tk.ThemedTk()
root.set_theme("breeze")

executor = ThreadPoolExecutor()

# app status bar
statusbar = ttk.Label(root, text="Welcome to Classical Music Generator", relief=SUNKEN, anchor=W)
statusbar.pack(side=BOTTOM, fill=X)

# tab bar for selecting to generate or play music
tab_bar = ttk.Notebook(root)
generate_frame = ttk.Frame(tab_bar)
play_frame = ttk.Frame(tab_bar)
tab_bar.add(generate_frame, text="Generate Music")
tab_bar.add(play_frame, text="Listen to Music")
tab_bar.pack(expand=1, fill="both")

# songs list for storing found songs
songs = []

# index for keeping track of the length of the song_list listbox
song_list_length = 0

# initializing the audio mixer
mixer.init()

# name the root
root.title("Classical Music Generator")

# create the left part of the play frame containing the song list
play_left = Frame(play_frame)
play_left.pack(side=LEFT, padx=30, pady=30)
song_list = Listbox(play_left, selectmode=SINGLE)
song_list.pack()

# song generator object
song_generator = SongGenerator()


# function for adding a song to the song_list
def add_song(song_name):
    global song_list_length
    songs.append(song_name)
    song_list.insert(song_list_length, song_name)
    song_list_length = 1 + song_list_length


# load all of the songs already stored in the songs folder
for (dirpath, dirnames, filenames) in os.walk("songs"):
    for file_name in filenames:
        add_song(file_name)
    break


# generate song info
ttk.Label(generate_frame, text="Song Name").grid(row=0)
ttk.Label(generate_frame, text="Song Length (Ticks)").grid(row=1)
ttk.Label(generate_frame, text="Song Tempo").grid(row=2)

song_name = ttk.Entry(generate_frame)
song_length = ttk.Entry(generate_frame)
song_tempo = ttk.Entry(generate_frame)

song_name.insert(0, str(uuid.uuid4()))
song_length.insert(0, "1000")
song_tempo.insert(0, "520")

song_name.grid(row=0, column=1)
song_length.grid(row=1, column=1)
song_tempo.grid(row=2, column=1)


def new_song(name, length, tempo):
    song_generator.generate(length, 500, tempo, name)
    pass


def generate_song():
    try:
        name, length, tempo = song_name.get(), int(song_length.get()), int(song_tempo.get())
        # executor.submit(new_song, song_name.get(), int(song_length.get()), int(song_tempo.get()))
        song_generator.generate(length, 500, tempo, name)

        add_song(song_name.get())
        song_name.delete(0, 'end')
        song_name.insert(0, str(uuid.uuid4()))
    except Exception as e:
        print(e)
        tkinter.messagebox.showerror('Error', str(e))
    pass


generate_button = ttk.Button(generate_frame, text="Generate", command=generate_song)
generate_button.grid(row=4, column=1)


# create the right part of the play frame containing the start stop and volume control
play_right = Frame(play_frame)
play_right.pack(pady=30)

# top frame of the play frame
play_top_frame = Frame(play_right)
play_top_frame.pack()


# used to play a song
def play_music():
    try:
        # stop music that is already playing and give a delay before playing the new song
        stop_music()
        time.sleep(1)

        # get the currently selected song
        selected_song = song_list.curselection()
        selected_song = int(selected_song[0])

        # get the song name from the songs list
        song_name = songs[selected_song]

        # load the song into the mixer
        mixer.music.load("songs/" + song_name)

        # play the song
        mixer.music.play()

        # update the status bar
        statusbar['text'] = "Playing music" + ' - ' + os.path.basename(song_name)
    except Exception as e:
        print("Exception occurred when trying to open a song file, exception:" + str(e))
        tkinter.messagebox.showerror('File not found', 'Unable to find the file, please check if the file exists on'
                                                       ' your system.')


# stop the music being played
def stop_music():
    mixer.music.stop()
    statusbar['text'] = "Music Stopped"


# use to set the volume of the music via the slider
def set_volume(val):
    volume = float(val) / 100
    mixer.music.set_volume(volume)


play_middle_frame = Frame(play_right)
play_middle_frame.pack(pady=30, padx=30)

playPhoto = PhotoImage(file='images/play_button.png')
playBtn = ttk.Button(play_middle_frame, image=playPhoto, command=play_music)
playBtn.grid(row=0, column=0, padx=10)

stopPhoto = PhotoImage(file='images/stop_button.png')
stopBtn = ttk.Button(play_middle_frame, image=stopPhoto, command=stop_music)
stopBtn.grid(row=0, column=1, padx=10)

# bottom frame for volume control
play_bottom_frame = Frame(play_right)
play_bottom_frame.pack()

# configure the scale used for volume control
scale = ttk.Scale(play_bottom_frame, from_=0, to=100, orient=HORIZONTAL, command=set_volume)
scale.set(50)
mixer.music.set_volume(0.5)
scale.grid(row=0, column=2, pady=15, padx=30)


# stop the music and destroy the window when the window is closed
def on_closing():
    stop_music()
    root.destroy()


root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
