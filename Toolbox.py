from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Generator import Generator
    from Survivor import Survivor


class Toolbox:
    def __init__(self, charges: int, speed: float):
        self.heldCharges = charges
        self.maxCharges = charges
        self.speedBonusPercent = speed
        self.depleted = False

    def repairGen(self, target: Generator, survivor: Survivor):
        from CSVVersion import SIM_FPS
        chargesToAddPerSecond = 1 + self.speedBonusPercent
        chargesToAddPerFrame = chargesToAddPerSecond / SIM_FPS
        if (self.heldCharges < chargesToAddPerFrame):
            self.depleted = True
        else:
            self.depleted = False
        if (self.depleted):
            self.repairWithoutBox(target, survivor)
            return
        self.heldCharges -= chargesToAddPerFrame
        # print("Toolbox: Transferring " + str(chargesToAdd) + " charges to gen")
        # print("Toolbox: " + str(self.heldCharges) + " charges remaining")
        target.addCharges(chargesToAddPerFrame, survivor, self)

    def getIsDepleted(self):
        return self.depleted

    def repairWithoutBox(self, target: Generator, survivor: Survivor):
        from CSVVersion import SIM_FPS
        # print("Toolbox: Repairing 1 charge by hand")
        chargesToAddPerSecond = 1
        chargesToAddPerFrame = chargesToAddPerSecond / SIM_FPS
        target.addCharges(chargesToAddPerFrame, survivor)
