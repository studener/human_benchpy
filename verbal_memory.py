import pygame
import time
import numpy as np

pygame.init()

screen = pygame.display.set_mode((720,720))
font = pygame.font.Font(size=75)
img = pygame.image.load('assets/verbmem.png')
points_font = pygame.font.Font(size=1000)
screen.fill("#57B7F3")
start_text = font.render('CLICK TO PLAY', True, 'white')
text_pos = start_text.get_rect(center = pygame.display.get_surface().get_rect().center)
screen.blit(start_text, text_pos)
pygame.display.flip()
clock = pygame.time.Clock()

# Variables
words = open("assets/words.txt", "r").readlines() # source for list of words: https://gist.github.com/cjhveal/3753018#file-gistfile1-txt
seen = []
truth = 'new'
rounds = -1 # counts number of rounds

done = False # Puts game loop on hold until mouse has been clicked required number of times

def clicked_half(x):
    if x <= 360:
        return "seen"
    return "new"

while True:
    # Process player inputs.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if rounds == -1:
                index = np.random.randint(0, len(words))
                word = words[index]
                print(word)
                del words[index]
                seen.append(word)

                screen.fill("#57B7F3")
                word = font.render(f'{word}', True, 'white')
                pos = word.get_rect(center = pygame.display.get_surface().get_rect().center)
                screen.blit(word, pos)
                screen.blit(img, (0,480))
                pygame.display.flip()
                truth = 'new'
                rounds = 0

            elif clicked_half(pygame.mouse.get_pos()[0]) == truth:
                done = True
                rounds += 1

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

        while done == True:
            done = False

            if np.random.randint(1, np.random.randint(3, 6)) == 1 and rounds > 1:
                # make sure new word isnt last word
                word = seen[np.random.randint(0, max(1, len(seen)-1))]
                del seen[seen.index(word)]
                seen.append(word)
                print(word)
                truth = 'seen'
            else:
                index = np.random.randint(0, len(words))
                word = words[index]
                print(word)
                del words[index]
                seen.append(word)
                truth = 'new'

            # draw screen and squares
            screen.fill("#57B7F3")
            word = font.render(f'{word}', True, 'white')
            pos = word.get_rect(center = pygame.display.get_surface().get_rect().center)
            screen.blit(word, pos)
            screen.blit(img, (0,480))

            pygame.display.flip()  # Refresh on-screen display

    clock.tick(60)         # wait until next frame (at 60 FPS)
