class Rating:

    def __init__(self):
        self.total_rating = 0

        self.scale_correctness_rating = 0
        self.zipfs_law_distance_pitches = 0
        self.zipfs_law_distance_intervals = 0

        self.neighbour_pitch_rating = 0
        self.melody_direction_rating = 0
        self.direction_stability_rating = 0
        self.unique_pitches_rating = 0

        self.bindings_rating = 0
        self.measures_rating = 0

        #advanced relative ratings of sample
        self.types_distance_rating = 0
        self.semitones_distance_rating = 0
        self.pitches_distance_rating = 0
        self.duration_distance_rating = 0
        self.offsets_distance_rating = 0


        #advanced ABSOLUTE ratings of sample
        self.absolute_rhythm_rating = 0
        self.absolute_types_rating = 0
        self.absolute_types_rating = 0
        self.types_distr_rating = 0






    def calculate_rating(self):
        self.total_rating = 0
        ratings = vars(self)
        for key, value in ratings.items():
            self.total_rating += value

    def print_rating(self):
        ratings = vars(self)
        for key, value in ratings.items():
            print("     "+str(key) + ": "+ str(value))






