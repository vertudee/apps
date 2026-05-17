# ========================================================
# ARCHITECTURE QUANTUM-Z v8.0 - EMARANHAMENTO MULTIDIMENSIONAL
# SIMETRIA EXPANDIDA (ESTADO GHZ BASEADO NO CADERNO)
# ========================================================
import cirq
import math
import time

def rodar_sistema_expandido():
    print("=== [ZARANYX_OS] PROJETANDO EXTENSÃO DA MALHA QUANTUM-Z v8.0 ===")
    print("-> Acoplando 3 dimensões quânticas em emaranhamento simétrico...")
    time.sleep(1.5)

    simulador = cirq.Simulator()
    
    # Criamos um sistema tridimensional de qubits (q0, q1, q2)
    qubits = [cirq.GridQubit(0, i) for i in range(3)]
    
    # Vamos testar o choque entre o extremo positivo (+10) e negativo (-9) do seu caderno
    valores_sistema = [-9, 10]

    for valor in valores_sistema:
        circuito = cirq.Circuit()
        
        # Passo 1: Coloca o líder na superposição da tabela
        fase = (valor * math.pi) / 10
        circuito.append(cirq.ry(fase).on(qubits[0]))
        
        # Passo 2: A PEÇA CHAVE - Emaranhamento em Cadeia (GHZ)
        # O qubit 0 puxa o 1, que puxa o 2. A simetria do caderno se espalha pelo sistema.
        circuito.append(cirq.CNOT(qubits[0], qubits[1]))
        circuito.append(cirq.CNOT(qubits[1], qubits[2]))
        
        # Medição de todo o bloco de contexto
        circuito.append(cirq.measure(*qubits, key='sistema_z'))
        
        resultado = simulador.run(circuito, repetitions=1000)
        frequencias = resultado.histogram(key='sistema_z')
        
        print("\n" + "="*55)
        print(f"[MATRIZ EXPANDIDA - VALOR DO CADERNO: {valor}]")
        print("="*55)
        for estado, contagem in sorted(frequencias.items()):
            # Converte a chave do estado para binário de 3 bits para facilitar a leitura
            binario = format(estado, '03b')
            print(f" -> Estado [{binario}] : {contagem} vezes")
            
    print("\n[Z-CONTEXT] Alinhamento multidimensional concluído.")
    print("[STATUS]: Sistema quântico unificado com a simetria Z.")

if __name__ == '__main__':
    rodar_sistema_expandido()

