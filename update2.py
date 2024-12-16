import pygame
import random
import sys

# Function to load sentences from Sentences.txt file
def load_sentences(file_path):
    with open(file_path, 'r') as file:
        sentences = file.readlines()
    return [sentence.strip() for sentence in sentences]

# Function to display text on the screen
def display_text(screen, font, text, position, color):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, position)

# Function to calculate words per minute (WPM)
def calculate_wpm(time_elapsed, typed_text):
    words = len(typed_text.split())
    minutes = time_elapsed / 60
    wpm = words / minutes
    return wpm

# Function to calculate accuracy
def calculate_accuracy(original_text, typed_text):
    correct_chars = sum(1 for c1, c2 in zip(original_text, typed_text) if c1 == c2)
    accuracy = (correct_chars / len(original_text)) * 100
    return accuracy

def main():
    pygame.init()

    # Colors
    white = (255, 255, 255)
    green = (0, 255, 0)
    red = (255, 0, 0)

    # Load sentences from file
    sentences = load_sentences("C:/Users/Kryptos/Documents/Python Project/sentences.txt")

    # Initialize pygame window in fullscreen mode
    pygame.display.init()
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

    # Get screen dimensions
    screen_width, screen_height = pygame.display.get_surface().get_size()

    # Load background image
    background = pygame.image.load("C:/Users/Kryptos/Documents/Python Project/background.jpg")
    background = pygame.transform.scale(background, (screen_width, screen_height))

    # Load splash screen image
    splash_screen = pygame.image.load("C:/Users/Kryptos/Documents/Python Project/type-speed-open.png")

    # Load reset button image
    reset_button = pygame.image.load("C:/Users/Kryptos/Documents/Python Project/icon.png")
    reset_button = pygame.transform.scale(reset_button, (50, 50))  # Resize the button
    reset_button_rect = reset_button.get_rect(topleft=(screen_width - 60, 10))  # Button rect for collision detection

    # Load input button image
    input_button = pygame.image.load("C:/Users/Kryptos/Documents/Python Project/input.jpg")
    input_button = pygame.transform.scale(input_button, (200, 50))
    input_button_rect = input_button.get_rect(center=(screen_width // 2, screen_height // 2))

    # Fonts
    font = pygame.font.Font(None, 36)

    # Variables
    clock = pygame.time.Clock()
    typing = False
    typed_text = ""
    start_time = 0
    user_sentence = ""
    sentence = random.choice(sentences)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_RETURN:
                    if not typing:
                        typing = True
                        typed_text = ""
                        start_time = pygame.time.get_ticks()
                elif event.key == pygame.K_BACKSPACE:
                    typed_text = typed_text[:-1]
                else:
                    typed_text += event.unicode

        # Check if left mouse button is pressed on the input button
        if pygame.mouse.get_pressed()[0] and input_button_rect.collidepoint(pygame.mouse.get_pos()):
            user_sentence = input("Enter a sentence: ")
            typing = True
            typed_text = ""
            start_time = pygame.time.get_ticks()

        screen.blit(background, (0, 0))

        if not typing:
            screen.blit(splash_screen, (0, 0))
        else:
            if user_sentence:
                sentence = user_sentence
            correct_prefix = all(c1 == c2 for c1, c2 in zip(sentence[:len(typed_text)], typed_text))
            color = green if correct_prefix else red
            display_text(screen, font, sentence, (50, 50), color)
            display_text(screen, font, typed_text, (50, 100), white)

            # Calculate time elapsed
            current_time = pygame.time.get_ticks()
            time_elapsed = (current_time - start_time) / 1000

            # Calculate WPM and accuracy
            if time_elapsed > 0:
                wpm = calculate_wpm(time_elapsed, typed_text)
                accuracy = calculate_accuracy(sentence, typed_text)
                display_text(screen, font, f"WPM: {wpm:.2f}", (50, 150), green)
                display_text(screen, font, f"Accuracy: {accuracy:.2f}%", (50, 200), green)

        # Display reset button
        screen.blit(reset_button, reset_button_rect)

        # Display input button
        screen.blit(input_button, input_button_rect)

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
