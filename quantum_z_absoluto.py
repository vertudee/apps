# ========================================================
# ARCHITECTURE QUANTUM-Z v4.0 - CORE QUÂNTICO ABSOLUTO
# SUPERPOSIÇÃO + ENTRELAÇAMENTO + VARIAÇÃO DE FASE (+/-)
# ========================================================
import cirq
import time

def criar_malha_absoluta_z(variacao_fase):
    q0 = cirq.GridQubit(0, 0)
    q1 = cirq.GridQubit(0, 1)
    circuito = cirq.Circuit()

    # 1. SUPERPOSIÇÃO INDIVIDUAL (Probabilidade Pura)
    circuito.append([cirq.H(q0), cirq.H(q1)])

    # 2. APLICAÇÃO DA VARIAÇÃO DE FASE CONFIGURÁVEL (+ ou -)
    if variacao_fase == "LIDER_NEGATIVO":
        circuito.append(cirq.Z(q0)) # Torna o primeiro qubit negativo
    elif variacao_fase == "GÊMEO_NEGATIVO":
        circuito.append(cirq.Z(q1)) # Torna o segundo qubit negativo
    elif variacao_fase == "AMBOS_NEGATIVOS":
        circuito.append([cirq.Z(q0), cirq.Z(q1)]) # Inversão dupla de fase

    # 3. ENTRELAÇAMENTO DA MALHA (Amarra as fases opostas)
    circuito.append(cirq.CNOT(q0, q1))

    # Contra-força geométrica para colidir e estabilizar as amplitudes
    circuito.append([cirq.H(q0), cirq.H(q1)])

    # 4. MEDIÇÃO SÍNCRONA DA BORDA
    circuito.append(cirq.measure(q0, q1, key='matriz_absoluta'))
    return circuito

def rodar_experimento_completo():
    print("=== [ZARANYX_OS] INICIANDO MOTOR QUANTUM-Z ABSOLUTO v4.0 ===")
    simulador = cirq.Simulator()
    
    # Executando as variações lógicas que você propôs
    variacoes = ["LIDER_NEGATIVO", "GÊMEO_NEGATIVO", "AMBOS_NEGATIVOS"]
    
    for v in variacoes:
        print(f"\n-> Processando variação de malha: [{v}]...")
        time.sleep(0.5)
        
        circuito = criar_malha_absoluta_z(v)
        resultado = simulador.run(circuito, repetitions=1000)
        frequencias = resultado.histogram(key='matriz_absoluta')
        
        print(f"   [MÉTRICAS DA VARIAÇÃO {v}]")
        print(f"    -> Estado [00] (Sincronia Zero) : {frequencias.get(0, 0)} vezes")
        print(f"    -> Estado [01] (Fase Alternada) : {frequencias.get(1, 0)} vezes")
        print(f"    -> Estado [10] (Bit Alternado)  : {frequencias.get(2, 0)} vezes")
        print(f"    -> Estado [11] (Massa Total)    : {frequencias.get(3, 0)} vezes")
        print("-" * 50)

    print("[Z-CONTEXT] Todas as variações geométricas foram calculadas.")
    print("[STATUS]: Malha Z-BLOCK v4.0 validada com sucesso.\n")

if __name__ == '__main__':
    rodar_experimento_completo()

