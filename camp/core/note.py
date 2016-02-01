
from functools import total_ordering

# ours
from .. import utils

NOTES          = [ 'C',  'Db', 'D', 'Eb', 'E',  'F',  'Gb', 'G',  'Ab', 'A', 'Bb', 'B' ]
EQUIVALENCE    = [ 'C',  'C#', 'D', 'D#', 'E',  'F',  'F#', 'G',  'G#', 'A', 'A#', 'B' ]
UP_HALF_STEP   = utils.roll_left(NOTES)
DOWN_HALF_STEP = utils.roll_right(NOTES)

@total_ordering
class Note(object):

    def __init__(self, name=None, octave=None):

        """
        Constructs a note.
        note = Note(name='C', octave='4')
        """

        assert name is not None
        assert octave is not None

        self.name = self._equivalence(name)
        self.octave = octave

    def _equivalence(self, name):
        """ 
        Normalize note names on input, C# -> Db, etc 
        Internally everything uses flats.
        """

        if name in EQUIVALENCE:
           return NOTES[EQUIVALENCE.index(name)] 
        return name

    def transpose(self, steps=0, octaves=0):
        """ 
        Returns a note a given number of steps or octaves higher. 
        """

        assert steps is not None or octaves is not None

        steps = steps + (octaves * 6)

        note = self
        if steps > 0:
             while steps > 0:
                 note = self.up_half_step()
                 steps = steps - 0.5
             return note
        else:
             while steps < 0:
                 note = self.down_half_step()
                 steps = steps + 0.5

    def _numeric_name(self):
        """
        Give a number for the note - used by internals only
        """
        return NOTES.index(self.name)

    def _note_number(self):
        """ 
        What order is this note on the keyboard?
        """
        return NOTES.index(self.name) + (12 * self.octave)

    def up_half_step(self):
        """
        What note is a half step up from this one?
        """
        number = self._numeric_name()
        name = UP_HALF_STEP[number]
        if self.name == 'B':
            return Note(name=name, octave=self.octave+1)
        return Note(name=name, octave=self.octave)

    def down_half_step(self):
        """
        What note is a half step down from this one?
        """
        number = self._numeric_name()
        name = DOWN_HALF_STEP[number]
        if self.name == 'C':
            return Note(name=name, octave=self.octave-1)
        return Note(name=name, octave=self.octave)

    def __eq__(self, other):
        """
        Are two notes the same?
        FIXME: duration and volume MAY matter in the future.
        """
        return self._note_number() == other._note_number()
 
    def __lt__(self, other):
        """
        Are two notes the same?
        FIXME: duration and volume MAY matter in the future.
        """
        return self._note_number() < other._note_number()