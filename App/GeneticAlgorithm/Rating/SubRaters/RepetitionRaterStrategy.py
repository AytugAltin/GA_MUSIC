from GeneticAlgorithm.Rating.SubRaters.AbstractSubRater import *
from Model.Measure import Measure
import math
from music21 import stream

from fuzzywuzzy import fuzz
import numpy as np
class RepetitionRaterStrategy(AbstractSubRater):

    def __init__(self, measures_rating_weight = MEASURES_RATING_WEIGHT, bindings_rating_weight = BINDINGS_RATING_WEIGHT,
                  master_strong_measures_ratio=MASTER_STRONG_MEASURES_RATIO,
                 master_normal_measures_ratio=MASTER_NORMAL_MEASURES_RATIO, master_weak_measures_ratio=MASTER_WEAK_MEASURES_RATIO,
                 master_garbage_measures_ratio=MASTER_GARBAGE_MEASURES_RATIO, master_strong_bindings_ratio=MASTER_STRONG_BINDINGS_RATIO,
                 master_normal_bindings_ratio=MASTER_NORMAL_BINDINGS_RATIO, master_weak_bindings_ratio=MASTER_WEAK_BINDINGS_RATIO,
                 master_garbage_bindings_ratio=MASTER_GARBAGE_BINDINGS_RATIO):

        self.bindings_rating_weight = bindings_rating_weight
        self.measures_rating_weight = measures_rating_weight

        self.master_strong_measures_ratio = master_strong_measures_ratio
        self.master_normal_measures_ratio = master_normal_measures_ratio
        self.master_weak_measures_ratio = master_weak_measures_ratio
        self.master_garbage_measures_ratio = master_garbage_measures_ratio

        self.master_strong_bindings_ratio = master_strong_bindings_ratio
        self.master_normal_bindings_ratio = master_normal_bindings_ratio
        self.master_weak_bindings_ratio = master_weak_bindings_ratio
        self.master_garbage_bindings_ratio = master_garbage_bindings_ratio



    def add_rating(self,song):
        self.add_measures_patterns_rating(song)



    def add_measures_patterns_rating(self, song):
        self.create_measure_list(song)
        self.bind_measures_rating(song)
        self.calculate_song_measures_scores(song)
        self.create_measure_rating(song)

        bindings_rating, measures_rating = self.create_pattern_ratings(song)


        song.rating.measures_rating = measures_rating * self.measures_rating_weight
        song.rating.bindings_rating = bindings_rating * self.bindings_rating_weight

    def get_list_rates(self, strong_objects, normal_objects, weak_objects, garbage):
        total_bindings = len(strong_objects) + len(normal_objects) + len(weak_objects) + len(garbage)

        strong_bindings = len(strong_objects) / total_bindings
        normal_bindings = len(normal_objects) / total_bindings
        weak_bindings = len(weak_objects) / total_bindings
        garbage_bindings = len(garbage) / total_bindings

        return strong_bindings, normal_bindings, weak_bindings, garbage_bindings




    def create_pattern_ratings(self, song):
        strong_objects, normal_objects, weak_objects, garbage =  self.get_pattern_lists(song)
        strong_bindings, normal_bindings, weak_bindings, garbage_bindings = self.get_list_rates(strong_objects, normal_objects, weak_objects, garbage)


        strong_objects = list(dict.fromkeys(strong_objects))
        normal_objects = list(dict.fromkeys(normal_objects))
        normal_objects = [x for x in normal_objects if x not in strong_objects]

        weak_objects = list(dict.fromkeys(weak_objects))
        weak_objects = [x for x in weak_objects if x not in strong_objects]
        weak_objects = [x for x in weak_objects if x not in normal_objects]

        garbage = list(dict.fromkeys(garbage))
        garbage = [x for x in garbage if x not in strong_objects]
        garbage = [x for x in garbage if x not in normal_objects]
        garbage = [x for x in garbage if x not in weak_objects]

        strong_measures, normal_measures, weak_measures, garbage_measures = self.get_list_rates(strong_objects, normal_objects, weak_objects, garbage)


        strong_bindings_rating = self.calculate_difference(strong_bindings, self.master_strong_bindings_ratio)
        normal_bindings_rating = self.calculate_difference(normal_bindings, self.master_normal_bindings_ratio)
        weak_bindings_rating = self.calculate_difference(weak_bindings, self.master_weak_bindings_ratio)
        garbage_bindings_rating = self.calculate_difference(garbage_bindings, self.master_garbage_bindings_ratio)

        bindings_rating = strong_bindings_rating + normal_bindings_rating + weak_bindings_rating + garbage_bindings_rating
        bindings_rating /= 4

        strong_measures_rating = self.calculate_difference(strong_measures, self.master_strong_measures_ratio)
        normal_measures_rating = self.calculate_difference(normal_measures, self.master_normal_measures_ratio)
        weak_measures_rating = self.calculate_difference(weak_measures, self.master_weak_measures_ratio)
        garbage_measures_rating = self.calculate_difference(garbage_measures, self.master_garbage_measures_ratio)

        measures_rating = strong_measures_rating + normal_measures_rating + weak_measures_rating + garbage_measures_rating
        measures_rating /= 4

        """
        print("  - strong_bindings: "+ str(strong_bindings))
        print("  - normal_bindings: "+ str(normal_bindings))
        print("  - weak_bindings: "+ str(weak_bindings))
        print("  - garbage_bindings: "+ str(garbage_bindings))
        print()

        print("  - strong_measures: "+ str(strong_measures))
        print("  - normal_measures: "+ str(normal_measures))
        print("  - weak_measures: "+ str(weak_measures))
        print("  - garbage_measures: "+ str(garbage_measures))
        """

        return bindings_rating, measures_rating




    def get_pattern_lists(self, song):

        done_objects = []

        strong_objects = []
        normal_objects = []
        weak_objects = []
        garbage = []

        ratio = 0.15
        strong_threshold = 80
        normal_threshold = 70
        weak_threshold = 55


        for measure_object in song.measure_list:
            for key, value in measure_object.reference_list.items():
                if key not in done_objects:
                    weight = (value["combined"] + value["semitones"]) / 2

                    strongs = self.calculate_over_threshold(strong_threshold,value)
                    normals = self.calculate_over_threshold(normal_threshold,value)
                    weaks = self.calculate_over_threshold(weak_threshold,value)


                    if strongs >= 3 and weight >= strong_threshold:
                        strong_objects.append(measure_object.number())
                        strong_objects.append(key.number())

                    elif normals >= 3 and weight >= normal_threshold:
                        normal_objects.append(measure_object.number())
                        normal_objects.append(key.number())

                    elif weaks >= 3 and weight >= weak_threshold:
                        weak_objects.append(measure_object.number())
                        weak_objects.append(key.number())

                    else:
                        garbage.append(measure_object.number())
                        garbage.append(key.number())

            done_objects.append(measure_object)

        return  strong_objects, normal_objects, weak_objects, garbage


    def calculate_over_threshold(self, threshold, value):
        strongs = math.floor(value["pitches"] / threshold)
        strongs += math.floor(value["types"] / threshold)
        strongs += math.floor(value["durations"] / threshold + 5)
        strongs += math.floor(value["offsets"] / threshold + 5)
        strongs += math.floor(value["semitones"] / threshold)
        return strongs


    def create_measure_rating(self,song):
        average_pattern_scores = self.calculate_pattern_scores(song)
        song.pattern_average = average_pattern_scores





    #region PATTERN_DEFINING

    def calculate_pattern_scores(self, song):
        types = []
        pitches = []
        durations = []
        offsets = []
        combined = []
        semitones = []

        for measure in song.measure_list:
            types.append(measure.average_reference_scores["types"])
            pitches.append(measure.average_reference_scores["pitches"])
            durations.append(measure.average_reference_scores["durations"])
            offsets.append(measure.average_reference_scores["offsets"])
            combined.append(measure.average_reference_scores["combined"])
            semitones.append(measure.average_reference_scores["semitones"])

        average_pattern_scores = {
            "combined": np.mean(combined),
            "pitches": np.mean(pitches),
            "durations": np.mean(durations),
            "offsets": np.mean(offsets),
            "types": np.mean(types),
            "semitones": np.mean(semitones)
        }

        return average_pattern_scores


    def create_measure_list(self,song):
        measure_stream = song.get_measures()
        measure_list = []

        for measure in measure_stream:
            measure_object = Measure(measure)
            measure_list.append(measure_object)
            self.create_string_dict(measure_object)
            self.add_dict_to_song(song,measure_object)
        song.measure_list = measure_list


    def add_dict_to_song(self,song,measure_object):
        song.string_dict['types'].extend(measure_object.string_dict["types"])
        song.string_dict['pitches'].extend(measure_object.string_dict["pitches"])
        song.string_dict['durations'].extend(measure_object.string_dict["durations"])
        song.string_dict['offsets'].extend(measure_object.string_dict["offsets"])
        song.string_dict['semitones'].extend(measure_object.string_dict["semitones"])
        song.string_dict['combined'].extend(measure_object.string_dict["combined"])


    def bind_measures_rating(self,song):
        index = 0
        for measure_A in song.measure_list[:-1]:
            for measure_B in song.measure_list[index+1:]:
                self.rate_measure(measure_A, measure_B)
            index +=1

    def rate_measure(self,measure_A,measure_B):
        ratio = self.compare_ratings(measure_A.string_dict, measure_B.string_dict)
        measure_A.add_reference(measure_B,ratio)
        measure_B.add_reference(measure_A,ratio)


    def create_string_dict(self, measure):
        types = []
        pitches = []
        durations = []
        offsets = []

        for element in measure.measure.elements:
            try:
                if element.isNote:
                    types.append("N")
                    pitches.append(element.nameWithOctave)

                elif element.isChord:
                    types.append('X')
                    string =""
                    for pitch in element.pitches:
                        string += pitch.nameWithOctave
                    pitches.append(string)

                elif element.isRest:
                    types.append("R")
                    pitches.append("")
                offsets.append(element.offset)
                durations.append(element.duration.type)
            except:
                pass


        intervals_list = measure.measure.melodicIntervals(skipRests=True, skipOctaves=False,getOverlaps=True).elements
        semitones = []
        for interval in intervals_list:
            semitones.append(interval.semitones)




        measure.string_dict = {
            "types" : types,
            "pitches" : pitches,
            "durations" : durations,
            "offsets" : offsets,
            "semitones" : semitones
        }

        mergedA = [
            measure.string_dict["types"][i] + str(measure.string_dict["pitches"][i]) + str(measure.string_dict["durations"][i][0]) + str(
                measure.string_dict["offsets"][i]) for i in range(0, len(measure.string_dict["offsets"]), 1)]

        measure.string_dict["combined"] = mergedA



    def compare_ratings(self,string_dict_A,string_dict_B):

        try:
            #mergedA = [string_dict_A["types"][i] + str(string_dict_A["pitches"][i]) + str(string_dict_A["durations"][i][0]) + str(string_dict_A["offsets"][i]) for i in range(0, len(string_dict_A["offsets"]), 1)]
            #mergedB = [string_dict_B["types"][i] + str(string_dict_B["pitches"][i]) + str(string_dict_B["durations"][i][0]) + str(string_dict_B["offsets"][i]) for i in range(0, len(string_dict_B["offsets"]), 1)]
            ratio = {
                "combined": fuzz.ratio(string_dict_A["combined"], string_dict_B["combined"]),
                "types" : fuzz.ratio(string_dict_A["types"], string_dict_B["types"]),
                "pitches" : fuzz.ratio(string_dict_A["pitches"], string_dict_B["pitches"]),
                "durations" : fuzz.ratio(string_dict_A["durations"], string_dict_B["durations"]),
                "offsets" : fuzz.ratio(string_dict_A["offsets"], string_dict_B["offsets"]),
                "semitones" : fuzz.ratio(string_dict_A["semitones"], string_dict_B["semitones"])

            }
            return ratio
        except Exception as e:
            print(e.with_traceback())
            return None






    def calculate_song_measures_scores(self, song):
        for measure in song.measure_list:
            self.calculate_measure_scores(measure)


    def calculate_measure_scores(self,measure):
        types = []
        pitches = []
        durations = []
        offsets = []
        combined =[]
        semitones =[]

        for key, value in measure.reference_list.items():
            types.append(value["types"])
            pitches.append(value["pitches"])
            durations.append(value["durations"])
            offsets.append(value["offsets"])
            combined.append(value["combined"])
            semitones.append(value["semitones"])

        measure.average_reference_scores = {
            "combined": np.mean(combined),
            "pitches": np.mean(pitches),
            "durations": np.mean(durations),
            "offsets": np.mean(offsets),
            "types": np.mean(types),
            "semitones": np.mean(semitones)
        }


    #endregion











