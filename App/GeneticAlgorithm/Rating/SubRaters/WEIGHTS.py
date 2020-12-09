
#region IntervalRaterStrategy
#WEIGHTS
NEIGHBORING_PITCH_WEIGHT = 5
MELODY_DIRECTION_WEIGHT = 1
DIRECTION_STABILITY_WEIGHT = 1
UNIQUE_PITCHES_WEIGHT = 1
#DEFAULTS
MAX_INTERVAL_SIZE = 20
MIN_INTERVAL_SIZE = -20
MELODY_DIRECTION = 0.5
DIRECTION_STABILITY = 0.5
UNIQUE_PITCHES_RATE = 0.5
#endregion


#region RepetitionRaterStrategy
#WEIGHTS
MEASURES_RATING_WEIGHT = 15
BINDINGS_RATING_WEIGHT = 15
#DEFAULTS
MASTER_STRONG_MEASURES_RATIO=0.5
MASTER_NORMAL_MEASURES_RATIO=0.3
MASTER_WEAK_MEASURES_RATIO=0.2
MASTER_GARBAGE_MEASURES_RATIO=0.2
MASTER_STRONG_BINDINGS_RATIO=0.5
MASTER_NORMAL_BINDINGS_RATIO=0.3
MASTER_WEAK_BINDINGS_RATIO=0.2
MASTER_GARBAGE_BINDINGS_RATIO=0.2
#endregion

#region SampleBasedMeasureRaterStrategy
#WEIGHTS
TYPES_DISTANCE_RATING_WEIGHT = 15
SEMITONES_DISTANCE_RATING_WEIGHT = 15
PITCHES_DISTANCE_RATING_WEIGHT = 15
DURATION_DISTANCE_RATING_WEIGHT = 15
OFFSETS_DISTANCE_RATING_WEIGHT = 15
#endregion

#region MusicalRater
#WEIGHTS
SCALE_CORRECTNESS_WEIGHT = 2
ZIPFS_LAW_DISTANCE_PITCHES_WEIGHT = 0
ZIPFS_LAW_DISTANCE_INTERVALS_WEIGHT = 0
#DEFAULTS
SCALE_CORRECTNESS_RATING = 0
ZIPFS_LAW_DISTANCE_PITCHES = 0
ZIPFS_LAW_DISTANCE_INTERVALS = 0
#endregion

#region SampleBasedMeasureRaterStrategy
#WEIGHTS
ABSOLUTE_RHYTHM_WEIGHT = 20
ABSOLUTE_TYPES_WEIGHT = 20
INTERVAL_DISTR_DISTNCE_RATING_WEIGHT = 15
TYPES_DISTR_RATING_WEIGHT = 7
ELEMENT_COUNT_WEIGHT = 5
#DEFAULTS
#endregion

