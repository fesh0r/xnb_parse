"""
FEZ music types
"""

from xnb_parse.xna_types.xna_primitive import Enum
from xnb_parse.file_formats.xml_utils import E


class ShardNotes(Enum):
    enum_values = dict(enumerate(['C2', 'Csharp2', 'D2', 'Dsharp2', 'E2', 'F2', 'Fsharp2', 'G2', 'Gsharp2', 'A2',
                                  'Asharp2', 'B2', 'C3', 'Csharp3', 'D3', 'Dsharp3', 'E3', 'F3', 'Fsharp3', 'G3',
                                  'Gsharp3', 'A3', 'Asharp3', 'B3', 'C4']))
    xml_tag = 'Note'


class AssembleChords(Enum):
    enum_values = dict(enumerate(['C_maj', 'Csharp_maj', 'D_maj', 'Dsharp_maj', 'E_maj', 'F_maj', 'Fsharp_maj', 'G_maj',
                                  'Gsharp_maj', 'A_maj', 'Asharp_maj', 'B_maj']))
    xml_tag = 'Chord'


class TrackedSong(object):
    def __init__(self, loops, name, tempo, time_signature, notes, assemble_chord, random_ordering, custom_ordering):
        self.loops = loops
        self.name = name
        self.tempo = tempo
        self.time_signature = time_signature
        self.notes = notes
        self.assemble_chord = assemble_chord
        self.random_ordering = random_ordering
        self.custom_ordering = custom_ordering

    def __str__(self):
        return "TrackedSong: '%s'" % self.name

    def xml(self):
        root = E.TrackedSong(name=self.name, tempo=str(self.tempo), timeSignature=str(self.time_signature))
        root.append(self.assemble_chord.xml())
        root.append(self.notes.xml('Notes'))
        root.append(self.loops.xml('Loops'))
        if self.random_ordering:
            root.append(E.RandomOrdering())
        if self.custom_ordering:
            root.append(self.custom_ordering.xml('CustomOrdering', 'Order'))
        return root

    def export(self, _):
        return self.xml()


class Loop(object):
    def __init__(self, duration, loop_times_from, loop_times_to, name, trigger_from, trigger_to, delay, night, day,
                 dusk, dawn, fractional_time, one_at_a_time, cut_off_tail):
        self.duration = duration
        self.loop_times_from = loop_times_from
        self.loop_times_to = loop_times_to
        self.name = name
        self.trigger_from = trigger_from
        self.trigger_to = trigger_to
        self.delay = delay
        self.night = night
        self.day = day
        self.dusk = dusk
        self.dawn = dawn
        self.fractional_time = fractional_time
        self.one_at_a_time = one_at_a_time
        self.cut_off_tail = cut_off_tail

    def __str__(self):
        return "Loop: '%s' d:%d" % (self.name, self.duration)

    def xml(self):
        root = E.Loop(name=self.name, duration=str(self.duration), loopTimesFrom=str(self.loop_times_from),
                      loopTimesTo=str(self.loop_times_to), triggerFrom=str(self.trigger_from),
                      triggerTo=str(self.trigger_to), delay=str(self.delay), fractionalTime=str(self.fractional_time),
                      oneAtATime=str(self.one_at_a_time), cutOffTail=str(self.cut_off_tail))
        if self.night:
            root.append(E.Night())
        if self.day:
            root.append(E.Day())
        if self.dusk:
            root.append(E.Dusk())
        if self.dawn:
            root.append(E.Dawn())
        return root
