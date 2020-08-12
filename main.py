from midi_recorder import Recorder
from note import Note

MAX_NOTES_PER_RECORDING = 176
MIN_TIME_BETWEEN_NOTES = 50

def detect_chords(notes):
    chords = []
    
    chord = []
    i = 0
    while i < len(notes):
        chord.append(notes[i])

        first_note_time = notes[i].time
        j = i + 1
        while j < len(notes):
            second_note_time = notes[j].time
            time_diff = second_note_time - first_note_time

            if time_diff < MIN_TIME_BETWEEN_NOTES:
                chord.append(notes[j])
            else:
                chords.append(chord)
                chord = []
                break
            j += 1
        i = j

    chords.append(chord)
    return chords


def get_missed_notes(original, attempted):
    missed_notes = 0
    for i in range(len(original)):
        original_chord = original[i]
        attempted_chord = attempted[i]
        
        missed_notes += abs(len(original_chord) - len(attempted_chord))
        min_length = min(len(original_chord), len(attempted_chord))

        missed_notes += sum(attempted_chord[j].value != original_chord[j].value \
                            for j in range(min_length))
          
    return missed_notes


def print_velocities(chords):
    for chord in chords:
        print("(", end="")
        print(", ".join([str(note.velocity) for note in chord]), end="")
        print(")", end=" ")


def print_chords(chords):
    for chord in chords:
        print("(", end="")
        print(", ".join([note.value for note in chord]), end="")
        print(")", end=" ")


def print_playback_results(original, attempted):
    print("\nResults:")
    print(get_missed_notes(original, attempted), "missed notes")

    print("Original:")
    print_chords(original)
        
    print("\nAttempted:")
    print_chords(attempted)

    print("\nVelocities:")
    print_velocities(attempted)
    print("\n")
    

def record_sequence(recorder):
    recorder.start_recording(MAX_NOTES_PER_RECORDING)
    input("Recording started press enter to stop")
    recorder.stop_recording()
    return recorder.notes


def playback_sequence(recorder, sequence):
    max_notes = sum(len(chord) for chord in sequence)
    recorder.start_recording(max_notes)
    print("Start playing")
    while(recorder.recording):
        pass
    attempted_sequence = detect_chords(recorder.notes)
    print_playback_results(sequence, attempted_sequence)


def main_loop():
    recorder = Recorder()
    sequence = []

    running = True
    while(running):
        command = input("Enter a command: ")
        if(command == "record"):
            sequence = record_sequence(recorder)
            sequence = detect_chords(sequence)
        elif(command == "playback"):
            if(len(sequence) == 0):
                print("No sequence recorded")
            else:
                playback_sequence(recorder, sequence)
        elif(command == "exit"):
            running = False


main_loop()

midi_input.close()

pygame.midi.quit()
