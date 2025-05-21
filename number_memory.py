# TODO: add blinking cursor, loosing screen looks bad
import numpy as np
import pygame
import time

pygame.init()

screen = pygame.display.set_mode((720,720))
font = pygame.font.Font(size=100)
title = pygame.font.Font(size=75)

screen.fill("#57B7F3")
start_text = title.render('CLICK TO PLAY', True, 'white')
text_pos = start_text.get_rect(center = pygame.display.get_surface().get_rect().center)
screen.blit(start_text, text_pos)
pygame.display.flip()
clock = pygame.time.Clock()

# Variables
done = False # These 3 are to execute according action
countdown = False
player = False
timer = 0 # mainly for timer bar
digits = 1 # length of number
number = 0 # current number
guess = '' # stores guess as string

while True:
    # Process player inputs.
    for event in pygame.event.get():
        if player:
            screen.fill("#57B7F3")
            pygame.draw.rect(screen, '#3478C6', (100, 315, 520, 80), border_radius=5)
            guessed = font.render(f'{guess}', True, '#FFFFFF')
            guess_pos = guessed.get_rect(center = pygame.display.get_surface().get_rect().center)
            screen.blit(guessed, guess_pos)

            pygame.display.flip()
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and digits == 1:
            done = True 
        if event.type == pygame.KEYDOWN and not countdown:
            if event.key == pygame.K_RETURN:
                if int(guess) == number:
                    countdown = True
                    done = True
                    guess = ''
                else: 
                    # Loosing Screen
                    screen.fill("#FF0000")
                    points = title.render(f'{digits-2}', True, '#B50012')
                    points_pos = points.get_rect(center = pygame.display.get_surface().get_rect().center)
                    screen.blit(points, points_pos)
                    pygame.display.flip()
                    print(f'\nThe longest number you remembered was {digits-2} digits.')
                    time.sleep(3)
                    pygame.quit()
                    raise SystemExit
            elif event.key == pygame.K_BACKSPACE:
                guess = guess[:-1]
            else:
                guess += event.unicode
            
    if done:
        done = False
        player = False
        countdown = True

        # draw screen
        screen.fill("#57B7F3")
        number = np.random.randint(10**(digits-1), 10**(digits))
        points = font.render(f'{number}', True, '#FFFFFF')
        points_pos = points.get_rect(center = pygame.display.get_surface().get_rect().center)
        screen.blit(points, points_pos)

        timer = 60+20*digits
        digits+=1

    if countdown:
        if timer > 0:
            timer -= 1
            pygame.draw.rect(screen, '#3478C6', (160, 500, 400, 10))
            pygame.draw.rect(screen, '#FFFFFF', (160, 500, np.floor(400*timer/(60+20*digits)), 10))
            pygame.display.flip()
        else:
            player = True
            countdown = False
            screen.fill("#57B7F3")
            pygame.draw.rect(screen, '#3478C6', (100, 315, 520, 80), border_radius=5)
            pygame.display.flip()

    clock.tick(60)         # wait until next frame (at 60 FPS)
