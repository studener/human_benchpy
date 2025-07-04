# TODO: add blinking cursor, loosing screen looks bad, game breaks when submitting string
import numpy as np
import pandas as pd
import pygame
from plot_scores import make_plot

pygame.init()

pygame.display.set_caption('Number Memory')
icon = pygame.image.load('assets/icon.png')
pygame.display.set_icon(icon)

screen = pygame.display.set_mode((720,720))
font = pygame.font.Font(size=100)
points_font = pygame.font.Font(size=1000)
title = pygame.font.Font(size=75)

screen.fill('#57B7F3')
start_text = title.render('CLICK TO PLAY', True, 'white')
text_pos = start_text.get_rect(center = pygame.display.get_surface().get_rect().center)
screen.blit(start_text, text_pos)
pygame.display.flip()
clock = pygame.time.Clock()

# Variables
done = False # These 3 are to execute according action
countdown = False
player = False
lost = False
timer = 0 # mainly for timer bar
digits = 1 # length of number
number = 0 # current number
guess = '' # stores guess as string

while True:
    # Process player inputs.
    if number > -1:
        for event in pygame.event.get():
            if player:
                screen.fill('#57B7F3')
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
                        print(f'\nThe longest number you remembered was {digits-2} digits.')
                        lost = True
                        lost_clicked = 0
                        number = -1

                elif event.key == pygame.K_BACKSPACE:
                    guess = guess[:-1]
                else:
                    guess += event.unicode
            
    if done:
        done = False
        player = False
        countdown = True

        # draw screen
        screen.fill('#57B7F3')
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
            screen.fill('#57B7F3')
            pygame.draw.rect(screen, '#3478C6', (100, 315, 520, 80), border_radius=5)
            pygame.display.flip()

    if lost:
        if lost_clicked == 0:
            screen.fill('#FF0000')
            points = points_font.render(f'{digits-2}', True, '#B50012')
            points_pos = points.get_rect(center = pygame.display.get_surface().get_rect().center)
            screen.blit(points, points_pos)
            pygame.display.flip()

        if lost_clicked == 1:
            df = pd.DataFrame({'Score':[digits-2]})
            df.to_csv('scores/number_memory.csv', mode='a', index=False, header=False)
            make_plot('number_memory')

            hist = pygame.image.load('scores/number_memory.png')
            screen.fill('#FFFFFF')
            screen.blit(hist, (0,60))
            pygame.display.flip()
            lost_clicked += 1
        
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                lost_clicked += 1
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit

    clock.tick(60)         # wait until next frame (at 60 FPS)
