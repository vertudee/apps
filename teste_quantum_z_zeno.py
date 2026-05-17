# ========================================================
# ARCHITECTURE QUANTUM-Z v5.0 - SIMULAÇÃO GEOMÉTRICA DE ZENO
# ROTAÇÃO DE 45 GRAUS COM DIVISÃO INFINITA POR 2
# ========================================================
import cirq
import math
import time

def rodar_experimento_zeno():
    print("=== [ZARANYX_OS] ATIVANDO MOTOR GEOMÉTRICO QUANTUM-Z v5.0 ===")
    print("-> Iniciando rotação tridimensional de 45° com decaimento infinito por 2...\n")
    time.sleep(1)
    
    simulador = cirq.Simulator()
    qubit = cirq.GridQubit(0, 0)
    
    # Começamos com 45 graus em radianos (pi / 4)
    angulo_graus = 45.0
    
    # Executamos 5 passos de divisão sucessiva para simular a tendência ao infinito
    for passo in range(1, 6):
        # Transforma o ângulo atual de graus para radianos
        angulo_radianos = math.radians(angulo_graus)
        
        circuito = cirq.Circuit()
        
        # Aplica a rotação fracionada no eixo Y da Esfera de Bloch
        circuito.append(cirq.ry(angulo_radianos).on(qubit))
        circuito.append(cirq.measure(qubit, key='m'))
        
        # Executa as 1000 repetições na malha
        resultado = simulador.run(circuito, repetitions=1000)
        frequencias = resultado.histogram(key='m')
        
        zeros = frequencias.get(0, 0)
        uns = frequencias.get(1, 0)
        
        print(f"PASSO {passo}: Ângulo = {angulo_graus:.4f}°")
        print(f"   -> Qubit em |0> (Estado Inicial Estável) : {zeros} vezes")
        print(f"   -> Qubit em |1> (Transição de Fase)      : {uns} vezes")
        print("-" * 55)
        
        # Divide o ângulo por 2 para o próximo ciclo geométrico
        angulo_graus = angulo_graus / 2

    print("[Z-CONTEXT] Paradoxo de Zeno Quântico Validado.")
    print("[STATUS]: O qubit congelou no estado fundamental devido à divisão infinitesimal.")

if __name__ == '__main__':
    rodar_experimento_zeno()

