import pandas as pd
import multiprocessing
import time
from dataclasses import dataclass
from concurrent.futures import ProcessPoolExecutor
from tqdm import tqdm 

from Toolbox import Toolbox
from Survivor import Survivor
from Generator import Generator


@dataclass
class SimResult:
    framesToComplete: int
    skillchecks: int
    greatHit: int
    missSk: int
    toolBoxUsed: bool
    toolBoxSpeed: float
    toolBoxCharges: int
    hyperfocusUsed: bool
    skillFactor: float
    simulatedFPS: int

# Simulation settings
SIM_FPS = 120
SIM_COUNT_PER_OPTIONSET = 4000


def simGen(gen: Generator, survivor: Survivor):
    """Runs a single generator repair simulation."""
    frames = 0
    while not gen.isCompleted():
        frames += 1
        survivor.repair(gen)
    return SimResult(
        framesToComplete=frames,
        skillchecks=survivor.getSkillCheckInstance().skCount,
        greatHit=survivor.getSkillCheckInstance().greatCount,
        missSk= survivor.getSkillCheckInstance().skCount - survivor.getSkillCheckInstance().greatCount - survivor.getSkillCheckInstance().goodCount,
        toolBoxUsed=survivor.getItem().speedBonusPercent != 0,
        toolBoxSpeed=survivor.getItem().speedBonusPercent,
        toolBoxCharges=survivor.getItem().maxCharges,
        hyperfocusUsed=survivor.hyperfocusEnabled,
        skillFactor=survivor.skill,
        simulatedFPS=SIM_FPS
    )


def simGenWrapper(args):
    """
    Worker function that runs multiple simulations for a given parameter set.
    It updates the shared batch_progress dictionary using its batch index.
    """
    batch_index, skill, useHyp, useTb, batch_progress = args
    results = []
    for i in range(SIM_COUNT_PER_OPTIONSET):
        result = simGen(Generator(), Survivor(Toolbox(32, 0.5) if useTb else Toolbox(0, 0), useHyp, skill))
        results.append(result.__dict__)
        # Update shared progress for this batch
        batch_progress[batch_index] = i + 1
    return results


def runSim():
    """Runs the entire simulation in parallel with individual progress bars per batch."""
    # Define parameter sets.
    skill_args = [0.2, 0.8, 1.0, 3.0]
    hy_tb_args = [(False, False), (False, True), (True, False), (True, True)]
    all_arg_sets = [(skill, hy, tb) for skill in skill_args for hy, tb in hy_tb_args]
    num_batches = len(all_arg_sets)
    
    results = []

    with multiprocessing.Manager() as manager:
        # Create a shared dict to track progress for each batch.
        batch_progress = manager.dict({i: 0 for i in range(num_batches)})
        
        # Prepare argument sets with an index and the shared dict.
        arg_sets_with_progress = [
            (i, skill, hy, tb, batch_progress) 
            for i, (skill, hy, tb) in enumerate(all_arg_sets)
        ]
        
        # Create a tqdm progress bar for each batch.
        bars = [
            tqdm(total=SIM_COUNT_PER_OPTIONSET, desc=f"Batch {i}", position=i, leave= True, colour= "#45f1c2", unit="Gen", dynamic_ncols= True)
            for i, (skill, hy, tb) in enumerate(all_arg_sets)
        ]
        
        # Launch the simulations in parallel.
        with ProcessPoolExecutor() as executor:
            futures = executor.map(simGenWrapper, arg_sets_with_progress)
            
            # While not all batches complete, refresh the individual progress bars.
            while any(batch_progress[i] < SIM_COUNT_PER_OPTIONSET for i in range(num_batches)):
                for i in range(num_batches):
                    bars[i].n = batch_progress[i]
                    bars[i].refresh()
                time.sleep(0.5)  # Update every 0.5 seconds.
            
            # Retrieve the results.
            for batch in futures:
                results.extend(batch)
        
        # Close all progress bars.
        for bar in bars:
            bar.close()

    # Save results.
    df = pd.DataFrame(results)
    df.to_csv("simResults3.csv", index=False)
    print("Simulation complete. Results saved to simResults2.csv.")


if __name__ == '__main__':
    multiprocessing.set_start_method("spawn")  # Ensure Windows uses spawn.
    runSim()
