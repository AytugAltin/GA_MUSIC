from Model.Rating import Rating
from GeneticAlgorithm.Rating.SubRaters.ScaleRaterStrategy import ScaleRaterStrategy
from GeneticAlgorithm.Rating.SubRaters.IntervalRaterStrategy import IntervalRaterStrategy
from GeneticAlgorithm.Rating.SubRaters.ZipfianRaterStrategy import ZipfianRaterStrategy
from GeneticAlgorithm.Rating.SubRaters.RepetitionRaterStrategy import RepetitionRaterStrategy

class RatingStrategy:


    def __init__(self ):

        # ---------------------------- WEIGHTS ----------------------------

        # 1. SCALE
        self.scale_rater_strategy = self.create_scale_rater_strategy()

        # 2. BASED ON INTERVALS
        self.interval_rater_strategy = self.create_interval_rater_strategy()


        # 3. Zipf's Law
        self.zipfian_rater_strategy = self.create_zipfian_rater_strategy()

        self.repetition_rater_strategy = self.create_repetition_rater_strategy()

    def create_scale_rater_strategy(self):
        return ScaleRaterStrategy()


    def create_interval_rater_strategy(self):
        return IntervalRaterStrategy()

    def create_zipfian_rater_strategy(self):
        return ZipfianRaterStrategy()

    def create_repetition_rater_strategy(self):
        return RepetitionRaterStrategy()

    def rate_population(self, population):
        # TODO with threads
        for child in population:
            self.rate_song(child)


        return population


    def rate_song(self,song):

        #   1. SCALE RATING
        self.scale_rater_strategy.add_rating(song)

        #   2. INTERVAL BASED
        self.interval_rater_strategy.add_rating(song)

        #   3. ZIPFS LAW RATING
        self.zipfian_rater_strategy.add_rating(song)

        #   4. Repetition RATING
        self.repetition_rater_strategy.add_rating(song)


        song.rating.calculate_rating()










