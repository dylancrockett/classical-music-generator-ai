from midi_converter import char_to_note, note_to_char
import random


def load_data(filename):
    data = []

    # load the file
    with open(filename, "r") as f:
        file = f.readlines()
        for line in file:
            line = line.replace("\n", "")
            line = line.replace(",", "")

            data.append(line)

    return data


# generate a seed for the model to use to generate a song sequence
def generate_seed(size):
    seed = []

    for i in range(size):
        arr = []

        for x in range(88):
            arr.append(0)

        for x in range(random.randint(5, 10)):
            arr[random.randint(0, 81)] = 1

        seed.append(arr)

    print(seed)
    return seed


def str_to_mask(string: str):
    arr = []

    for x in range(88):
        arr.append(0)

    if string == " ":
        return arr
    else:
        for note in string:
            arr[char_to_note(note) - 1] = 1

        return arr


def bool_to_mask(boolean_list: list):
    arr = []

    for x in range(88):
        if boolean_list[0][x - 1]:
            arr.append(1)
        else:
            arr.append(0)

    return arr


def mask_to_string(mask: list):
    string = ""

    for x, val in enumerate(mask):
        if val == 1:
            string += note_to_char(x + 1)

    return string


# convert a dataset into a sample for the AI to train off of
class Sample:
    def __init__(self, song: list):
        self.song = song
        self.data = []

        for beat in song:
            arr = []

            for x in range(88):
                arr.append(0)

            if beat == " ":
                self.data.append(arr)
                continue
            else:
                for note in beat:
                    arr[char_to_note(note) - 1] = 1

                self.data.append(arr)
                continue


def get_unique_list(origin: list):
    unique = []

    for item in origin:
        if item not in unique:
            unique.append(item)

    return unique
