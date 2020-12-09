from Model.Song import *
import copy
from Constants import *

class Outsider(Song):

    def __init__(self, raw_stream = None, generation=0, measurenr = NUMBER_OF_MEASURES ):
        Song.__init__(self,raw_stream=raw_stream ,generation=generation)
        self.raw_stream = self.strip_song(measurenr,self.raw_stream)
        Song.analyze(self)





    def strip_song(self, measurenr,raw_stream):
        try:
            measure_list = raw_stream.makeMeasures()
            measure_list.makeTies(inPlace=True)
            result_stream = stream.Stream()

            measure_size = len(measure_list.elements)

            if measure_size == measurenr:
                return self.raw_stream
            while measurenr != measure_size:

                if measure_size > measurenr:
                    measures = measure_list[-(measure_size-measurenr):]
                    measure_list.remove(measures.elements)
                    measure_list.write(fmt="midi", fp="Midi/Temp/temp.mid")
                    result_stream = converter.parse("Midi/Temp/temp.mid")


                else:
                    result_stream.append(raw_stream)
                    temp = copy.deepcopy(raw_stream)
                    result_stream.append(temp)
                    result_stream.flattenUnnecessaryVoices(force=True, inPlace=True)
                    result_stream.write(fmt="midi", fp="Midi/Temp/temp.mid")
                    result_stream = converter.parse("Midi/Temp/temp.mid")



                measure_list = result_stream.makeMeasures()
                measure_list.makeTies(inPlace=True)
                measure_size = len(measure_list.elements)

            return result_stream


        except Exception as e:
            print(e)
            return None




    def analyze_notes(self):

        instruments = self.raw_stream.getInstruments()

        try:
            for part in instrument.partitionByInstrument(self.raw_stream):
                if isinstance(part.getInstrument(), instrument.Piano):
                    self.raw_stream = part
                    break
                if isinstance(part.getInstrument(), instrument.AcousticGuitar):
                    self.raw_stream = part
                    break
                if isinstance(part.getInstrument(), instrument.ElectricGuitar):
                    self.raw_stream = part
                    break
                if isinstance(part.getInstrument(), instrument.Guitar):
                    self.raw_stream = part
                    break
        except:
            pass

        self.notes = []
        self.raw_stream.flattenUnnecessaryVoices(force=True, inPlace=True)
        self.raw_stream.makeRests(fillGaps=True, inPlace=True)

        for element in self.raw_stream.recurse():
            try:
                if element.isNote or element.isChord or element.isRest:
                    self.notes.append(element)
            except:
                pass

        self.raw_stream = stream.Stream(self.notes)

        self.raw_stream.flattenUnnecessaryVoices(force=True, inPlace=True)
        self.raw_stream.makeRests(fillGaps=True, inPlace=True)

        self.notes = []
        for element in self.raw_stream.recurse():
            try:
                if element.isNote or element.isChord or element.isRest:
                    self.notes.append(element)
            except:
                pass




    def fix_song(self,raw_stream):

        result_stream = stream.Stream()

        for element in raw_stream.recurse():
            try:
                if element.isNote or element.isChord or element.isRest:
                    new_note = copy.deepcopy(element)
                    result_stream.append(element)
            except:
                pass

        return result_stream





