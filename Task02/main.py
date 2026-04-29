import os
import random
from music21 import converter, note, chord, stream

notes = []

# ==============================
# STEP 1: READ MIDI FILES
# ==============================
for file in os.listdir("data"):
    if file.endswith(".mid") or file.endswith(".MID"):
        print(f"Reading file: {file}")
        midi = converter.parse("data/" + file)

        # FIX: use flatten() instead of deprecated flat
        for element in midi.flatten().notes:
            if isinstance(element, note.Note):
                notes.append(str(element.pitch))
            elif isinstance(element, chord.Chord):
                notes.append('.'.join(str(n) for n in element.normalOrder))

print("Total notes:", len(notes))

# ==============================
# STEP 2: LEARN PATTERNS
# ==============================
patterns = {}

for i in range(len(notes) - 1):
    current_note = notes[i]
    next_note = notes[i + 1]

    if current_note not in patterns:
        patterns[current_note] = []

    patterns[current_note].append(next_note)

# ==============================
# STEP 3: GENERATE MUSIC
# ==============================
current_note = random.choice(notes)
generated_notes = []

for i in range(100):
    generated_notes.append(current_note)

    if current_note in patterns:
        current_note = random.choice(patterns[current_note])
    else:
        current_note = random.choice(notes)

# ==============================
# STEP 4: CONVERT TO MIDI
# ==============================
output_stream = stream.Stream()
offset = 0

for pattern in generated_notes:

    # Handle chords
    if '.' in pattern:
        notes_in_chord = pattern.split('.')
        chord_notes = []

        for n in notes_in_chord:
            try:
                new_note = note.Note(int(n))
                chord_notes.append(new_note)
            except:
                continue

        if chord_notes:  # only add if valid
            new_chord = chord.Chord(chord_notes)
            new_chord.offset = offset
            output_stream.append(new_chord)

    # Handle single notes
    else:
        try:
            new_note = note.Note(pattern)
            new_note.offset = offset
            output_stream.append(new_note)
        except:
            # skip invalid notes like "2"
            continue

    offset += 0.5

# ==============================
# STEP 5: SAVE OUTPUT
# ==============================
output_stream.write('midi', fp='output/generated.mid')

print("✅ Music Generated Successfully!")
print("📁 Check: output/generated.mid")