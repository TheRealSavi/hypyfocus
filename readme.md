# Dead by Daylight Generator Emulation with Hyperfocus Perk

## Overview

This Python script emulates the completion of Dead by Daylight generators while taking into account the Hyperfocus perk. The script sequentially emulates each frame of the generator repair process to accutately calculate the average reduced repair time based on the diminishing return of having less chances for skill checks as the gen repairs faster.

## Features

- **Frame-by-Frame Emulation**: The script emulates each frame of the generator repair process, skillchecks, and toolboxes, and calculates the exact charges to use.
- **Hyperfocus Perk Simulation**: The perk’s effect on the frequency and difficulty of skill checks is taken into account.
- **Skill Check Time Reduction**: A skill factor determines the probability of hitting great skill checks as speed of skillcheck increases.

## Output

Produces a CSV of the tidy data produced by the simulation.

### Example Graphs

Below is an example image of extrapolated data from the simulator.

#### Hyperfocus Completion Time

![Skill Checks vs. Completion Time](https://github.com/TheRealSavi/hypyfocus/blob/master/Figure_1.png)
_Description: This graph depicts the relationship between using hyperfocus or not across skill factor._

### Interpreting the Graphs

For a more detailed explanation of the results, you can watch the video where I review the findings in depth: [Watch Video](https://www.youtube.com/watch?v=g8QfRM7GwD8)

## Requirements

- Python 3.12 or higher
- Required Python packages (listed in `requirements.txt`)
- Pipenv optional

## Installation

1. Clone the repository
2. Navigate to the project directory
3. Install the required packages using pipenv or manually
4. Run CSVVersion.py

## Usage

Parameters can be changed in the code to change simulation count and fidelity.

## Bonus

There is also a crude pygame script you can run called skillcheckgame.py where you can practice and see how difficult hyperfocus skillechecks can be.
