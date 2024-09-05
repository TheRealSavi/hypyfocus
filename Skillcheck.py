from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from Generator import Generator
    from Survivor import Survivor

import random


class SkillCheck:
    def __init__(self):
        self.baseTriggerChance = 0.08
        self.triggerChanceWToolbox = 0.4
        self.baseGreatBonusPercent = 0.01
        self.greatBonusPercent = self.baseGreatBonusPercent
        self.activeTime = 1.1

    def increaseRotationSpeedByPercent(self, percent: float):
        self.activeTime = self.activeTime * (1 / (1 + percent))
        # print("SkillCheck: Increase Rotation Speed By " + str(percent) + "%")
        # print("SkillCheck: Active Time is now " + str(self.activeTime) + " seconds")

    def increaseBonusPercentByPercent(self, percent: float):
        self.greatBonusPercent += self.baseGreatBonusPercent * percent
        # print("SkillCheck: Increase Bonus by " + str(percent) + "%")
        # print("SkillCheck: Bonus is now " + str(self.greatBonusPercent) + "%")

    def increaseTriggerChanceByPercent(self, percent: float):
        self.baseTriggerChance += percent
        self.triggerChanceWToolbox += percent
        # print("SkillCheck: Increase Trigger Chance by " + str(percent) + "%")
        # print("SkillCheck: Base Trigger Chance is now " + str(self.baseTriggerChance) + "%")
        # print("SkillCheck: Toolbox Trigger Chance is now " + str(self.triggerChanceWToolbox) + "%")

    def attemptTrigger(self, target: Generator, withToolbox: bool, survivor: Survivor):
        # print("SkillCheck: Attempting skill check trigger")
        triggerChance = self.baseTriggerChance
        if (withToolbox):
            # print("SkillCheck: Using toolbox Odds")
            triggerChance = self.triggerChanceWToolbox
        triggered = random.uniform(0, 1) <= triggerChance
        if (triggered):
            # print("SkillCheck: Skill check triggered")
            bonusCharges = target.getMaxCharges() * self.greatBonusPercent
            # print("SkillCheck: Adding " + str(bonusCharges) + " charges")
            target.addChargesFromSkillcheck(bonusCharges)
            if survivor.hyperfocusEnabled:
                survivor.getHyperfocus().addToken(self)
        else:
            # print("SkillCheck: SkillCheck not triggered")
            return
