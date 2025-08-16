import os
import hashlib

def generate_quantum_mnemonic():
    """
    Generates a 9-character mnemonic using quantum randomness.
    """
    try:
        # Try to import Qiskit components
        from qiskit import QuantumCircuit
        from qiskit_ibm_runtime import QiskitRuntimeService, Sampler
        
        # 1. Initialize IBM Quantum Service
        # It will automatically load the token from the .env file if it's not passed here.
        service = QiskitRuntimeService()
        backend = service.least_busy(operational=True, simulator=True) # Use a simulator for speed

        # 2. Create a simple quantum circuit
        # A single qubit in superposition will give us a random 0 or 1.
        qc = QuantumCircuit(1)
        qc.h(0)  # Apply Hadamard gate to create superposition
        qc.measure_all()

        # 3. Run the job on the backend
        sampler = Sampler(backend)
        # We run it 256 times to get a good string of random bits
        job = sampler.run(qc, shots=256)
        result = job.result()

        # The memory gives us the result of each individual shot ('0' or '1')
        binary_string = "".join([str(bit) for bit in result.get_memory(0)])

        # 4. Hash the result to create the mnemonic
        # We hash the raw binary string for cryptographic security
        sha256_hash = hashlib.sha256(binary_string.encode('utf-8')).hexdigest()

        # 5. Truncate to 9 characters for the attendance code
        mnemonic = sha256_hash.upper()[:9]
        job_id = job.job_id()

        print(f"✅ Generated new mnemonic: {mnemonic} from Job ID: {job_id}")
        return {"mnemonic": mnemonic, "job_id": job_id}

    except ImportError as e:
        print(f"❌ Qiskit not available: {e}, using fallback generator")
        fallback_hash = hashlib.sha256(os.urandom(32)).hexdigest()
        return {"mnemonic": fallback_hash.upper()[:9], "job_id": "fallback-no-qiskit"}
    except Exception as e:
        print(f"❌ Quantum generator failed: {e}")
        # Fallback to a pseudo-random generator in case of API failure
        fallback_hash = hashlib.sha256(os.urandom(32)).hexdigest()
        return {"mnemonic": fallback_hash.upper()[:9], "job_id": "fallback-error"}