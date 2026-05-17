# ========================================================
# ARCHITECTURE QUANTUM-Z v7.0 - VARREDURA COMPLETA DE MATRIZ
# MAPEAMENTO GEOMÉTRICO DO CADERNO (-9 ATÉ +10)
# ========================================================
import cirq
import math
import time

def mapear_valor_para_fase(valor):
    # Mapeia a amplitude linear da tabela do caderno para um espaço geométrico.
    # Usamos uma divisão angular para que o espectro de -9 a 10 caiba na malha.
    return (valor * math.pi) / 10

def executar_varredura_tabela():
    print("=== [ZARANYX_OS] INICIANDO VARREDURA COMPLETA DA MALHA Z ===")
    print("-> Carregando limites do caderno: Mínimo [-9] até Máximo [+10]...\n")
    time.sleep(1.5)

    simulador = cirq.Simulator()
    q0 = cirq.GridQubit(0, 0)

    # Valores críticos da sua tabela para testar a ortogonalidade extrema
    pontos_teste = [-9, -5, -1, 0, 1, 5, 10]

    print(f"{'VALOR Z':<10} | {'ÂNGULO RAD':<12} | {'ESTADO |0>':<12} | {'ESTADO |1>':<12} | STATUS DA MALHA")
    print("-" * 75)

    for valor in points_teste if 'points_teste' in locals() else pontos_teste:
        fase = mapear_valor_para_fase(valor)
        
        circuito = cirq.Circuit()
        
        # Reconstrói a rotação baseada estritamente no número do seu caderno
        # Se for negativo, a rotação vai para a esquerda; se positivo, para a direita.
        circuito.append(cirq.ry(fase).on(q0))
        circuito.append(cirq.measure(q0, key='m'))
        
        resultado = simulador.run(circuito, repetitions=1000)
        frequencias = resultado.histogram(key='m')
        
        zeros = frequencias.get(0, 0)
        uns = frequencias.get(1, 0)
        
        # Define o comportamento de isolação baseado na sua lógica de eixos
        if valor == 0:
            status = "CENTRO ABSOLUTO"
        elif valor == -9 or valor == 10:
            status = "ORTOGONALIDADE MÁXIMA"
        else:
            status = "TRANSLAÇÃO DE FASE"

        print(f"{valor:<10} | {fase:<12.4f} | {zeros:<12} | {uns:<12} | {status}")

    print("\n[Z-CONTEXT] Varredura matricial finalizada.")
    print("[STATUS]: Dados prontos para serem acoplados ao Live Flow.")

if __name__ == '__main__':
    executar_varredura_tabela()

