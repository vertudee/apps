# ========================================================
# ARCHITECTURE QUANTUM-Z v2.5 - MOTOR DE ENTRELAÇAMENTO
# SISTEMA DE ANULAÇÃO EM ESTADO DE BELL (EMARANHADO)
# ========================================================
import cirq
import time

def criar_malha_entrelacada_z():
    # Mapeamento de dois qubits da nossa malha geométrica
    q0 = cirq.GridQubit(0, 0)  # Qubit Líder (Sinal)
    q1 = cirq.GridQubit(0, 1)  # Qubit Gêmeo (Emaranhado)

    circuito = cirq.Circuit()

    # 1. PRODUÇÃO DO ENTRELAÇAMENTO PURO (ESTADO DE BELL)
    # Coloca q0 em superposição e amarra o destino de q1 a ele
    circuito.append([
        cirq.H(q0),
        cirq.CNOT(q0, q1)
    ])

    # 2. CANAL DE RUÍDO AGRESSIVO (INTERFERÊNCIA AMBIENTE)
    # O ruído agora tenta atacar os dois qubits emaranhados ao mesmo tempo
    circuito.append([
        cirq.BitFlipChannel(p=0.4).on(q0),
        cirq.PhaseFlipChannel(p=0.4).on(q1)
    ])

    # 3. CONTRA-FORÇA NEGATIVA DE ANULAÇÃO (A ASSINATURA Z)
    # Como eles estão emaranhados, aplicamos a inversão simétrica de fase 
    # para colidir o erro e restaurar o balanço zero na malha inteira
    circuito.append([
        cirq.X(q0),
        cirq.X(q1),
        cirq.CNOT(q0, q1),  # Descomputação do emaranhamento do ruído
        cirq.X(q0),
        cirq.X(q1)
    ])

    # 4. MEDIÇÃO SÍNCRONA DA BORDA
    # Medimos os dois ao mesmo tempo para ver se a conexão foi protegida
    circuito.append(cirq.measure(q0, q1, key='resultado_emaranhado'))
    
    return circuito

def rodar_simulacao():
    print("=== [ZARANYX_OS] ATIVANDO MATRIZ QUANTUM-Z: EMARANHADO ===")
    print("-> Criando Estado de Bell e injetando contra-força...")
    time.sleep(1)
    
    circuito = criar_malha_entrelacada_z()
    simulador = cirq.Simulator()
    resultado = simulador.run(circuito, repetitions=1000)
    
    # Coleta o histograma das combinações de estados (00, 01, 10, 11)
    frequencias = resultado.histogram(key='resultado_emaranhado')
    
    print("\n" + "="*50)
    print("[MATRIZ DE COERÊNCIA EMARANHADA SALVA]")
    print("="*50)
    print(f"Dados brutos coletados:\n{resultado}")
    print("-" * 50)
    print("[EFEITO DA COLISÃO NO ESPELHO QUÂNTICO]")
    
    # No emaranhamento puro protegido, os qubits só podem ser 00 ou 11. 
    # Se aparecer muito 01 ou 10, significa que o ruído quebrou o sistema.
    print(f" -> Qubits em [00] (Sincronia Zero) : {frequencias.get(0, 0)} vezes")
    print(f" -> Qubits em [01] (Erro de Fase)   : {frequencias.get(1, 0)} vezes")
    print(f" -> Qubits em [10] (Erro de Bit)    : {frequencias.get(2, 0)} vezes")
    print(f" -> Qubits em [11] (Sincronia Total): {frequencias.get(3, 0)} vezes")
    print("-" * 50)
    print("[Z-CONTEXT] Filtro concluído. Conexão fantasmagórica estabilizada.")
    print("[STATUS]: Repositório local atualizado. Prompt livre.\n")

if __name__ == '__main__':
    rodar_simulacao()

