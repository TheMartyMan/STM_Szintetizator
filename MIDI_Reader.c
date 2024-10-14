void Read_MIDI_File() {
    char buffer[256];
    fres = f_open(&fil, "test.mid", FA_READ);
    if (fres == FR_OK) {
        UINT bytesRead;
        f_read(&fil, buffer, sizeof(buffer), &bytesRead);
        // MIDI fájl feldolgozása (parser segítségével)
        f_close(&fil);
    } else {
        // TODO - Hibakezelés
    }
}
