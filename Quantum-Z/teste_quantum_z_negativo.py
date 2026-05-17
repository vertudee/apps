# ========================================================
# ARCHITECTURE QUANTUM-Z v3.0 - ANULAÇÃO DE FASE NEGATIVA
# COLISÃO DE AMPLITUDES POSITIVAS E NEGATIVAS
# ========================================================
import cirq
import time

def criar_malha_fase_negativa_z():
    # Mapeamento dos nossos pontos na malha geométrica
    q_positivo = cirq.GridQubit(0, 0)
    q_negativo = cirq.GridQubit(0, 1)

    circuito = cirq.Circuit()

    # 1. CRIAÇÃO DO QUBIT POSITIVO |+>
    circuito.append(cirq.H(q_positivo))

    # 2. CRIAÇÃO DO QUBIT NEGATIVO |->
    # Aplicamos Hadamard para criar superposição e Z para negativar a fase
    circuito.append([
        cirq.H(q_negativo),
        cirq.Z(q_negativo)  # Inverte a fase do componente |1>, tornando-o negativo
    ])

    # 3. A SOMA / COLISÃO DE MATRIZES (A OPERAÇÃO Z)
    # Combinamos os dois estados através de um emaranhamento controlado
    circuito.append(cirq.CNOT(q_positivo, q_negativo))

    # Aplicamos a contra-força para trazer o resultado de volta ao bloco estável
    circuito.append(cirq.H(q_positivo))

    # 4. MEDIÇÃO DA BORDA DO BLOCO
    circuito.append([
        cirq.measure(q_positivo, key='resultado_pos'),
        cirq.measure(q_negativo, key='resultado_neg')
    ])
    
    return circuito

def rodar_simulacao():
    print("=== [ZARANYX_OS] ATIVANDO CONFIGURAÇÃO QUANTUM-Z v3.0 ===")
    print("-> Gerando qubits com amplitudes positivas e negativas...")
    time.sleep(1)
    
    circuito = criar_malha_fase_negativa_z()
    simulador = cirq.Simulator()
    resultado = simulador.run(circuito, repetitions=1000)
    
    # Coleta os resultados das medições
    freq_pos = resultado.histogram(key='resultado_pos')
    freq_neg = resultado.histogram(key='resultado_neg')
    
    print("\n" + "="*50)
    print("[MATRIZ DE COLISÃO DE FASE CONCLUÍDA]")
    print("="*50)
    print("-" * 50)
    print("[MÉTRICAS DA ANULAÇÃO DE SINAL]")
    print(f" -> Qubit Positivo - Estado |0> : {freq_pos.get(0, 0)} vezes")
    print(f" -> Qubit Positivo - Estado |1> : {freq_pos.get(1, 0)} Association")
    print(f" -> Qubit Negativo - Estado |0> : {freq_neg.get(0, 0)} vezes")
    print(f" -> Qubit Negativo - Estado |1> : {freq_neg.get(1, 0)} vezes")
    print("-" * 50)
    print("[Z-CONTEXT] Colisão concluída. Amplitudes negativas processadas.")
    print("[STATUS]: Código pronto para versionamento.\n")

if __name__ == '__main__':
    rodar_simulacao()

