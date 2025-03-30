"""
Eve Detection Module

This module implements eavesdropper detection in quantum communication.
It analyzes quantum measurements to detect potential eavesdropping attempts
and calculates error rates in the quantum channel.

Classes:
    EveDetector: Handles eavesdropper detection and analysis

Functions:
    detect_eve(): Detects potential eavesdropping attempts
    calculate_error_rate(): Calculates error rate in measurements
    analyze_quantum_state(): Analyzes quantum state for anomalies
    validate_measurements(): Validates quantum measurements

Dependencies:
    - NumPy
    - Qiskit
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

class EveDetector:
    """
    A class to handle eavesdropper detection in quantum communication.
    
    Attributes:
        error_threshold (float): Threshold for Eve detection
        measurement_history (List[Dict]): History of quantum measurements
        error_rates (List[float]): History of error rates
    
    Methods:
        detect_eve(): Detects potential eavesdropping
        calculate_error_rate(): Calculates error rate
        analyze_quantum_state(): Analyzes quantum state
        validate_measurements(): Validates measurements
    """
    
    def __init__(self, error_threshold: float = 0.1):
        """
        Initialize the EveDetector.
        
        Args:
            error_threshold (float): Threshold for Eve detection
        """
        self.error_threshold = error_threshold
        self.measurement_history = []
        self.error_rates = []
    
    def detect_eve(self, measured_bases: str, received_bases: str) -> Tuple[bool, float]:
        """
        Detects potential eavesdropping attempts.
        
        Args:
            measured_bases (str): The bases used for measurement
            received_bases (str): The bases received from the other party
        
        Returns:
            Tuple[bool, float]: A tuple containing:
                - True if eavesdropping is detected
                - The calculated error rate
        
        Raises:
            Exception: If detection fails
        """
        try:
            # Calculate error rate
            error_rate = self.calculate_error_rate(measured_bases, received_bases)
            
            # Store measurement history
            self.measurement_history.append({
                'measured': measured_bases,
                'received': received_bases,
                'error_rate': error_rate
            })
            
            # Store error rate
            self.error_rates.append(error_rate)
            
            # Check if error rate exceeds threshold
            eve_detected = error_rate > self.error_threshold
            
            return eve_detected, error_rate
        except Exception as e:
            logger.error(f"Error detecting Eve: {str(e)}")
            raise
    
    def calculate_error_rate(self, measured_bases: str, received_bases: str) -> float:
        """
        Calculates the error rate between measured and received bases.
        
        Args:
            measured_bases (str): The bases used for measurement
            received_bases (str): The bases received from the other party
        
        Returns:
            float: The calculated error rate
        
        Raises:
            Exception: If calculation fails
        """
        try:
            if len(measured_bases) != len(received_bases):
                return 1.0
            
            # Count mismatches
            errors = sum(1 for m, r in zip(measured_bases, received_bases) if m != r)
            
            # Calculate error rate
            error_rate = errors / len(measured_bases)
            
            return error_rate
        except Exception as e:
            logger.error(f"Error calculating error rate: {str(e)}")
            return 1.0
    
    def analyze_quantum_state(self, circuit: QuantumCircuit) -> Dict[str, Any]:
        """
        Analyzes quantum state for potential anomalies.
        
        Args:
            circuit (QuantumCircuit): The quantum circuit to analyze
        
        Returns:
            Dict[str, Any]: Analysis results
        
        Raises:
            Exception: If analysis fails
        """
        try:
            # Execute circuit
            backend = Aer.get_backend('qasm_simulator')
            job = execute(circuit, backend, shots=1000)
            result = job.result()
            
            # Get measurement counts
            counts = result.get_counts(circuit)
            
            # Calculate state distribution
            total_shots = sum(counts.values())
            distribution = {k: v/total_shots for k, v in counts.items()}
            
            # Check for anomalies
            anomalies = self._check_anomalies(distribution)
            
            return {
                'distribution': distribution,
                'anomalies': anomalies,
                'total_shots': total_shots
            }
        except Exception as e:
            logger.error(f"Error analyzing quantum state: {str(e)}")
            raise
    
    def validate_measurements(self, measurements: List[Dict[str, Any]]) -> bool:
        """
        Validates quantum measurements for consistency.
        
        Args:
            measurements (List[Dict[str, Any]]): List of measurements to validate
        
        Returns:
            bool: True if measurements are valid, False otherwise
        
        Raises:
            Exception: If validation fails
        """
        try:
            if not measurements:
                return False
            
            # Check measurement consistency
            for measurement in measurements:
                if not self._validate_single_measurement(measurement):
                    return False
            
            return True
        except Exception as e:
            logger.error(f"Error validating measurements: {str(e)}")
            return False
    
    def _check_anomalies(self, distribution: Dict[str, float]) -> List[str]:
        """
        Checks for anomalies in quantum state distribution.
        
        Args:
            distribution (Dict[str, float]): State distribution to check
        
        Returns:
            List[str]: List of detected anomalies
        """
        try:
            anomalies = []
            
            # Check for uniform distribution
            expected_prob = 1.0 / len(distribution)
            tolerance = 0.1
            
            for state, prob in distribution.items():
                if abs(prob - expected_prob) > tolerance:
                    anomalies.append(f"Non-uniform distribution in state {state}")
            
            return anomalies
        except Exception as e:
            logger.error(f"Error checking anomalies: {str(e)}")
            return []
    
    def _validate_single_measurement(self, measurement: Dict[str, Any]) -> bool:
        """
        Validates a single quantum measurement.
        
        Args:
            measurement (Dict[str, Any]): The measurement to validate
        
        Returns:
            bool: True if measurement is valid, False otherwise
        """
        try:
            # Check required fields
            required_fields = ['measured', 'received', 'error_rate']
            if not all(field in measurement for field in required_fields):
                return False
            
            # Validate error rate
            if not 0 <= measurement['error_rate'] <= 1:
                return False
            
            # Validate bases
            if len(measurement['measured']) != len(measurement['received']):
                return False
            
            return True
        except Exception as e:
            logger.error(f"Error validating single measurement: {str(e)}")
            return False

def detect_eve(measured_bases: str, received_bases: str, threshold: float = 0.1) -> Tuple[bool, float]:
    """
    Detects potential eavesdropping attempts.
    
    Args:
        measured_bases (str): The bases used for measurement
        received_bases (str): The bases received from the other party
        threshold (float): Threshold for Eve detection
    
    Returns:
        Tuple[bool, float]: A tuple containing:
            - True if eavesdropping is detected
            - The calculated error rate
    """
    try:
        detector = EveDetector(threshold)
        return detector.detect_eve(measured_bases, received_bases)
    except Exception as e:
        logger.error(f"Error detecting Eve: {str(e)}")
        return True, 1.0

def calculate_error_rate(measured_bases: str, received_bases: str) -> float:
    """
    Calculates the error rate between measured and received bases.
    
    Args:
        measured_bases (str): The bases used for measurement
        received_bases (str): The bases received from the other party
    
    Returns:
        float: The calculated error rate
    """
    try:
        detector = EveDetector()
        return detector.calculate_error_rate(measured_bases, received_bases)
    except Exception as e:
        logger.error(f"Error calculating error rate: {str(e)}")
        return 1.0

def analyze_quantum_state(circuit: QuantumCircuit) -> Dict[str, Any]:
    """
    Analyzes quantum state for potential anomalies.
    
    Args:
        circuit (QuantumCircuit): The quantum circuit to analyze
    
    Returns:
        Dict[str, Any]: Analysis results
    """
    try:
        detector = EveDetector()
        return detector.analyze_quantum_state(circuit)
    except Exception as e:
        logger.error(f"Error analyzing quantum state: {str(e)}")
        return {}

def validate_measurements(measurements: List[Dict[str, Any]]) -> bool:
    """
    Validates quantum measurements for consistency.
    
    Args:
        measurements (List[Dict[str, Any]]): List of measurements to validate
    
    Returns:
        bool: True if measurements are valid, False otherwise
    """
    try:
        detector = EveDetector()
        return detector.validate_measurements(measurements)
    except Exception as e:
        logger.error(f"Error validating measurements: {str(e)}")
        return False 