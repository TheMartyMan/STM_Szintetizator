typedef struct {
    uint8_t status;
    uint8_t data1;
    uint8_t data2;
} MIDI_Event;

void Parse_MIDI_Event(uint8_t* buffer, size_t length) {
    for (size_t i = 0; i < length; i++) {
        if (buffer[i] == 0x90) { // Note On
            uint8_t note = buffer[i + 1];
            uint8_t velocity = buffer[i + 2];
            if (velocity > 0) {
                Play_Note(note);
            }
            i += 2;
        } else if (buffer[i] == 0x80) { // Note Off
            uint8_t note = buffer[i + 1];
            Stop_Note(note);
            i += 2;
        }
    }
}
