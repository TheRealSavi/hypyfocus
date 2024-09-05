import math
import random
from numpy import pi
import pygame


def initGame():
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    clock = pygame.time.Clock()
    font = pygame.font.Font('freesansbold.ttf', 24)
    running = True

    posclock: list[float] = [0.0] * 13
    posclock[12] = 0.0 + (pi / 2)
    posclock[11] = pi/6 + (pi / 2)
    posclock[10] = pi/3 + (pi / 2)
    posclock[9] = pi/2 + (pi / 2)
    posclock[8] = 2*pi/3 + (pi / 2)
    posclock[7] = 5*pi/6 + (pi / 2)
    posclock[6] = pi + (pi / 2)
    posclock[5] = 7*pi/6 + (pi / 2)
    posclock[4] = 4*pi/3 + (pi / 2)
    posclock[3] = 3*pi/2 + (pi / 2)
    posclock[2] = 5*pi/3 + (pi / 2)
    posclock[1] = 11*pi/6 + (pi / 2)

    startingPos = posclock[12]

    theta = startingPos

    skOrigin = [int(1280/2), int(720/2)]
    skRadius = 200

    skEarliestPos = 4
    skLatestPos = 10

    skPosClock = random.randint(skEarliestPos, skLatestPos)
    skPos = posclock[skPosClock]

    lineOrigin = [0, 0]

    greatZone = 0.03
    goodZone = 0.13

    rotTime = 1.1
    dRotTime = rotTime

    consecGreats = 0
    inGoodZone = False
    inGreatZone = False

    prevTime = pygame.time.get_ticks()

    while running:

        cTime = pygame.time.get_ticks()
        deltaTime = (cTime - prevTime) / 1000
        prevTime = cTime
        if deltaTime == 0:
            continue

        if theta <= skPos:
            if theta >= skPos - (greatZone * 2 * pi):
                inGreatZone = True
            else:
                inGreatZone = False
        else:
            inGreatZone = False

        if theta < skPos - (greatZone * 2 * pi):
            if theta >= skPos - (greatZone * 2 * pi) - (goodZone * 2 * pi):
                inGoodZone = True
            else:
                inGoodZone = False
        else:
            inGoodZone = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if inGreatZone:
                        consecGreats += 1
                        skPosClock = random.randint(skEarliestPos, skLatestPos)
                        skPos = posclock[skPosClock]
                        theta = startingPos
                    elif inGoodZone:
                        consecGreats = 0
                        skPosClock = random.randint(skEarliestPos, skLatestPos)
                        skPos = posclock[skPosClock]
                        theta = startingPos
                    else:
                        consecGreats = 0
                        skPosClock = random.randint(skEarliestPos, skLatestPos)
                        skPos = posclock[skPosClock]
                        theta = startingPos

        theta -= (2 * pi / rotTime) * deltaTime
        theta %= 2 * math.pi

        screen.fill("black")

        infoText = font.render(
            f"Consec Great: {consecGreats:02d} "
            f"RotTime: {rotTime:06.3f} "
            f"SkClock: {skPosClock} "
            f"In Great: {inGreatZone}"
            f"In Good: {inGoodZone}"
            f"Theta: {theta:06.3f} "

            f"FPS: {1 / deltaTime:05.2f} "
            f"Delta Time: {deltaTime:06.2f}",
            True,
            (120, 120, 120)
        )

        skText = font.render("[Space]", True, (120, 120, 120))

        infoTextRect = infoText.get_rect()
        skTextRect = skText.get_rect()

        skTextRect.center = (skOrigin[0], skOrigin[1])

        screen.blit(infoText, infoTextRect)
        screen.blit(skText, skTextRect)

        lineColor = (200, 0, 0)
        if inGreatZone:
            lineColor = (0, 200, 0)
        if inGoodZone:
            lineColor = (0, 0, 200)

        pygame.draw.circle(screen, (255, 0, 255), (skOrigin[0], skOrigin[1]), skRadius, 2)

        # good zone
        pygame.draw.arc(screen, (122, 122, 122),
                        pygame.Rect(skOrigin[0] - skRadius, skOrigin[1] - skRadius, skRadius * 2, skRadius * 2),
                        skPos - (greatZone * 2 * pi) - (goodZone * 2 * pi),
                        skPos - (greatZone * 2 * pi), 7)

        # great zone
        pygame.draw.arc(screen, (220, 220, 220),
                        pygame.Rect(skOrigin[0] - skRadius, skOrigin[1] - skRadius, skRadius * 2, skRadius * 2),
                        skPos - (greatZone * 2 * pi),
                        skPos, 7)

        pygame.draw.line(screen, lineColor, (skOrigin[0], skOrigin[1]),
                         (skOrigin[0] + skRadius * math.cos(theta),
                          skOrigin[1] - skRadius * math.sin(theta)), 5)

        pygame.display.flip()
        clock.tick(700)
    # end game loop


initGame()
