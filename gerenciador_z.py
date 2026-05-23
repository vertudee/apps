import os
import sys

# Cor exótica escolhida: Rosa Neon / Magenta Ácido (ANSI 198)
COR_GÊMEO = "\033[38;5;198m"
RESET = "\033[0m"
COR_SUB_ITEM = "\033[32m"  # Verde para o conteúdo interno

def criar_hibrido(nome_base):
    """Cria os dois corpos (pasta e arquivo) que agem como um só"""
    nome_pasta = f"{nome_base}.z"
    nome_arquivo = f"{nome_base}.z.txt" # Extensão interna oculta para o arquivo
    
    # 1. Cria a pasta se não existir
    if not os.path.exists(nome_pasta):
        os.makedirs(nome_pasta)
        # Cria um sub-item de exemplo dentro da pasta
        with open(os.path.join(nome_pasta, "config_sistema.z"), "w") as f:
            f.write("ESTADO: Ambiguidade Ativa")
            
    # 2. Cria o arquivo gêmeo de texto
    if not os.path.exists(nome_arquivo):
        with open(nome_arquivo, "w") as f:
            f.write(f"// Conteúdo de texto do bloco híbrido: {nome_base}\n")
            
    print(f"\n[+] Corpo duplo '{nome_base}' gerado com sucesso no sistema!")

def listar_diretorio_z():
    """Varre o diretório e condensa os gêmeos em um único componente visual"""
    itens = os.listdir('.')
    
    # Conjuntos para mapear o que encontramos
    pastas_z = set()
    arquivos_z = set()
    exibidos = set()
    
    # Identifica os componentes do ecossistema Z
    for item in itens:
        if item.endswith('.z') and os.path.isdir(item):
            pastas_z.add(item[:-2]) # Pega só o nome base
        elif item.endswith('.z.txt') and os.path.isfile(item):
            arquivos_z.add(item[:-6]) # Pega só o nome base

    print(f"\n==================================================")
    print(f"               Z-LS : PROTOTIPO GEOMETRICO        ")
    print(f"==================================================")

    # Lista os elementos Híbridos (Gêmeos) primeiro
    for base in pastas_z.intersection(arquivos_z):
        print(f"{COR_GÊMEO}󰉋 {base}.z  [HÍBRIDO: PASTA-ARQUIVO GÊMEO]{RESET}")
        # Mostra o que tem dentro da pasta de forma compacta
        sub_itens = os.listdir(f"{base}.z")
        for sub in sub_itens:
            print(f"  └── {COR_SUB_ITEM}Item Lido: • {sub} >> [Ativo]{RESET}")
        exibidos.add(f"{base}.z")
        exibidos.add(f"{base}.z.txt")

    # Lista o restante dos arquivos normais do usuário (se houver) para não sumir com nada
    for item in itens:
        if item != "gerenciador_z.py" and item not in exibidos and not item.endswith('.z.txt'):
            print(f"  {item}")
            
    print(f"==================================================")

if __name__ == "__main__":
    # Se passar argumento, ele cria. Se não, ele apenas lista.
    if len(sys.argv) > 1:
        nome_do_bloco = sys.argv[1]
        criar_hibrido(nome_do_bloco)
    
    # Mostra o resultado visual do comando customizado
    listar_diretorio_z()

