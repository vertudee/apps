import sys
import time

def motor_adaptativo_z_block(casas_alvo):
    print("=== OPERADOR Z: MOTOR ADAPTATIVO QUÂNTICO ===")
    print(f"Alvo Dimensional: {casas_alvo} casas | Sincronismo de Silício")
    print("-" * 65)
    
    q, r, t, i = 1, 180, 60, 2
    contagem_digitos = 0
    bloco_tamanho = 1000
    margem_seguranca = 0.000001 
    descanso_atual = margem_seguranca
    
    tempo_inicio_bloco = time.time()
    
    with open("pi_balanco_zero.txt", "w") as f:
        f.write("3.")
        
        while contagem_digitos < casas_alvo:
            u = 3 * (3 * i + 1) * (3 * i + 2)
            y = (q * (27 * i - 12) + 5 * r) // (5 * t)
            
            f.write(str(y))
            
            # Álgebra Reversa (Descomputação)
            r = 10 * u * (q * (5 * i - 2) + r - y * t)
            q = 10 * q * i * (2 * i - 1)
            t = t * u
            i = i + 1
            contagem_digitos += 1
            
            # Feedback e Calibragem de Pulsação
            if contagem_digitos % bloco_tamanho == 0:
                tempo_decorrido = time.time() - tempo_inicio_bloco
                num_bloco = contagem_digitos // bloco_tamanho
                print(f"Bloco {num_bloco:04d} | Tempo: {tempo_decorrido:.6f}s | Recalibrado: {descanso_atual * 1000000:.2f} µs")
                
                # Sincronização dinâmica com o clock físico
                descanso_atual = (tempo_decorrido * 0.0001) + margem_seguranca
                time.sleep(descanso_atual)
                tempo_inicio_bloco = time.time()

    print("-" * 65)
    print("Estado de Balanço Concluído. Malha Pronta para Inversão.")

# Ponto de partida para a nova janela
# motor_adaptativo_z_block(100000)

