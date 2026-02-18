# API Reference

## environment.py

### `class ContinuousEnvironment`
Main simulation environment.

**Methods:**
- `__init__(size=500, obstacles=50, dynamic=20)`
  - Create new environment (500×500)
  - 50 static obstacles, 20 dynamic obstacles

- `reset_targets()`
  - Reset targets for new epoch
  - 800 regular, 150 golden, 20 mega targets

- `update()`
  - Update dynamic obstacle positions

- `check_collision(pos)`
  - Check collision with obstacles
  - Input: position (x, y)
  - Output: True (collision) or False (no collision)

- `collect_target(pos)`
  - Try to collect targets from current position
  - Input: position (x, y)
  - Output: list of collected targets

## agents.py

### `class QMAS2Agent`
Individual agent with 7 layers of consciousness.

**Attributes:**
- `id`: Agent number
- `position`: Current position
- `velocity`: Current velocity
- `phase`: Current phase (explore, return, guard)
- `pheromone_map`: Pheromone memory grid

**Methods:**

- `gas_diffusion(neighbors)`
  - **Layer 1:** Gas Physics
  - Move away from crowded areas

- `wave_vibration(targets)`
  - **Layer 2:** Wave Vibration
  - Attraction toward discovered targets

- `stigmergic_chemistry()`
  - **Layer 4:** Pheromone Chemistry
  - Read and write pheromone trails

- `neural_oracle()`
  - **Layer 7:** Neural Oracle
  - Predict path when communication is lost

- `update(env, neighbors, targets, comms, step)`
  - Update agent by combining all layers

## experiments.py

### `class QMAS2Swarm`
Full swarm management.

**Methods:**

- `__init__(n_agents=100, env_size=500)`
  - Create swarm with specified number of agents

- `run_epoch(env, steps=1200, comms=True)`
  - Run one complete epoch
  - Output: dictionary with results (regular, golden, mega, total, time)

- `get_neighbors(agent, radius=60)`
  - Find nearby agents

### `function run_experiments(epochs=10, agents=100)`
Run complete experiments and return results table.

## qmas_final.py

### `function main()`
Main program entry point.

### `function print_banner()`
Print Q-MAS 2.0 banner.

## Constants

### Target Values
- Regular target: 1 point
- Golden target: 10 points
- Mega target: 100 points

### Environment Limits
- Environment size: 500 × 500
- Regular targets per epoch: 800
- Golden targets per epoch: 150
- Mega targets per epoch: 20