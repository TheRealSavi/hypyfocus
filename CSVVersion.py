from dataclasses import dataclass

from Skillcheck import SkillCheck
from Toolbox import Toolbox
from Survivor import Survivor
from Generator import Generator
import pandas as pd


@dataclass
class SimResult:
    frames: int
    skillchecks: int
    greatHit: int
    missSk: int
    toolBox: bool
    toolBoxSpeed: float
    toolBoxCharges: int
    hyperfocus: bool
    skill: float


def simGen(gen: Generator, survivor: Survivor):
    frames = 0  # current simultions frames

    while not gen.isCompleted():
        frames += 1  # if the gen isnt completed simulate another frame and count it
        survivor.repair(gen)  # simulate the frame

    # print("Gen completion took " + str(frames) + " seconds")
    # print("Great Skillchecks hit: " + str(gen.getSkillCheckCount()))

    return SimResult(frames=frames, 
                     skillchecks=survivor.getSkillCheckInstance().skCount,
                     greatHit=survivor.getSkillCheckInstance().greatCount, 
                     missSk= survivor.getSkillCheckInstance().skCount - survivor.getSkillCheckInstance().greatCount - survivor.getSkillCheckInstance().goodCount,
                     toolBox=survivor.getItem().speedBonusPercent != 0,
                     toolBoxSpeed=survivor.getItem().speedBonusPercent,
                     toolBoxCharges=survivor.getItem().maxCharges,
                     hyperfocus=survivor.hyperfocusEnabled,
                     skill=survivor.skill
                     )


def runSim():
    simCount = 4000  # Number of simulations to run per arg set
    
    skill_args = [0.2, 0.8, 1.0, 3.0]

    # Simulation argument sets
    sim_args = [
        (False, False),
        (False, True),
        (True, False),
        (True, True),
    ]
    
    results = []

    # Perform simulations
    
    for skill in skill_args:
        for useHyperfocus, useToolbox in sim_args:
            for _ in range(simCount):
                result = simGen(Generator(), Survivor(Toolbox(32, 0.5) if useToolbox else Toolbox(0, 0), useHyperfocus, skill))
                results.append(result.__dict__)
                print(f"{len(results)} / {simCount * 16}")
        
    df = pd.DataFrame(results)
    df.to_csv("simResults.csv", index= False)






if __name__ == '__main__':
    runSim()

