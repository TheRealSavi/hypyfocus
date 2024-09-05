from dataclasses import dataclass
import time
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde
from numpy import linspace

from Toolbox import Toolbox
from Survivor import Survivor
from Generator import Generator


@dataclass
class SimResult:
    frames: int
    skillchecks: int
    name: str


def simStart(name: str, useHyperfocus: bool, useToolbox: bool):
    result = simGen(name, Generator(), Survivor(Toolbox(32, 0.5) if useToolbox else Toolbox(0, 0), useHyperfocus))
    return result


def simGen(name: str, gen: Generator, survivor: Survivor):
    frames = 0  # current simultions frames

    while not gen.isCompleted():
        frames += 1  # if the gen isnt completed simulate another frame and count it
        survivor.repair(gen)  # simulate the frame

    # print("Gen completion took " + str(frames) + " seconds")
    # print("Great Skillchecks hit: " + str(gen.getSkillCheckCount()))

    return SimResult(frames, gen.getSkillCheckCount(), name)


def runSim():
    simCount = 100000  # How many times to run each simulation

    # Arguments for the simulations
    base_args = ("base", False, False)
    toolbox_args = ("toolbox", False, True)
    hyperfocus_args = ("hyperfocus", True, False)
    hyperfocusToolbox_args = ("hyperfocus and toolbox", True, True)

    # Initialize result lists
    baseResults = []
    toolboxResults = []
    hyperfocusResults = []
    hyperfocusToolboxResults = []

    # Timing serial execution
    start_time = time.time()

    # Run base simulations
    for _ in range(simCount):
        result = simStart(*base_args)
        baseResults.append(result)

    # Run toolbox simulations
    for _ in range(simCount):
        result = simStart(*toolbox_args)
        toolboxResults.append(result)

    # Run hyperfocus simulations
    for _ in range(simCount):
        result = simStart(*hyperfocus_args)
        hyperfocusResults.append(result)

    # Run hyperfocus and toolbox simulations
    for _ in range(simCount):
        result = simStart(*hyperfocusToolbox_args)
        hyperfocusToolboxResults.append(result)

    end_time = time.time()
    print(f"Serial execution time: {end_time - start_time:.2f} seconds")

    createGraphs([baseResults, toolboxResults, hyperfocusResults, hyperfocusToolboxResults])


def createGraphs(simulations: list[list[SimResult]]):
    # values over which to evaluate a kernel
    dist_spaceTime = linspace(0, 90, 100)
    dist_spaceSkillcheck = linspace(0, 30, 100)

    # create subplots
    fig, axs = plt.subplots(simulations.__len__(), 2)

    nextOpenRow = 0

    for simulationResults in simulations:
        timeDataset = []
        skillcheckDataset = []
        for result in simulationResults:
            timeDataset.append(result.frames)
            skillcheckDataset.append(result.skillchecks)
        timeKDE = gaussian_kde(timeDataset)
        skillcheckKDE = gaussian_kde(skillcheckDataset)
        axs[nextOpenRow, 0].plot(dist_spaceTime, timeKDE(dist_spaceTime))
        axs[nextOpenRow, 0].set_title(result.name + ' time')
        axs[nextOpenRow, 1].plot(dist_spaceSkillcheck, skillcheckKDE(dist_spaceSkillcheck))
        axs[nextOpenRow, 1].set_title(result.name + ' skillchecks')
        nextOpenRow += 1

    plt.show()


if __name__ == '__main__':
    runSim()
