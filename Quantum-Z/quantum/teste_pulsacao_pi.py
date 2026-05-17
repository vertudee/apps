import sys
import time

def teste_pi_com_pulsacao(casas_alvo, microsegundos_descanso):
    # Converte microsegundos para a escala do time.sleep (segundos)
    tempo_descanso = microsegundos_descanso / 1000000.0
    
    print(f"=== INICIANDO MOTOR PULSADO: {casas_alvo} DIANOS ===")
    print(f"Intervalo de relaxamento da malha: {microsegundos_descanso} µs por ciclo.")
    print("Gravando e limpando resíduos em fluxo controlado...")
    print("-" * 50)
    
    inicio = time.time()
    
    q = 1
    r = 180
    t = 60
    i = 2
    
    contagem_digitos = 0
    
    with open("pi_pulsado.txt", "w") as f:
        f.write("3.")
        
        while contagem_digitos < casas_alvo:
            u = 3 * (3 * i + 1) * (3 * i + 2)
            y = (q * (27 * i - 12) + 5 * r) // (5 * t)
            
            # Extrai o resíduo para o arquivo
            f.write(str(y))
            
            # Operação reversa e descomputação (Retorno ao Zero)
            r = 10 * u * (q * (5 * i - 2) + r - y * t)
            q = 10 * q * i * (2 * i - 1)
            t = t * u
            i = i + 1
            
            contagem_digitos += 1
            
            # O PULO DO GATO: Micro-pausa para o processador descansar
            if tempo_descanso > 0:
                time.sleep(tempo_descanso)
            
            # Monitoramento em tempo real a cada 10.000 dígitos
            if contagem_digitos % 10000 == 0:
                print(f"-> Malha Estável: {contagem_digitos} dígitos. Processador respirando...")

    fim = time.time()
    print("-" * 50)
    print(f"Fluxo de Pulsação Concluído!")
    print(f"Tempo Total de Corrida: {fim - inicio:.4f} segundos")
    print(f"Resultado guardado em 'pi_pulsado.txt'")

# Executa 1 Milhão de casas dando 1 microsegundo de descanso a cada dígito
teste_pi_com_pulsacao(1000000, 1)

