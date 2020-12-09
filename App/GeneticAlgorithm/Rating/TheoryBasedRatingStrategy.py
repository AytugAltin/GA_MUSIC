from GeneticAlgorithm.Rating.RatingStrategy import *

class TheoryBasedRatingStrategy(RatingStrategy):


    def __init__(self):
        RatingStrategy.__init__(self)





    def create_scale_rater_strategy(self):
        return ScaleRaterStrategy(
                scale_correctness_weight = 2,
                scale_correctness_rating = 0
            )


    def create_interval_rater_strategy(self):
        return IntervalRaterStrategy(
            neighboring_pitch_weight=10,
            melody_direction_weight=1,
            direction_stability_weight=1,
            unique_pitches_weight=1,
            max_interval_size=20,
            min_interval_size=-20,
            melody_direction=0.5,
            direction_stability=0.5,
            unique_pitches_rate=0.5
        )

    def create_zipfian_rater_strategy(self):
        return ZipfianRaterStrategy(
            zipfs_law_distance_pitches_weight=10,
            zipfs_law_distance_intervals_weight=10,
            zipfs_law_distance_pitches=0,
            zipfs_law_distance_intervals=0
        )

    def create_repetition_rater_strategy(self):
        return RepetitionRaterStrategy(measures_rating_weight = 10, bindings_rating_weight = 10,
                                        master_strong_measures_ratio=0.35,
                                       master_normal_measures_ratio=0.50, master_weak_measures_ratio=0.10,
                                       master_garbage_measures_ratio=0.05, master_strong_bindings_ratio=0.15,
                                       master_normal_bindings_ratio=0.25, master_weak_bindings_ratio=0.4,
                                       master_garbage_bindings_ratio=0.2)







