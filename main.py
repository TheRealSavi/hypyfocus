import random
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde
from numpy import cos, linspace, sin
import pygame
import time


class Generator:
    def __init__(self):
        self.heldCharges = 0
        self.maxCharges = 90
        self.completed = False
        self.skillCheckCount = 0

    def addCharges(self, charges, survivor):
        print("Generator: Adding " + str(charges) + " charges")
        self.heldCharges += charges
        if not (survivor.getItem().getIsDepleted()):
            beingDoneWithToolbox = True
        else:
            beingDoneWithToolbox = False

        if not (self.getIsComplete()):
            survivor.getSkillCheckInstance().attemptTrigger(
                self, beingDoneWithToolbox, survivor)

    def addChargesFromSkillcheck(self, charges):
        self.heldCharges += charges
        self.skillCheckCount += 1
        self.getIsComplete()

    def removeCharges(self, charges):
        self.heldCharges -= charges

    def getMaxCharges(self):
        return self.maxCharges

    def getSkillCheckCount(self):
        return self.skillCheckCount

    def getPercentOfCurrent(self, percent):
        return self.heldCharges * percent

    def getCompleteionPercentage(self):
        return self.heldCharges / self.maxCharges

    def isCompleted(self):
        return self.completed

    def getIsComplete(self):
        print("Generator: Gen has " + str(self.heldCharges) + " charges")
        if (self.heldCharges >= self.maxCharges):
            self.completed = True
            print("Generator: Gen complete")
            return True
        return False


class SkillCheck:
    def __init__(self):
        self.baseTriggerChance = 0.08
        self.triggerChanceWToolbox = 0.4
        self.baseGreatBonusPercent = 0.01
        self.greatBonusPercent = self.baseGreatBonusPercent
        self.activeTime = 1.1

    def increaseRotationSpeedByPercent(self, percent):
        self.activeTime = self.activeTime * (1 / (1 + percent))
        print("SkillCheck: Increase Rotation Speed By " + str(percent) + "%")
        print("SkillCheck: Active Time is now " +
              str(self.activeTime) + " seconds")

    def increaseBonusPercentByPercent(self, percent):
        self.greatBonusPercent += self.baseGreatBonusPercent * percent
        print("SkillCheck: Increase Bonus by " + str(percent) + "%")
        print("SkillCheck: Bonus is now " + str(self.greatBonusPercent) + "%")

    def increaseTriggerChanceByPercent(self, percent):
        self.baseTriggerChance += percent
        self.triggerChanceWToolbox += percent
        print("SkillCheck: Increase Trigger Chance by " + str(percent) + "%")
        print("SkillCheck: Base Trigger Chance is now " +
              str(self.baseTriggerChance) + "%")
        print("SkillCheck: Toolbox Trigger Chance is now " +
              str(self.triggerChanceWToolbox) + "%")

    def attemptTrigger(self, target, withToolbox, survivor):
        print("SkillCheck: Attempting skill check trigger")
        triggerChance = self.baseTriggerChance
        if (withToolbox):
            print("SkillCheck: Using toolbox Odds")
            triggerChance = self.triggerChanceWToolbox
        triggered = random.uniform(0, 1) <= triggerChance
        if (triggered):
            print("SkillCheck: Skill check triggered")
            bonusCharges = target.getMaxCharges() * self.greatBonusPercent
            print("SkillCheck: Adding " + str(bonusCharges) + " charges")
            target.addChargesFromSkillcheck(bonusCharges)
            survivor.getHyperfocus().addToken(self)
        else:
            print("SkillCheck: SkillCheck not triggered")


class Hyperfocus:
    def __init__(self, startingTokens):
        self.tokens = startingTokens
        self.maxTokens = 6
        self.increaseTriggerChanceBy = 0.04
        self.increaseRotationSpeedBy = 0.04
        self.increaseBonusBy = 0.3

    def addToken(self, target):
        if (self.tokens >= self.maxTokens):
            return
        self.tokens += 1
        print("Hyperfocus: Now has " + str(self.tokens) + " tokens")
        target.increaseRotationSpeedByPercent(self.increaseRotationSpeedBy)
        target.increaseBonusPercentByPercent(self.increaseBonusBy)
        target.increaseTriggerChanceByPercent(self.increaseTriggerChanceBy)


