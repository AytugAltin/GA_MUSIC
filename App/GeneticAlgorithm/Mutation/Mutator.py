from Model.Song import Song
from Model.Outsider import Outsider
from music21 import *
import random
import copy

from Constants import *

class Mutator:

    def __init__(self,rating_strategy, probability = 0.2):
        self.mutation_probability = probability # the higher the more mutations
        self.song_probability = 0.5 # the higher the more mutations
        self.rating_strategy = rating_strategy
        self.pitch_action_strength = 0.5
        self.increase_percentage = 0.15
        self.decrease_percentage = self.increase_percentage
        self.remutation_probability = 0.5
        self.difference = 0.05


        self.count_measure_swap = 0
        self.count_note_swap = 0
        self.count_neighbour_pitch_mutation = 0

        self.count_pitch_mutation = 0
        self.count_type_mutation = 0
        self.count_duration_mutation = 0
        self.count_measure_mix  = 0

    #region MUTATION
    def to_mutate_or_not(self,fittest):

        difference = abs(fittest[-1].rating.total_rating - fittest[0].rating.total_rating) /fittest[-1].rating.total_rating
        print(" *difference: " + str(difference) )


        if difference < self.difference:
            return True

        return False


    def increase_probability(self):
        self.mutation_probability = abs(self.mutation_probability  + ( (1 -self.mutation_probability ) * self.increase_percentage))
        self.remutation_probability =abs(self.remutation_probability   + ( (1 -self.remutation_probability ) * self.increase_percentage))


    def decrease_probability(self):
        self.mutation_probability = abs(self.mutation_probability  - ( (1 -self.mutation_probability ) * self.increase_percentage))
        self.remutation_probability = abs(self.remutation_probability   - ( (1 -self.remutation_probability ) * self.increase_percentage))



    def mutate_population(self, population):
        self.count_measure_swap = 0
        self.count_note_swap = 0
        self.count_neighbour_pitch_mutation = 0
        self.count_pitch_mutation = 0
        self.count_type_mutation = 0
        self.count_duration_mutation = 0
        self.count_measure_mix = 0

        print(" *mp: " + str(self.mutation_probability) + " *rmp: " + str(self.remutation_probability), end='  ')

        count_mutations = 0
        for song in population:
            choice = random.random()
            if choice < self.song_probability:
                count_mutations += 1
                self.mutate(song)


        print(' ' + str(count_mutations) +"/"+ str(len(population)) +" ", end='')


        print(' measr_swp: ' + str(self.count_measure_swap) +
              ' measr_mix: ' + str(self.count_measure_mix) +
              ' note_swp: ' + str(self.count_note_swap) +
              ' NP_mut: ' + str(self.count_neighbour_pitch_mutation) +
              ' pitch_mut: ' + str(self.count_pitch_mutation)+
              ' type_mut: ' + str(self.count_type_mutation)+
              ' duratn_mut: ' + str(self.count_duration_mutation)
              , end=' ')

        return population




    def mutate(self,song):


        choice = random.random()
        if choice < self.mutation_probability:
            self.pitch_mutation(song)


        choice = random.random()
        if choice < self.mutation_probability:
            self.swap_measure(song)


        choice = random.random()
        if choice < self.mutation_probability:
            self.mix_measure(song)

        choice = random.random()
        if choice < self.mutation_probability:
            self.replace_measure(song)


        choice = random.random()
        if choice < self.mutation_probability:
            self.swap_notes(song)

        
        choice = random.random()
        if choice < self.mutation_probability:
            self.mutate_type(song)


        choice = random.random()
        if choice < self.mutation_probability:
            self.mutate_duration(song)


        choice = random.random()
        if choice < self.mutation_probability:
            self.mutate_pitch(song)
            

        choice = random.random()
        if choice < self.remutation_probability:
            self.mutate(song)





    #endregion


    #region notes_mutation

    def mutate_type(self,song):
        size = len(song.notes) - 1
        index_note = random.randint(0, size)
        note = song.notes[index_note]
        copy_note = copy.deepcopy(note)

        index_note2 = random.randint(0, size)
        note2 = song.notes[index_note2]
        count = 0

        while note2.isRest == note.isRest and note2.isNote == note.isNote and note2.isChord == note.isChord and count < 15:
            index_note2 = random.randint(0, size)
            note2 = song.notes[index_note2]
            count += 1

        copy_note = copy.deepcopy(note2)
        copy_note.offset = note.offset
        copy_note.duration = note.duration
        song.notes[index_note] = copy_note
        song.analyze_notes_reversed()
        self.count_type_mutation += 1


    def mutate_duration(self,song):
        duration_types = ["eighth", "half", 'whole', '32nd', "16th"]
        size = len(song.notes) - 1
        index_note = random.randint(0, size)
        note = song.notes[index_note]

        type = random.choice(duration_types)

        d3 = duration.Duration(type=type)

        note.duration = d3

        song.analyze_notes_reversed()
        song.analyze()
        self.count_duration_mutation += 1


    def mutate_pitch(self,song):
        minimum = self.rating_strategy.interval_rater_strategy.min_interval_size
        maximum = self.rating_strategy.interval_rater_strategy.max_interval_size
        size = random.randint(minimum, maximum)
        aInterval = interval.Interval(size)

        size = len(song.notes) - 1

        index_note = random.randint(0, size)
        note = song.notes[index_note]

        while note.isRest:
            index_note = random.randint(0, size)
            note = song.notes[index_note]

        note.transpose(aInterval, inPlace=True)
        song.analyze_notes_reversed()
        song.analyze()


        self.count_pitch_mutation+= 1


    #endregion



    #region PITCH
    def choose_pitch_index(self,song):
        semitones = song.semitones
        rating_minimum = self.rating_strategy.interval_rater_strategy.min_interval_size
        rating_maximum = self.rating_strategy.interval_rater_strategy.max_interval_size


        filtered = list(filter(lambda x: x > rating_maximum or x < rating_minimum, semitones))

        value = random.choice(filtered)


        index = semitones.index(value)

        return index



    def pitch_mutation(self,song):
        try:
            index = self.choose_pitch_index(song)
            self.fix_interval_mistake(song,index)
            self.count_neighbour_pitch_mutation += 1
        except Exception as e:
            pass

    def fix_interval_mistake(self, song,index):

        interval_stream = song.raw_stream.melodicIntervals(skipRests=True, skipOctaves=False,getOverlaps=True)
        middle_interval = interval_stream.recurse()[index ]

        try:
            previous_interval = interval_stream.recurse()[index-1]
            previous_semitone = previous_interval.semitones
        except:
            previous_semitone = 0
        try:
            next_interval = interval_stream.recurse()[index + 1]
            next_semitone = next_interval.semitones
        except:
            next_semitone = 0

        next_sign = next_semitone > 0
        previous_sign = previous_semitone > 0


        middle_semitone = middle_interval.semitones
        middle_sign = middle_semitone > 0

        if abs(next_semitone) > abs( previous_semitone):
            if middle_sign is not next_sign:
                selected_note = middle_interval.noteEnd
            else:
                selected_note = middle_interval.noteStart

        else:
            if middle_sign is not previous_sign:
                selected_note = middle_interval.noteStart
            else:
                selected_note = middle_interval.noteEnd

        if selected_note == middle_interval.noteStart:
            sign_multiplier  = 1
        else:
            sign_multiplier  = -1

        selected_note = song.raw_stream.getElementById(selected_note.id)

        aInterval = interval.Interval(sign_multiplier * round(middle_semitone*self.pitch_action_strength))

        selected_note.transpose(aInterval,inPlace = True)
        self.correct_note(song.scale, selected_note)
        song.reform_stream()



    #endregion

    #region SCALE Correcting

    def scale_mutation(self,song):
        incorrect_notes = self.find_incorrect_notes(song.notes,song.scale)



    def find_incorrect_notes(self,notes,scale):
        incorrect_notes = []

        return incorrect_notes

    def correct_note(self, scale, object):

        if object.isNote:
            noteAName = object.nameWithOctave
        if object.isChord:
            noteAName = object.root().nameWithOctave

        noteA = note.Note(noteAName)
        pitch = random.choice(scale.pitches)
        name = pitch.name + str(noteA.octave)
        noteB = note.Note(name)
        ainterval = interval.Interval(noteStart=noteA, noteEnd=noteB)
        semitone = ainterval.semitones
        if abs(semitone) > 7:
            if semitone > 0:
                semitone -= 12
                temp = interval.Interval(-12)
            else:
                semitone += 12
                temp = interval.Interval(12)

            noteB.transpose(temp, inPlace=True)
            ainterval = interval.Interval(noteStart=noteA, noteEnd=noteB)

        object.transpose(value=interval.Interval(semitone), inPlace=True)

    #endregion

    #region MEASURE_SWAP

    def get_worst_measures_index(self,song):

        measure_stream = song.get_measures()
        size = len(measure_stream) - 1

        try:
            temp = song.measure_list
            temp.sort(key=lambda x: x.get_absolute_rating())
            index_a = temp[0].number() - 1
            if index_a == size - 1:
                index_a = random.randint(0, size)
        except:
            index_a = random.randint(0, size)

        index_b = random.randint(0, size)

        while index_b == index_a:
            index_b = random.randint(0, size)


        return index_a,index_b

    def swap_measure(self,song):
        measure_stream = song.get_measures()
        size = len(measure_stream)

        index_a, index_b = self.get_worst_measures_index(song)

        m_a = measure_stream[index_a]
        m_b = measure_stream[index_b]



        elements_a = m_a.elements
        elements_b = m_b.elements

        measure_stream_copy = copy.deepcopy(measure_stream)
        m_a = measure_stream_copy[index_a]
        m_b = measure_stream_copy[index_b]
        m_a.remove(m_a.elements)
        m_b.remove(m_b.elements)


        #m_b.append(elements_a)
        for element in elements_a:
            m_b.insert(element.offset,element)

        #m_a.append(elements_b)
        for element in elements_b:
            m_a.insert(element.offset,element)


        size2 = len(measure_stream_copy)
        if size == size2:
            measure_stream_copy.write(fmt="midi", fp="Midi/Temp/temp.mid")
            song.raw_stream  = converter.parse("Midi/Temp/temp.mid")
            song.analyze_deep()

            self.count_measure_swap += 1

    def replace_measure(self, song):
        measure_stream = song.get_measures()
        size = len(measure_stream)

        index_a, index_b = self.get_worst_measures_index(song)

        m_a = measure_stream[index_a]
        m_b = measure_stream[index_b]



        elements_b = m_b.elements

        measure_stream_copy = copy.deepcopy(measure_stream)
        m_a = measure_stream_copy[index_a]
        m_b = measure_stream_copy[index_b]
        m_a.remove(m_a.elements)

        for element in elements_b:
            m_a.insert(element.offset,element)

        choice = random.random()
        if choice < self.mutation_probability:
            m_a.chordify()

        size2 = len(measure_stream_copy)
        if size == size2:
            measure_stream_copy.write(fmt="midi", fp="Midi/Temp/temp.mid")
            song.raw_stream  = converter.parse("Midi/Temp/temp.mid")
            song.analyze_deep()

            self.count_measure_mix += 1

    def mix_measure(self, song):
        measure_stream = song.get_measures()
        size = len(measure_stream)

        index_a, index_b = self.get_worst_measures_index(song)

        m_a = measure_stream[index_a]
        m_b = measure_stream[index_b]



        elements_b = m_b.elements

        measure_stream_copy = copy.deepcopy(measure_stream)
        m_a = measure_stream_copy[index_a]
        m_b = measure_stream_copy[index_b]
        m_a.remove(m_a.elements)

        for element in m_a.elements:
            choice = random.random()
            if choice < self.mutation_probability:
                m_a.remove(element)

        for element in elements_b:
            choice = random.random()
            if choice < self.mutation_probability:
                m_a.insert(element.offset,element)



        size2 = len(measure_stream_copy)
        if size == size2:
            measure_stream_copy.write(fmt="midi", fp="Midi/Temp/temp.mid")
            song.raw_stream  = converter.parse("Midi/Temp/temp.mid")
            song.analyze_deep()

            self.count_measure_mix += 1




    # endregion

    #region NOTE_SWAP
    def swap_notes(self,song):

        notes = song.notes

        note_A = random.choice(notes)
        while note_A.isRest:
            note_A = random.choice(notes)
        offset_A = note_A.offset

        note_B = random.choice(notes)
        while note_B.isRest:
            note_B = random.choice(notes)

        offset_B = note_B.offset

        note_A.offset = offset_B
        note_B.offset = offset_A

        song.raw_stream = stream.Stream(notes)
        song.analyze()


        self.count_note_swap += 1
    #endregion


