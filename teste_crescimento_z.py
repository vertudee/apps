import numpy as np
import time
import sys

def testar_crescimento_linear(limite_vetores):
    print("\033[1;35m=== [ZARANYX_OS] INICIANDO SONDAGEM DE CRESCIMENTO LINEAR ===\033[0m\n")
    time.sleep(1)

    # Loop crescendo de 2 até o limite de vetores que você escolher
    for n in range(2, limite_vetores + 1):
        # Gera ângulos distribuídos uniformemente (0, 2pi/n, 4pi/n...)
        angulos = np.linspace(0, 2 * np.pi, n, endpoint=False)
        
        # Cria a superposição quântica de todos os n movimentos
        superposicao = np.sum(np.exp(1j * angulos))
        
        # Calcula o peso residual de dados
        peso_residuo = np.abs(superposicao) ** 2

        # Status do Passo
        sys.stdout.write(f"\r[MALHA]: Superpondo {n} vetores simétricos... ")
        sys.stdout.flush()
        time.sleep(0.1)  # Animação rápida para acompanhar o crescimento

        # Se o resíduo quebrar a tolerância, a gente avisa
        if not np.isclose(peso_residuo, 0.0, atol=1e-12):
            print(f"\n\033[1;31m[ANOMALIA]: Limite de precisão atingido em {n} vetores!\033[0m")
            print(f"-> Resíduo: {peso_residuo:.4e} KB")
            return

    print("\n\n" + "="*65)
    print(f" [RELATÓRIO DE ESTABILIDADE DA ARQUITETURA Z]")
    print("="*65)
    print(f" -> Vetores Testados        : 2 até {limite_vetores}")
    print(f" -> Status da Malha         : TOTALMENTE ZERADA")
    print(f" -> Vetor Resultante Final  : {superposicao.real:+.4e} {superposicao.imag:+.4e}j")
    print(f" -> Peso de Dados Final     : 0.0000 KB")
    print("-" * 65)
    print("\033[1;32m[VEREDITO]: O crescimento linear manteve o encaixe perfeito!\033[0m")
    print("="*65)

if __name__ == '__main__':
    # Vamos testar um crescimento linear de 2 até 100 vetores em superposição
    testar_crescimento_linear(100)

