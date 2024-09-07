from dataclasses import dataclass
import sys
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


fig, axs = plt.subplots(4, 2)
plt.tight_layout()
plt.style.use('fivethirtyeight')

# Initialize result lists
baseResults = CircularBuffer(300)
toolboxResults = CircularBuffer(300)
hyperfocusResults = CircularBuffer(300)
hyperfocusToolboxResults = CircularBuffer(300)


def update_skill(val):
    # print(val)
    SkillCheck.skill = float(val) / 100
    return


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
    while True:
        simCount = 10  # Number of simulations to run

        # Simulation argument sets
        sim_args = [
            ("base", False, False),
            ("toolbox", False, True),
            ("hyperfocus", True, False),
            ("hyperfocus and toolbox", True, True),
        ]

        # Perform simulations
        for sim_name, useHyperfocus, useToolbox in sim_args:
            for _ in range(simCount):
                result = simStart(sim_name, useHyperfocus, useToolbox)
                if sim_name == "base":
                    baseResults.add(result)
                elif sim_name == "toolbox":
                    toolboxResults.add(result)
                elif sim_name == "hyperfocus":
                    hyperfocusResults.add(result)
                elif sim_name == "hyperfocus and toolbox":
                    hyperfocusToolboxResults.add(result)
        time.sleep(1/60)


def update(frame):
    for ax in axs.flat:
        ax.cla()

    simulations = [baseResults, toolboxResults, hyperfocusResults, hyperfocusToolboxResults]

    dist_spaceTime = linspace(0, 90, 100)
    dist_spaceSkillcheck = linspace(0, 30, 100)

    nextOpenRow = 0

    for simulationResults in simulations:
        if not simulationResults.get():  # If no data in buffer, skip plotting
            continue

    for simulationResults in simulations:
        data = simulationResults.get()

        timeDataset = []
        skillcheckDataset = []
        for result in data:
            timeDataset.append(result.frames)  # type: ignore
            skillcheckDataset.append(result.skillchecks)  # type: ignore

        if len(timeDataset) >= 2 and len(skillcheckDataset) >= 2:
            timeKDE = gaussian_kde(timeDataset)
            skillcheckKDE = gaussian_kde(skillcheckDataset)

           # Plot the time KDE
            axs[nextOpenRow, 0].plot(dist_spaceTime, timeKDE(dist_spaceTime))
            axs[nextOpenRow, 0].set_title(data[-1].name + ' time', fontsize=10)  # type: ignore # Use the most recent result for title

            # Plot the skillcheck KDE
            axs[nextOpenRow, 1].plot(dist_spaceSkillcheck, skillcheckKDE(dist_spaceSkillcheck))
            axs[nextOpenRow, 1].set_title(data[-1].name + ' skillchecks', fontsize=10)  # type: ignore

            nextOpenRow += 1

    return axs.flat


def init():
    for ax in axs.flat:
        ax.clear()
    return axs.flat


def startPlotter():
    plt.show()


def start_simulation_thread():
    sim_thread = threading.Thread(target=runSim)
    sim_thread.daemon = True  # Daemon thread will exit when the main program exits
    sim_thread.start()


ani = FuncAnimation(fig, update, frames=None, init_func=init, blit=False, interval=1000, save_count=20)

root = tk.Tk()
root.title("Skill Check Configuration")
root.geometry("500x250")
root.configure(bg='#f0f0f0')
root.protocol("WM_DELETE_WINDOW", sys.exit)

description_label = tk.Label(
    root,
    text="Skill Level Adjustment",
    font=("Arial", 14, "bold"),
    bg='#f0f0f0'
)
description_label.pack(pady=(10, 5))

info_label = tk.Label(
    root,
    text="Adjust the skill level to control the % chance of hitting a great skill check \ninstead of a good skill check.",
    font=("Arial", 10),
    bg='#f0f0f0'
)
info_label.pack(pady=(0, 10))

slider = tk.Scale(
    root,
    from_=2, to=100,
    orient="horizontal",
    command=update_skill,
    font=("Arial", 10),
    bg='#e0e0e0',
    length=300,
    highlightthickness=0
)
slider.pack(pady=(5, 20))
slider.set(100)

pause_button = tk.Button(root, text="Pause", font=("Arial", 12), command=ani.event_source.stop)
pause_button.pack(pady=5)

resume_button = tk.Button(root, text="Resume", font=("Arial", 12), command=ani.event_source.start)
resume_button.pack(pady=5)

if __name__ == '__main__':
    start_simulation_thread()

    startPlotter()
