# Analyze the relationship between binary, base-4, and base-6 states
import numpy as np
from qiskit import QuantumCircuit
from qiskit_aer import Aer
import matplotlib.pyplot as plt

def create_multi_base_circuit():
    # Create circuit with 4 qubits
    # - 1 sign qubit (positive/negative)
    # - 1 qubit for binary encoding
    # - 2 qubits for base-4 encoding (which can represent base-6 states)
    qc = QuantumCircuit(4, 4)
    
    # Initialize sign qubit in superposition
    qc.h(0)
    
    # Create different base encodings
    # Binary encoding (qubit 1)
    qc.h(1)
    
    # Base-4 encoding (qubits 2-3)
    qc.h(2)
    qc.h(3)
    
    # Add phase relationships
    # Binary to Base-4
    qc.cx(1, 2)
    
    # Base-4 to Base-6 mapping through phase
    phi = (1 + np.sqrt(5)) / 2  # Golden ratio
    qc.cp(2 * np.pi / 6, 2, 3)  # Base-6 phase
    qc.cp(phi * np.pi / 4, 1, 3)  # Cross-base relationship
    
    # Measure all qubits
    qc.measure_all()
    
    return qc

# Create and run the circuit
qc = create_multi_base_circuit()
backend = Aer.get_backend('statevector_simulator')
job = backend.run(qc)
result = job.result()
statevector = result.get_statevector()

# Calculate probabilities
probabilities = np.abs(statevector) ** 2

# Analyze state distributions
def analyze_state(binary_state):
    binary = format(binary_state, '04b')
    sign = 'Positive' if binary[0] == '0' else 'Negative'
    binary_val = int(binary[1], 2)
    base4_val = int(binary[2:], 2)
    base6_val = base4_val % 6
    return binary, sign, binary_val, base4_val, base6_val

# Create visualization of the base relationships
plt.figure(figsize=(15, 10))

# Plot 1: Overall state distribution
plt.subplot(2, 2, 1)
plt.bar(range(len(probabilities)), probabilities)
plt.title('Full Quantum State Distribution')
plt.xlabel('State Index')
plt.ylabel('Probability')

# Plot 2: Base-4 to Base-6 mapping
base4_to_base6 = np.zeros(4)
for i in range(4):
    base4_to_base6[i] = i % 6
plt.subplot(2, 2, 2)
plt.scatter(range(4), base4_to_base6, c='red', s=100)
plt.title('Base-4 to Base-6 Mapping')
plt.xlabel('Base-4 Value')
plt.ylabel('Base-6 Value')
plt.grid(True)

# Plot 3: Positive vs Negative state distribution
positive_probs = probabilities[:len(probabilities)//2]
negative_probs = probabilities[len(probabilities)//2:]
plt.subplot(2, 2, 3)
plt.bar(range(len(positive_probs)), positive_probs, alpha=0.6, label='Positive')
plt.bar(range(len(negative_probs)), negative_probs, alpha=0.6, label='Negative')
plt.title('Positive vs Negative State Distribution')
plt.xlabel('State Index within Sign')
plt.ylabel('Probability')
plt.legend()

# Plot 4: Base relationship diagram
plt.subplot(2, 2, 4)
plt.text(0.5, 0.8, 'Binary (2 states)\
[0,1]', ha='center', va='center', bbox=dict(facecolor='lightblue'))
plt.text(0.5, 0.5, 'Base-4 (4 states)\
[0,1,2,3]', ha='center', va='center', bbox=dict(facecolor='lightgreen'))
plt.text(0.5, 0.2, 'Base-6 (6 states)\
[0,1,2,3,4,5]', ha='center', va='center', bbox=dict(facecolor='lightpink'))
plt.arrow(0.5, 0.75, 0, -0.15, head_width=0.05, head_length=0.05)
plt.arrow(0.5, 0.45, 0, -0.15, head_width=0.05, head_length=0.05)
plt.title('Base System Relationships')
plt.axis('off')

plt.tight_layout()
plt.show()

# Print analysis
print("Multi-Base System Analysis:")
print("=========================")
print("\
Base System Relationships:")
print("------------------------")
print("Binary: 2 states (0,1) -> Sign determination")
print("Base-4: 4 states (0,1,2,3) -> Intermediate encoding")
print("Base-6: 6 states (0,1,2,3,4,5) -> Final state space")

print("\
State Space Analysis:")
print("-------------------")
print(f"Total quantum states: {len(probabilities)}")
print(f"Positive states: {len(probabilities)//2}")
print(f"Negative states: {len(probabilities)//2}")

print("\
Base Conversion Examples:")
print("----------------------")
significant_states = [(i, p) for i, p in enumerate(probabilities) if p > 0.01]
for state_idx, prob in significant_states:
    binary, sign, bin_val, base4_val, base6_val = analyze_state(state_idx)
    print(f"State |{binary}>:")
    print(f"  - {sign}")
    print(f"  - Binary value: {bin_val}")
    print(f"  - Base-4 value: {base4_val}")
    print(f"  - Base-6 mapping: {base6_val}")
    print(f"  - Probability: {prob:.4f}")

print("\
Feedback Loop Analysis:")
print("---------------------")
print("1. Binary (2 states) provides sign determination")
print("2. Base-4 (4 states) provides intermediate encoding")
print("3. Base-6 (6 states) emerges from Base-4 through modulo mapping")
print("4. The sign (binary) creates positive/negative versions of Base-6 states")
print("5. This creates a natural feedback loop: Binary -> Base-4 -> Base-6 -> Binary")