import numpy as np
import pandas as pd
import pygame
import time
from plot_scores import make_plot

pygame.init()

pygame.display.set_caption('Aim Trainer')
icon = pygame.image.load('assets/icon.png')
pygame.display.set_icon(icon)

screen = pygame.display.set_mode((720,720))
font = pygame.font.Font(size=75)
points_font = pygame.font.Font(size=150)

screen.fill('#57B7F3')
start_text = font.render('CLICK TO PLAY', True, 'white')
text_pos = start_text.get_rect(center = pygame.display.get_surface().get_rect().center)
screen.blit(start_text, text_pos)
pygame.display.flip()
clock = pygame.time.Clock()

# Variables
player = True
done = False # Puts game loop on hold until mouse has been clicked required number of times
finished = False
rounds = 0 # stores which buttons lit up
xcord = 0
ycord = 0

while True:
    # Process player inputs.
    if player:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if rounds == 0:
                    start = time.time()
                    rounds += 1
                    done = True

                elif rounds < 15:
                    x, y = pygame.mouse.get_pos()
                    if ((x-xcord)**2 + (y-ycord)**2)**(0.5) < 50:
                        player = False
                        done = True
                        rounds += 1

                else:
                    # This is what happens after hitting all targets
                    finished = True
                    finished_clicked = 0
                    player = False
                    interval = round((time.time()-start)/15, 3)
                    print(f'\nAverage Time: {interval}s')

    if done:
        player = True
        done = False

        # draw screen and circle
        screen.fill('#57B7F3')
        xcord, ycord = np.random.randint(low=50, high=670, size = 2)
        pygame.draw.circle(screen, '#FFFFFF', (xcord, ycord), 50)
        pygame.display.flip()

    if finished:
        if finished_clicked == 0:
            screen.fill('#57B7F3')
            points = points_font.render(f'{interval}s', True, '#FFFFFF')
            points_pos = points.get_rect(center = pygame.display.get_surface().get_rect().center)
            screen.blit(points, points_pos)
            pygame.display.flip()

        if finished_clicked == 1:
            df = pd.DataFrame({'Score':[int(interval*1000)]})
            df.to_csv('scores/aim_trainer.csv', mode='a', index=False, header=False)
            make_plot('aim_trainer')

            hist = pygame.image.load('scores/aim_trainer.png')
            screen.fill('#FFFFFF')
            screen.blit(hist, (0,60))
            pygame.display.flip()
            finished_clicked += 1
        
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                finished_clicked += 1
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit

    clock.tick(60)         # wait until next frame (at 60 FPS)
