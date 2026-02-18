"""
Q-MAS 2.0 - Experiments Module
Run complete experiments and generate results
"""
import numpy as np
import pandas as pd
import time
from environment import ContinuousEnvironment
from agents import QMAS2Agent

class QMAS2Swarm:
    """Complete swarm with distributed consciousness"""
    
    def __init__(self, n_agents=100, env_size=500):
        self.n_agents = n_agents
        self.env_size = env_size
        self.agents = []
        self.fitness_history = []
        
        # Initialize agents
        positions = np.random.uniform(20, env_size-20, (n_agents, 2))
        for i in range(n_agents):
            self.agents.append(QMAS2Agent(i, positions[i], env_size))
        
        # Select leaders and guardians
        self.leaders = np.random.choice(n_agents, 5, replace=False)
        self.guardians = np.random.choice(n_agents, 10, replace=False)
    
    def reset_for_epoch(self):
        """Reset all agents for new epoch"""
        for agent in self.agents:
            agent.reset()
    
    def get_neighbors(self, agent, radius=60):
        """Get nearby agents"""
        neighbors = []
        for other in self.agents:
            if other.id != agent.id:
                dist = np.linalg.norm(agent.position - other.position)
                if dist < radius:
                    neighbors.append(other)
        return neighbors
    
    def run_epoch(self, env, timesteps=1200, comms_active=True):
        """Run one complete epoch"""
        
        # Reset everything
        env.reset_targets()
        self.reset_for_epoch()
        
        # Track results
        regular_found = 0
        golden_found = 0
        mega_found = 0
        
        start_time = time.time()
        
        for t in range(timesteps):
            # Update environment
            env.update()
            
            # Get active targets (simplified for demo)
            active_targets = []
            
            # Update each agent
            for i, agent in enumerate(self.agents):
                neighbors = self.get_neighbors(agent)
                collected = agent.update(env, neighbors, active_targets, comms_active, t)
                
                # Count collected targets
                for ctype, cval in collected:
                    if cval == 1:
                        regular_found += 1
                    elif cval == 10:
                        golden_found += 1
                    elif cval == 100:
                        mega_found += 1
            
            # Leader coordination (every 50 steps)
            if t % 50 == 0:
                leader_positions = np.array([self.agents[l].position for l in self.leaders])
                if len(leader_positions) > 0:
                    centroid = np.mean(leader_positions, axis=0)
                    for l in self.leaders:
                        to_centroid = centroid - self.agents[l].position
                        self.agents[l].velocity += to_centroid * 0.02
            
            # Guardian protection (every 30 steps)
            if t % 30 == 0:
                for g in self.guardians:
                    self.agents[g].velocity *= 1.1
        
        # Calculate epoch time
        epoch_time = time.time() - start_time
        
        # Store result
        epoch_result = {
            'regular': regular_found,
            'golden': golden_found,
            'mega': mega_found,
            'total': regular_found + golden_found*10 + mega_found*100,
            'time': epoch_time,
            'comms': comms_active
        }
        
        return epoch_result

def run_experiments(n_epochs=10, n_agents=100):
    """Run complete experiment suite"""
    
    print("=" * 60)
    print("Q-MAS 2.0 Experiments")
    print("=" * 60)
    
    # Initialize
    env = ContinuousEnvironment(size=500)
    swarm = QMAS2Swarm(n_agents=n_agents, env_size=500)
    
    results = []
    
    print(f"\n{'Epoch':<6} {'Regular':<8} {'Golden':<8} {'Mega':<6} {'Total':<8} {'Comms':<6}")
    print("-" * 50)
    
    for epoch in range(1, n_epochs + 1):
        # Alternate comms to test robustness
        comms = epoch % 2 == 0  # Even epochs: comms OFF
        
        result = swarm.run_epoch(env, timesteps=1200, comms_active=comms)
        result['epoch'] = epoch
        results.append(result)
        
        print(f"{epoch:<6} {result['regular']:<8} {result['golden']:<8} "
              f"{result['mega']:<6} {result['total']:<8} "
              f"{'OFF' if not comms else 'ON':<6}")
    
    print("-" * 50)
    
    # Create DataFrame
    df = pd.DataFrame(results)
    
    # Summary statistics
    print(f"\nSummary:")
    print(f"  Total Regular: {df['regular'].sum()} / {n_epochs*800}")
    print(f"  Total Golden: {df['golden'].sum()} / {n_epochs*150}")
    print(f"  Total Mega: {df['mega'].sum()} / {n_epochs*20}")
    print(f"  Total Value: {df['total'].sum():,}")
    
    return df

if __name__ == "__main__":
    # Quick test when run directly
    df = run_experiments(n_epochs=3, n_agents=20)
    print("\nTest complete!")