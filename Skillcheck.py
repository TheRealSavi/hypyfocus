from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from Generator import Generator
    from Survivor import Survivor

import random


class SkillCheck:

    def __init__(self):
        self.triggerChance = 0.08
        self.triggerChanceToolbox = 0.4
        self.bonusPercent = 0.01
        self.activeTime = 1.1

        self.dTriggerChance = self.triggerChance
        self.dTriggerChanceToolbox = self.triggerChanceToolbox
        self.dBonusPercent = self.bonusPercent
        self.dActiveTime = self.activeTime
        
        self.skCount = 0
        self.greatCount = 0
        self.goodCount = 0


    def increaseBaseRotationSpeedByPercent(self, percent: float):
        #assuming each stack doesnt incur its own 4% the perk sends a 
        # constant 1 modifier decrease
        #assuming dbd calculates rotationSpeed increases as a negative modifier
        #so that the active time can never reach 0
        self.activeTime = self.dActiveTime / (1 + percent)
        # print("SkillCheck: Increase Rotation Speed By " + str(percent) + "%")
        # print("SkillCheck: Active Time is now " + str(self.activeTime) + " seconds")

    def increaseBonusPercentByPercent(self, percent: float):
        self.bonusPercent += self.dBonusPercent * percent
        # print("SkillCheck: Increase Bonus by " + str(percent) + "%")
        # print("SkillCheck: Bonus is now " + str(self.greatBonusPercent) + "%")

    def increaseTriggerChanceByPercent(self, percent: float):
        #assuming it just adds the percent and isnt of base
        self.triggerChance += percent
        self.triggerChanceToolbox += percent
        # print("SkillCheck: Increase Trigger Chance by " + str(percent) + "%")
        # print("SkillCheck: Base Trigger Chance is now " + str(self.baseTriggerChance) + "%")
        # print("SkillCheck: Toolbox Trigger Chance is now " + str(self.triggerChanceWToolbox) + "%")

    def attemptTrigger(self, target: Generator, withToolbox: bool, survivor: Survivor):
        # print("SkillCheck: Attempting skill check trigger")
        triggerChance = self.triggerChance
        if (withToolbox):
            # print("SkillCheck: Using toolbox Odds")
            triggerChance = self.triggerChanceToolbox
        triggered = random.uniform(0, 1) <= triggerChance
        if (triggered):
            # print("SkillCheck: Skill check triggered")
            hitGreat = random.uniform(0, 1) <= survivor.skill * self.activeTime
            self.skCount += 1
            if (hitGreat):
                self.greatCount += 1
                bonusCharges = target.getMaxCharges() * self.bonusPercent
                # print("SkillCheck: Adding " + str(bonusCharges) + " charges")
                target.addChargesFromSkillcheck(bonusCharges)
                if survivor.hyperfocusEnabled:
                    survivor.getHyperfocus().addToken(self)
            elif random.uniform(0, 1) <= max((1 - survivor.skill), survivor.skill) * self.activeTime:
                self.goodCount +=1
                if survivor.hyperfocusEnabled:
                    survivor.getHyperfocus().reset()
                    self.reset()
            else:
                #miss
                if survivor.hyperfocusEnabled:
                    survivor.getHyperfocus().reset()
                    self.reset()
        else:
            # print("SkillCheck: SkillCheck not triggered")
            return

    def reset(self):
        self.triggerChance = self.dTriggerChance
        self.triggerChanceToolbox = self.dTriggerChanceToolbox
        self.bonusPercent = self.dBonusPercent
        self.activeTime = self.dActiveTime