class Toolbox:
    def __init__(self, charges, speed):
        self.baseCharges = charges
        self.speedBonusPercent = speed
        self.depleted = False

    def repairGen(self, target, survivor):
        chargesToAdd = 1 + self.speedBonusPercent
        if not (self.baseCharges >= chargesToAdd):
            if (self.depleted == False):
                print("Toolbox: Now depleted")
                self.depleted = True
        if (self.depleted):
            self.repairWithoutBox(target, survivor)
            return
        self.baseCharges -= chargesToAdd
        print("Toolbox: Transferring " + str(chargesToAdd) + " charges to gen")
        print("Toolbox: " + str(self.baseCharges) + " charges remaining")
        target.addCharges(chargesToAdd, survivor)

    def getIsDepleted(self):
        return self.depleted

    def repairWithoutBox(self, target, survivor):
        print("Toolbox: Repairing 1 charge by hand")
        target.addCharges(1, survivor)


class Survivor:
    def __init__(self, item, hyperFocusTokens):
        self.item = item
        self.skillCheckInstance = SkillCheck()
        self.hyperfocus = Hyperfocus(hyperFocusTokens)

    def repair(self, gen):
        self.item.repairGen(gen, self)

    def getItem(self):
        return self.item

    def getSkillCheckInstance(self):
        return self.skillCheckInstance

    def getHyperfocus(self):
        return self.hyperfocus


iterCount = 3000

basetime = []
baseskck = []
tbtime = []
tbskck = []
hyptime = []
hypskck = []
tbhytime = []
tbhyskck = []


pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True

