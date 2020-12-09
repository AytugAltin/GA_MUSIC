from music21 import *
from music21 import interval
import random

from scipy.stats import wasserstein_distance
from Model.Song import Song
from Model.Outsider import Outsider
from Model.Measure import Measure

from GeneticAlgorithm.Rating.TheoryBasedRatingStrategy import  *
from GeneticAlgorithm.Rating.SubRaters.RepetitionRaterStrategy import *

import copy
import matplotlib.pyplot as plt
import math
import networkx as nx

from difflib import get_close_matches
import os
from collections import Counter
from itertools import repeat, chain
from math import log
from fuzzywuzzy import fuzz

from GeneticAlgorithm.CrossoverStrategy import CrossoverStrategy

#region opencreatemidi
def open_midi(midi_path):
    mf = midi.MidiFile()
    mf.open(midi_path)
    mf.read()
    mf.close()
    return midi.translate.midiFileToStream(mf)


def create_songs():
    song = converter.parse("Midi/Input/correct/AMajor.mid")
    notes1 = song.notesAndRests.stream()
    creation = stream.Score()




    track2 = stream.Score()

    alnotes = ["C8", "B7", "A#7", "A7", "G#7", "G7", "F#7" ,"F7", "E7", "D#7", "D7", "C#7", "C7", "B6",
               "A#6", "A6", "G#6", "G6", "F#6", "F6", "E6", "D#6", "D6", "C#6", "C6#", "B5", "A#5", "A5",
               "G#5", "G5", "F#5", "F5", "E5", "D#5", "D5", "C#5", "C5", "B4", "A#4", "A4", "G#4", "G4",
               "F#4", "F4", "E4", "D#4", "D4", "C#4", "C4", "B3", "A#3", "A3", "G#3", "G3", "F#3", "F3",
               "E3", "D#3", "D3", "C#3", "C3", "B2", "A#2", "A2", "G#2", "G2", "F#2", "F2", "E2", "D#2",
               "D2", "C#2", "C2", "B1", "A#1", "A1", "G#1", "G1", "F#1", "F1", "E1", "D#1", "D1", "C#1",
               "C1", "B0", "A#0", "A0"]

    highnotes = ["C8", "B7", "A#7", "A7", "G#7", "G7", "F#7", "F7", "E7", "D#7", "D7", "C#7", "C7", "B6",
               "A#6", "A6", "G#6", "G6", "F#6", "F6", "E6", "D#6", "D6", "C#6", "C6#", "B5", "A#5"]

    lownotes = [ "A#2", "A2", "G#2", "G2", "F#2", "F2", "E2", "D#2", "D2", "C#2", "C2", "B1", "A#1", "A1",
                 "G#1", "G1", "F#1", "F1", "E1", "D#1", "D1", "C#1", "C1", "B0", "A#0", "A0"]

    midnotes = ["D5", "C#5", "C5", "B4", "A#4", "A4", "G#4", "G4","F#4", "F4", "E4", "D#4", "D4", "C#4",
                "C4", "B3", "A#3", "A3", "G#3", "G3", "F#3", "F3", "E3", "D#3", "D3", "C#3", "C3", "B2"]

    aminor = ["A3", "C4", "D4", "E4", "G4", "A4", "C5", "D5", "E5", "G5", "A5", "C6"]

    AMajor = ["G#3", "A3", "B3", "C#4", "D4", "F4", "F#4", "G#4", "A4", "B4", "C#5", "D5", "E5", "F#5", "G#5", "A5",
              "B5"]

    type = ["quarter", "whole", "half", "quarter", "half", "quarter", "quarter", "quarter", "quarter", "quarter", "quarter", "quarter", "quarter", "quarter", "quarter", "quarter", "quarter", "quarter", "quarter", "quarter", "quarter", "quarter", "quarter", "quarter", "quarter"]
    rest = ["0", "0", "0", "0", "0", "1"]

    resttype = ["quarter", "half", "quarter"]


    print("GENERATING")
    for n in range(100):
        if random.choice(rest) == "0":
            track2.append(note.Note(random.choice(midnotes), type=random.choice(type)))
        else:
            track2.append(note.Rest(type=random.choice(resttype)))

    track2.show("midi")
    track2.write(fmt="xml", fp="Midi/Input/random/RandomMid.xml")


