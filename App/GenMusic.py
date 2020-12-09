from Controller.IOController import IOController
from GeneticAlgorithm.GeneticAlgorithm import GeneticAlgorithm
from GeneticAlgorithm.Rating.SampleBasedRatingStrategy import SampleBasedRatingStrategy
from GeneticAlgorithm.Rating.TheoryBasedRatingStrategy import TheoryBasedRatingStrategy
from Model.Outsider import Outsider
from Constants import *

import sys


class GenMusic:

    def __init__(self, input_path, output_path):

        self.IOController = IOController(input_path, output_path)

        self.genetic_algorithm = self.create_genetic_algorithm()


        self.population = self.init_population()


    def create_genetic_algorithm(self):

        print("MASTER: " ,end='')
        try:
            print(PATH_TO_MASTER)
            sample = Outsider(raw_stream=self.IOController.get_input(PATH_TO_MASTER),generation=-1)
            return GeneticAlgorithm(ratingStrategy=SampleBasedRatingStrategy(master_song=sample),controller=self.IOController)
        except:
            print("NO MASTER")
            return GeneticAlgorithm(ratingStrategy= TheoryBasedRatingStrategy(),controller=self.IOController)

    def init_population(self):
        stream_list = self.IOController.get_all_input()
        population = self.init_songs(stream_list)
        return population

    def init_songs(self, stream_list, generation = 0):
        song_list = []
        for stream in stream_list:
            song = Outsider(raw_stream=stream, generation=generation)
            song_list.append(song)
        return song_list


    def play_last_gen(self):
        for song in self.population:
            song.play()

    def display_last_gen(self):
        for song in self.population:
            song.print_info()


    def run(self):
        self.population = self.genetic_algorithm.start(self.population, max_generations=MAX_GEN,number_of_parents=NR_PARENTS, premix=NR_PRE_MIX)
        self.IOController.write_population(self.population)





if __name__ == '__main__':
    if len(sys.argv) != 3:
        sys.exit("ARGUMENT ERROR: Invalid number fo arguments, 2 arguments (input path,output path) needed" + str(
            len(sys.argv)) + " were given!")
    input_path = sys.argv[1]
    output_path = sys.argv[2]



    GenMusic = GenMusic(input_path, output_path)
    GenMusic.run()


    print("done")
