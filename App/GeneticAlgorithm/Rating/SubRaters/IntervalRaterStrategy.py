from GeneticAlgorithm.Rating.SubRaters.AbstractSubRater import *

import time


class IntervalRaterStrategy(AbstractSubRater):

    def __init__(self,neighboring_pitch_weight = NEIGHBORING_PITCH_WEIGHT,
                 melody_direction_weight = MELODY_DIRECTION_WEIGHT,
                 direction_stability_weight = DIRECTION_STABILITY_WEIGHT ,
                 unique_pitches_weight = UNIQUE_PITCHES_RATE, max_interval_size = MAX_INTERVAL_SIZE,
                 min_interval_size = MIN_INTERVAL_SIZE, melody_direction = MELODY_DIRECTION,
                 direction_stability = DIRECTION_STABILITY, unique_pitches_rate = UNIQUE_PITCHES_RATE):

        self.neighboring_pitch_weight = neighboring_pitch_weight
        self.melody_direction_weight = melody_direction_weight
        self.direction_stability_weight = direction_stability_weight
        self.unique_pitches_weight = unique_pitches_weight
        self.max_interval_size = max_interval_size
        self.min_interval_size = min_interval_size
        self.melody_direction = melody_direction
        self.direction_stability = direction_stability
        self.unique_pitches_rate = unique_pitches_rate

    def add_rating(self,song):
        self.add_interval_ratings(song)

    def add_interval_ratings(self, song):
        rating = song.rating
        neighbour_pitch_rating, melody_direction_rating, direction_stability_rating, unique_pitches_rating, semitones_list \
            = self.analyze_intervals(song=song)

        rating.neighbour_pitch_rating = neighbour_pitch_rating * self.neighboring_pitch_weight
        rating.melody_direction_rating = melody_direction_rating * self.melody_direction_weight
        rating.direction_stability_rating = direction_stability_rating * self.direction_stability_weight
        rating.unique_pitches_rating = unique_pitches_rating * self.unique_pitches_weight


    def analyze_intervals(self, song):

        interval_stream = song.raw_stream.melodicIntervals(skipRests=True, skipOctaves=False,getOverlaps=True)
        wrong_intervals = 0
        semitones_list = []

        direction_changes  = 0
        upwards_intervals = 0
        previous = None

        for interval in interval_stream.recurse():
            try:
                previous = interval.semitones
                break
            except:
                pass

        for interval in interval_stream.recurse():
            try:
                semitone = interval.semitones
                if semitone > 0:
                    upwards_intervals +=1
                if (previous>0) == (semitone>0):
                    direction_changes +=1
                semitones_list.append(semitone)

                if (semitone > self.max_interval_size or semitone < self.min_interval_size) and semitone is not 0:
                    wrong_intervals +=1
            except:
                pass


        #MELODY -----------------------------------------
        melody_direction = upwards_intervals / len(semitones_list)
        melody_direction_rating = abs(self.melody_direction - melody_direction)

        direction_stability = direction_changes / len(semitones_list)
        direction_stability_rating = abs(self.direction_stability - direction_stability)

        nr_unique_semitones = len(set(song.raw_stream.pitches))
        unique_pitches_rate = nr_unique_semitones / len(song.raw_stream.pitches)
        unique_pitches_rating = abs(self.unique_pitches_rate - unique_pitches_rate)
        #-----------------------------------------

        neighbour_pitch_rating = wrong_intervals / len(semitones_list)

        song.semitones = semitones_list


        return neighbour_pitch_rating,melody_direction_rating,direction_stability_rating, unique_pitches_rating,semitones_list




