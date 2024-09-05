import random
from numpy import cos, pi, sin
import pygame


def initGame():
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    clock = pygame.time.Clock()
    font = pygame.font.Font('freesansbold.ttf', 24)
    running = True
    dt = 0.00001

    posclock = [0.0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    posclock[12] = pi/2
    posclock[1] = pi/3
    posclock[2] = pi/6
    posclock[3] = 0
    posclock[4] = 11*pi/6
    posclock[5] = 5*pi/3
    posclock[6] = 3*pi/2
    posclock[7] = 4*pi/3
    posclock[8] = 7*pi/6
    posclock[9] = pi
    posclock[10] = 5*pi/6
    posclock[11] = 2 * pi/3

    startingPos = posclock[8]
    greatZone = 0.03
    goodZone = 0.13

    lineStartX = 200
    lineStartY = 62

    lineEndX = 200
    lineEndY = 150

    originX = 200
    originY = 200

    theta = 0

    rotTime = 1.1
    dRotTime = rotTime

    fails = 0
    success = 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:

                    if startingPos - 1.57 - (greatZone * 2 * pi) <= 2 * pi - theta:
                        if 2 * pi - theta <= startingPos - 1.57:
                            success += 1
                            if success <= 6:
                                rotTime = rotTime * (1 / (1 + 0.04))
                            startingPos = posclock[random.randint(4, 10)]
                            theta = 0
                        else:
                            fails += 1
                            rotTime = dRotTime
                            success = 0
                            startingPos = posclock[random.randint(4, 10)]
                            theta = 0
                    else:
                        fails += 1
                        rotTime = dRotTime
                        success = 0
                        startingPos = posclock[random.randint(4, 10)]
                        theta = 0

        theta += 2*pi / (rotTime * 1/dt)

        screen.fill("black")
        text = font.render("Fails: " + str(fails) + " Success: " + str(success) + "RotTime: " + str(round(rotTime, 4)) + " Endpos: " + str(round(startingPos - 1.57, 4)) + " Startpos: " + str(round(startingPos - 1.57 - (goodZone * 2 * pi), 4))+" Theta: " + str(round((2 * pi - theta), 4)) + " FPS: " +
                           str(round(1 / dt, 4)), True, (120, 120, 120))
        text2 = font.render(str(success), True, (120, 120, 120))
        textRect = text.get_rect()
        text2Rect = text2.get_rect()
        text2Rect.center = (200, 200)

        screen.blit(text, textRect)
        screen.blit(text2, text2Rect)

        if startingPos - 1.57 - (greatZone * 2 * pi) <= 2 * pi - theta:
            if 2 * pi - theta <= startingPos - 1.57:
                lineColor = (0, 200, 0)
            else:
                lineColor = (200, 0, 0)
        else:
            lineColor = (200, 0, 0)

        pygame.draw.circle(screen, (255, 255, 255), (200, 200), 95, 2)

        pygame.draw.arc(screen, (122, 122, 122), [
                        100, 100, 200, 200], startingPos - (goodZone * 2 * pi), startingPos, 7)

        pygame.draw.arc(screen, (255, 255, 255), [
                        100, 100, 200, 200], startingPos - (greatZone * 2 * pi), startingPos, 7)

        pygame.draw.line(screen, lineColor, (originX + ((lineStartX - originX) * cos(theta) - (lineStartY - originY) *
                                                        sin(theta)), originY + ((lineStartX - originX) * sin(theta) + (lineStartY - originY) * cos(theta))), (originX + ((lineEndX - originX) * cos(theta) - (lineEndY - originY) *
                                                                                                                                                                         sin(theta)), originY + ((lineEndX - originX) * sin(theta) + (lineEndY - originY) * cos(theta))), 5)

        if startingPos - 1.57 - (goodZone * 2 * pi) >= 2 * pi - theta:
            fails += 1
            rotTime = dRotTime
            success = 0
            startingPos = posclock[random.randint(4, 10)]
            theta = 0

        pygame.display.flip()
        dt = clock.tick(144) / 1000


initGame()
