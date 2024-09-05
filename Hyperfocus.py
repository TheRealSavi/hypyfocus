from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from Skillcheck import SkillCheck


class Hyperfocus:
    def __init__(self):
        self.tokens = 0
        self.maxTokens = 6
        self.increaseTriggerChanceBy = 0.04
        self.increaseRotationSpeedBy = 0.04
        self.increaseBonusBy = 0.3

    def addToken(self, target: SkillCheck):
        if (self.tokens >= self.maxTokens):
            return
        self.tokens += 1
        # print("Hyperfocus: Now has " + str(self.tokens) + " tokens")
        target.increaseRotationSpeedByPercent(self.increaseRotationSpeedBy)
        target.increaseBonusPercentByPercent(self.increaseBonusBy)
        target.increaseTriggerChanceByPercent(self.increaseTriggerChanceBy)
