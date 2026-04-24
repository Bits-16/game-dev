import pygame

pygame.init()

screen_width = 400
screen_height = 700
screen = pygame.display.set_mode((screen_width, screen_height), pygame.NOFRAME)

run = True

# Colours
bg = (135, 206, 235)
green = (80, 200, 120)

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False

    screen.fill(bg)

    pygame.display.update()

pygame.quit()
