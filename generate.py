import pickle
import numpy as np
from tensorflow.keras.models import load_model
from music21 import note, chord, stream
import random

with open("notes.pkl", "rb") as f:
    notes = pickle.load(f)

unique_notes = sorted(set(notes))
int_to_note = {num: note for num, note in enumerate(unique_notes)}

model = load_model("model/music_model.h5")

sequence_length = 100
start = random.randint(0, len(notes) - sequence_length)
pattern = [unique_notes.index(n) for n in notes[start:start+sequence_length]]

output_notes = []

for _ in range(200):
    prediction_input = np.reshape(pattern, (1, len(pattern), 1))
    prediction_input = prediction_input / float(len(unique_notes))
    prediction = model.predict(prediction_input, verbose=0)
    index = np.argmax(prediction)
    result = int_to_note[index]
    output_notes.append(result)
    pattern.append(index)
    pattern = pattern[1:]

# Convert to MIDI
offset = 0
output = []

for pattern in output_notes:
    if '.' in pattern:
        notes_in_chord = pattern.split('.')
        chord_notes = [note.Note(int(n)) for n in notes_in_chord]
        new_chord = chord.Chord(chord_notes)
        new_chord.offset = offset
        output.append(new_chord)
    else:
        new_note = note.Note(pattern)
        new_note.offset = offset
        output.append(new_note)
    offset += 0.5

midi_stream = stream.Stream(output)
midi_stream.write('midi', 'generated_music/output.mid')

print("Music generated!")
