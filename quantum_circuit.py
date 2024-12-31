import numpy as np
from qiskit import QuantumCircuit
from qiskit_aer import Aer
import matplotlib.pyplot as plt

# Create circuit with 4 qubits (1 for sign, 3 for base-6 encoding)
qc = QuantumCircuit(4, 4)

# Initialize the sign qubit (0 for positive, 1 for negative)
qc.h(0)  # Superposition of positive/negative states

# Create base-6 encoding using 3 qubits
for i in range(1, 4):
    qc.h(i)
    # Add phase rotation for base-6 encoding
    qc.rz(2 * np.pi * i / 6, i)

# Entangle the sign qubit with the encoding qubits
for i in range(1, 4):
    qc.cx(0, i)

# Add controlled phase relationships
phi = (1 + np.sqrt(5)) / 2  # Golden ratio
qc.cp(phi * np.pi/6, 1, 2)
qc.cp(phi * np.pi/6, 2, 3)

# Measure all qubits
qc.measure_all()

# Get the simulator
backend = Aer.get_backend('statevector_simulator')
job = backend.run(qc)
result = job.result()
statevector = result.get_statevector()

# Calculate probabilities
probabilities = np.abs(statevector) ** 2

# Separate positive and negative states
positive_states = []
negative_states = []

for i, prob in enumerate(probabilities):
    if prob > 0.01:  # Filter significant probabilities
        binary = format(i, '04b')
        if binary[0] == '0':
            positive_states.append((binary, prob))
        else:
            negative_states.append((binary, prob))

print("Pos/Neg Quantum State Analysis:")
print("====================================")
print(f"Total number of states: {len(probabilities)}")
print(f"Sum of probabilities: {np.sum(probabilities):.6f}")

print("\
Positive States:")
print("----------------------------------")
for binary, prob in positive_states:
    base6_val = int(binary[1:], 2) % 6
    print(f"State |{binary}> (Base-6: {base6_val}): {prob:.4f}")

print("\
Negative States:")
print("----------------------------------")
for binary, prob in negative_states:
    base6_val = int(binary[1:], 2) % 6
    print(f"State |{binary}> (Base-6: {base6_val}): {prob:.4f}")

# Plot the probability distribution
plt.figure(figsize=(15, 6))
plt.subplot(1, 2, 1)
plt.bar([i for i, _ in enumerate(probabilities) if i < len(probabilities)//2], 
        [p for i, p in enumerate(probabilities) if i < len(probabilities)//2],
        color='blue', alpha=0.6, label='Positive States')
plt.title('Positive States')
plt.xlabel('Quantum State')
plt.ylabel('Probability')
plt.legend()

plt.subplot(1, 2, 2)
plt.bar([i for i, _ in enumerate(probabilities) if i >= len(probabilities)//2], 
        [p for i, p in enumerate(probabilities) if i >= len(probabilities)//2],
        color='red', alpha=0.6, label='Negative States')
plt.title('Negative States')
plt.xlabel('Quantum State')
plt.ylabel('Probability')
plt.legend()

plt.tight_layout()
plt.show()

# Calculate quantum biological metrics
print("\
Quantum Metrics:")
print("=========================")
print(f"φ (Golden Ratio): {phi:.6f}")
print(f"Base-6 Phase Angle: {2*np.pi/6:.6f} radians")
print(f"Entanglement Measure: {np.sum(probabilities[len(probabilities)//2:]):.6f}")
print(f"Pos/Neg Balance Ratio: {np.sum(probabilities[:len(probabilities)//2])/np.sum(probabilities[len(probabilities)//2:]):.6f}")