from __future__ import annotations
from typing import TYPE_CHECKING, Union


if TYPE_CHECKING:
    from Survivor import Survivor

class Generator:
    def __init__(self):
        self.heldCharges = 0.0
        self.maxCharges = 90.0
        self.completed = False
        self.skillCheckCount = 0
        self.framesSinceLastSKAttempt = 999999999

    def addCharges(self, charges: float, survivor: Survivor, toolbox = None):
        from CSVVersion import SIM_FPS
        # print("Generator: Adding " + str(charges) + " charges")
        self.heldCharges += charges

        if not (self.getIsComplete()):
            if (self.framesSinceLastSKAttempt >= SIM_FPS):
                survivor.getSkillCheckInstance().attemptTrigger(self, survivor, toolbox)
                self.framesSinceLastSKAttempt = 0
            else:
                self.framesSinceLastSKAttempt += 1

    def addChargesFromSkillcheck(self, charges: float):
        self.heldCharges += charges
        self.skillCheckCount += 1
        self.getIsComplete()

    def removeCharges(self, charges: float):
        self.heldCharges -= charges

    def getMaxCharges(self):
        return self.maxCharges

    def getSkillCheckCount(self):
        return self.skillCheckCount

    def getPercentOfCurrent(self, percent: float):
        return self.heldCharges * percent

    def getCompleteionPercentage(self):
        return self.heldCharges / self.maxCharges

    def isCompleted(self):
        return self.completed

    def getIsComplete(self):
        # print("Generator: Gen has " + str(self.heldCharges) + " charges")
        if (self.heldCharges >= self.maxCharges):
            self.completed = True
            # print("Generator: Gen complete")
            return True
        return False
