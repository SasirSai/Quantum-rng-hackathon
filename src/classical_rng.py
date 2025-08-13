"""
Classical Random Number Generator for comparison with quantum RNG

This module implements various classical random number generation algorithms
for benchmarking against quantum random number generators.
"""

import random
import numpy as np
import time
from typing import List, Optional
import hashlib
import os


class ClassicalRNG:
    """Classical Random Number Generator with multiple algorithms."""
    
    def __init__(self, seed: Optional[int] = None):
        """
        Initialize the Classical RNG.
        
        Args:
            seed: Random seed for reproducibility
        """
        self.seed = seed if seed is not None else int(time.time())
        random.seed(self.seed)
        np.random.seed(self.seed)
    
    def generate_random_bits_python(self, num_bits: int, count: int = 1024) -> List[str]:
        """
        Generate random bits using Python's built-in random module.
        
        Args:
            num_bits: Number of bits per sample
            count: Number of samples to generate
            
        Returns:
            List of binary strings
        """
        random_bits = []
        for _ in range(count):
            # Generate random integer and convert to binary
            max_val = 2**num_bits - 1
            rand_int = random.randint(0, max_val)
            bit_string = format(rand_int, f'0{num_bits}b')
            random_bits.append(bit_string)
        
        return random_bits
    
    def generate_random_bits_numpy(self, num_bits: int, count: int = 1024) -> List[str]:
        """
        Generate random bits using NumPy's random module.
        
        Args:
            num_bits: Number of bits per sample
            count: Number of samples to generate
            
        Returns:
            List of binary strings
        """
        random_bits = []
        for _ in range(count):
            # Generate random bits directly
            bits = np.random.randint(0, 2, num_bits)
            bit_string = ''.join(map(str, bits))
            random_bits.append(bit_string)
        
        return random_bits
    
    def generate_random_bits_lfsr(self, num_bits: int, count: int = 1024) -> List[str]:
        """
        Generate random bits using Linear Feedback Shift Register (LFSR).
        
        Args:
            num_bits: Number of bits per sample
            count: Number of samples to generate
            
        Returns:
            List of binary strings
        """
        # Simple LFSR implementation
        def lfsr_step(state, taps):
            feedback = 0
            for tap in taps:
                feedback ^= (state >> tap) & 1
            return ((state << 1) | feedback) & ((1 << 16) - 1)
        
        # 16-bit LFSR with taps at positions 16, 14, 13, 11
        state = self.seed & 0xFFFF
        if state == 0:
            state = 1  # Avoid all-zero state
        
        taps = [15, 13, 12, 10]  # 0-indexed
        random_bits = []
        
        for _ in range(count):
            bits = []
            for _ in range(num_bits):
                bit = state & 1
                bits.append(str(bit))
                state = lfsr_step(state, taps)
            
            bit_string = ''.join(bits)
            random_bits.append(bit_string)
        
        return random_bits
    
    def generate_random_bits_os(self, num_bits: int, count: int = 1024) -> List[str]:
        """
        Generate random bits using OS entropy source.
        
        Args:
            num_bits: Number of bits per sample
            count: Number of samples to generate
            
        Returns:
            List of binary strings
        """
        random_bits = []
        bytes_needed = (num_bits + 7) // 8  # Round up to nearest byte
        
        for _ in range(count):
            # Get random bytes from OS
            random_bytes = os.urandom(bytes_needed)
            
            # Convert to binary string
            bit_string = ''
            for byte in random_bytes:
                bit_string += format(byte, '08b')
            
            # Trim to exact number of bits needed
            bit_string = bit_string[:num_bits]
            random_bits.append(bit_string)
        
        return random_bits
    
    def generate_random_integers(self, min_val: int, max_val: int, 
                                count: int = 1, method: str = 'python') -> List[int]:
        """
        Generate random integers in a specified range.
        
        Args:
            min_val: Minimum value (inclusive)
            max_val: Maximum value (inclusive)
            count: Number of random integers to generate
            method: Method to use ('python', 'numpy', 'os')
            
        Returns:
            List of random integers
        """
        if method == 'python':
            return [random.randint(min_val, max_val) for _ in range(count)]
        elif method == 'numpy':
            return np.random.randint(min_val, max_val + 1, count).tolist()
        elif method == 'os':
            # Use OS entropy
            range_size = max_val - min_val + 1
            num_bits = int(np.ceil(np.log2(range_size)))
            bit_strings = self.generate_random_bits_os(num_bits, count * 2)  # Generate extra
            
            integers = []
            for bit_string in bit_strings:
                if len(integers) >= count:
                    break
                integer_val = int(bit_string, 2)
                if integer_val < range_size:
                    integers.append(min_val + integer_val)
            
            return integers[:count]
        else:
            raise ValueError(f"Unknown method: {method}")
    
    def generate_random_floats(self, min_val: float = 0.0, max_val: float = 1.0,
                              count: int = 1, method: str = 'python') -> List[float]:
        """
        Generate random floating-point numbers.
        
        Args:
            min_val: Minimum value
            max_val: Maximum value
            count: Number of random floats to generate
            method: Method to use ('python', 'numpy')
            
        Returns:
            List of random floats
        """
        if method == 'python':
            return [random.uniform(min_val, max_val) for _ in range(count)]
        elif method == 'numpy':
            return np.random.uniform(min_val, max_val, count).tolist()
        else:
            raise ValueError(f"Unknown method: {method}")
    
    def test_randomness(self, method: str = 'python', num_samples: int = 10000) -> dict:
        """
        Test the randomness quality of the generator.
        
        Args:
            method: Method to test
            num_samples: Number of samples to test
            
        Returns:
            Dictionary with test results
        """
        # Generate random bits
        if method == 'python':
            random_bits = self.generate_random_bits_python(1, num_samples)
        elif method == 'numpy':
            random_bits = self.generate_random_bits_numpy(1, num_samples)
        elif method == 'lfsr':
            random_bits = self.generate_random_bits_lfsr(1, num_samples)
        elif method == 'os':
            random_bits = self.generate_random_bits_os(1, num_samples)
        else:
            raise ValueError(f"Unknown method: {method}")
        
        # Count 0s and 1s
        zeros = sum(1 for bits in random_bits if bits == '0')
        ones = sum(1 for bits in random_bits if bits == '1')
        
        # Calculate statistics
        total = zeros + ones
        zero_ratio = zeros / total if total > 0 else 0
        one_ratio = ones / total if total > 0 else 0
        
        return {
            'method': method,
            'total_samples': total,
            'zeros': zeros,
            'ones': ones,
            'zero_ratio': zero_ratio,
            'one_ratio': one_ratio,
            'bias': abs(zero_ratio - 0.5),
            'is_balanced': abs(zero_ratio - one_ratio) < 0.05
        }
    
    def benchmark_methods(self, num_bits: int = 8, count: int = 1000) -> dict:
        """
        Benchmark different random number generation methods.
        
        Args:
            num_bits: Number of bits per sample
            count: Number of samples to generate
            
        Returns:
            Dictionary with benchmark results
        """
        methods = ['python', 'numpy', 'lfsr', 'os']
        results = {}
        
        for method in methods:
            start_time = time.time()
            
            try:
                if method == 'python':
                    bits = self.generate_random_bits_python(num_bits, count)
                elif method == 'numpy':
                    bits = self.generate_random_bits_numpy(num_bits, count)
                elif method == 'lfsr':
                    bits = self.generate_random_bits_lfsr(num_bits, count)
                elif method == 'os':
                    bits = self.generate_random_bits_os(num_bits, count)
                
                end_time = time.time()
                execution_time = end_time - start_time
                
                results[method] = {
                    'execution_time': execution_time,
                    'samples_per_second': count / execution_time if execution_time > 0 else float('inf'),
                    'success': True
                }
            except Exception as e:
                results[method] = {
                    'execution_time': None,
                    'samples_per_second': None,
                    'success': False,
                    'error': str(e)
                }
        
        return results


