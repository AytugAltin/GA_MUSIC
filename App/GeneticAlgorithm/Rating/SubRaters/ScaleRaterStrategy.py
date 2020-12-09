from GeneticAlgorithm.Rating.SubRaters.AbstractSubRater import *


class ScaleRaterStrategy(AbstractSubRater):

    def __init__(self,scale_correctness_weight = SCALE_CORRECTNESS_WEIGHT,
                 scale_correctness_rating = SCALE_CORRECTNESS_RATING):
        self.scale_correctness_weight = scale_correctness_weight
        self.scale_correctness_rating = scale_correctness_rating

    def add_rating(self,song):
        song.rating.scale_correctness_rating = self.get_scale_rating(song)


    def get_scale_rating(self, song):
        song_scale_correctness_rate = self.analyze_scale(song=song)
        return self.calculate_difference(song_scale_correctness_rate,self.scale_correctness_rating) * self.scale_correctness_weight

    def analyze_scale(self, song):
        scale = song.get_scale()
        result_tuple = scale.match(song.get_raw_stream())
        matchlen = len(result_tuple["matched"])
        notmatchlen = len(result_tuple["notMatched"])
        not_matched = result_tuple["notMatched"]

        scale_rating = notmatchlen / (notmatchlen + matchlen)

        wrong = 0
        total = 0

        for note in song.notes:
            if note.isNote:
                if contains(not_matched, lambda x: x.name == note.pitch.name):
                    wrong += 1
                total += 1
            if note.isChord:
                if contains(not_matched, lambda x: x.name == note.root().name):
                    wrong += 1
                total += 1

        scale_rating = wrong / total
        return scale_rating
