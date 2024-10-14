FATFS fs;
FIL fil;
FRESULT fres;

void MX_FATFS_Init(void) {
    fres = f_mount(&fs, "", 1);
    if (fres != FR_OK) {
        // TODO - Hibakezelés
    }
}
