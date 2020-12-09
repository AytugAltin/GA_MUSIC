from Model.Song import Song
from Model.Outsider import Outsider
from music21 import *
import random
import copy
from multiprocessing.pool import ThreadPool
from threading import Thread
import numpy as np

class CrossoverStrategy:

    def __init__(self):
        self.current_generation = 0
        self.pool = ThreadPool(processes=8)
        self.children = []

        self.A = []
        self.B = []

        self.result_stream = None

        self.list = []

        self.indexA = 0
        self.indexB = 0

        self.choice = 0


    def age(self):
        self.current_generation = self.current_generation + 1


    def crosover_parents(self, parents):

        self.children = []
        #self.pool = ThreadPool(processes=18)
        i = 0
        while i < len(parents):
            j = i+1
            parentA = parents[i]
            while j < len(parents):
                """async_result = self.pool.apply_async(self.cross_songs, (parentA, parents[j]))
                results.append(async_result)"""

                self.cross_songs(parentA, parents[j])
                j += 1
            i += 1


        """self.pool.close()
        self.pool.join()"""



        return self.children

    def flip(self):
        temp = self.A
        self.A = self.B
        self.B = temp
        temp = self.indexA
        self.indexA = self.indexB
        self.indexB = temp

    def possible_flip(self):
        if self.choice > 0.5:
            self.flip()

    def cross_songs_4(self, parentA, parentB):


        self.A = parentA.notes
        self.B = parentB.notes

        self.result_stream = stream.Stream()

        self.list = []

        self.indexA = 0
        self.indexB = 0

        self.fix_start_index()


        while True:
            #SET order right
            self.choice = random.random()
            self.possible_flip()


            self.list.append(self.A[self.indexA])
            self.indexA += 1


            #SET order BACK
            self.possible_flip()

    def fix_start_index(self):
        note_A = self.A[self.indexA]
        note_B = self.B[self.indexB]






    def cross_songs(self, parentA, parentB):

        cross_A = np.array(parentA.notes)
        cross_B = np.array(parentB.notes)

        cross_A = parentA.notes
        cross_B = parentB.notes



        result_stream = stream.Stream()

        list = []

        indexA = 0
        indexB = 0



        try:
            while True:
                choice = random.random()

                if choice > 0.5:
                    temp = cross_A
                    cross_A = cross_B
                    cross_B = temp
                    temp = indexA
                    indexA = indexB
                    indexB = temp

                note = cross_A[indexA]

                new_note = copy.deepcopy(note)
                list.append(new_note)
                result_stream.insert(note.offset, new_note)

                currentoffsetB = cross_B[indexB].offset
                nextoffsetB = cross_B[indexB + 1].offset

                while nextoffsetB <= currentoffsetB:
                    indexB += 1
                    nextoffsetB = cross_B[indexB + 1].offset

                indexA+= 1
                note = cross_A[indexA]
                try:
                    next_note = cross_A[indexA+1]
                except:
                    next_note = cross_A[indexA]

                try:
                    while next_note.offset < nextoffsetB :
                        new_note = copy.deepcopy(note)
                        list.append(new_note)
                        result_stream.insert(note.offset, new_note)
                        indexA += 1
                        note = cross_A[indexA]

                        try:
                            next_note = cross_A[indexA + 1]
                        except:
                            next_note = cross_A[indexA]

                    if next_note.offset == nextoffsetB and note.offset < next_note.offset:
                        new_note = copy.deepcopy(note)
                        result_stream.insert(note.offset, new_note)
                        list.append(new_note)
                        indexA += 1




                finally:
                    currentoffset = cross_A[indexA].offset
                    while cross_B[indexB].offset < currentoffset:
                        indexB += 1


                if choice > 0.5:
                    temp = cross_A
                    cross_A = cross_B
                    cross_B = temp
                    temp = indexA
                    indexA = indexB
                    indexB = temp



        except Exception as e:
            #print(e)
            pass


        result = Song(raw_stream = result_stream, generation = self.current_generation)
        print(str(len(cross_A)) + " X " +str(len(cross_B)) + " = " +str(len(list)) ,end=', ')

        self.children.append(result)


    def cross_songs_2(self, parentA, parentB):

        cross_A = np.array(parentA.notes)
        cross_B = np.array(parentB.notes)

        result_stream = stream.Stream()

        list = []

        indexA = 0
        indexB = 0

        measures_A = parentA.raw_stream.makeMeasures()
        measures_B = parentB.raw_stream.makeMeasures()

        for index in range(0,len(measures_A)):
            A = measures_A[index]
            B = measures_B[index]











