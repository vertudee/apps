import os
import sys

# Cor exótica: Rosa Neon / Magenta Ácido (ANSI 198)
COR_GÊMEO = "\033[38;5;198m"
RESET = "\033[0m"
COR_LINHA = "\033[34m"  # Azul para as linhas de contexto

def listar_diretorio_z():
    itens = os.listdir('.')
    
    # Desenha o seu cabeçalho clássico e limpo
    print("\n      /--- Rabisco_Z ---\\ ")
    print("     |   [ Z-BLOCK ]     |")
    print("      \\_________________/")
    print("==================================================")
    print(" SISTEMA Z - INTERPRETADOR DE AMBIGUIDADE (Z-LS) ")
    print("==================================================")

    bloco_detectado = False

    for item in itens:
        # Se for o seu arquivo/pasta dia_arquivo.z ou qualquer .z
        if item.endswith('.z'):
            bloco_detectado = True
            print(f"\n{COR_GÊMEO}[ENTRANDO NO CONTEXTO]: 󰉋 {item} [HÍBRIDO: PASTA-ARQUIVO]{RESET}")
            print(f"{COR_LINHA} ↳ Metadado Detectado: [ESTADO] Ambiguidade Ativa{RESET}")
            
            # Se for uma pasta real, vamos listar o que tem dentro no padrão Z
            if os.path.isdir(item):
                try:
                    sub_itens = os.listdir(item)
                    if sub_itens:
                        print(f"{COR_LINHA} ┌── [BLOCO: LISTA_DIRETORIO]{RESET}")
                        for sub in sub_itens:
                            print(f"{COR_LINHA} │   ├── Item Lido: • \033[32m{sub}\033[0m >> [Dado Compactado]")
                        print(f"{COR_LINHA} └── [FIM DO BLOCO]{RESET}")
                    else:
                        print(f"{COR_LINHA} └── [BLOCO VAZIO]{RESET}")
                except Exception:
                    pass
            print(f"==================================================")

    # Se não houver nenhum bloco Z no diretório
    if not bloco_detectado:
        print("\n[!] Nenhum bloco geométrico Z detectado neste diretório.")
        print(f"==================================================")

if __name__ == "__main__":
    listar_diretorio_z()

