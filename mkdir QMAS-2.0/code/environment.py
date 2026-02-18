"""
Q-MAS 2.0 - Environment Module
Continuous environment with obstacles, hazards, and targets
"""
import numpy as np
from typing import List, Tuple, Dict

class ContinuousEnvironment:
    """Realistic continuous space with dynamic obstacles"""
    
    def __init__(self, size=500, n_obstacles=50, n_dynamic=20):
        self.size = size
        self.n_obstacles = n_obstacles
        self.n_dynamic = n_dynamic
        self.epoch = 0
        
        # Static obstacles
        self.obstacles = np.random.uniform(0, size, (n_obstacles, 2))
        self.obstacle_radius = np.random.uniform(5, 15, n_obstacles)
        
        # Dynamic obstacles
        self.dynamic_obs = np.random.uniform(0, size, (n_dynamic, 2))
        self.dynamic_vel = np.random.uniform(-2, 2, (n_dynamic, 2))
        self.dynamic_radius = np.random.uniform(3, 8, n_dynamic)
        
        # Target counts
        self.regular_count = 800
        self.golden_count = 150
        self.mega_count = 20
        self.target_values = {'regular': 1, 'golden': 10, 'mega': 100}
        
        # Hazards
        self.hazards = np.random.uniform(0, size, (30, 2))
        self.hazard_radius = np.random.uniform(10, 20, 30)
        
        self.reset_targets()
    
    def reset_targets(self):
        """Reset all targets at beginning of epoch"""
        self.regular_targets = np.random.uniform(10, self.size-10, (self.regular_count, 2))
        self.golden_targets = np.random.uniform(10, self.size-10, (self.golden_count, 2))
        self.mega_targets = np.random.uniform(10, self.size-10, (self.mega_count, 2))
        
        self.regular_collected = np.zeros(self.regular_count, dtype=bool)
        self.golden_collected = np.zeros(self.golden_count, dtype=bool)
        self.mega_collected = np.zeros(self.mega_count, dtype=bool)
        
        self.epoch += 1
    
    def update(self):
        """Update dynamic obstacles"""
        self.dynamic_obs += self.dynamic_vel
        for i in range(self.n_dynamic):
            for j in range(2):
                if self.dynamic_obs[i,j] < 0 or self.dynamic_obs[i,j] > self.size:
                    self.dynamic_vel[i,j] *= -1
        return self.dynamic_obs
    
    def check_collision(self, pos):
        """Check if position collides with any obstacle"""
        for obs, rad in zip(self.obstacles, self.obstacle_radius):
            if np.linalg.norm(pos - obs) < rad:
                return True
        
        for obs, rad in zip(self.dynamic_obs, self.dynamic_radius):
            if np.linalg.norm(pos - obs) < rad:
                return True
        
        for haz, rad in zip(self.hazards, self.hazard_radius):
            if np.linalg.norm(pos - haz) < rad:
                return 'hazard'
        
        return False
    
    def collect_target(self, pos, detection_radius=12):
        """Check if position collects any targets"""
        collected = []
        
        for i in range(self.regular_count):
            if not self.regular_collected[i]:
                if np.linalg.norm(pos - self.regular_targets[i]) < detection_radius:
                    self.regular_collected[i] = True
                    collected.append(('regular', 1))
        
        for i in range(self.golden_count):
            if not self.golden_collected[i]:
                if np.linalg.norm(pos - self.golden_targets[i]) < detection_radius:
                    self.golden_collected[i] = True
                    collected.append(('golden', 10))
        
        for i in range(self.mega_count):
            if not self.mega_collected[i]:
                if np.linalg.norm(pos - self.mega_targets[i]) < detection_radius:
                    self.mega_collected[i] = True
                    collected.append(('mega', 100))
        
        return collected
    
    def get_remaining_counts(self):
        """Get count of remaining targets"""
        return {
            'regular': np.sum(~self.regular_collected),
            'golden': np.sum(~self.golden_collected),
            'mega': np.sum(~self.mega_collected)
        }