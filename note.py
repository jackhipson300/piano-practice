NOTES = ['C', 'D♭', 'D', 'E♭', 'E', 'F', 'G♭', 'G', 'A♭', 'A', 'B♭', 'B']

class MidiParser:
    @staticmethod
    def get_value(data):
        pitch = data[0][0][1]
        value = NOTES[pitch % 12]
        return value

    @staticmethod
    def get_velocity(data):
        return data[0][0][2]

    @staticmethod
    def get_time(data):
        return data[0][1]
    

class Note:
    def __init__(self, data):
        self.value = MidiParser.get_value(data)
        self.velocity = MidiParser.get_velocity(data)
        self.time = MidiParser.get_time(data)
