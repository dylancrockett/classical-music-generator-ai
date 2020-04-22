from model_converter import Sample, load_data, get_unique_list
import textgenrnn
import numpy as np
import math
import os

"""
model.save("music_bot")
model.load_weights("music_bot")

np.set_printoptions(threshold=np.inf)
"""


class Dataset:
    def __init__(self):
        self.samples = []

        self.unique_set = []

        self.set = []

        self.sequences = {
            "x": [],
            "y": []
        }

        self.sequence_len = 10  # sequence_size

    def add_sample(self, sample: Sample):
        self.samples.append(sample)

    def generate_file(self, filename):
        self.set = []

        for sample in self.samples:
            self.set.append(sample.song)

        contents = ""

        for song in self.set:
            song_text = ""

            for beat in song:
                song_text += "," + beat

            song_text = song_text[1:]
            contents += song_text + "\n"

        print(contents)

        with open(filename + ".txt", "w", newline="") as f:
            f.write(contents)

    def get_training_set(self):
        self.set = []
        self.sequences["x"] = []
        self.sequences["y"] = []

        for sample in self.samples:
            for beat in sample.data:
                self.set.append(beat)

        self.unique_set = get_unique_list(self.set)

        print(len(self.unique_set))

        for x in range(math.floor(len(self.set) / self.sequence_len)):
            sequence = self.set[self.sequence_len * x:self.sequence_len * (x + 1)]
            self.sequences["x"].append(sequence)
            self.sequences["y"].append(self.set[self.sequence_len * (x + 1) + 1])

        print(len(self.sequences))

        training_data = {
            "x": np.array(self.sequences["x"]),
            "y": np.array(self.sequences["y"]),
            "batch_size": len(self.sequences)
        }

        return training_data


set = Dataset()

for file_name in os.listdir("training_data"):
    set.add_sample(Sample(load_data("training_data/" + file_name)))

set.generate_file("training_set")

generator = textgenrnn.textgenrnn()
generator.train_from_file("training_data.txt", num_epochs=25, gen_epochs=0)
generator.save("better_bot.hdf5")
os.remove("training_data.txt")

"""
print("TRAINING MODEL")

training = d.get_training_set()

print(training["x"].shape)
print(training["y"].shape)

model.fit(training["x"], training["y"], batch_size=training["batch_size"], epochs=50)

model.save("music_bot")
"""
