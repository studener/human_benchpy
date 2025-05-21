import numpy as np
import pygame
import time

pygame.init()

screen = pygame.display.set_mode((720,720))
font = pygame.font.Font(size=75)
points_font = pygame.font.Font(size=150)

screen.fill("#57B7F3")
start_text = font.render('CLICK TO PLAY', True, 'white')
text_pos = start_text.get_rect(center = pygame.display.get_surface().get_rect().center)
screen.blit(start_text, text_pos)
pygame.display.flip()
clock = pygame.time.Clock()

# Variables
done = False # Puts game loop on hold until mouse has been clicked required number of times
rounds = 0 # stores which buttons lit up
xcord = 0
ycord = 0

while True:
    # Process player inputs.
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
                    done = True
                    rounds += 1

            else:
                # This is what happens after hitting all targets
                screen.fill("#57B7F3")
                interval = round((time.time()-start)/15, 2)
                points = points_font.render(f'{interval}s', True, '#FFFFFF')
                points_pos = points.get_rect(center = pygame.display.get_surface().get_rect().center)
                screen.blit(points, points_pos)
                # screen.blit(font.render('THIS WINDOW WILL CLOSE IN 5 SECONDS', True, 'white'), (10, 400))
                pygame.display.flip()
                print(f'\nAverage Time: {interval}s')
                time.sleep(3)
                pygame.quit()
                raise SystemExit

    if done:
        done = False

        # draw screen and circle
        screen.fill("#57B7F3")
        xcord, ycord = np.random.randint(low=50, high=670, size = 2)
        # pygame.draw.rect(screen, '#FFFFFF', (xcord,ycord,200,200),border_radius=100)
        pygame.draw.circle(screen, '#FFFFFF', (xcord, ycord), 50)
        pygame.display.flip()

    clock.tick(60)         # wait until next frame (at 60 FPS)
