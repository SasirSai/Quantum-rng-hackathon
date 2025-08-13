"""
Visualization module for quantum and classical random number generators

This module provides various visualization tools to analyze and compare
the randomness quality of quantum and classical RNG outputs.
"""

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from typing import List, Dict, Tuple, Optional
import pandas as pd
from scipy import stats
from collections import Counter
import warnings
warnings.filterwarnings('ignore')

# Set style
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")


class RNGVisualizer:
    """Visualization tools for random number generator analysis."""
    
    def __init__(self, figsize: Tuple[int, int] = (12, 8)):
        """
        Initialize the visualizer.
        
        Args:
            figsize: Default figure size for plots
        """
        self.figsize = figsize
        plt.rcParams['figure.figsize'] = figsize
    
    def plot_bit_distribution(self, quantum_bits: List[str], classical_bits: List[str],
                             title: str = "Bit Distribution Comparison") -> None:
        """
        Plot the distribution of 0s and 1s for quantum vs classical RNG.
        
        Args:
            quantum_bits: List of bit strings from quantum RNG
            classical_bits: List of bit strings from classical RNG
            title: Plot title
        """
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=self.figsize)
        
        # Count bits for quantum RNG
        q_zeros = sum(bit.count('0') for bit in quantum_bits)
        q_ones = sum(bit.count('1') for bit in quantum_bits)
        q_total = q_zeros + q_ones
        
        # Count bits for classical RNG
        c_zeros = sum(bit.count('0') for bit in classical_bits)
        c_ones = sum(bit.count('1') for bit in classical_bits)
        c_total = c_zeros + c_ones
        
        # Quantum RNG plot
        ax1.bar(['0', '1'], [q_zeros/q_total, q_ones/q_total], 
                color=['lightcoral', 'lightblue'], alpha=0.7)
        ax1.set_title('Quantum RNG')
        ax1.set_ylabel('Proportion')
        ax1.set_ylim(0, 1)
        ax1.axhline(y=0.5, color='red', linestyle='--', alpha=0.5, label='Expected (0.5)')
        ax1.legend()
        
        # Add text annotations
        ax1.text(0, q_zeros/q_total + 0.02, f'{q_zeros/q_total:.3f}', 
                ha='center', va='bottom')
        ax1.text(1, q_ones/q_total + 0.02, f'{q_ones/q_total:.3f}', 
                ha='center', va='bottom')
        
        # Classical RNG plot
        ax2.bar(['0', '1'], [c_zeros/c_total, c_ones/c_total], 
                color=['lightcoral', 'lightblue'], alpha=0.7)
        ax2.set_title('Classical RNG')
        ax2.set_ylabel('Proportion')
        ax2.set_ylim(0, 1)
        ax2.axhline(y=0.5, color='red', linestyle='--', alpha=0.5, label='Expected (0.5)')
        ax2.legend()
        
        # Add text annotations
        ax2.text(0, c_zeros/c_total + 0.02, f'{c_zeros/c_total:.3f}', 
                ha='center', va='bottom')
        ax2.text(1, c_ones/c_total + 0.02, f'{c_ones/c_total:.3f}', 
                ha='center', va='bottom')
        
        plt.suptitle(title, fontsize=16)
        plt.tight_layout()
        plt.show()
    
    def plot_histogram_comparison(self, quantum_data: List[int], classical_data: List[int],
                                 bins: int = 50, title: str = "Distribution Comparison") -> None:
        """
        Plot histograms comparing quantum and classical random number distributions.
        
        Args:
            quantum_data: List of integers from quantum RNG
            classical_data: List of integers from classical RNG
            bins: Number of histogram bins
            title: Plot title
        """
        fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(self.figsize[0], self.figsize[1] * 1.5))
        
        # Quantum histogram
        ax1.hist(quantum_data, bins=bins, alpha=0.7, color='blue', edgecolor='black')
        ax1.set_title('Quantum RNG Distribution')
        ax1.set_ylabel('Frequency')
        ax1.grid(True, alpha=0.3)
        
        # Classical histogram
        ax2.hist(classical_data, bins=bins, alpha=0.7, color='red', edgecolor='black')
        ax2.set_title('Classical RNG Distribution')
        ax2.set_ylabel('Frequency')
        ax2.grid(True, alpha=0.3)
        
        # Overlay comparison
        ax3.hist(quantum_data, bins=bins, alpha=0.5, color='blue', 
                label='Quantum', density=True)
        ax3.hist(classical_data, bins=bins, alpha=0.5, color='red', 
                label='Classical', density=True)
        ax3.set_title('Overlay Comparison (Normalized)')
        ax3.set_xlabel('Value')
        ax3.set_ylabel('Density')
        ax3.legend()
        ax3.grid(True, alpha=0.3)
        
        plt.suptitle(title, fontsize=16)
        plt.tight_layout()
        plt.show()
    
    def plot_autocorrelation(self, quantum_bits: List[str], classical_bits: List[str],
                           max_lag: int = 50) -> None:
        """
        Plot autocorrelation function for bit sequences.
        
        Args:
            quantum_bits: Quantum RNG bit strings
            classical_bits: Classical RNG bit strings
            max_lag: Maximum lag for autocorrelation
        """
        # Convert bit strings to binary sequences
        q_sequence = [int(bit) for bits in quantum_bits for bit in bits]
        c_sequence = [int(bit) for bits in classical_bits for bit in bits]
        
        # Limit sequence length for computation efficiency
        max_len = min(10000, len(q_sequence), len(c_sequence))
        q_sequence = q_sequence[:max_len]
        c_sequence = c_sequence[:max_len]
        
        # Calculate autocorrelation
        q_autocorr = np.correlate(q_sequence, q_sequence, mode='full')
        c_autocorr = np.correlate(c_sequence, c_sequence, mode='full')
        
        # Normalize
        q_autocorr = q_autocorr / np.max(q_autocorr)
        c_autocorr = c_autocorr / np.max(c_autocorr)
        
        # Get the positive lags
        mid = len(q_autocorr) // 2
        lags = np.arange(-max_lag, max_lag + 1)
        q_autocorr_plot = q_autocorr[mid-max_lag:mid+max_lag+1]
        c_autocorr_plot = c_autocorr[mid-max_lag:mid+max_lag+1]
        
        # Plot
        plt.figure(figsize=self.figsize)
        plt.plot(lags, q_autocorr_plot, 'b-', label='Quantum RNG', linewidth=2)
        plt.plot(lags, c_autocorr_plot, 'r-', label='Classical RNG', linewidth=2)
        plt.axhline(y=0, color='black', linestyle='--', alpha=0.5)
        plt.xlabel('Lag')
        plt.ylabel('Autocorrelation')
        plt.title('Autocorrelation Function Comparison')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.show()
    
    def plot_runs_test(self, quantum_bits: List[str], classical_bits: List[str]) -> None:
        """
        Visualize runs test results for randomness assessment.
        
        Args:
            quantum_bits: Quantum RNG bit strings
            classical_bits: Classical RNG bit strings
        """
        def count_runs(bit_sequence):
            """Count runs in a binary sequence."""
            if not bit_sequence:
                return 0
            
            runs = 1
            for i in range(1, len(bit_sequence)):
                if bit_sequence[i] != bit_sequence[i-1]:
                    runs += 1
            return runs
        
        # Convert to single bit sequences
        q_sequence = ''.join(quantum_bits)
        c_sequence = ''.join(classical_bits)
        
        # Count runs
        q_runs = count_runs(q_sequence)
        c_runs = count_runs(c_sequence)
        
        # Expected runs for random sequence
        n = len(q_sequence)
        expected_runs = (2 * q_sequence.count('0') * q_sequence.count('1')) / n + 1
        
        # Plot
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=self.figsize)
        
        # Runs comparison
        methods = ['Quantum', 'Classical']
        runs_counts = [q_runs, c_runs]
        colors = ['blue', 'red']
        
        bars = ax1.bar(methods, runs_counts, color=colors, alpha=0.7)
        ax1.axhline(y=expected_runs, color='green', linestyle='--', 
                   label=f'Expected ({expected_runs:.0f})')
        ax1.set_ylabel('Number of Runs')
        ax1.set_title('Runs Test Comparison')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Add value labels on bars
        for bar, count in zip(bars, runs_counts):
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height + 5,
                    f'{count}', ha='center', va='bottom')
        
        # Runs distribution visualization
        window_size = min(100, len(q_sequence) // 10)
        q_runs_windowed = []
        c_runs_windowed = []
        
        for i in range(0, len(q_sequence) - window_size, window_size):
            q_window = q_sequence[i:i+window_size]
            c_window = c_sequence[i:i+window_size]
            q_runs_windowed.append(count_runs(q_window))
            c_runs_windowed.append(count_runs(c_window))
        
        ax2.hist(q_runs_windowed, bins=20, alpha=0.5, color='blue', 
                label='Quantum', density=True)
        ax2.hist(c_runs_windowed, bins=20, alpha=0.5, color='red', 
                label='Classical', density=True)
        ax2.set_xlabel('Runs per Window')
        ax2.set_ylabel('Density')
        ax2.set_title(f'Runs Distribution (Window size: {window_size})')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.show()
    
    def plot_entropy_analysis(self, quantum_data: List[int], classical_data: List[int],
                             block_sizes: List[int] = [1, 2, 4, 8]) -> None:
        """
        Plot entropy analysis for different block sizes.
        
        Args:
            quantum_data: Quantum RNG integer data
            classical_data: Classical RNG integer data
            block_sizes: List of block sizes to analyze
        """
        def calculate_entropy(data, block_size):
            """Calculate Shannon entropy for given block size."""
            # Convert to binary and group into blocks
            binary_str = ''.join(format(x, '08b') for x in data)
            blocks = [binary_str[i:i+block_size] 
                     for i in range(0, len(binary_str)-block_size+1, block_size)]
            
            # Count block frequencies
            block_counts = Counter(blocks)
            total_blocks = len(blocks)
            
            # Calculate entropy
            entropy = 0
            for count in block_counts.values():
                p = count / total_blocks
                if p > 0:
                    entropy -= p * np.log2(p)
            
            return entropy
        
        q_entropies = []
        c_entropies = []
        theoretical_entropies = []
        
        for block_size in block_sizes:
            q_entropy = calculate_entropy(quantum_data, block_size)
            c_entropy = calculate_entropy(classical_data, block_size)
            theoretical_entropy = block_size  # Maximum entropy for block_size bits
            
            q_entropies.append(q_entropy)
            c_entropies.append(c_entropy)
            theoretical_entropies.append(theoretical_entropy)
        
        # Plot
        plt.figure(figsize=self.figsize)
        plt.plot(block_sizes, q_entropies, 'bo-', label='Quantum RNG', linewidth=2, markersize=8)
        plt.plot(block_sizes, c_entropies, 'ro-', label='Classical RNG', linewidth=2, markersize=8)
        plt.plot(block_sizes, theoretical_entropies, 'g--', label='Theoretical Maximum', linewidth=2)
        
        plt.xlabel('Block Size (bits)')
        plt.ylabel('Shannon Entropy')
        plt.title('Entropy Analysis by Block Size')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.xticks(block_sizes)
        
        # Add value annotations
        for i, (bs, qe, ce) in enumerate(zip(block_sizes, q_entropies, c_entropies)):
            plt.annotate(f'{qe:.2f}', (bs, qe), textcoords="offset points", 
                        xytext=(0,10), ha='center', color='blue')
            plt.annotate(f'{ce:.2f}', (bs, ce), textcoords="offset points", 
                        xytext=(0,-15), ha='center', color='red')
        
        plt.tight_layout()
        plt.show()
    
    def create_comprehensive_report(self, quantum_bits: List[str], classical_bits: List[str],
                                  quantum_ints: List[int], classical_ints: List[int]) -> None:
        """
        Create a comprehensive visualization report comparing RNG methods.
        
        Args:
            quantum_bits: Quantum RNG bit strings
            classical_bits: Classical RNG bit strings
            quantum_ints: Quantum RNG integers
            classical_ints: Classical RNG integers
        """
        print("Generating Comprehensive RNG Analysis Report...")
        print("=" * 50)
        
        # 1. Bit distribution
        print("\n1. Bit Distribution Analysis")
        self.plot_bit_distribution(quantum_bits, classical_bits)
        
        # 2. Integer distribution
        print("\n2. Integer Distribution Analysis")
        self.plot_histogram_comparison(quantum_ints, classical_ints)
        
        # 3. Autocorrelation
        print("\n3. Autocorrelation Analysis")
        self.plot_autocorrelation(quantum_bits, classical_bits)
        
        # 4. Runs test
        print("\n4. Runs Test Analysis")
        self.plot_runs_test(quantum_bits, classical_bits)
        
        # 5. Entropy analysis
        print("\n5. Entropy Analysis")
        self.plot_entropy_analysis(quantum_ints, classical_ints)
        
        print("\nReport generation complete!")


if __name__ == "__main__":
    # Example usage with dummy data
    print("RNG Visualization Demo")
    print("=" * 25)
    
    # Generate some dummy data for demonstration
    np.random.seed(42)
    
    # Simulate quantum and classical bit strings
    quantum_bits = [format(np.random.randint(0, 256), '08b') for _ in range(1000)]
    classical_bits = [format(np.random.randint(0, 256), '08b') for _ in range(1000)]
    
    # Simulate integer data
    quantum_ints = np.random.randint(0, 100, 1000).tolist()
    classical_ints = np.random.randint(0, 100, 1000).tolist()
    
    # Create visualizer
    visualizer = RNGVisualizer()
    
    print("\nNote: This demo uses simulated data.")
    print("In practice, use real quantum and classical RNG outputs.")
    
    # Uncomment to run full report
    # visualizer.create_comprehensive_report(quantum_bits, classical_bits, 
    #                                       quantum_ints, classical_ints)
