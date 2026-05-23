import sys
import os

# Definição de cores ANSI para o terminal
COR_LARANJA = "\033[38;5;208m"
COR_RESET = "\033[0m"
COR_VERDE = "\033[1;32m"
COR_AZUL = "\033[1;34m"

def desenhar_icone_laranja():
    # Desenha a silhueta da pasta com a aba em cima e a dobra embaixo usando texto
    icone_texto = f"""
{COR_LARANJA}   ._________________.
  /   Rabisco_Z     / \\
 /                 /   \\
|  [ Z-BLOCK ]    |     |
|                 |_____|
|                       |
|                 .---. |
|                /   /  |
|_______________/___/__/ {COR_RESET}
    """
    print(icone_texto)

def analisar_arquivo_z(caminho_arquivo):
    if not os.path.exists(caminho_arquivo):
        print(f"Erro: O arquivo '{caminho_arquivo}' não foi encontrado.")
        return

    # 1. Simulação do comando 'ls' diferenciado que você pediu
    print(f"\n[ZARANYX_OS] $ ls -l {caminho_arquivo}")
    print(f"-rwxr-xr-x 1 user user 2048 May 17 11:22 {COR_LARANJA}{caminho_arquivo}{COR_RESET} (HÍBRIDO: PASTA-ARQUIVO)")
    print("-" * 50)

    # 2. Renderização do Ícone minimalista em formato de texto laranja
    desenhar_icone_laranja()

    print("=" * 50)
    print("SISTEMA Z - INTERPRETADOR DE AMBIGUIDADE")
    print("=" * 50)

    with open(caminho_arquivo, 'r', encoding='utf-8') as f:
        linhas = f.readlines()

    bloco_atual = None
    
    for linha in linhas:
        linha = linha.strip()
        if not linha:
            continue

        if "█" in linha:
            bloco_atual = linha
            print(f"\n{COR_AZUL}[ENTRANDO NO CONTEXTO]: {bloco_atual}{COR_RESET}")
        elif linha.startswith("[ICONE]") or linha.startswith("[ESTADO]"):
            print(f"  └─► Metadado Detectado: {linha}")
        elif linha.startswith("•"):
            print(f"      {COR_VERDE}├── Item Lido: {linha}{COR_RESET}")

    print("\n" + "=" * 50)
    print("Teste de leitura visual concluído!")
    print("=" * 50)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso correto: python3 sistema.py dia_arquivo.z")
    else:
        analisar_arquivo_z(sys.argv[1])
