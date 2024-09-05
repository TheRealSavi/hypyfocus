# Dead by Daylight Generator Emulation with Hyperfocus Perk

## Overview

This Python script emulates the completion of Dead by Daylight generators while taking into account the Hyperfocus perk. The script sequentially emulates each frame of the generator repair process to avoid calculating the reduced time for skill checks as the number of skill checks increases due to the Hyperfocus perk.

## Features

- **Frame-by-Frame Emulation**: The script emulates each frame of the generator repair process, skillchecks, and toolboxes, and calculates the exact charges to use.
- **Hyperfocus Perk Simulation**: The perk’s effect on the frequency and difficulty of skill checks is taken into account.
- **Skill Check Time Reduction**: Calculates how the time required for skill checks decreases with each successive skill check.

## Output and Graphs

The script produces graphical representations of the generator repair process, showing the impact of the Hyperfocus perk. The output includes the following key visualizations:

### Graphs Overview

1. **Probability of Completion Times**:

   - **Description**: This graph depicts the probability distribution of the time required to complete the generator repair process.
   - **Details**: The x-axis represents the time taken to complete the generator, while the y-axis shows the probability of that time occurring.

2. **Skill Checks**:
   - **Description**: This graph illustrates the relationship between the number of skill checks required and the total time taken to complete the generator.
   - **Details**: The x-axis represents the number of skill checks that were hit, and the y-axis represents the probability of tht number. This graph shows how an increasing number of skill checks (due to the Hyperfocus perk) impacts the overall completion time.

### Example Graphs

Below is an example image of the generated graphs:

#### Skill Checks vs. Completion Time

![Skill Checks vs. Completion Time](https://github.com/TheRealSavi/hypyfocus/blob/master/Figure_1.png)
_Description: This graph depicts the relationship between the number of skill checks and the total repair time._

### Interpreting the Graphs

- **Probability of Completion Times**: Helps you understand the most likely durations for completing the generator repair and how the Hyperfocus perk shifts these probabilities.
- **Skill Checks vs. Completion Time**: Shows how the number of skill checks impacts the repair process. A higher number of skill checks will result in a decreased repair time, and this graph helps quantify that effect.

For a more detailed explanation of the results, you can watch the video where I review the findings in depth: [Watch Video](https://www.youtube.com/watch?v=g8QfRM7GwD8)

## Requirements

- Python 3.12 or higher
- Required Python packages (listed in `requirements.txt`)

## Installation

1. Clone the repository
2. Navigate to the project directory
3. Install the required packages using pipenv or manually

## Usage

Run the script using Python. The entry file is main.py. You can specify the number of generators to simulate and other parameters by editing the code.

## Bonus

There is also a crude pygame script you can run called skillcheckgame.py where you can practice and see how difficult hyperfocus skillechecks can be.
