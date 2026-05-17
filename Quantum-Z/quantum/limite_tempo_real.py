import cirq
import numpy as np
import time

def testar_limite_exponencial():
    qubit = cirq.GridQubit(0, 0)
    script = cirq.Circuit()
    
    # Montando a estrutura fundamental baseada no seu cálculo
    script.append(cirq.H(qubit))
    angulo_teste = 1.0
    script.append(cirq.rz(angulo_teste)(qubit))
    script.append(cirq.H(qubit))
    script.append(cirq.measure(qubit, key='resultado'))
    
    simulador = cirq.Simulator()
    
    # Escala de testes em tempo real (Aumentando a carga)
    escalas = [1000, 10000, 100000, 500000, 1000000]
    
    print("=== INICIANDO TESTE DE LIMITE EM TEMPO REAL ===")
    print("Monitorando a estabilidade da malha quântica...\n")
    
    for i, carga in enumerate(escalas, 1):
        t_inicio = time.time()
        
        # Executa a amostragem na máquina quântica
        operacao = simulador.run(script, repetitions=carga)
        frequencias = operacao.histogram(key='resultado')
        
        t_fim = time.time()
        tempo_gasto = t_fim - t_inicio
        
        # Extração do Pi através do colapso geométrico
        probabilidade_zero = frequencias[0] / carga
        angulo_medido = np.arccos(2 * probabilidade_zero - 1)
        pi_estimado = angulo_medido / (angulo_teste / np.pi)
        
        print(f"--- PASSO {i}: {carga} Colapsos Simultâneos ---")
        print(f"Tempo de Processamento: {tempo_gasto:.4f} segundos")
        print(f"Zonas na Caverna: {frequencias}")
        print(f"Precisão do PI alcançada: {pi_final_ajustado(pi_estimado)}")
        print("-" * 45)

def pi_final_ajustado(val):
    # Retorna o valor limpo
    return f"{val:.14f}"

if __name__ == "__main__":
    testar_limite_exponencial()

