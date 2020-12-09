from GeneticAlgorithm.Rating.SubRaters.AbstractSubRater import *
from Model.Measure import Measure
import math
from music21 import stream
from scipy.stats import wasserstein_distance
from fuzzywuzzy import fuzz
import numpy as np

class SampleBasedMeasureRaterStrategy(AbstractSubRater):


    def __init__(self,master,
                 types_distance_rating_weight = TYPES_DISTANCE_RATING_WEIGHT,
                 semitones_distance_rating_weight = SEMITONES_DISTANCE_RATING_WEIGHT,
                 pitches_distance_rating_weight = PITCHES_DISTANCE_RATING_WEIGHT,
                 duration_distance_rating_weight = DURATION_DISTANCE_RATING_WEIGHT,
                 offsets_distance_rating_weight = OFFSETS_DISTANCE_RATING_WEIGHT):

        self.master_song = master

        self.types_distance_rating_weight = types_distance_rating_weight
        self.semitones_distance_rating_weight = semitones_distance_rating_weight
        self.pitches_distance_rating_weight = pitches_distance_rating_weight
        self.duration_distance_rating_weight = duration_distance_rating_weight
        self.offsets_distance_rating_weight = offsets_distance_rating_weight


        self.types_distance_rating = 0
        self.semitones_distance_rating = 0
        self.pitches_distance_rating = 0
        self.duration_distance_rating = 0
        self.offsets_distance_rating = 0

    def reset_values(self):
        self.types_distance_rating = 0
        self.semitones_distance_rating = 0
        self.pitches_distance_rating = 0
        self.duration_distance_rating = 0
        self.offsets_distance_rating = 0


    def add_rating(self,song):
        self.reset_values()
        self.calculate_measure_bindings_order_rating(song=song)
        self.create_ratings(song)

    def create_ratings(self,song):
        number_of_measures = len(song.measure_list)

        song.rating.types_distance_rating = self.types_distance_rating / number_of_measures * self.types_distance_rating_weight
        song.rating.semitones_distance_rating = self.semitones_distance_rating / number_of_measures* self.semitones_distance_rating_weight
        song.rating.pitches_distance_rating = self.pitches_distance_rating  / number_of_measures* self.pitches_distance_rating_weight
        song.rating.duration_distance_rating = self.duration_distance_rating  / number_of_measures* self.duration_distance_rating_weight
        song.rating.offsets_distance_rating = self.offsets_distance_rating / number_of_measures* self.offsets_distance_rating_weight



    def calculate_measure_bindings_order_rating(self, song):
        for measure,master_measure in zip (song.measure_list,self.master_song.measure_list):
            self.measure_bindings_distance(measure_a=measure, measure_b=master_measure)



    def measure_bindings_distance(self, measure_a, measure_b):

        types_distance_rating =  self.create_distance_rating(measure_a,measure_b,"types")
        self.types_distance_rating +=  types_distance_rating
        measure_a.absolute_distance_from_master["types"] += types_distance_rating

        semitones_distance_rating =  self.create_distance_rating(measure_a,measure_b,"semitones")
        self.semitones_distance_rating +=  semitones_distance_rating
        measure_a.absolute_distance_from_master["semitones"] += semitones_distance_rating


        pitches_distance_rating =  self.create_distance_rating(measure_a,measure_b,"pitches")
        self.pitches_distance_rating +=  pitches_distance_rating
        measure_a.absolute_distance_from_master["pitches"] += pitches_distance_rating


        duration_distance_rating =  self.create_distance_rating(measure_a,measure_b,"durations")
        self.duration_distance_rating +=  duration_distance_rating
        measure_a.absolute_distance_from_master["durations"] += duration_distance_rating


        offsets_distance_rating =  self.create_distance_rating(measure_a,measure_b,"offsets")
        self.offsets_distance_rating +=  offsets_distance_rating
        measure_a.absolute_distance_from_master["offsets"] += offsets_distance_rating



    def create_distance_rating(self,measure_a, measure_b,list_key):
        types_list_a = self.create_array_out_of_type(measure_a,list_key)
        types_list_b = self.create_array_out_of_type(measure_b,list_key)
        types_distance = self.calculate_wasserstein_difference(types_list_a, types_list_b)
        complement = self.create_list_complement(types_list_b)
        maximum_types_distance = self.calculate_wasserstein_difference(complement, types_list_b)

        return types_distance / maximum_types_distance


    def create_list_complement(self,list):
        complement_list=[]
        for element in list:
            negative_element = 100 -  (round(element /100) * 100)
            complement_list.append(negative_element)

        return complement_list


    def create_array_out_of_type(self,measure_object,list_key):
        list=[]
        for key,value in measure_object.reference_list.items():

            list.append(value[list_key])

        return list



    def calculate_wasserstein_difference(self,listA,listB):
        return abs(wasserstein_distance(listA, listB))

