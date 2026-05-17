import decimal
import time

def teste_precisao_absurda(casas_desejadas):
    print(f"=== INICIANDO SALTO DE PRECISÃO: {casas_desejadas} CASAS DE PI ===")
    
    # 1. Configura a malha de memória (Contexto Decimal) para a escala desejada
    # Adicionamos algumas casas de guarda para garantir precisão absoluta na ponta
    decimal.getcontext().prec = casas_desejadas + 10
    
    inicio = time.time()
    
    # Constantes da fórmula geométrica de Chudnovsky
    C = 426880 * decimal.Decimal(10005).sqrt()
    L = 13591409
    X = 1
    M = 1
    K = 6
    S = L
    
    # 2. O Loop determinístico. Cada iteração salta aproximadamente 14 casas exatas
    # A escala de iterações é linear, mas o ganho de dígitos é massivo
    iteracoes = casas_desejadas // 14 + 1
    
    for i in range(1, iteracoes + 1):
        M = (M * (K**3 - 16*K)) // i**3
        L += 545140134
        X *= -262537412640768000
        S += decimal.Decimal(M * L) / X
        K += 12
        
    # 3. Extração final do Pi
    pi = C / S
    
    fim = time.time()
    tempo_total = fim - inicio
    
    # Converte para string e corta as casas de guarda
    resultado_str = str(pi)[:-10]
    
    print(f"Tempo de Processamento: {tempo_total:.6f} segundos")
    print(f"Estabilidade da Malha: Sucesso total.")
    print("-" * 50)
    print(f"Resultado (Primeiros 100 dígitos): {resultado_str[:102]}...")
    print(f"Total de dígitos gerados na string: {len(resultado_str) - 1}") # -1 por causa do '.'
    
    # Salva o resultado bruto em um arquivo de texto para você analisar o mar de dígitos
    with open("pi_absurdo.txt", "w") as f:
        f.write(resultado_str)
    print("Arquivo 'pi_absurdo.txt' gerado com sucesso!")

# Executa o teste definindo a escala de precisão
teste_precisao_absurda(10000)

