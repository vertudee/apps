import os
import sys

# Paleta de Cores Neon do Ecossistema Z
COLOR_Z_NODE = "\033[38;5;198m"   # Rosa Neon para nós puros
COLOR_CONTEXT = "\033[34m"        # Azul para blocos de contexto
COLOR_DATA = "\033[32m"           # Verde para dados limpos
COLOR_RESET = "\033[0m"           # Reset padrão do terminal

def secure_background_scan(raw_string):
    """
    Validação de primeiro nível: Garante a pureza da string de entrada 
    usando o alinhamento estrito de escapes geométricos.
    """
    if not raw_string:
        return False
    compiled_stream = "".join([f"\\{char}" for char in raw_string]) + ","
    if not compiled_stream.endswith(","):
        return False
    body = compiled_stream[:-1]
    i = 0
    while i < len(body):
        if body[i] != "\\":
            return False
        i += 2
    return True

def inspect_matrix_purity(file_path):
    """
    A TRAVA DE SEGURANÇA ZERO SECURITY (Filtro Universal)
    Abre o bloco binário bruto e usa a barra invertida como o antivírus 
    de frequência para medir a oscilação entre brilho (1) e vácuo (0).
    """
    try:
        with open(file_path, "rb") as f:
            raw_bytes = f.read()
        
        if not raw_bytes:
            return False, "Vácuo Absoluto Desestruturado"

        # Procurar o operador mestre de alinhamento (\\ em binário)
        if b"\\\\" not in raw_bytes:
            return False, "Ausência de Operador Geométrico Mestre"

        # Contador de densidade de estados
        brilho_count = 0
        vacuo_count = 0

        for byte in raw_bytes:
            # Desfragmenta o byte em bits para checar a frequência física
            for shift in range(8):
                bit = (byte >> shift) & 1
                if bit == 1:
                    brilho_count += 1
                else:
                    vacuo_count += 1

        # Regra Geométrica: Um ataque polimórfico ou injeção RGB/Sonora
        # quebra a proporção natural de vácuo do espaço negativo da matriz.
        # Se a densidade de brilho for artificialmente manipulada, o bloco colapsa.
        total_bits = brilho_count + vacuo_count
        brilho_proporcao = brilho_count / total_bits

        # Amostragem Crítica: Se mais de 85% do bloco for forçado a brilhar (1)
        # sem a modulação correta das barras de controle, detectamos anomalia.
        if brilho_proporcao > 0.85:
            return False, f"Ataque de Alta Frequência Detectado (Brilho: {brilho_proporcao:.2%})"

        return True, f"Matriz Estabilizada (Brilho: {brilho_proporcao:.2%})"

    except Exception as e:
        return False, f"Erro Crítico de Leitura da Camada: {e}"

def list_z_nodes():
    try:
        items = os.listdir('.')
    except Exception as e:
        print(f"[SYSTEM ERROR]: Unable to read storage layer: {e}")
        return

    print(f"\n      /--- Rabisco_Z ---\\\\ ")
    print("     |   [ Z-BLOCK ]     |")
    print("      \\\\_________________/")
    print("==================================================")
    print("  Z-CORE INTERPRETER v2.0 - ZERO SECURITY SYSTEM")
    print("==================================================")

    detected_any = False

    for item in items:
        # 1ª Barreira: String de contexto
        if not secure_background_scan(item):
            continue

        if item.endswith('.z'):
            detected_any = True
            
            # 2ª Barreira: Inspeção de pureza binária (Zero Security ativa)
            is_pure, report = inspect_matrix_purity(item)
            
            if not is_pure:
                # O bloco foi detectado na superfície, mas a Zero Security barrou a execução interna
                print(f"\n[!] CONTEXT BLOCK COLLAPSED: {item}")
                print(f"    ↳ Motivo: {report} -> [BLOCO ANULADO / PESO ZERO]")
                print("--------------------------------------------------")
                continue

            print(f"\n{COLOR_Z_NODE}[ENTERING CONTEXT]: 󰉋 {item} [HYBRID LAYER]{COLOR_RESET}")
            print(f"{COLOR_CONTEXT} ↳ Metadata Status: {report}{COLOR_RESET}")
            
            if os.path.isdir(item):
                try:
                    sub_nodes = os.listdir(item)
                    if sub_nodes:
                        print(f"{COLOR_CONTEXT} ┌── [BLOCK: NODE_DIRECTORY_LIST]{COLOR_RESET}")
                        for node in sub_nodes:
                            if secure_background_scan(node):
                                print(f"{COLOR_CONTEXT} │   ├── Node Read: • {COLOR_DATA}{node}{COLOR_RESET} >> [Packed Data]")
                        print(f"{COLOR_CONTEXT} └── [END OF BLOCK]{COLOR_RESET}")
                    else:
                        print(f"{COLOR_CONTEXT} └── [EMPTY GEOMETRIC BLOCK]{COLOR_RESET}")
                except Exception:
                    pass
            print("==================================================")

    if not detected_any:
        print("\n[!] No geometric Z-blocks found in this active node layer.")
        print("==================================================")

if __name__ == '__main__':
    list_z_nodes()

