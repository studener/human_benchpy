import pygame
import time
import numpy as np
import pandas as pd
from plot_scores import make_plot

pygame.init()

pygame.display.set_caption('Sequence Memory')
icon = pygame.image.load('assets/icon.png')
pygame.display.set_icon(icon)

screen = pygame.display.set_mode((720,720))
move_sound = pygame.mixer.Sound('assets/move.mp3')
win_sound = pygame.mixer.Sound('assets/win.mp3')
font = pygame.font.Font(size=75)
points_font = pygame.font.Font(size=1000)
screen.fill('#57B7F3')
start_text = font.render('CLICK TO PLAY', True, 'white')
text_pos = start_text.get_rect(center = pygame.display.get_surface().get_rect().center)
screen.blit(start_text, text_pos)
pygame.display.flip()
clock = pygame.time.Clock()

# Variables
player = True
done = False # Puts game loop on hold until mouse has been clicked required number of times
lost = False

rounds = [] # stores which buttons lit up
rounds_copy = [1] # copy of rounds, of which elements get removed to check if right square was clicked
counter = -1 # keep track of how many times mouse has been clicked
squares = {'one':[15,15,220,220], 'two':[250,15,220,220], 'three':[485,15,220,220], 
           'four':[15,250,220,220], 'five':[250,250,220,220], 'six':[485,250,220,220], 
           'seven':[15,485,220,220], 'eight':[250,485,220,220], 'nine':[485,485,220,220]}
last_item = set(['a'])

while True:
    # Process player inputs.
    if player:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                square = rounds_copy.pop(0)
                if counter == -1:
                    player = False
                    done = True
                elif squares[square][0] < pygame.mouse.get_pos()[0] < squares[square][0] + 220 and squares[square][1] < pygame.mouse.get_pos()[1] < squares[square][1] + 220:
                    counter -= 1
                    pygame.draw.rect(screen, 'white', squares[square],border_radius=20)
                    if counter == 0:
                        win_sound.play()
                    else:
                        move_sound.play()
                    pygame.display.flip()
                    time.sleep(0.4)
                    pygame.draw.rect(screen, '#3478C6', squares[square],border_radius=20)
                    pygame.display.flip()
                    if counter == 0:
                        screen.fill('#4A97C7')
                        for i in squares:
                            pygame.draw.rect(screen, '#3478C6', squares[i],border_radius=20)
                else:
                    # This is what happens when you lose
                    print(f'\nYou lost. Score: {len(rounds)-1}')
                    lost = True
                    lost_clicked = 0
                    player = False

                if counter == 0:
                    player = False
                    done = True
                    time.sleep(0.8)

    if done:
        done = False
        player = True

        # draw screen and squares
        screen.fill('#57B7F3')
        for i in squares:
            pygame.draw.rect(screen, '#3478C6', squares[i],border_radius=20)

        pygame.display.flip()

        if len(rounds): # make sure there are no direct repeats
            last_item = {rounds[-1]}
        rounds.append(np.random.choice(list(set(squares.keys()).difference(last_item))))
        rounds_copy = rounds.copy()
        counter = len(rounds)
        
        for i in range(len(rounds)):
            time.sleep(0.2)
            pygame.draw.rect(screen, 'white', squares[rounds[i]],border_radius=20)
            if i == len(rounds)-1:
                win_sound.play()
            else:
                move_sound.play()
            pygame.display.flip()
            time.sleep(0.4)
            pygame.draw.rect(screen, '#3478C6', squares[rounds[i]],border_radius=20)
            pygame.display.flip()

        pygame.event.clear()

    if lost:
        if lost_clicked == 0:
            screen.fill('#FF0000')
            points = points_font.render(f'{len(rounds)-1}', True, '#B50012')
            points_pos = points.get_rect(center = pygame.display.get_surface().get_rect().center)
            screen.blit(points, points_pos)
            pygame.display.flip()

        if lost_clicked == 1:
            df = pd.DataFrame({'Score':[len(rounds)-1]})
            df.to_csv('scores/sequence_memory.csv', mode='a', index=False, header=False)
            make_plot('sequence_memory')

            hist = pygame.image.load('scores/sequence_memory.png')
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
