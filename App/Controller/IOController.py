from music21 import *
import os


class IOController:

    def __init__(self, input_path, output_path):
        self.input_path = input_path
        self.output_path = output_path
        if not os.path.exists(output_path):
            os.makedirs(output_path)

    def get_all_input(self):

        print("READING FILES------------")
        objects = []
        path_list = os.listdir(self.input_path)
        for path in path_list:
            if path.endswith(".mid"):
                print("  - " + path)
                o = self.get_input(self.input_path + "/" +path)
                objects.append(o)

        print("READING DONE-------------")
        return objects



    def get_input(self, file_path):
        return converter.parse(file_path)


    def write_population(self,population):
        i = 1
        for song in population:
            song.raw_stream.write(fmt="midi", fp=self.output_path+"/GEN"+str(song.generation)+"Song"+str(i)+".mid")
            i += 1