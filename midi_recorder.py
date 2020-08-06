import threading
import pygame.midi
from note import Note

pygame.midi.init()
input_id = pygame.midi.get_default_input_id()

midi_input = pygame.midi.Input(input_id)

class Recorder:
    recording = False
    notes = []

    def record_sequence(self, max_notes):
        while(self.recording and len(self.notes) < max_notes):
            data = midi_input.read(64)
            if(len(data) > 0 and data[0][0][0] == 144):
                note = Note(data)
                self.notes.append(note)
                
        if(self.recording):
            self.stop_recording()

    def start_recording(self, max_notes):
        self.recording = True
        self.notes = []
        recording_thread = threading.Thread(target=self.record_sequence, args=(max_notes,))
        recording_thread.start()

    def stop_recording(self):
        self.recording = False
