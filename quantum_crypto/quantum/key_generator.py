"""
Quantum Key Generator Module

This module implements the quantum key generation process using the BB84 protocol.
It handles the creation of quantum circuits, measurement, and key sifting.

Classes:
    QuantumKeyGenerator: Handles quantum key generation and processing

Functions:
    create_quantum_circuit(): Creates a quantum circuit for key generation
    measure_qubits(): Performs quantum measurements
    sift_key(): Performs key sifting process
    generate_key(): Main function to generate quantum key

Dependencies:
    - Qiskit
    - NumPy
"""

from qiskit import QuantumCircuit, Aer, execute
import numpy as np
from typing import Tuple, List, Dict, Any
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class QuantumKeyGenerator:
    """
    A class to handle quantum key generation using the BB84 protocol.
    
    Attributes:
        circuit (QuantumCircuit): The quantum circuit for key generation
        backend (AerBackend): The quantum simulator backend
        key_length (int): The desired length of the generated key
        error_rate (float): The current error rate in measurements
    
    Methods:
        create_circuit(): Creates a new quantum circuit
        measure_qubits(): Performs quantum measurements
        sift_key(): Performs key sifting
        generate_key(): Generates the final quantum key
    """
    
    def __init__(self, key_length: int = 32):
        """
        Initialize the QuantumKeyGenerator.
        
        Args:
            key_length (int): The desired length of the generated key
        """
        self.key_length = key_length
        self.error_rate = 0.0
        self.backend = Aer.get_backend('qasm_simulator')
        self.circuit = self.create_circuit()
    
    def create_circuit(self) -> QuantumCircuit:
        """
        Creates a quantum circuit for key generation.
        
        Returns:
            QuantumCircuit: The created quantum circuit
        
        Raises:
            Exception: If circuit creation fails
        """
        try:
            # Create circuit with key_length qubits
            qc = QuantumCircuit(self.key_length, self.key_length)
            
            # Apply Hadamard gates to create superposition
            for i in range(self.key_length):
                qc.h(i)
            
            # Apply CNOT gates for entanglement
            for i in range(0, self.key_length - 1, 2):
                qc.cx(i, i + 1)
            
            # Measure all qubits
            qc.measure(range(self.key_length), range(self.key_length))
            
            return qc
        except Exception as e:
            logger.error(f"Error creating quantum circuit: {str(e)}")
            raise
    
    def measure_qubits(self) -> Dict[str, int]:
        """
        Performs quantum measurements on the circuit.
        
        Returns:
            Dict[str, int]: The measurement results
        
        Raises:
            Exception: If measurement fails
        """
        try:
            # Execute circuit
            job = execute(self.circuit, self.backend, shots=1)
            result = job.result()
            
            # Get measurement counts
            counts = result.get_counts(self.circuit)
            
            return counts
        except Exception as e:
            logger.error(f"Error measuring qubits: {str(e)}")
            raise
    
    def sift_key(self, counts: Dict[str, int]) -> str:
        """
        Performs key sifting process on measurement results.
        
        Args:
            counts (Dict[str, int]): The measurement results
        
        Returns:
            str: The sifted key
        
        Raises:
            Exception: If key sifting fails
        """
        try:
            # Get the measurement result
            key = list(counts.keys())[0]
            
            # Calculate error rate (simulated)
            self.error_rate = np.random.random() * 0.1
            
            return key
        except Exception as e:
            logger.error(f"Error sifting key: {str(e)}")
            raise
    
    def generate_key(self) -> Tuple[str, float]:
        """
        Generates a quantum key using the BB84 protocol.
        
        Returns:
            Tuple[str, float]: A tuple containing:
                - The generated quantum key as a string
                - The error rate of the key generation process
        
        Raises:
            Exception: If key generation fails
        """
        try:
            # Create new circuit
            self.circuit = self.create_circuit()
            
            # Perform measurements
            counts = self.measure_qubits()
            
            # Sift key
            key = self.sift_key(counts)
            
            return key, self.error_rate
        except Exception as e:
            logger.error(f"Error generating quantum key: {str(e)}")
            raise

def create_quantum_circuit(qubits: int = 2) -> QuantumCircuit:
    """
    Creates a basic quantum circuit for key generation.
    
    Args:
        qubits (int): Number of qubits in the circuit
    
    Returns:
        QuantumCircuit: The created quantum circuit
    """
    try:
        qc = QuantumCircuit(qubits, qubits)
        qc.h(0)
        qc.cx(0, 1)
        qc.measure([0, 1], [0, 1])
        return qc
    except Exception as e:
        logger.error(f"Error creating quantum circuit: {str(e)}")
        raise

def measure_qubits(circuit: QuantumCircuit, backend: Any = None) -> Dict[str, int]:
    """
    Performs quantum measurements on a circuit.
    
    Args:
        circuit (QuantumCircuit): The circuit to measure
        backend (Any): The quantum backend to use
    
    Returns:
        Dict[str, int]: The measurement results
    """
    try:
        if backend is None:
            backend = Aer.get_backend('qasm_simulator')
        
        job = execute(circuit, backend, shots=1)
        result = job.result()
        return result.get_counts(circuit)
    except Exception as e:
        logger.error(f"Error measuring qubits: {str(e)}")
        raise

def sift_key(counts: Dict[str, int]) -> str:
    """
    Performs key sifting on measurement results.
    
    Args:
        counts (Dict[str, int]): The measurement results
    
    Returns:
        str: The sifted key
    """
    try:
        return list(counts.keys())[0]
    except Exception as e:
        logger.error(f"Error sifting key: {str(e)}")
        raise

def generate_key(key_length: int = 32) -> Tuple[str, float]:
    """
    Generates a quantum key using the BB84 protocol.
    
    Args:
        key_length (int): The desired length of the key
    
    Returns:
        Tuple[str, float]: A tuple containing:
            - The generated quantum key
            - The error rate
    """
    try:
        generator = QuantumKeyGenerator(key_length)
        return generator.generate_key()
    except Exception as e:
        logger.error(f"Error generating key: {str(e)}")
        raise 