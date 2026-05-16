# ========================================================
# ARCHITECTURE QUANTUM-Z v9.0 - DIAGNÓSTICO DE PORTAS PURAS
# MAPEAMENTO DA TABELA DO CADERNO EM X, H, Z E CNOT
# ========================================================
import cirq
import math
import time

def rodar_laboratorio_portas():
    print("=== [ZARANYX_OS] INICIANDO DIAGNÓSTICO DE PORTAS v9.0 ===")
    print("-> Testando o impacto da escala do caderno nas portas fundamentais...\n")
    time.sleep(1)

    simulador = cirq.Simulator()
    
    # Valores críticos da tabela do seu caderno para o teste de estresse
    valores_caderno = [-9, 0, 10]

    # 1. TESTE DA PORTA X (INVERSÃO BINÁRIA)
    print("=" * 60)
    print("[FASE 1]: ANALISANDO PORTA X (NOT)")
    print("=" * 60)
    q = cirq.GridQubit(0, 0)
    for v in valores_caderno:
        circuito = cirq.Circuit()
        fase = (v * math.pi) / 10
        circuito.append(cirq.ry(fase).on(q)) # Injeta o valor do caderno
        circuito.append(cirq.X(q))           # Aplica o operador X
        circuito.append(cirq.measure(q, key='m'))
        res = simulador.run(circuito, repetitions=1000).histogram(key='m')
        print(f"Caderno [{v: >2}] -> Pós-Porta X -> |0>: {res.get(0,0):<4} | |1>: {res.get(1,0):<4}")

    # 2. TESTE DA PORTA H (HADAMARD - SUPERPOSIÇÃO)
    print("\n" + "=" * 60)
    print("[FASE 2]: ANALISANDO PORTA H (HADAMARD)")
    print("=" * 60)
    for v in valores_caderno:
        circuito = cirq.Circuit()
        fase = (v * math.pi) / 10
        circuito.append(cirq.ry(fase).on(q)) # Injeta o valor do caderno
        circuito.append(cirq.H(q))           # Aplica o operador H
        circuito.append(cirq.measure(q, key='m'))
        res = simulador.run(circuito, repetitions=1000).histogram(key='m')
        print(f"Caderno [{v: >2}] -> Pós-Porta H -> |0>: {res.get(0,0):<4} | |1>: {res.get(1,0):<4}")

    # 3. TESTE DA PORTA Z (INVERSÃO DE FASE)
    print("\n" + "=" * 60)
    print("[FASE 3]: ANALISANDO PORTA Z (PHASE FLIP)")
    print("=" * 60)
    for v in valores_caderno:
        circuito = cirq.Circuit()
        fase = (v * math.pi) / 10
        circuito.append(cirq.ry(fase).on(q)) # Injeta o valor do caderno
        circuito.append(cirq.Z(q))           # Aplica o operador Z
        circuito.append(cirq.measure(q, key='m'))
        res = simulador.run(circuito, repetitions=1000).histogram(key='m')
        print(f"Caderno [{v: >2}] -> Pós-Porta Z -> |0>: {res.get(0,0):<4} | |1>: {res.get(1,0):<4}")

    # 4. TESTE DA PORTA CNOT (EMARANHAMENTO CONTROLADO)
    print("\n" + "=" * 60)
    print("[FASE 4]: ANALISANDO PORTA CNOT (2 QUBITS)")
    print("=" * 60)
    q0 = cirq.GridQubit(0, 0)
    q1 = cirq.GridQubit(0, 1)
    for v in valores_caderno:
        circuito = cirq.Circuit()
        fase = (v * math.pi) / 10
        circuito.append(cirq.ry(fase).on(q0)) # Injeta o valor no controle (q0)
        circuito.append(cirq.CNOT(q0, q1))    # q0 controla q1
        circuito.append(cirq.measure(q0, q1, key='m'))
        res = simulador.run(circuito, repetitions=1000).histogram(key='m')
        print(f"Caderno [{v: >2}] -> Pós-CNOT   -> [00]: {res.get(0,0):<4} | [11]: {res.get(3,0):<4}")

    print("\n[Z-CONTEXT] Diagnóstico completo de operadores finalizado.")
    print("[STATUS]: Motores validados com a simetria do caderno.")

if __name__ == '__main__':
    rodar_laboratorio_portas()