def crossover():
    A = converter.parse("Midi/Input/correct/AMajor.mid")
    B = converter.parse("Midi/Input/correct/AMinor.mid")

    notes1 = A.flat.notesAndRests
    om = A.secondsMap

    for n in om:
        print(n)


    ANOTES = []
    for element in A.recurse():
        if not element.isStream:
            ANOTES.append(element)

    BNOTES = []
    for element in B.recurse():
        if not element.isStream:
            BNOTES.append(element)

    Asize = ANOTES[-1].offset
    Bsize = BNOTES[-1].offset

    listA = [None] * (int(Asize) + 1)
    listB = [None] * (int(Bsize) + 1)

    for n in ANOTES:
        index = int(n.offset)
        listA[int(n.offset)] = n

    print("test")


def rate_song():
    random = converter.parse("Midi/Input/random/Random1.mid")


    key = random.analyze_insider('key')
    scale = key.getScale(key.mode)



    test = scale.match(random)
    match_results = scale.match(random)
    match_results_pitch = scale.match(random.pitches)
    matchlen = len(match_results["matched"])
    notmatchlen = len(match_results["notMatched"])

    song = Song(raw_stream= random)

    temp = random.melodicIntervals()

    print(temp.iter.elementsLength)

    list = []
    for element in temp.recurse():
        if not element.isStream:
            list.append(element)
    print(scale)
    print(key.tonic.name, key.mode)

#endregion

#region test
def test():
    song = converter.parse("Midi/Input/selection/63261.mid")

    song = Outsider(raw_stream= song)

    interval_stream = song.raw_stream.melodicIntervals(skipRests=True, skipOctaves=False)
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
                upwards_intervals += 1
            if (previous > 0) == (semitone > 0):
                direction_changes += 1

            semitones_list.append(abs(semitone))
        except:
            pass

    melody_direction = upwards_intervals / len(semitones_list)
    direction_stability = direction_changes / len(semitones_list)

    max_interval_size = max(semitones_list)
    min_interval_size = min(x for x in semitones_list if x > 0)


    nr_unique_semitones = len(set(semitones_list))

    unique_pitches = nr_unique_semitones / len(semitones_list)

    print("max_interval_size: " + str(max_interval_size))
    print("min_interval_size: " + str(min_interval_size))
    print("melody_direction: " + str(melody_direction))
    print("direction_stability: " + str(direction_stability))





#endregion


#region zipfs
def analyze_zipfs_law(song):
    pitches = song.raw_stream.pitches
    pitchfreq = []

    for pitch in pitches:
        pitchfreq.append(pitch.frequency)

    tes = list(chain.from_iterable(repeat(i, c) for i, c in Counter(pitchfreq).most_common()))
    uniques_sorted = list(dict.fromkeys(tes))

    zipfs_distr = create_zipfs_distr(len(pitchfreq),uniques_sorted)

    #zipfs_distance_rating = abs(wasserstein_distance(pitchfreq, zipfs_distr))

    #print(zipfs_distance_rating)

def Harmonic(n):
    gamma = 0.57721566490153286060651209008240243104215933593992
    return gamma + log(n) + 0.5/n - 1./(12*n**2) + 1./(120*n**4)

def create_zipfs_distr(size,unique_sorted):
    list = []
    H = Harmonic(len(unique_sorted))

    rate = size / H

    for n in range(len(unique_sorted)):
        rank = 1/(n+1)
        count = round(rank * rate)
        element = [unique_sorted[n]]
        list.extend(element * count)



    return list

#endregion


def rate_song(song):

    rating = TheoryBasedRatingStrategy()
    song.rating = rating.rate_song(song)
    song.rating.print_rating()

#region Mutate
def contains(list, filter):
    for x in list:
        if filter(x):
            return True
    return False




def scale_mutation(song):
    incorrect_notes = find_incorrect_notes(song.notes,song.scale,song)



