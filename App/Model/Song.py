from music21 import *
import numpy as np
from Model.Rating import Rating
from Constants import *

class Song:

    def __init__(self, raw_stream = None, generation = 0,measure_length = NUMBER_OF_MEASURES ):
        self.raw_stream =  raw_stream
        self.notes = []
        self.generation = generation
        self.rating = Rating()
        self.scale = None
        self.key = None
        self.semitones = []
        self.intervals = None
        self.measure_list = []
        self.pattern_average = None
        self.measure_length = measure_length

        self.string_dict = {
            "types": [],
            "pitches": [],
            "durations": [],
            "offsets": [],
            "semitones": [],
            "combined": []
        }

        try:
            self.analyze_deep()
        except Exception as e:
            print("Error analyzing song" , str(e))
            pass

    def get_scale(self):
        return self.scale

    def analyze(self):
        self.analyze_notes()
        self.key = self.raw_stream.analyze("key")
        self.scale = self.key.getScale(self.key.mode)

    def analyze_deep(self):
        self.notes = []
        for element in self.raw_stream.recurse():
            try:
                if element.isNote or element.isChord or element.isRest:
                    self.notes.append(element)
            except:
                pass


        self.raw_stream = stream.Stream()

        for note in self.notes:
            self.raw_stream.insert(note.offset,note)

        #self.raw_stream.makeRests(fillGaps=True, inPlace=True)


        self.notes = []

        for element in self.raw_stream.recurse():
            try:
                if element.isNote or element.isChord or element.isRest:
                    self.notes.append(element)
            except:
                pass





        self.key = self.raw_stream.analyze("key")
        self.scale = self.key.getScale(self.key.mode)

    def get_measures(self):
        measure_list = self.raw_stream.makeMeasures()
        size = len(measure_list)
        measure_list.makeTies(inPlace=True)
        size2 = len(measure_list)
        if size is not size2:
            print("EEEEEEEEEEEEEEEEERRRRRRRRRRRRRRRRRROOOOOOOOOOOOOOOOOORRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRR +++++++++++++++++++++++++++++++++++++")
            print("EEEEEEEEEEEEEEEEERRRRRRRRRRRRRRRRRROOOOOOOOOOOOOOOOOORRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRR +++++++++++++++++++++++++++++++++++++")
            print("EEEEEEEEEEEEEEEEERRRRRRRRRRRRRRRRRROOOOOOOOOOOOOOOOOORRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRR +++++++++++++++++++++++++++++++++++++")
            print("EEEEEEEEEEEEEEEEERRRRRRRRRRRRRRRRRROOOOOOOOOOOOOOOOOORRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRR +++++++++++++++++++++++++++++++++++++")
            print("EEEEEEEEEEEEEEEEERRRRRRRRRRRRRRRRRROOOOOOOOOOOOOOOOOORRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRR +++++++++++++++++++++++++++++++++++++")
            print("EEEEEEEEEEEEEEEEERRRRRRRRRRRRRRRRRROOOOOOOOOOOOOOOOOORRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRR +++++++++++++++++++++++++++++++++++++")
        measures = list(measure_list.elements[:self.measure_length])
        return measure_list

    def analyze_notes_reversed(self):
        self.raw_stream = stream.Stream(self.notes)
        self.raw_stream.makeRests(fillGaps=True, inPlace=True)
        self.analyze_deep()

    def analyze_notes(self):
        self.notes = []
        self.raw_stream.makeRests(fillGaps=True, inPlace=True)
        for element in self.raw_stream.recurse():
            if not element.isStream:
                self.notes.append(element)


    def reform_stream(self):
        self.raw_stream = stream.Stream(self.notes)
        self.analyze()



    def play(self):
        self.raw_stream.show("midi")

    def show(self):
        self.raw_stream.show("lily")



    def get_notes(self):
        return self.notes

    def get_cross_list(self):
        return self.cross_list

    def get_raw_stream(self):
        return self.raw_stream

    def set_rating(self,rating):
        self.rating = rating













