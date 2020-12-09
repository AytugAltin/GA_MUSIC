from GeneticAlgorithm.Rating.SubRaters.WEIGHTS import *

class AbstractSubRater():

    def __init__(self):
        pass

    def add_rating(self,song):
        pass

    def calculate_difference(self, song_rate, master_rate):
        return abs(master_rate - song_rate)






def contains(list, filter):
    for x in list:
        if filter(x):
            return True
    return False


