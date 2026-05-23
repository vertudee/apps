
# ========================================================
# QUANTUM-Z AUTOMATION SCRIPT - LIVE FLOW
# ========================================================

echo "=== [ZARANYX_OS] INICIANDO SINCRO QUANTUM-Z ==="

# 1. GERANDO A DOCUMENTAÇÃO README.MD AUTOMATICAMENTE
echo "-> Atualizando documentação em inglês (README.md)..."
cat << 'EOF' > README.md
# Quantum-Z Architecture (v4.0)
> A Python-based framework simulating quantum operations, state stabilization, and phase-collision logic using Google's Cirq.

This repository hosts the core modules of the **Quantum-Z Architecture**, a conceptual framework designed to test deterministic state outcomes, phase inversions, and interference patterns within simulated quantum circuits.

---

## 🌌 Core Concepts Developed

### 1. Active Noise Mitigation & Phase Inversion
Testing how active reverse operations can mitigate simulated environmental noise (such as `BitFlip` and `PhaseFlip` channels) to preserve state coherence over multiple repetitions.

### 2. Entanglement in Bell States
Simulating coupled qubits where states remain interlinked. Testing how specific operations impact entangled pairs under noise-induced stress.

### 3. Phase Collision & Amplitudes
Utilizing positive and negative amplitudes (via the Pauli-Z gate) to induce constructive and destructive interference, forcing deterministic collapses under specific matrix conditions.

---

## 📂 File Architecture

* `teste_matriz_quanti_z.py` (v1.0/v2.0): Baseline matrix execution and noise isolation filters.
* `teste_quantum_z_entrelaçado.py` (v2.5): Evaluation of noise impacts on an entangled Bell State.
* `teste_quantum_z_negativo.py` (v3.0): Demonstration of destructive interference using negative phases.
* `quantum_z_absoluto.py` (v4.0): Master module evaluating 3 specific phase variations (`LIDER_NEGATIVO`, `GÊMEO_NEGATIVO`, `AMBOS_NEGATIVOS`) showing deterministic distribution outcomes.

---

## 🛠️ How to Run the Environment

### Prerequisites
Make sure you have Python 3 and the `cirq` framework installed in your environment (e.g., Termux or Linux console):

```bash
pip install cirq

