from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from Generator import Generator
    from Survivor import Survivor


class Toolbox:
    def __init__(self, charges: int, speed: float):
        self.baseCharges = charges
        self.speedBonusPercent = speed
        self.depleted = False

    def repairGen(self, target: Generator, survivor: Survivor):
        chargesToAdd = 1 + self.speedBonusPercent
        if not (self.baseCharges >= chargesToAdd):
            if (self.depleted == False):
                # print("Toolbox: Now depleted")
                self.depleted = True
        if (self.depleted):
            self.repairWithoutBox(target, survivor)
            return
        self.baseCharges -= chargesToAdd
        # print("Toolbox: Transferring " + str(chargesToAdd) + " charges to gen")
        # print("Toolbox: " + str(self.baseCharges) + " charges remaining")
        target.addCharges(chargesToAdd, survivor)

    def getIsDepleted(self):
        return self.depleted

    def repairWithoutBox(self, target: Generator, survivor: Survivor):
        # print("Toolbox: Repairing 1 charge by hand")
        target.addCharges(1, survivor)
