import numpy as np
import pickle
from tensorflow.keras.utils import to_categorical

with open("notes.pkl", "rb") as f:
    notes = pickle.load(f)

sequence_length = 100

# Create vocabulary
unique_notes = sorted(set(notes))
note_to_int = {note: num for num, note in enumerate(unique_notes)}

input_seq = []
output_seq = []

for i in range(len(notes) - sequence_length):
    input_seq.append([note_to_int[n] for n in notes[i:i+sequence_length]])
    output_seq.append(note_to_int[notes[i+sequence_length]])

X = np.reshape(input_seq, (len(input_seq), sequence_length, 1))
X = X / float(len(unique_notes))
y = to_categorical(output_seq)

print("Data prepared")
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from tensorflow.keras.callbacks import ModelCheckpoint

model = Sequential()
model.add(LSTM(256, input_shape=(X.shape[1], X.shape[2]), return_sequences=True))
model.add(Dropout(0.3))
model.add(LSTM(256))
model.add(Dense(len(unique_notes), activation='softmax'))

model.compile(loss='categorical_crossentropy', optimizer='adam')

checkpoint = ModelCheckpoint(
    "model/music_model.h5",
    monitor='loss',
    save_best_only=True
)

model.fit(X, y, epochs=20, batch_size=64, callbacks=[checkpoint])
