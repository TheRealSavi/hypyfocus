from dataclasses import dataclass
import threading
import time
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde
from numpy import linspace
from matplotlib.animation import FuncAnimation
import tkinter as tk

from Skillcheck import SkillCheck
from Toolbox import Toolbox
from Survivor import Survivor
from Generator import Generator

plt.style.use('fivethirtyeight')
fig, axs = plt.subplots(4, 2)


class CircularBuffer:
    def __init__(self, size):
        self.size = size
        self.buffer = [None] * size
        self.start = 0
        self.count = 0

    def add(self, value):
        self.buffer[(self.start + self.count) % self.size] = value
        if self.count == self.size:
            self.start = (self.start + 1) % self.size  # Move the start pointer when the buffer is full
        else:
            self.count += 1

    def get(self):
        return [self.buffer[(self.start + i) % self.size] for i in range(self.count)]


@dataclass
class SimResult:
    frames: int
    skillchecks: int
    name: str


# Initialize result lists
baseResults = CircularBuffer(1000)
toolboxResults = CircularBuffer(1000)
hyperfocusResults = CircularBuffer(1000)
hyperfocusToolboxResults = CircularBuffer(1000)


def update_skill(val):
    SkillCheck.skill = float(val) / 100
    return


root = tk.Tk()
root.title("Slider")

slider = tk.Scale(root, from_=2, to=100, orient="horizontal", command=update_skill)
slider.pack()


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


def runSim(anis):
    simCount = 50  # How many times to run each simulation

    # Arguments for the simulations
    base_args = ("base", False, False)
    toolbox_args = ("toolbox", False, True)
    hyperfocus_args = ("hyperfocus", True, False)
    hyperfocusToolbox_args = ("hyperfocus and toolbox", True, True)

    # Timing serial execution
    start_time = time.time()

    # Run base simulations
    for _ in range(simCount):
        result = simStart(*base_args)
        baseResults.add(result)

    # Run toolbox simulations
    for _ in range(simCount):
        result = simStart(*toolbox_args)
        toolboxResults.add(result)

    # Run hyperfocus simulations
    for _ in range(simCount):
        result = simStart(*hyperfocus_args)
        hyperfocusResults.add(result)

    # Run hyperfocus and toolbox simulations
    for _ in range(simCount):
        result = simStart(*hyperfocusToolbox_args)
        hyperfocusToolboxResults.add(result)

    end_time = time.time()
    print(f"Serial execution time: {end_time - start_time:.2f} seconds")

    createGraphs([baseResults, toolboxResults, hyperfocusResults, hyperfocusToolboxResults])


def createGraphs(simulations: list[CircularBuffer]):
    # values over which to evaluate a kernel
    dist_spaceTime = linspace(0, 90, 100)
    dist_spaceSkillcheck = linspace(0, 30, 100)

    # create subplots

    nextOpenRow = 0

    for simulationResults in simulations:
        timeDataset = []
        skillcheckDataset = []
        for result in simulationResults.get():
            timeDataset.append(result.frames)  # type: ignore
            skillcheckDataset.append(result.skillchecks)  # type: ignore
        timeKDE = gaussian_kde(timeDataset)
        skillcheckKDE = gaussian_kde(skillcheckDataset)
        axs[nextOpenRow, 0].cla()
        axs[nextOpenRow, 1].cla()
        axs[nextOpenRow, 0].plot(dist_spaceTime, timeKDE(dist_spaceTime))
        axs[nextOpenRow, 0].set_title(result.name + ' time')  # type: ignore
        axs[nextOpenRow, 1].plot(dist_spaceSkillcheck, skillcheckKDE(dist_spaceSkillcheck))
        axs[nextOpenRow, 1].set_title(result.name + ' skillchecks')  # type: ignore
        nextOpenRow += 1


def startPlotter():
    ani = FuncAnimation(fig, runSim)  # type: ignore
    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    # Start the background task in a separate thread
    thread = threading.Thread(target=root.mainloop, daemon=True)
    thread.start()

    startPlotter()
