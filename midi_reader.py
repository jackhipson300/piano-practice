import pygame.midi
import threading

MAX_NOTES_PER_RECORDING = 176
MIN_TIME_BETWEEN_NOTES = 50
NOTES = ['C', 'D♭', 'D', 'E♭', 'E', 'F', 'G♭', 'G', 'A♭', 'A', 'B♭', 'B']

pygame.midi.init()
input_id = pygame.midi.get_default_input_id()

midi_input = pygame.midi.Input(input_id)

class MidiParser:
    @staticmethod
    def get_note(data):
        pitch = data[0][0][1]
        note = NOTES[pitch % 12]
        return note

    @staticmethod
    def get_velocity(data):
        return data[0][0][2]

    @staticmethod
    def get_time(data):
        return data[0][1]
    

class Recorder:
    recording = False
    notes = []

    def record_sequence(self, max_notes):
        note = ""
        while(self.recording and len(self.notes) < max_notes):
            data = midi_input.read(64)
            if(len(data) > 0 and data[0][0][0] == 144):
                note = MidiParser.get_note(data)
                time = MidiParser.get_time(data)
                velocity = MidiParser.get_velocity(data)
                self.notes.append((note, time, velocity))
                
        if(self.recording):
            self.stop_recording()

    def start_recording(self, max_notes):
        self.recording = True
        self.notes = []
        recording_thread = threading.Thread(target=self.record_sequence, args=(max_notes,))
        recording_thread.start()

    def stop_recording(self):
        self.recording = False


def detect_chords(notes):
    sequence = []
    
    chord = []
    chord_velocities = []
    i = 0
    while i < len(notes):
        chord.append(notes[i][0])
        chord_velocities.append(notes[i][2])

        first_note_time = notes[i][1]
        j = i + 1
        while j < len(notes):
            second_note_time = notes[j][1]
            time_diff = second_note_time - first_note_time

            if time_diff < MIN_TIME_BETWEEN_NOTES:
                chord.append(notes[j][0])
                chord_velocities.append(notes[j][2])
            else:
                sequence.append((chord, chord_velocities))
                chord = []
                chord_velocities = []
                break
            j += 1
        i = j

    sequence.append((chord, chord_velocities))
    return sequence
  

def get_missed_notes(original, attempted):
    missed_notes = 0
    for i in range(len(original)):
        original_note = original[i][0]
        attempted_note = attempted[i][0]
        
        missed_notes += abs(len(original_note) - len(attempted_note))
        min_length = min(len(original_note), len(attempted_note))

        missed_notes += sum(attempted_note[j] != original_note[j] for j in range(min_length))
          
    return missed_notes


def print_playback_results(original, attempted):
    print("\nResults:")
    print(get_missed_notes(original, attempted), "missed notes")
    print("Original:")
    for note in original:
        print(note[0], end=" ")
        
    print("\nAttempted:")
    for note in attempted:
        print(note[0], end=" ")

    print("\nVelocities:")
    for note in attempted:
        print(note[1], end=" ")
    print("\n")


def record_sequence(recorder):
    recorder.start_recording(MAX_NOTES_PER_RECORDING)
    input("Recording started press enter to stop")
    recorder.stop_recording()
    return recorder.notes


def playback_sequence(recorder, sequence):
    max_notes = sum(len(i[0]) for i in sequence)
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
