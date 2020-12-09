from GeneticAlgorithm.Rating.SubRaters.AbstractSubRater import *
from math import log
from scipy.stats import wasserstein_distance
from collections import Counter
from itertools import repeat, chain


class ZipfianRaterStrategy(AbstractSubRater):

    def __init__(self,zipfs_law_distance_pitches_weight = 10,zipfs_law_distance_intervals_weight = 10,
                 zipfs_law_distance_pitches = 0, zipfs_law_distance_intervals = 0):

        self.zipfs_law_distance_pitches_weight = zipfs_law_distance_pitches_weight
        self.zipfs_law_distance_intervals_weight = zipfs_law_distance_intervals_weight
        self.zipfs_law_distance_pitches = zipfs_law_distance_pitches
        self.zipfs_law_distance_intervals = zipfs_law_distance_intervals

    def add_rating(self,song):
        self.add_intervals_zipfs_law_rating(song.semitones, song.rating)
        self.add_pitches_zipfs_law_rating(song, song.rating)


    def add_intervals_zipfs_law_rating(self, semitones, rating):
        zipfs_law_distance_intervals = self.calc_zipfs_law_distance(semitones)
        rating.zipfs_law_distance_intervals = self.calculate_difference(
            zipfs_law_distance_intervals,self.zipfs_law_distance_intervals) * self.zipfs_law_distance_intervals_weight

    def add_pitches_zipfs_law_rating(self, song, rating):
        zipfs_law_distance_pitches = self.calc_zipfs_law_distance_pitches(song=song)
        rating.zipfs_law_distance_pitches = self.calculate_difference(
            zipfs_law_distance_pitches, self.zipfs_law_distance_pitches) * self.zipfs_law_distance_pitches_weight




    def calc_zipfs_law_distance(self, dist_list):
        tes = list(chain.from_iterable(repeat(i, c) for i, c in Counter(dist_list).most_common()))
        uniques_sorted = list(dict.fromkeys(tes))

        zipfs_distr = self.create_zipfs_distr(len(dist_list), uniques_sorted)
        distance = abs(wasserstein_distance(dist_list, zipfs_distr))

        equal_distr = self.create_equal_distr(len(dist_list), uniques_sorted)
        max_distance = abs(wasserstein_distance(dist_list, equal_distr))

        return abs(distance / max_distance)

    def create_equal_distr(self, size, uniques):
        list = []
        length = round(size / len(uniques))
        for element in uniques:
            list.extend([element] * length)

        return list

    def Harmonic(self, n):
        gamma = 0.57721566490153286060651209008240243104215933593992
        return gamma + log(n) + 0.5 / n - 1. / (12 * n ** 2) + 1. / (120 * n ** 4)

    def create_zipfs_distr(self, size, unique_sorted):
        list = []
        H = self.Harmonic(len(unique_sorted))
        rate = size / H
        for n in range(len(unique_sorted)):
            rank = 1 / (n + 1)
            count = round(rank * rate)
            element = [unique_sorted[n]]
            list.extend(element * count)
        return list


    def calc_zipfs_law_distance_pitches(self, song):
        pitches = song.raw_stream.pitches
        pitchfreq = []

        for pitch in pitches:
            pitchfreq.append(pitch.frequency)

        return self.calc_zipfs_law_distance(pitchfreq)




