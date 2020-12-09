from GeneticAlgorithm.Rating.RatingStrategy import RatingStrategy
from GeneticAlgorithm.Rating.SubRaters.SampleBasedMeasureRaterStrategy import SampleBasedMeasureRaterStrategy
from GeneticAlgorithm.Rating.SubRaters.SampleBasedAbsoluteRaterStrategy import SampleBasedAbsoluteRaterStrategy

class SampleBasedRatingStrategy(RatingStrategy):


    def __init__(self, master_song ):
        RatingStrategy.__init__(self)

        self.master_semitones = []
        self.master_song = master_song
        self.analyze_master()
        self.sample_based_repetition_rater_strategy =  self.create_master_repetition_rater_strategy()
        self.sample_based_absolute_rater_strategy =  self.create_master_absolute_rater_strategy()

    def create_master_repetition_rater_strategy(self):
        return SampleBasedMeasureRaterStrategy(self.master_song)

    def create_master_absolute_rater_strategy(self):
        return SampleBasedAbsoluteRaterStrategy(self.master_song)

    def rate_song(self,song):

        #   1. SCALE RATING
        self.scale_rater_strategy.add_rating(song)

        #   2. INTERVAL BASED
        self.interval_rater_strategy.add_rating(song)

        #   3. ZIPFS LAW RATING
        self.zipfian_rater_strategy.add_rating(song)

        #   4. repetition LAW RATING
        self.repetition_rater_strategy.add_rating(song)

        #   5. master repetition LAW RATING
        self.sample_based_repetition_rater_strategy.add_rating(song)

        #   6. master repetition LAW RATING
        self.sample_based_absolute_rater_strategy.add_rating(song)




        song.rating.calculate_rating()


    def analyze_master(self):
        self.scale_rater_strategy.scale_correctness_rating = self.scale_rater_strategy.analyze_scale(self.master_song)

        self.set_repetition_values()

        self.set_master_interval_properties(self.master_song)
        self.zipfian_rater_strategy.zipfs_law_distance_pitches = self.zipfian_rater_strategy.calc_zipfs_law_distance_pitches(self.master_song)


    # This function analyzes the masters intervals and extracts boundaries
    # that is going to be used for rating other songs
    def set_master_interval_properties(self,song):

        interval_stream = song.raw_stream.melodicIntervals(skipRests=True, skipOctaves=False,getOverlaps=True)
        semitones_list = []

        upwards_intervals = 0
        previous = None
        direction_changes = 0

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
            except:
                pass


        self.interval_rater_strategy.melody_direction = upwards_intervals / len(semitones_list)
        self.interval_rater_strategy.direction_stability = direction_changes / len(semitones_list)

        self.interval_rater_strategy.max_interval_size = max(semitones_list)
        self.interval_rater_strategy.min_interval_size = min(semitones_list)


        nr_unique_semitones = len(set(semitones_list))

        self.interval_rater_strategy.unique_pitches = nr_unique_semitones / len(semitones_list)

        self.interval_rater_strategy.master_semitones = semitones_list
        self.zipfian_rater_strategy.zipfs_law_distance_intervals = self.zipfian_rater_strategy.calc_zipfs_law_distance(semitones_list)
        song.semitones = semitones_list


        nr_unique_semitones = len(set(song.raw_stream.pitches))
        self.interval_rater_strategy.unique_pitches_rate = nr_unique_semitones / len(song.raw_stream.pitches)

        print("MASTER SONG DATA-------------")
        print(" - max_interval_size: " + str(self.interval_rater_strategy.max_interval_size))
        print(" - min_interval_size: " + str(self.interval_rater_strategy.min_interval_size))
        print(" - melody_direction: " + str(self.interval_rater_strategy.melody_direction))
        print(" - direction_stability: " + str(self.interval_rater_strategy.direction_stability))
        print(" - zipfs_law_distance_intervals: " + str(self.zipfian_rater_strategy.zipfs_law_distance_intervals))
        print("-----------------------------")


    def set_repetition_values(self):
        self.repetition_rater_strategy.create_measure_list(self.master_song)
        self.repetition_rater_strategy.bind_measures_rating(self.master_song)
        self.repetition_rater_strategy.calculate_song_measures_scores(self.master_song)

        strong_objects, normal_objects, weak_objects, garbage = self.repetition_rater_strategy.get_pattern_lists(
            self.master_song)

        strong_bindings, normal_bindings, weak_bindings, garbage_bindings = self.repetition_rater_strategy.get_list_rates(
            strong_objects,
            normal_objects,
            weak_objects,
            garbage)

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

        strong_measures, normal_measures, weak_measures, garbage_measures = self.repetition_rater_strategy.get_list_rates(
            strong_objects,normal_objects,
            weak_objects,garbage)

        self.repetition_rater_strategy.master_strong_measures_ratio = strong_measures
        self.repetition_rater_strategy.master_normal_measures_ratio = normal_measures
        self.repetition_rater_strategy.master_weak_measures_ratio = weak_measures
        self.repetition_rater_strategy.master_garbage_measures_ratio = garbage_measures

        self.repetition_rater_strategy.master_strong_bindings_ratio = strong_bindings
        self.repetition_rater_strategy.master_normal_bindings_ratio = normal_bindings
        self.repetition_rater_strategy.master_weak_bindings_ratio = weak_bindings
        self.repetition_rater_strategy.master_garbage_bindings_ratio = garbage_bindings

        print(
            "  - strong_bindings: " + str(strong_bindings)+
            "  - normal_bindings: " + str(normal_bindings)+
            "  - weak_bindings: " + str(weak_bindings) +
            "  - garbage_bindings: " + str(garbage_bindings)
              )

        print(
            "  - strong_measures: " + str(strong_measures)+
            "  - normal_measures: " + str(normal_measures)+
            "  - weak_measures: " + str(weak_measures)+
            "  - garbage_measures: " + str(garbage_measures)
              )











