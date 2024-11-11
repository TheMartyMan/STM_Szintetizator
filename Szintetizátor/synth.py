import pygame
from pynput import keyboard
import serial

# UART
ser = serial.Serial('COM14', 9600)

pygame.init()
screen = pygame.display.set_mode((1200, 500))
pygame.display.set_caption("Szintetizátor")

# Frekvenciák
key_frequencies = {
    'c': 261,
    'd': 294,
    'e': 330,
    'f': 349,
    'g': 392,
    'a': 440,
    'b': 494
}

# Gombok
piano_keys = {
    'c': pygame.Rect(50, 50, 80, 100),
    'd': pygame.Rect(150, 50, 80, 100),
    'e': pygame.Rect(250, 50, 80, 100),
    'f': pygame.Rect(350, 50, 80, 100),
    'g': pygame.Rect(450, 50, 80, 100),
    'a': pygame.Rect(550, 50, 80, 100),
    'b': pygame.Rect(650, 50, 80, 100)
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
        if hasattr(key, 'char') and key.char in key_frequencies:
            frequency = key_frequencies[key.char]
            ser.write(f"{frequency}\n".encode())  # Frekvencia küldése UART-on
            print(f"Frekvencia: {frequency} Hz küldése")
    except AttributeError:
        pass

# Billentyűzet felengedés
def on_release(key):
    if hasattr(key, 'char') and key.char in key_frequencies:
        ser.write("900\n".encode())  # Elnémítja a hangot
        print("Elnémítva.")

# Adott hang lejátszása
def play_tone(key):
    frequency = key_frequencies.get(key)
    if frequency < 900:
        ser.write(f"{frequency}\n".encode())
        print(f"Elküldve: {frequency} Hz")
    else:
        ser.write(f"{frequency}\n".encode())
        print("Elnémítva.")

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

    pygame.display.flip()

# Cleanup
pygame.quit()
listener.stop()
ser.close()
