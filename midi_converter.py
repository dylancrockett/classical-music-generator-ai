import py_midicsv
import os
import csv

keys = """! " # $ % & ' ( ) * + , - . / 0 1 2 3 4 5 6 7 8 9 : ; < = > ? @ A B C D E F G H I J K L M N O P Q R S T U"""
keys += """ V W X Y Z a b c d e f g h i j k l m n o p q r s t u v w x y z { | } ~"""

# a key value pair of note ints and key chars
key_table = {}

# inverted key_table
note_table = {}

for x, char in enumerate(keys.split(" ")):
    key_table.update({x + 1: char})
    note_table.update({char: x + 1})


# convert from a note int to a char
def note_to_char(note: int):
    return key_table.get(note, "p")


# convert from a char to a note int
def char_to_note(ch: str):
    return note_table.get(ch, 52)


class Track:
    def __init__(self):
        self.raw = []

        self.data = []

    def convert(self):
        for stamp in self.raw:
            self.data.append((stamp["time"], note_to_char(stamp["note"])))

    def add_entry(self, time, note):
        self.raw.append({
            "time": time,
            "note": note
        })


# generate a song file from a Midi file
class Song:
    def __init__(self, filename):
        # load the file
        csv_data = py_midicsv.midi_to_csv(filename)

        self.tracks = {}

        self.song = []

        self.length = 0

        self.current_time = 0

        self.length_distance = 120

        # fill the tracks table
        for track in range(10):
            self.tracks.update({track: Track()})

        for entry in csv_data:
            entry = entry.replace(" ", "")
            entry = entry.split(",")

            if entry[2] == "Note_on_c":
                # print(str(int(entry[0])) + " | " + entry[2] + " | " + str(entry[1]) + " | " + str(entry[4]))
                self.tracks[int(entry[0])].add_entry(int(entry[1]), int(entry[4]))

                if int(entry[1]) > self.length:
                    self.length = int(entry[1])

        to_delete = []

        for number in self.tracks:
            if not self.tracks[number].raw:
                self.tracks[number] = None
                to_delete.append(number)
                continue

            # convert the raw data
            self.tracks[number].convert()

        # remove dumb tracks
        for track in to_delete:
            del self.tracks[track]

        # loop until ending time reached
        while self.current_time <= self.length:
            notes = ""

            for track in self.tracks:
                for note in self.tracks[track].data:
                    if self.current_time in note:
                        val = note[1]

                        if val is not None:
                            notes += val

            if notes != "":
                self.song.append(notes)
            else:
                self.song.append(" ")

            self.current_time += self.length_distance

        print("-------\n COMBINED TRACK")
        print(self.song)

    # convert the song into a csv
    def save(self, filename):
        with open(filename + ".csv", "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerows(self.song)


# convert a song file into a Midi File
class Midi:
    def __init__(self, filename=None, song=None, tempo=420):
        if song is None:
            self.song = []
        else:
            self.song = song

        if filename is not None:
            # load the file
            with open(filename + ".csv", "r") as f:
                file = f.readlines()
                for line in file:
                    line = line.replace("\n", "")
                    line = line.replace(",", "")

                    self.song.append(line)

        self.time = 0

        self.time_distance = 120

        self.pedal_queue = []

        self.csv_string = []

        # midi setup
        self.csv_string.append("0, 0, Header, 1, 10, 480")
        self.csv_string.append("1, 0, Start_track")
        self.csv_string.append('1, 0, Title_t, "AI Song"')
        self.csv_string.append('1, 0, Copyright_t, "None"')
        self.csv_string.append("1, 0, Time_signature, 4, 2, 24, 8")
        self.csv_string.append('1, 0, Key_signature, 2, "major"')
        self.csv_string.append("1, 0, Tempo, " + str(tempo) + "000")
        self.csv_string.append('1, 0, Marker_t, "Teil 1"')
        self.csv_string.append("1, 0, End_track")
        self.csv_string.append("2, 0, Start_track")
        self.csv_string.append('2, 0, Title_t, "Piano"')

        for beat in self.song:
            # self.pedal_queue.append("4, " + str(self.time) + ", Control_c, 0, 64, 0")

            if beat == " ":
                self.time += self.time_distance
                continue

            for note in beat:
                # print(str(track) + ", " + str(self.time) + ", Note_on_c, 0, "
                #                        + str(char_to_note(note)) + ", 127")

                self.csv_string.append("2, " + str(self.time) + ", Note_on_c, 0, "
                                       + str(char_to_note(note)) + ", 63")

            self.time += self.time_distance

        # add silence at end of file
        for space in range(20):
            self.time += self.time_distance

            self.csv_string.append("2, " + str(self.time) + ", Note_on_c, 0, 1, 0")

        self.csv_string.append("2, " + str(self.time) + ", End_track")

        self.csv_string.append("4, 0, Start_track")
        self.csv_string.append('4, 0, Title_t, "Pedal"')
        self.csv_string.append("4, 0, Program_c, 0, 0")

        for pedal in self.pedal_queue:
            self.csv_string.append(pedal)

        self.csv_string.append("4, " + str(self.time) + ", End_track")
        self.csv_string.append("0, 0, End_of_file")

    def save(self, filename):
        midi_file = py_midicsv.csv_to_midi(self.csv_string)

        with open(filename + ".mid", "wb") as output_file:
            midi_writer = py_midicsv.FileWriter(output_file)
            midi_writer.write(midi_file)


if __name__ == "__main__":
    count = 0

    for file_name in os.listdir("sources"):
        print(file_name)

        s = Song("sources/" + file_name)

        s.save("training_data/" + file_name.replace(".mid", ""))

        midi = Midi("training_data/" + file_name.replace(".mid", "") + "")

        midi.save("output/" + file_name.replace(".mid", ""))

        count += 1