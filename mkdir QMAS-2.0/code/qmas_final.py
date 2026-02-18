#!/usr/bin/env python3
"""
Q-MAS 2.0 - Quantum-inspired Multi-Agent Swarm with Distributed Consciousness
Main entry point for the project

Author: Abdullah Hawas
Date: February 18, 2026
"""

import numpy as np
import argparse
from experiments import run_experiments

def print_banner():
    """Print Q-MAS 2.0 banner"""
    banner = r"""
     ██████╗  ███╗   ███╗ █████╗ ███████╗    ██████╗  ██████╗ 
    ██╔═████╗ ████╗ ████║██╔══██╗██╔════╝    ╚════██╗██╔════╝ 
    ██║██╔██║ ██╔████╔██║███████║███████╗     █████╔╝███████╗ 
    ████╔╝██║ ██║╚██╔╝██║██╔══██║╚════██║    ██╔═══╝ ██╔═══██╗
    ╚██████╔╝ ██║ ╚═╝ ██║██║  ██║███████║    ███████╗╚██████╔╝
     ╚═════╝  ╚═╝     ╚═╝╚═╝  ╚═╝╚══════╝    ╚══════╝ ╚═════╝ 
    =================================================================
        Distributed Consciousness for Swarm Intelligence v2.0
    =================================================================
    """
    print(banner)

def main():
    """Main function"""
    print_banner()
    
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Q-MAS 2.0 - Swarm Intelligence')
    parser.add_argument('--epochs', type=int, default=10, 
                       help='Number of epochs to run (default: 10)')
    parser.add_argument('--agents', type=int, default=100, 
                       help='Number of agents in swarm (default: 100)')
    parser.add_argument('--output', type=str, default='results.csv', 
                       help='Output CSV file (default: results.csv)')
    
    args = parser.parse_args()
    
    # Display configuration
    print("\n📊 Configuration:")
    print(f"   • Epochs: {args.epochs}")
    print(f"   • Agents: {args.agents}")
    print(f"   • Output: {args.output}")
    print()
    
    # Run experiments
    print("🚀 Starting experiments...\n")
    results_df = run_experiments(n_epochs=args.epochs, n_agents=args.agents)
    
    # Save results
    results_df.to_csv(args.output, index=False)
    print(f"\n💾 Results saved to: {args.output}")
    
    # Final summary
    print("\n📈 Final Summary:")
    print(f"   • Total Value: {results_df['total'].sum():,}")
    print(f"   • Mean per Epoch: {results_df['total'].mean():.1f}")
    print(f"   • Best Epoch: {results_df['total'].max()}")
    
    print("\n✨ Q-MAS 2.0 completed successfully!")

if __name__ == "__main__":
    main()