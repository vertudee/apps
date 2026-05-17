from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

# 1. Criamos um circuito com 1 Qubit (nossa variável quântica) e 1 bit clássico (nosso travamento)
circuit = QuantumCircuit(1, 1)

# 2. Aplicamos um giro de 90 graus (Porta Hadamard) para colocar o qubit em sobreposição total
# Aqui ele vira uma mistura de 0 e 1 ao mesmo tempo
circuit.h(0)

# 3. Aplicamos o "Travamento" (Medição)
# Isso força o vetor a colapsar e decidir se vira 0 ou vira 1
circuit.measure(0, 0)

# 4. Rodamos o simulador dentro do celular para ver o resultado
simulator = AerSimulator()
result = simulator.run(circuit, shots=1000).result()
counts = result.get_counts(circuit)

print("\n--- Resultado do Travamento Quântico ---")
print(counts)

