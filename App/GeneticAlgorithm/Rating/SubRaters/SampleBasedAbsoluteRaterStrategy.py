from GeneticAlgorithm.Rating.SubRaters.AbstractSubRater import *
from Model.Measure import Measure
import math
from music21 import stream
from scipy.stats import wasserstein_distance
from fuzzywuzzy import fuzz
import numpy as np
from collections import Counter

class SampleBasedAbsoluteRaterStrategy(AbstractSubRater):

    def __init__(self,master,
                 absolute_rhythm_weight = ABSOLUTE_RHYTHM_WEIGHT,
                 absolute_types_weight = ABSOLUTE_TYPES_WEIGHT,
                 interval_distr_distnce_rating_weight = INTERVAL_DISTR_DISTNCE_RATING_WEIGHT,
                 types_distr_rating_weight = TYPES_DISTR_RATING_WEIGHT,
                 element_count_weight = ELEMENT_COUNT_WEIGHT
                 ):

        self.master_song = master
        self.absolute_rhythm_weight = absolute_rhythm_weight
        self.absolute_types_weight = absolute_types_weight

        self.types_distr_rating_weight = types_distr_rating_weight
        self.interval_distr_distnce_rating_weight =  interval_distr_distnce_rating_weight

        self.master_rhythm_string = self.create_rhythm_string(self.master_song)

        self.master_number_types = self.count_types(self.master_song)
        self.master_types_rate = self.calculate_type_dirst_rates(self.master_number_types)

        self.master_number_elements = len(self.master_song.notes)

        self.element_count_weight = element_count_weight

    def calculate_type_dirst_rates(self,types_rate):
        total = types_rate["chords"] + types_rate["notes"] + types_rate["rests"]

        type_dict = {
            "chords": 0,
            "notes": 0,
            "rests": 0
        }

        try:
            type_dict["chords"] = types_rate["chords"] / total
        except:
            pass
        try:
            type_dict["notes"] = types_rate["notes"] / total
        except:
            pass
        try:
            type_dict["rests"] = types_rate["rests"] / total
        except:
            pass

        return type_dict


    def count_types(self,song):
        type_dict = {
            "chords" : 0,
            "notes" : 0,
            "rests" : 0
        }
        counts = Counter(song.string_dict["types"])
        try:
            type_dict["chords"] = counts["X"]
        except:
            pass
        try:
            type_dict["notes"] = counts["N"]
        except:
            pass
        try:
            type_dict["rests"] = counts["R"]
        except:
            pass

        return type_dict



    def add_rating(self,song):
        absolute_rhythm_rating = self.create_absolute_rhythm_rating(song)
        song.rating.absolute_rhythm_rating = absolute_rhythm_rating * self.absolute_rhythm_weight

        absolute_types_rating = self.create_absolute_types_rating(song)
        song.rating.absolute_types_rating = absolute_types_rating * self.absolute_types_weight

        interval_distr_distance_rating = self.create_interval_distr_distance_rating(song)
        song.rating.interval_distr_distance_rating = interval_distr_distance_rating * self.interval_distr_distnce_rating_weight

        types_distr_rating = self.create_types_distr_rating(song)
        song.rating.types_distr_rating = types_distr_rating * self.types_distr_rating_weight

        length = len(song.notes)
        rests = abs(length - self.master_number_elements)
        rests = rests / self.master_number_elements
        song.rating.element_count_rating = rests * self.element_count_weight


    def create_types_distr_rating(self,song):
        number_types = self.count_types(song)
        type_distr = self.calculate_type_dirst_rates(number_types)
        difference = self.calculate_difference(type_distr["chords"],self.master_types_rate["chords"])
        difference += self.calculate_difference(type_distr["notes"],self.master_types_rate["notes"])
        difference += self.calculate_difference(type_distr["rests"],self.master_types_rate["rests"])

        return difference







    def create_interval_distr_distance_rating(self, song):
        absolute_distance = abs(wasserstein_distance( song.semitones,self.master_song.semitones))
        scaled_distance = abs(wasserstein_distance( [0],self.master_song.semitones))

        return absolute_distance/scaled_distance


    def create_absolute_types_rating(self,song):
        song_types_string = song.string_dict["types"]
        master_types_string = self.master_song.string_dict["types"]
        ratio = fuzz.ratio(song_types_string, master_types_string)
        return (100  - ratio) /100

    def create_absolute_rhythm_rating(self,song):
        song_rhythm_string = self.create_rhythm_string(song)
        ratio = fuzz.ratio(song_rhythm_string, self.master_rhythm_string)
        return (100  - ratio) /100


    def create_rhythm_string(self,song):
        string = [str(song.string_dict["offsets"][i]) + str(song.string_dict["durations"][i]) for i in
                   range(0, len(song.string_dict["offsets"]), 1)]
        return string





