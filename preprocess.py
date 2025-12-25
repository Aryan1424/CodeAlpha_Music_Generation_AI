import glob
from music21 import converter, instrument, note, chord
import numpy as np
import pickle

notes = []

# Read all MIDI files
for file in glob.glob("data/*.mid"):
    midi = converter.parse(file)
    parts = instrument.partitionByInstrument(midi)

    if parts:
        elements = parts.parts[0].recurse()
    else:
        elements = midi.flat.notes

    for element in elements:
        if isinstance(element, note.Note):
            notes.append(str(element.pitch))
        elif isinstance(element, chord.Chord):
            notes.append('.'.join(str(n) for n in element.normalOrder))

# Save notes
with open("notes.pkl", "wb") as f:
    pickle.dump(notes, f)

print("Total notes:", len(notes))
