import sys
import time

def teste_estresse_extremo(casas_alvo):
    print(f"=== INICIANDO TESTE DE ESTRESSE: {casas_alvo} DIANOS ===")
    print("Canalizando fluxo de anulação direto para arquivo 'pi_estresse.txt'...")
    
    inicio = time.time()
    
    q = 1
    r = 180
    t = 60
    i = 2
    
    contagem_digitos = 0
    
    # Abre o arquivo para ir gravando os blocos conforme eles são anulados
    with open("pi_estresse.txt", "w") as f:
        f.write("3.")
        
        while contagem_digitos < casas_alvo:
            u = 3 * (3 * i + 1) * (3 * i + 2)
            y = (q * (27 * i - 12) + 5 * r) // (5 * t)
            
            # Grava o dígito isolado diretamente no disco
            f.write(str(y))
            
            # Operação reversa e descomputação
            r = 10 * u * (q * (5 * i - 2) + r - y * t)
            q = 10 * q * i * (2 * i - 1)
            t = t * u
            i = i + 1
            
            contagem_digitos += 1
            
            # Feedback visual a cada 100.000 dígitos para monitorar a malha
            if contagem_digitos % 100000 == 0:
                print(f"-> Progresso da Malha: {contagem_digitos} dígitos processados.")

    fim = time.time()
    print("-" * 50)
    print(f"Teste de Estresse Concluído!")
    print(f"Tempo Total: {fim - inicio:.4f} segundos")
    print(f"Arquivo 'pi_estresse.txt' gerado com sucesso.")

# Dispara o milhão
teste_estresse_extremo(1000000)

