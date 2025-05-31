import pygame
import time
import numpy as np
import pandas as pd

pygame.init()

screen = pygame.display.set_mode((720,720))
move_sound = pygame.mixer.Sound('assets/move.mp3')
win_sound = pygame.mixer.Sound('assets/win.mp3')
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
rounds = 0 # counts number of rounds
displayed = [1] # saves lit up squares
counter = -1 # keep track of how many times mouse has been clicked
field_size = [3,3,4,4,4,5,5,5,6,6,6,6,6,7,7,7,7] # lets hope nobody gets further than this

def make_squares(n):
    gap = [15, 12, 10, 12, 13]
    size = [220, 165, 132, 106, 88]

    names = (np.arange(n**2)+1).astype(str)
    gaps = np.arange(1, n+1) * gap[n-3] + np.arange(n) * size[n-3]
    np.repeat(gaps, n)
    np.tile(gaps, n)

    return pd.DataFrame([np.tile(gaps, n), np.repeat(gaps, n), np.repeat(size[n-3], n**2), np.repeat(size[n-3], n**2)], columns=names).to_dict('list')

squares = make_squares(3)

def clicked_square(x,y):
    options = pd.DataFrame(np.array(list(squares.keys()),).reshape(int(len(squares)**(1/2)),int(len(squares)**(1/2))))
    axisvals = np.linspace(0, 720, options.shape[0]+1)[1:]
    return options.loc[list(y<axisvals), list(x<axisvals)].iloc[0,0]

while True:
    # Process player inputs.
    if not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                clicked = clicked_square(*pygame.mouse.get_pos())
                if counter == -1:
                    done = True
                elif clicked in displayed:
                    displayed = displayed[displayed != clicked] # make sure square cant be clicked multiple times
                    counter -= 1
                    square = clicked
                    pygame.draw.rect(screen, 'white', squares[square],border_radius=20)
                    if counter == 0:
                        win_sound.play()
                    else:
                        move_sound.play()
                    pygame.display.flip()

                else:
                    # This is what happens when you lose
                    screen.fill("#FF0000")
                    points = points_font.render(f'{rounds}', True, '#B50012')
                    points_pos = points.get_rect(center = pygame.display.get_surface().get_rect().center)
                    screen.blit(points, points_pos)
                    # screen.blit(font.render('THIS WINDOW WILL CLOSE IN 5 SECONDS', True, 'white'), (10, 400))
                    pygame.display.flip()
                    print(f'\nYou lost. Score: {rounds}')
                    time.sleep(3)
                    pygame.quit()
                    raise SystemExit

                if counter == 0:
                    rounds += 1
                    done = True
                    time.sleep(0.8)

    if done:
        done = False

        # draw screen and squares
        screen.fill("#57B7F3")
        pygame.display.flip()
        squares = make_squares(field_size[rounds])
        for i in squares:
            pygame.draw.rect(screen, '#3478C6', squares[i],border_radius=20)

        pygame.display.flip()
        time.sleep(0.5)

        displayed = np.random.choice(list(squares.keys()), replace=False, size=rounds+3)
        counter = len(displayed)
        
        for i in displayed:
            pygame.draw.rect(screen, 'white', squares[i],border_radius=20)
        
        pygame.display.flip()
        win_sound.play()
        time.sleep(1.5)

        screen.fill("#57B7F3")
        for i in squares:
            pygame.draw.rect(screen, '#3478C6', squares[i],border_radius=20)

        pygame.event.clear()
        pygame.display.flip()  # Refresh on-screen display

    clock.tick(60)         # wait until next frame (at 60 FPS)