if __name__ == "__main__":
    # Example usage
    crng = ClassicalRNG(seed=42)
    
    print("Classical Random Number Generator Demo")
    print("=" * 42)
    
    # Generate random bits with different methods
    print("\n1. Random Bits (4-bit samples):")
    methods = ['python', 'numpy', 'lfsr', 'os']
    
    for method in methods:
        print(f"\n   {method.upper()} method:")
        try:
            if method == 'python':
                bits = crng.generate_random_bits_python(4, 5)
            elif method == 'numpy':
                bits = crng.generate_random_bits_numpy(4, 5)
            elif method == 'lfsr':
                bits = crng.generate_random_bits_lfsr(4, 5)
            elif method == 'os':
                bits = crng.generate_random_bits_os(4, 5)
            
            for i, bit in enumerate(bits):
                print(f"     Sample {i+1}: {bit}")
        except Exception as e:
            print(f"     Error: {e}")
    
    # Test randomness for each method
    print("\n2. Randomness Tests:")
    for method in methods:
        try:
            test_results = crng.test_randomness(method, 1000)
            print(f"\n   {method.upper()}:")
            print(f"     Zeros: {test_results['zeros']} ({test_results['zero_ratio']:.3f})")
            print(f"     Ones: {test_results['ones']} ({test_results['one_ratio']:.3f})")
            print(f"     Bias: {test_results['bias']:.3f}")
            print(f"     Balanced: {test_results['is_balanced']}")
        except Exception as e:
            print(f"   {method.upper()}: Error - {e}")
    
    # Benchmark methods
    print("\n3. Performance Benchmark:")
    benchmark_results = crng.benchmark_methods(8, 1000)
    
    for method, result in benchmark_results.items():
        if result['success']:
            print(f"   {method.upper()}: {result['samples_per_second']:.0f} samples/sec")
        else:
            print(f"   {method.upper()}: Failed - {result['error']}")
