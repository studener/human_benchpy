import pygame
import numpy as np
import time

pygame.init()

screen = pygame.display.set_mode((720,720))
sound = pygame.mixer.Sound('assets/sound.mp3')
font = pygame.font.Font(size=75)
points_font = pygame.font.Font(size=1000)
screen.fill("#57B7F3")
start_text = font.render('CLICK TO PLAY', True, 'white')
text_pos = start_text.get_rect(center = pygame.display.get_surface().get_rect().center)
screen.blit(start_text, text_pos)
pygame.display.flip()
clock = pygame.time.Clock()

# Variables
done = False # Puts game loop on hold until mouse has been clicked required number of times
rounds = [] # stores which buttons lit up
rounds_copy = [1] # copy of rounds, of which elements get removed to check if right square was clicked
counter = -1 # keep track of how many times mouse has been clicked
squares = {'one':[15,15,220,220], 'two':[250,15,220,220], 'three':[485,15,220,220], 
           'four':[15,250,220,220], 'five':[250,250,220,220], 'six':[485,250,220,220], 
           'seven':[15,485,220,220], 'eight':[250,485,220,220], 'nine':[485,485,220,220]}
last_item = set(['a'])

while True:
    # Process player inputs.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            square = rounds_copy.pop(0)
            if counter == -1:
                done = True
            elif squares[square][0] < pygame.mouse.get_pos()[0] < squares[square][0] + 220 and squares[square][1] < pygame.mouse.get_pos()[1] < squares[square][1] + 220:
                counter -= 1
                pygame.draw.rect(screen, 'white', squares[square],border_radius=20)
                sound.play()
                pygame.display.flip()
                time.sleep(0.3)
                pygame.draw.rect(screen, '#3478C6', squares[square],border_radius=20)
                pygame.display.flip()
                if counter == 0:
                    screen.fill("#4A97C7")
                    for i in squares:
                        pygame.draw.rect(screen, '#3478C6', squares[i],border_radius=20)
            else:
                # This is what happens when you lose
                screen.fill("#FF0000")
                points = points_font.render(f'{len(rounds)-1}', True, '#B50012')
                points_pos = points.get_rect(center = pygame.display.get_surface().get_rect().center)
                screen.blit(points, points_pos)
                # screen.blit(font.render('THIS WINDOW WILL CLOSE IN 5 SECONDS', True, 'white'), (10, 400))
                pygame.display.flip()
                print(f'\nYou lost. Score: {len(rounds)-1}')
                time.sleep(3)
                pygame.quit()
                raise SystemExit

            if counter == 0:
                done = True

        while done == True:
            time.sleep(0.8)
            done = False

            # draw screen and squares
            screen.fill("#57B7F3")
            for i in squares:
                pygame.draw.rect(screen, '#3478C6', squares[i],border_radius=20)

            pygame.display.flip()

            if len(rounds): # make sure there are no direct repeats
                last_item = set(rounds[-1])
            rounds.append(np.random.choice(list(set(squares.keys()).difference(last_item))))
            rounds_copy = rounds.copy()
            counter = len(rounds)
            
            for i in range(len(rounds)):
                time.sleep(0.2)
                pygame.draw.rect(screen, 'white', squares[rounds[i]],border_radius=20)
                sound.play()
                pygame.display.flip()
                time.sleep(0.7)
                pygame.draw.rect(screen, '#3478C6', squares[rounds[i]],border_radius=20)
                pygame.display.flip()

            pygame.display.flip()  # Refresh on-screen display

    clock.tick(60)         # wait until next frame (at 60 FPS)