def find_incorrect_notes(notes,scale,song):
    print("1########################")
    rate_song(song)

    incorrect_pitc = []
    #not_matched = scale.match(song.raw_stream)["notMatched"]
    not_matched = [scale.match(song.raw_stream)["notMatched"][0]]
    print(song.scale)


    index = 0
    for note in song.notes:
        if note.isNote:
            if contains(not_matched, lambda x: x.name == note.pitch.name):
                correct_note(note.nameWithOctave, scale,note)
        if note.isChord:
            if contains(not_matched, lambda x: x.name == note.root().name):
                correct_note(note.root().nameWithOctave, scale,note)
        index +=1


    song.reform_stream()
    print("2########################")

    print(song.scale)
    rate_song(song)

def correct_note(noteAName,scale,object):
    noteA = note.Note(noteAName)
    pitch = random.choice(scale.pitches)
    name =  pitch.name + str(noteA.octave)
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

        noteB.transpose(temp,inPlace=True)
        ainterval = interval.Interval(noteStart=noteA, noteEnd=noteB)


    object.transpose(value=interval.Interval(semitone),inPlace=True)


#endregion


#region PATTERNS


def measure_function():
    song = converter.parse("Midi/Output/GEN32Song5.mid")
    song = converter.parse("Midi/Input/master/GodFather_stripped.mid")
    song = Outsider(raw_stream=song)
    measure_stream = song.raw_stream.makeMeasures()

    i = 2
    while True:
        measureA = measure_stream[i]
        measureB = measure_stream[i+1]

        offsetsA = []
        durationA = []
        objectTypeA = []
        for element in measureA.elements:
            try:
                offsetsA.append(element.offset)
                durationA.append(element.duration.type)
                if element.isNote:
                    objectTypeA.append("N" + element.nameWithOctave)
                elif element.isChord:
                    string = 'X'
                    for pitch in element.pitches:
                        string += pitch.nameWithOctave
                    objectTypeA.append(string)

                elif element.isRest:
                    objectTypeA.append("R")
            except:
                pass



        offsetsB = []
        durationB = []
        objectTypeB = []
        for element in measureB.elements:
            try:
                offsetsB.append(element.offset)
                durationB.append(element.duration.type)
                if element.isNote:
                    objectTypeB.append("N" + element.nameWithOctave)

                elif element.isChord:
                    string = 'X'
                    for pitch in element.pitches:
                        string += pitch.nameWithOctave
                    objectTypeB.append(string)

                elif element.isRest:
                    objectTypeB.append("R")
            except:
                pass

        print("** " +str(i) + " and " + str(i+1))
        ratio = fuzz.ratio(offsetsA, offsetsB)
        print(" - Offsets: "+ str(ratio))

        ratio = fuzz.ratio(durationA, durationB)
        print(" - Duration: "+ str(ratio))

        ratio = fuzz.ratio(objectTypeA, objectTypeB)
        print(" - objectType: "+ str(ratio))

        mergedA = [objectTypeA[i] + str(durationA[i][0]) + str(offsetsA[i])  for i in range(0, len(offsetsA), 1)]

        mergedB = [objectTypeB[i] + str(durationB[i][0]) + str(offsetsB[i])  for i in range(0, len(offsetsB), 1)]

        ratio = fuzz.ratio(mergedA, mergedB)
        print(" - MERGED: " + str(ratio))
        print("-----------------")

        i +=1


def measure_function2():

    rater = RepetitionRaterStrategy()

    print("GodFather_stripped")
    song1 = converter.parse("Midi/Input/master/GodFather_stripped.mid")
    song1 = Outsider(raw_stream=song1)
    rater.add_rating(song1)
    get_pattern_lists(song=song1,name="GodFather_stripped")

    """
    print("Californication_stripped_short")
    song1 = converter.parse("Midi/Input/selection/Californication_stripped_short.mid")
    song1 = Outsider(raw_stream=song1)
    rater.add_rating(song1)
    #graph(song1,"Californication_stripped_short")

    print("GEN100Song2")
    song1 = converter.parse("Midi/Input/sources/GEN100Song2.mid")
    song1 = Outsider(raw_stream=song1)
    rater.add_rating(song1)
    #graph(song1,"GEN100Song2")

    print("beethoven_opus10_1")
    song1 = converter.parse("Midi/Input/selection/beethoven_opus10_1_s.mid")
    song1 = Outsider(raw_stream=song1)

    rater.add_rating(song1)
    #graph(song1,"beethoven_opus10_1")
    
    """



    #graph(song1,"GodFather_stripped")




