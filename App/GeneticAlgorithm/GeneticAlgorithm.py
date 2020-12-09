from GeneticAlgorithm.CrossoverStrategy import CrossoverStrategy
import numpy as np
import time
from Model.Outsider import Outsider
from GeneticAlgorithm.Mutation.Mutator import Mutator
import random
import gc
import traceback
from  Constants import *
import copy
import json


class GeneticAlgorithm:

    def __init__(self,ratingStrategy,controller):
        self.current_generation = 0
        self.max_generation = 20
        self.number_of_parents = 5
        self.rating_strategy = ratingStrategy
        self.crossover_strategy = CrossoverStrategy()
        self.controller = controller
        self.mutator = Mutator(ratingStrategy)
        self.data = {}
        self.data['songs'] = []


    def max_gen_reached(self):
        return  self.current_generation > self.max_generation


    def age(self):
        self.current_generation = self.current_generation + 1
        self.crossover_strategy.age()



    def start(self, population, max_generations,number_of_parents,premix):
        self.max_generation = max_generations
        self.number_of_parents = number_of_parents
        print('STARTING GENETIC ALGORITHM')
        parents = np.array(self.init_parents(population,premix))
        self.age()
        return self.loop(parents)


    def init_parents(self, parents,premix):
        # POPULATING
        print('INITIALISING PARENTS (mixing everything up): ', end='')
        start_time = time.time()

        for n in range(premix):
            print(' ' + str(n + 1) + "/" + str(premix)+ " " , end='')
            parents = self.crossover_strategy.crosover_parents(parents)
            children = []
            for n in range(min(self.number_of_parents,len(parents))):
                child = random.choice(parents)
                parents.remove(child)
                children.append(child)


            parents = children

        children = []
        for n in range(min(self.number_of_parents, len(parents))):

            child = random.choice(parents)
            parents.remove(child)
            children.append(child)

        parents = children




        print(str(round(time.time() - start_time, 2)) + " seconds")

        return parents



    def select_fittest(self,population):
        #TODO OPT: do you need to sort selecting the N lowest members?
        population.sort(key=lambda x:x.rating.total_rating)
        fittest = population[:self.number_of_parents]
        return fittest

    def fix_population(self,population):
        fixed = []
        for song in population:
            if len(song.get_measures()) is not NUMBER_OF_MEASURES:
                fixed.append(Outsider(raw_stream=song.raw_stream, generation=song.generation))
            else:
                fixed.append(song)
        return fixed

    def dump_to_json(self,song):

        ratings = vars(song.rating)
        jsonrate = {}
        for key, value in ratings.items():
            jsonrate[str(key)] = value

        self.data['songs'].append({
            'Gen': song.generation,
            'rating': jsonrate
        })

        with open(JSON+'/rating.txt', 'w+') as outfile:
            json.dump(self.data, outfile)





    def loop(self,parents):

        while not self.max_gen_reached():
            big_start_time = time.time()
            try:
                print("GENERATION" + str(self.current_generation))

                #POPULATING
                print('  - Populating: ', end='')
                start_time = time.time()
                children = self.crossover_strategy.crosover_parents(parents)
                print(str(round(time.time() - start_time, 2)) + " seconds")

                #RATING
                print('  - Rating: ', end='')
                start_time = time.time()
                children = self.rating_strategy.rate_population(children)
                print(str(round(time.time() - start_time, 2)) + " seconds")



                #SELECTING
                print('  - Selecting: ', end='')
                start_time = time.time()
                fittest = self.select_fittest(children)
                print(str(round(time.time() - start_time, 2)) + " seconds")
                print("   -- Best Child Rating = ")
                fittest[0].rating.print_rating()
                self.dump_to_json(fittest[0])

                if self.mutator.to_mutate_or_not(fittest):
                    # MUTATING
                    print('  - Mutating: ', end='')
                    start_time = time.time()
                    #left = fittest[0]
                    #copied = copy.deepcopy(left)
                    mutated = self.mutator.mutate_population(fittest)
                    #mutated.append(copied)
                    print(str(round(time.time() - start_time, 2)) + " seconds")
                else:
                    mutated = fittest

                fixed = self.fix_population(mutated)

                self.controller.write_population(population=fixed)



                parents = fixed
                self.age()
                gc.collect()
            except Exception as e:
                traceback.print_exc()
                print(e)

            print(str(round(time.time() - big_start_time, 2)) + " SECONDS")



        return parents







