
from camp.core.chord import Chord
from camp.utils import loop_around
from camp.band.member import Member
from camp.playback.event import Event

class Chordify(Member):

    def __init__(self, types=None):

        super().__init__()

        assert type(types) == list
        self._which_chord = loop_around(types)

    def signal(self, event):

        print("chordify :: signaled :: %s" % event)

        if event.typ == 'note':
            chord_typ = next(self._which_chord)
            chord = Chord(root=event.notes[0], typ=chord_typ)
            evt = Event(typ='note', velocity=127, channel=event.channel, notes=chord.notes)
            for send in self.sends:
                print("chordify :: signaling :: %s" % send)
                send.signal(evt)