def calculate_over_threshold( threshold, value):
    strongs = math.floor(value["pitches"] / threshold)
    strongs += math.floor(value["types"] / threshold)
    strongs += math.floor(value["durations"] / threshold + 5)
    strongs += math.floor(value["offsets"] / threshold + 5)
    strongs += math.floor(value["semitones"] / threshold)
    return strongs


def graph(song,name,loc):
    G = nx.Graph()

    done_objects = []

    print(str(song.pattern_average) + "  length: "  + str(len(song.measure_list)))
    ratio = 0.15
    limit = 80
    threshold = 80
    for measure_object in song.measure_list:
        for key, value in measure_object.reference_list.items():
            if key not in done_objects:


                weight = (value["combined"] + value["semitones"]) /2


                above_avarage = math.floor(value["pitches"] / threshold)

                above_avarage += math.floor(value["durations"] / (threshold+5))

                above_avarage += math.floor(value["types"] / threshold)

                above_avarage += math.floor(value["offsets"] / (threshold+5))

                above_avarage += math.floor(value["semitones"] / threshold)

                weight = (value["combined"] + value["semitones"]) / 2



                if above_avarage >= 3 and weight >= threshold :
                    p1 = stream.Stream()
                    p1.append(measure_object.measure)
                    p1.append(key.measure)
                    #p1.show("midi")
                    #weight = 1/(value["combined"])
                    #measure_object.play()
                    # key.play()
                    print("  -  (" + str(measure_object.number()) +" , "+ str(key.number())  +")  " + str(value))
                    G.add_edge(measure_object.number(), key.number(), weight=100-weight)

        done_objects.append(measure_object)

    try:
        edges = [(u, v) for (u, v, d) in G.edges(data=True) ]

        pos = nx.kamada_kawai_layout(G,scale=500)  # positions for all nodes
        G.size(10)
        # nodes
        nx.draw_networkx_nodes(G, pos, node_size=100)

        # edges
        nx.draw_networkx_edges(G, pos, edgelist=edges,width=0.5)

        # labels
        nx.draw_networkx_labels(G, pos, font_size=8, font_family='sans-serif')
        plt.savefig(loc+name+".png",dpi=300)  # save as png
        plt.show()  # display
    except:
        print("crash")
        pass


#endregion



#region measureSWAP
def cut_songs_even():

    rater = RepetitionRaterStrategy()

    song = converter.parse("Midi/Input/sources/Hans_Zimmer_Time.mid")
    song = Outsider(raw_stream=song,measurenr=4)
    rater.add_rating(song)


    swap_notes(song)

    # measure_list = song.measure_list
    # measure_A = random.choice(measure_list)
    # measure_B = random.choice(measure_list)
    #
    # measure_A.play()
    # measure_B.play()
    # track2 = stream.Stream()
    # track2.append(measure_A.measure)
    # #track2.append(measure_A.measure)
    # track2.append(measure_B.measure)
    # track2.show("midi")
    #
    #
    #





def swap_notes (song):
    notes = song.notes
    note_A = random.choice(notes)
    offset_A = note_A.offset

    note_B = random.choice(notes)
    offset_B = note_B.offset

    note_A.offset = offset_B
    note_B.offset = offset_A

    track2 = stream.Stream(notes)





def StripSong(song,measure):

    offset = measure.offset

    notes = song.notes
    element = song.raw_stream.getElementBeforeOffset(offset)
    noteindex  = song.notes.index(element)
    notes = song.notes[:noteindex]
    track2 = stream.Stream(notes)
    measure_list = track2.makeMeasures()
    print(len(measure_list))
    track2.show("midi")

    song.raw_stream.write(fmt="midi", fp="Midi/Input/selection/24/24_Otherside.mid")


#endregion


#region MEASURE_SWAP

cross = CrossoverStrategy()

