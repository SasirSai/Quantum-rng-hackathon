"""
Quantum Random Number Generator using Qiskit

This module implements a quantum random number generator using quantum superposition
and measurement to generate truly random numbers.
"""

import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt
from typing import List, Optional


class QuantumRNG:
    """Quantum Random Number Generator using quantum circuits."""
    
    def __init__(self, backend_name: str = 'aer_simulator'):
        """
        Initialize the Quantum RNG.
        
        Args:
            backend_name: Name of the quantum backend to use
        """
        self.backend = AerSimulator()
        self.circuit_cache = {}
    
    def create_quantum_circuit(self, num_qubits: int) -> QuantumCircuit:
        """
        Create a quantum circuit for random number generation.
        
        Args:
            num_qubits: Number of qubits to use
            
        Returns:
            QuantumCircuit: The quantum circuit
        """
        if num_qubits in self.circuit_cache:
            return self.circuit_cache[num_qubits]
        
        # Create quantum circuit
        qc = QuantumCircuit(num_qubits, num_qubits)
        
        # Apply Hadamard gates to create superposition
        for i in range(num_qubits):
            qc.h(i)
        
        # Measure all qubits
        qc.measure_all()
        
        self.circuit_cache[num_qubits] = qc
        return qc
    
    def generate_random_bits(self, num_bits: int, shots: int = 1024) -> List[str]:
        """
        Generate random bits using quantum measurements.
        
        Args:
            num_bits: Number of bits to generate
            shots: Number of quantum circuit executions
            
        Returns:
            List of binary strings
        """
        qc = self.create_quantum_circuit(num_bits)
        
        # Transpile and execute
        transpiled_qc = transpile(qc, self.backend)
        job = self.backend.run(transpiled_qc, shots=shots)
        result = job.result()
        counts = result.get_counts()
        
        # Extract random bit strings
        random_bits = []
        for bitstring, count in counts.items():
            random_bits.extend([bitstring] * count)
        
        return random_bits[:shots]
    
    def generate_random_integers(self, min_val: int, max_val: int, 
                                count: int = 1, shots: int = 1024) -> List[int]:
        """
        Generate random integers in a specified range.
        
        Args:
            min_val: Minimum value (inclusive)
            max_val: Maximum value (inclusive)
            count: Number of random integers to generate
            shots: Number of quantum measurements
            
        Returns:
            List of random integers
        """
        # Calculate number of bits needed
        range_size = max_val - min_val + 1
        num_bits = int(np.ceil(np.log2(range_size)))
        
        random_bits = self.generate_random_bits(num_bits, shots * count)
        random_integers = []
        
        for i in range(0, len(random_bits), 1):
            if len(random_integers) >= count:
                break
            
            # Convert binary string to integer
            bit_string = random_bits[i]
            integer_val = int(bit_string, 2)
            
            # Map to desired range
            if integer_val < range_size:
                random_integers.append(min_val + integer_val)
        
        return random_integers[:count]
    
    def generate_random_floats(self, min_val: float = 0.0, max_val: float = 1.0,
                              count: int = 1, precision: int = 16) -> List[float]:
        """
        Generate random floating-point numbers.
        
        Args:
            min_val: Minimum value
            max_val: Maximum value
            count: Number of random floats to generate
            precision: Number of bits for precision
            
        Returns:
            List of random floats
        """
        random_bits = self.generate_random_bits(precision, count)
        random_floats = []
        
        for bit_string in random_bits:
            # Convert to float between 0 and 1
            integer_val = int(bit_string, 2)
            max_integer = 2**precision - 1
            normalized_val = integer_val / max_integer
            
            # Scale to desired range
            scaled_val = min_val + normalized_val * (max_val - min_val)
            random_floats.append(scaled_val)
        
        return random_floats
    
    def test_randomness(self, num_samples: int = 10000) -> dict:
        """
        Test the randomness quality of the generator.
        
        Args:
            num_samples: Number of samples to test
            
        Returns:
            Dictionary with test results
        """
        # Generate random bits
        random_bits = self.generate_random_bits(1, num_samples)
        
        # Count 0s and 1s
        zeros = sum(1 for bits in random_bits if bits == '0')
        ones = sum(1 for bits in random_bits if bits == '1')
        
        # Calculate statistics
        total = zeros + ones
        zero_ratio = zeros / total if total > 0 else 0
        one_ratio = ones / total if total > 0 else 0
        
        return {
            'total_samples': total,
            'zeros': zeros,
            'ones': ones,
            'zero_ratio': zero_ratio,
            'one_ratio': one_ratio,
            'bias': abs(zero_ratio - 0.5),
            'is_balanced': abs(zero_ratio - one_ratio) < 0.05
        }


if __name__ == "__main__":
    # Example usage
    qrng = QuantumRNG()
    
    print("Quantum Random Number Generator Demo")
    print("=" * 40)
    
    # Generate random bits
    print("\n1. Random Bits:")
    bits = qrng.generate_random_bits(4, shots=10)
    for i, bit in enumerate(bits[:5]):
        print(f"   Sample {i+1}: {bit}")
    
    # Generate random integers
    print("\n2. Random Integers (1-100):")
    integers = qrng.generate_random_integers(1, 100, count=5)
    for i, num in enumerate(integers):
        print(f"   Sample {i+1}: {num}")
    
    # Generate random floats
    print("\n3. Random Floats (0.0-1.0):")
    floats = qrng.generate_random_floats(0.0, 1.0, count=5)
    for i, num in enumerate(floats):
        print(f"   Sample {i+1}: {num:.6f}")
    
    # Test randomness
    print("\n4. Randomness Test:")
    test_results = qrng.test_randomness(1000)
    print(f"   Total samples: {test_results['total_samples']}")
    print(f"   Zeros: {test_results['zeros']} ({test_results['zero_ratio']:.3f})")
    print(f"   Ones: {test_results['ones']} ({test_results['one_ratio']:.3f})")
    print(f"   Bias: {test_results['bias']:.3f}")
    print(f"   Is balanced: {test_results['is_balanced']}")
