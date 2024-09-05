from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from Survivor import Survivor


class Generator:
    def __init__(self):
        self.heldCharges = 0.0
        self.maxCharges = 90
        self.completed = False
        self.skillCheckCount = 0

    def addCharges(self, charges: float, survivor: Survivor):
        # print("Generator: Adding " + str(charges) + " charges")
        self.heldCharges += charges
        if not (survivor.getItem().getIsDepleted()):
            beingDoneWithToolbox = True
        else:
            beingDoneWithToolbox = False

        if not (self.getIsComplete()):
            survivor.getSkillCheckInstance().attemptTrigger(self, beingDoneWithToolbox, survivor)

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