posclock = [0.0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

posclock[12] = 3.14/2
posclock[1] = 3.14/3
posclock[2] = 3.14/6
posclock[3] = 0
posclock[4] = 11*3.14/6
posclock[5] = 5*3.14/3
posclock[6] = 3*3.14/2
posclock[7] = 4*3.14/3
posclock[8] = 7*3.14/6
posclock[9] = 3.14
posclock[10] = 5*3.14/6
posclock[11] = 2 * 3.14/3

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

dt = 0.00001

fails = 0
success = 0

font = pygame.font.Font('freesansbold.ttf', 24)

while not running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if startingPos - 1.57 - (greatZone * 6.28) <= 6.28 - theta:
                    if 6.28 - theta <= startingPos - 1.57:
                        success += 1
                        if success <= 6:
                            rotTime = rotTime * (1 / (1 + 0.04))
                        startingPos = posclock[random.randint(4, 10)]
                        theta = 0
                    else:
                        fails += 1
                        rotTime = 1.1
                        success = 0
                        startingPos = posclock[random.randint(4, 10)]
                        theta = 0
                else:
                    fails += 1
                    rotTime = 1.1
                    success = 0
                    startingPos = posclock[random.randint(4, 10)]
                    theta = 0

    theta += 6.28 / (rotTime * 1/dt)

    screen.fill("black")
    text = font.render("Fails: " + str(fails) + " Success: " + str(success) + "RotTime: " + str(round(rotTime, 4)) + " Endpos: " + str(round(startingPos - 1.57, 4)) + " Startpos: " + str(round(startingPos - 1.57 - (goodZone * 6.28), 4))+" Theta: " + str(round((6.28 - theta), 4)) + " FPS: " +
                       str(round(1 / dt, 4)), True, (120, 120, 120))
    text2 = font.render(str(success), True, (120, 120, 120))
    textRect = text.get_rect()
    text2Rect = text2.get_rect()
    text2Rect.center = (200, 200)

    screen.blit(text, textRect)
    screen.blit(text2, text2Rect)

    pygame.draw.circle(screen, (255, 255, 255), (200, 200), 95, 2)

    pygame.draw.arc(screen, (122, 122, 122), [
                    100, 100, 200, 200], startingPos - (goodZone * 6.28), startingPos, 7)

    pygame.draw.arc(screen, (255, 255, 255), [
                    100, 100, 200, 200], startingPos - (greatZone * 6.28), startingPos, 7)

    pygame.draw.line(screen, (200, 0, 0), (originX + ((lineStartX - originX) * cos(theta) - (lineStartY - originY) *
                     sin(theta)), originY + ((lineStartX - originX) * sin(theta) + (lineStartY - originY) * cos(theta))), (originX + ((lineEndX - originX) * cos(theta) - (lineEndY - originY) *
                                                                                                                                      sin(theta)), originY + ((lineEndX - originX) * sin(theta) + (lineEndY - originY) * cos(theta))), 5)

    if startingPos - 1.57 - (goodZone * 6.28) >= 6.28 - theta:
        fails += 1
        rotTime = 1.1
        success = 0
        startingPos = posclock[random.randint(4, 10)]
        theta = 0

    pygame.display.flip()
    dt = clock.tick(144) / 1000


def runSim():
    i = 0
    # base
    while i < iterCount:
        frames = 0
        gen1 = Generator()
        sur1 = Survivor(Toolbox(0, 0), 6)

        while not gen1.isCompleted():
            print("")
            frames += 1
            sur1.repair(gen1)
        print("Gen completion took " + str(frames) + " seconds")
        print("Great Skillchecks hit: " + str(gen1.getSkillCheckCount()))
        basetime.append(frames)
        baseskck.append(gen1.getSkillCheckCount())
        i += 1
    i = 0

    # tb
    while i < iterCount:
        frames = 0
        gen1 = Generator()
        sur1 = Survivor(Toolbox(32, 0.5), 6)

        while not gen1.isCompleted():
            print("")
            frames += 1
            sur1.repair(gen1)
        print("Gen completion took " + str(frames) + " seconds")
        print("Great Skillchecks hit: " + str(gen1.getSkillCheckCount()))
        tbtime.append(frames)
        tbskck.append(gen1.getSkillCheckCount())
        i += 1
    i = 0

    # hyp
    while i < iterCount:
        frames = 0
        gen1 = Generator()
        sur1 = Survivor(Toolbox(0, 0), 0)

        while not gen1.isCompleted():
            print("")
            frames += 1
            sur1.repair(gen1)
        print("Gen completion took " + str(frames) + " seconds")
        print("Great Skillchecks hit: " + str(gen1.getSkillCheckCount()))
        hyptime.append(frames)
        hypskck.append(gen1.getSkillCheckCount())
        i += 1
    i = 0

    # tbhy
    while i < iterCount:
        frames = 0
        gen1 = Generator()
        sur1 = Survivor(Toolbox(32, 0.5), 0)

        while not gen1.isCompleted():
            print("")
            frames += 1
            sur1.repair(gen1)
        print("Gen completion took " + str(frames) + " seconds")
        print("Great Skillchecks hit: " + str(gen1.getSkillCheckCount()))
        tbhytime.append(frames)
        tbhyskck.append(gen1.getSkillCheckCount())
        i += 1
    i = 0


def createGraphs():
    # this create the kernel, given an array it will estimate the probability over that values
    kdebasetime = gaussian_kde(basetime)
    kdebaseskck = gaussian_kde(baseskck)
    kdetbtime = gaussian_kde(tbtime)
    kdetbskck = gaussian_kde(tbskck)
    kdehyptime = gaussian_kde(hyptime)
    kdehypskck = gaussian_kde(hypskck)
    kdetbhytime = gaussian_kde(tbhytime)
    kdetbhyskck = gaussian_kde(tbhyskck)

    # these are the values over wich your kernel will be evaluated
    dist_spacetime = linspace(0, 90, 100)
    dist_spaceskck = linspace(0, 30, 100)

    # create subplots
    fig, axs = plt.subplots(4, 2)

    axs[0, 0].plot(dist_spacetime, kdebasetime(dist_spacetime))
    axs[0, 0].set_title('Base time')

    axs[0, 1].plot(dist_spaceskck, kdebaseskck(dist_spaceskck))
    axs[0, 1].set_title('Base Skillchecks')

    axs[1, 0].plot(dist_spacetime, kdetbtime(dist_spacetime))
    axs[1, 0].set_title('Toolbox time')

    axs[1, 1].plot(dist_spaceskck, kdetbskck(dist_spaceskck))
    axs[1, 1].set_title('Toolbox Skillchecks')

    axs[2, 0].plot(dist_spacetime, kdehyptime(dist_spacetime))
    axs[2, 0].set_title('Hyperfocus time')

    axs[2, 1].plot(dist_spaceskck, kdehypskck(dist_spaceskck))
    axs[2, 1].set_title('Hyperfocus Skillchecks')

    axs[3, 0].plot(dist_spacetime, kdetbhytime(dist_spacetime))
    axs[3, 0].set_title('Toolbox+Hyperfocus time')

    axs[3, 1].plot(dist_spaceskck, kdetbhyskck(dist_spaceskck))
    axs[3, 1].set_title('Toolbox+Hyperfocus Skillchecks')

    plt.show()

runSim()
createGraphs()
