void Play_Note(uint8_t note) {
    uint32_t frequency = Note_To_Frequency(note);
    uint32_t period = HAL_RCC_GetPCLK1Freq() / frequency;

    // Timer konfiguráció
    __HAL_TIM_SET_AUTORELOAD(&htim2, period - 1);
    __HAL_TIM_SET_COMPARE(&htim2, TIM_CHANNEL_1, period / 2);
    HAL_TIM_PWM_Start(&htim2, TIM_CHANNEL_1);
}

void Stop_Note() {
    HAL_TIM_PWM_Stop(&htim2, TIM_CHANNEL_1);
}

uint32_t Note_To_Frequency(uint8_t note) {
    // MIDI hangjegy frekvencia átalakítása (A4 = 440 Hz)
    return (uint32_t)(440 * pow(2, (note - 69) / 12.0));
}
