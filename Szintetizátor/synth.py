import pygame
from pynput import keyboard
import serial

# UART
ser = serial.Serial('COM13', 9600)

pygame.init()
screen = pygame.display.set_mode((1200, 500))
pygame.display.set_caption("Szintetizátor")

# Frekvenciák
key_frequencies = {
    'C': 261,
    'D': 294,
    'E': 330,
    'F': 349,
    'G': 392,
    'A': 440,
    'B': 494
}

# Gombok
piano_keys = {
    'C': pygame.Rect(50, 50, 80, 100),
    'D': pygame.Rect(150, 50, 80, 100),
    'E': pygame.Rect(250, 50, 80, 100),
    'F': pygame.Rect(350, 50, 80, 100),
    'G': pygame.Rect(450, 50, 80, 100),
    'A': pygame.Rect(550, 50, 80, 100),
    'B': pygame.Rect(650, 50, 80, 100)
}

# Gombok rajzolása
def draw_keys():
    for key, rect in piano_keys.items():
        pygame.draw.rect(screen, (255, 255, 255), rect)
        pygame.draw.rect(screen, (0, 0, 0), rect, 2)

        font = pygame.font.Font(None, 36)
        text = font.render(key.upper(), True, (0, 0, 0))
        text_rect = text.get_rect(center=rect.center)
        screen.blit(text, text_rect)

# Billentyűzet lenyomás
def on_press(key):
    try:
        if key.char in key_frequencies:
            play_tone(key.char)
    except AttributeError:
        pass

# Billentyűzet elengedés
def on_release(key):
    stop_tone()

# Adott hang lejátszása
def play_tone(key):
    frequency = key_frequencies.get(key)
    if frequency:
        ser.write(f"{frequency}\n".encode())
        print(f"Elküldve: {frequency} Hz ")

# Némítás
def stop_tone():
    ser.write(b"0\n")
    print("Néma")

# Pygame listener
listener = keyboard.Listener(on_press=on_press, on_release=on_release)
listener.start()

running = True
while running:
    screen.fill((200, 200, 200))
    draw_keys()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for key, rect in piano_keys.items():
                if rect.collidepoint(event.pos):
                    play_tone(key)
        elif event.type == pygame.MOUSEBUTTONUP:
            stop_tone()

    pygame.display.flip()

# Cleanup
pygame.quit()
listener.stop()
ser.close()
