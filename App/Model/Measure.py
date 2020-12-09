from music21 import *
import numpy as np

class Measure:

    def __init__(self, measure):
        self.measure = measure
        self.reference_list = {}
        self.average_reference_scores = None
        self.string_dict = None
        self.absolute_distance_from_master = {
            "types": 0,
            "pitches": 0,
            "durations": 0,
            "offsets": 0,
            "semitones": 0
        }

    def add_reference(self, measure, fuzz_ratio):
        self.reference_list[measure] = fuzz_ratio

    def number(self):
        return self.measure.measureNumber

    def play(self):
        self.measure.show("midi")

    def get_absolute_rating(self):
        total = self.absolute_distance_from_master["types"] +\
                self.absolute_distance_from_master["pitches"] +\
                self.absolute_distance_from_master["durations"] +\
                self.absolute_distance_from_master["offsets"] +\
                self.absolute_distance_from_master["semitones"]
        return total