def swap_measure(song):
    measure_stream = song.get_measures()
    size = len(measure_stream) - 1
    print("size: " + str(size))

    index_a = random.randint(0, size)
    index_b = random.randint(0, size)

    while index_b == index_a:
        index_b = random.randint(0, size)


    m_a = measure_stream[index_a]
    m_b = measure_stream[index_b]

    elements_a = m_a.elements
    elements_b = m_b.elements

    measure_stream_copy = copy.deepcopy(measure_stream)
    m_a = measure_stream_copy[index_a]
    m_b = measure_stream_copy[index_b]


    for element in m_a.elements:
        try:
            if element.isNote or element.isChord or element.isRest:
                m_a.remove(element)
        except:
            pass

    for element in m_b.elements:
        try:
            if element.isNote or element.isChord or element.isRest:
                m_b.remove(element)
        except:
            pass

    for element in elements_a:
        try:
            if element.isNote or element.isChord or element.isRest:
                m_b.insert(element.offset, element)
        except:
            pass

    for element in elements_b:
        try:
            if element.isNote or element.isChord or element.isRest:
                m_a.insert(element.offset, element)
        except:
            pass

    print("A:" + str(index_a))
    print(m_a.elements)
    print("B:" + str(index_b))
    print(m_b.elements)

    p2 = stream.Stream()
    for note in measure_stream_copy.flat.notesAndRests:
        p2.insert(note.offset,note)

    p2.write(fmt="midi", fp="Midi/Temp/temp.mid")
    raw_stream = converter.parse("Midi/Temp/temp.mid")

    measure_stream = raw_stream.makeMeasures()
    size2 = len(measure_stream) - 1
    print("sizeAfter: " + str(size2))
    print()

    if size2 == size:
        song.raw_stream = raw_stream
        song.analyze_deep()





# endregion

def overlap(song):
    overlaps = song.raw_stream.getOverlaps()
    gaps = song.raw_stream.findGaps()
    song.play()
    print((overlaps))


def mutate_type(song):
    duration_types = ["eighth","half",'whole','32nd',"16th"]
    size = len(song.notes) - 1
    index_note = random.randint(0, size)
    note = song.notes[index_note]

    type = random.choice(duration_types)

    d3 = duration.Duration(type=type)

    note.duration = d3

    song.analyze_notes_reversed()
    song.analyze()


def get_pattern_lists( song,name,loc):

    done_objects = []
    G = nx.Graph()
    strong_objects = []
    normal_objects = []
    weak_objects = []
    garbage = []

    ratio = 0.15
    strong_threshold = 80
    normal_threshold = 70
    weak_threshold = 55

    for measure_object in song.measure_list:
        for key, value in measure_object.reference_list.items():
            if key not in done_objects:
                weight = (value["combined"] + value["semitones"]) / 2

                strongs = calculate_over_threshold(strong_threshold,value)
                normals = calculate_over_threshold(normal_threshold,value)
                weaks = calculate_over_threshold(weak_threshold,value)


                if strongs >= 3 and weight >= strong_threshold:
                    strong_objects.append(measure_object.number())
                    strong_objects.append(key.number())
                    print("  -  (" + str(measure_object.number()) + " , " + str(key.number()) + ")  " + str(value))
                    G.add_edge(measure_object.number(), key.number(), weight=100 - weight)

                elif normals >= 3 and weight >= normal_threshold:
                    normal_objects.append(measure_object.number())
                    normal_objects.append(key.number())

                elif weaks >= 3 and weight >= weak_threshold:
                    weak_objects.append(measure_object.number())
                    weak_objects.append(key.number())

                else:
                    garbage.append(measure_object.number())
                    garbage.append(key.number())

        done_objects.append(measure_object)

    try:
        edges = [(u, v) for (u, v, d) in G.edges(data=True) ]

        pos = nx.kamada_kawai_layout(G,scale=500)  # positions for all nodes
        G.size(10)
        # nodes
        nx.draw_networkx_nodes(G, pos, node_size=100)

        # edges
        nx.draw_networkx_edges(G, pos, edgelist=edges,width=0.5)

        # labels
        nx.draw_networkx_labels(G, pos, font_size=8, font_family='sans-serif')
        plt.savefig(loc+name+".png",dpi=300)  # save as png
        plt.show()  # display
    except:
        print("crash")
        pass

if __name__ == '__main__':


    rater = RepetitionRaterStrategy()
    song1 = converter.parse("Midi/Input/master/beethoven_opus10_1_s.mid")
    song1 = Outsider(raw_stream=song1)
    rater.add_rating(song1)
    get_pattern_lists(song1,"gf last gen","Midi/Output/beethoven/")

















