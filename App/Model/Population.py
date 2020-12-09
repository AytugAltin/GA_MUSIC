class Population:

    def __init__(self, list = None, generation = 0):
        self.list = list
        self.generation = generation

    def get_generation(self):
        return self.generation

    def get_list(self):
        return self.list

    def set_list(self, parents):
        self.list = parents

    def get_generation(self):
        return self.generation

    def play_last_gen(self):
        for song in self.list:
            song.play()

    def display_last_gen(self):
        for song in self.list:
            song.print_info()








