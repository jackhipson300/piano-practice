import pygame.midi

NOTES = ['C', 'D♭', 'D', 'E♭', 'E', 'F', 'G♭', 'G', 'A♭', 'A', 'B♭', 'B']

pygame.midi.init()
input_id = pygame.midi.get_default_input_id()

midi_input = pygame.midi.Input(input_id)

def get_note(data):
    pitch = data[0][0][1]
    note = NOTES[pitch % 12]
    return note

def get_velocity(data):
    return data[0][0][2]

def record_sequence():
    sequence = []
    note = ""
    while(True):
        data = midi_input.read(64)
        if(len(data) > 0 and data[0][0][0] == 144):
            note = get_note(data)
            if(note == "D♭"):
                break
            sequence.append(note)

    return sequence

def playback_sequence(sequence):
    attemptedSequence = []
    velocities = []
    
    count = 0
    for note in sequence:
        invalidData = True
        while(invalidData):
            data = midi_input.read(64)
            if(len(data) > 0 and data[0][0][0] == 144):
                attemptedNote = get_note(data)
                attemptedSequence.append(attemptedNote)
                
                velocity = get_velocity(data)
                velocities.append(velocity)
                
                if(attemptedNote != note):
                    count += 1
                invalidData = False

    print(count, "missed notes")
    print("Original:\n", sequence)
    print("Attempted:\n", attemptedSequence)
    print("Velocities:\n", velocities)

sequence = []
while(True):
    command = input("Enter a command: ")
    if(command == "record"):
        sequence = record_sequence()
    elif(command == "playback"):
        if(len(sequence) == 0):
            print("No sequence recorded")
        else:
            playback_sequence(sequence)
    elif(command == "exit"):
        break

midi_input.close()

pygame.midi.quit()
