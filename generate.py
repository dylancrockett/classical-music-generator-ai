from midi_converter import Midi
import tensorflow as tf
import random
import time
import uuid
import textgenrnn

# check if GPUs are available to Tensorflow
print("Num GPUs Available: ", len(tf.config.experimental.list_physical_devices('GPU')))


# Song Generator Class
class SongGenerator:
    def __init__(self):
        self.generator = textgenrnn.textgenrnn()
        self.generator.load("better_bot.hdf5")

    def generate(self, song_length=1000, section_length=250, tempo=520, name=None):
        print("#####")
        print("Started Generating Song")
        print("#####")

        final = []
        success = 0
        batch_size = 10

        while True:
            print("Running Generation Loop")
            if success > int(song_length / section_length):
                print("Finishing Song Generation")
                break

            batch = self.generator.generate(batch_size, temperature=0.25, return_as_list=True, max_gen_length=section_length)

            for entry in batch:
                section = entry.split(",")

                empty_cnt = 0

                for line in section:
                    if line == " ":
                        empty_cnt += 1

                # if the song is more than 25% empty space ignore this garbage
                if empty_cnt > int(float(section_length) * 0.25):
                    continue

                # memory used for avoiding repeating sequences if 4 of the same notes/chords appear in series
                memory = []

                # sort the notes
                for index, line in enumerate(section):
                    section[index] = ''.join(sorted(line))

                # filter out repeating notes
                for i, line in enumerate(section):
                    if section[i - 4:i] == memory:
                        memory = section[i - 4:i]
                        continue
                    else:
                        final.append(line)

                    memory = section[i - 4:i]

                success += 1

        if name is None:
            song_name = time.strftime("%Y%m%d-%H%M%S") + "-" + str(uuid.uuid4())
        else:
            song_name = name

        print("#####")
        print("Finished Generating Song")
        print("#####")

        Midi(song=final, tempo=tempo).save("songs/" + song_name)
        return song_name


if __name__ == "__main__":
    lengths = [1000, 1500, 2000]
    section_lengths = [250, 500, 750]
    tempos = [480, 520, 560]
    generator = SongGenerator()

    # generate INFINITE songs
    while True:
        length = random.choice(lengths)
        r_section_length = random.choice(section_lengths)
        r_tempo = random.choice(tempos)

        print("GENERATING SONG WITH PARAMS: { LENGTH: '" + str(length) + "', SECTION_LENGTH: '" + str(r_section_length) +
              "', TEMPO: '" + str(r_tempo) + "' }")

        name = generator.generate(
            length,
            r_section_length,
            r_tempo
        )

        print("GENERATED SONG: " + name)
