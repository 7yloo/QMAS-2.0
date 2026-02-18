"""
Q-MAS 2.0 - Agents Module
Individual agent with 7 layers of distributed consciousness
"""
import numpy as np
from typing import List, Tuple

class QMAS2Agent:
    """Single agent with distributed consciousness"""
    
    def __init__(self, agent_id, position, env_size=500):
        self.id = agent_id
        self.position = position.copy()
        self.start_position = position.copy()
        self.velocity = np.zeros(2)
        self.phase = 'explore'  # explore, return, guard
        self.success_count = 0
        self.epoch_success = 0
        self.pheromone_map = np.zeros((50, 50))
        self.trajectory = [position.copy()]
        self.neural_buffer = []
    
    def reset(self):
        """Reset agent for new epoch"""
        self.position = self.start_position.copy()
        self.velocity = np.zeros(2)
        self.phase = 'explore'
        self.epoch_success = 0
        self.trajectory = [self.position.copy()]
        self.neural_buffer = []
    
    def gas_diffusion(self, neighbors):
        """Layer 1: Sovereign diffusion"""
        if len(neighbors) == 0:
            return np.random.randn(2) * 8
        
        neighbor_pos = np.array([n.position for n in neighbors])
        center = np.mean(neighbor_pos, axis=0)
        away = self.position - center
        dist = np.linalg.norm(away)
        
        if dist > 0:
            away = away / dist * 10
        
        randomness = np.random.randn(2) * 5
        return away * 0.6 + randomness * 0.4
    
    def wave_vibration(self, active_targets):
        """Layer 2: Wordless communication"""
        if not active_targets:
            return np.zeros(2)
        
        force = np.zeros(2)
        for tpos, tval in active_targets[:10]:
            r = np.linalg.norm(self.position - tpos)
            if r < 1:
                continue
            
            magnitude = tval / (r * r + 1) * 50
            direction = (tpos - self.position) / r
            force += magnitude * direction
        
        return np.clip(force, -20, 20)
    
    def stigmergic_chemistry(self):
        """Layer 4: Phase-gated pheromone memory"""
        gx = min(49, max(0, int(self.position[0] / 10)))
        gy = min(49, max(0, int(self.position[1] / 10)))
        
        # Only write during return phase
        if self.phase == 'return' and self.epoch_success > 0:
            self.pheromone_map[gx, gy] = min(10, self.pheromone_map[gx, gy] + 1)
        
        # Read pheromone gradient
        force = np.zeros(2)
        if self.pheromone_map[gx, gy] > 0.1:
            # Find strongest neighboring cell
            best_dir = np.zeros(2)
            best_val = 0
            
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    nx, ny = gx + dx, gy + dy
                    if 0 <= nx < 50 and 0 <= ny < 50:
                        val = self.pheromone_map[nx, ny]
                        if val > best_val:
                            best_val = val
                            best_dir = np.array([dx, dy])
            
            if best_val > 0:
                force = best_dir * self.pheromone_map[gx, gy] * 2
        
        # Evaporation
        self.pheromone_map *= 0.999
        
        return force
    
    def neural_oracle(self):
        """Layer 7: Reality extrapolation"""
        if len(self.neural_buffer) < 5:
            return np.random.randn(2) * 6
        
        recent = np.array(self.neural_buffer[-5:])
        if len(recent) > 1:
            velocities = np.diff(recent, axis=0)
            avg_vel = np.mean(velocities, axis=0)
            noise = np.random.randn(2) * 3
            return avg_vel * 2 + noise
        
        return np.random.randn(2) * 6
    
    def update(self, env, neighbors, active_targets, comms_active, timestep):
        """Update agent state"""
        
        # Store for neural oracle
        self.neural_buffer.append(self.position.copy())
        if len(self.neural_buffer) > 20:
            self.neural_buffer.pop(0)
        
        # Get forces from layers
        gas = self.gas_diffusion(neighbors)
        
        wave = np.zeros(2)
        if comms_active:
            wave = self.wave_vibration(active_targets)
        
        chem = self.stigmergic_chemistry()
        
        oracle = np.zeros(2)
        if not comms_active and np.random.random() < 0.4:
            oracle = self.neural_oracle()
        
        # Adaptive weights based on phase
        if self.phase == 'return':
            weights = [0.2, 0.1, 0.7, 0.0]  # Follow pheromone trail
        else:
            weights = [0.4, 0.4, 0.1, 0.1]  # Explore and communicate
        
        total = (weights[0] * gas + 
                 weights[1] * wave + 
                 weights[2] * chem + 
                 weights[3] * oracle)
        
        # Update velocity
        self.velocity = 0.7 * self.velocity + 0.3 * total
        self.velocity = np.clip(self.velocity, -15, 15)
        
        # Move
        new_pos = self.position + self.velocity
        
        # Check collisions
        collision = env.check_collision(new_pos)
        if collision == True:
            self.velocity *= -0.8
            new_pos = self.position + self.velocity
        elif collision == 'hazard':
            self.velocity = -self.velocity * 1.5
            new_pos = self.position + self.velocity
        
        # Stay in bounds
        self.position = np.clip(new_pos, 5, env.size - 5)
        self.trajectory.append(self.position.copy())
        
        # Collect targets
        collected = env.collect_target(self.position)
        for ctype, cval in collected:
            self.success_count += cval
            self.epoch_success += cval
            self.phase = 'return'  # Switch to return mode
        
        # Return to base logic
        if self.phase == 'return' and len(self.trajectory) > 100:
            self.phase = 'explore'
        
        return collected