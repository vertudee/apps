import re
import sys

# Script Z-Compiler: Versão Água (Fluida)
# Corrige falhas na captura de símbolos e espaços no Termux.

def compile_z_to_asm(input_file):
    try:
        # Tenta ler com UTF-8 explícito para capturar € ¥ ₩ £
        with open(input_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except Exception as e:
        print(f"Erro ao ler o arquivo: {e}")
        return

    # Usaremos dicionários para organizar as seções de forma dinâmica
    sections = {
        ".section .rodata": [],
        ".section .data": []
    }
    
    # O esqueleto padrão do Assembly para Linux
    asm_text = [
        ".section .text\n", 
        ".global _start\n", 
        "_start:\n",
        # Syscall Exit Padrão para Linux (evita travamento)
        "    mov $60, %rax\n",   # Syscall num: exit (60)
        "    xor %rdi, %rdi\n",  # Status: 0
        "    syscall\n"
    ]

    # Novo Regex: Mais robusto contra espaços extras e símbolos
    # Explicação: 
    # (.*?) : Captura qualquer símbolo (como €, ¥...)
    # (\w+) : O tipo de dado (int, char...)
    # ([\w_]+) : As coordenadas (A_base_)
    # @(.*?)\s*@ : Captura o conteúdo entre os arrobas.
    pattern = re.compile(r'^\s*(.*?)\s*(\w+)_\s*([\w_]+)\s*@\s*(.*?)\s*@')

    line_count = 0
    for line in lines:
        line_count += 1
        line = line.strip()
        if not line or line.startswith("//"): continue

        match = pattern.search(line)
        
        if match:
            symbol, dtype, coords, content = match.groups()
            symbol = symbol.strip() # Limpa possíveis espaços invisíveis
            
            # Definindo tamanhos de dados no ASM (ex: .long, .quad)
            # Você pode expandir isso conforme a necessidade de anulação de peso.
            asm_type = ".long" if symbol == '€' else ".byte" if symbol == '£' else ".quad" if symbol == '¥' else ".asciz"
            
            # Lógica Geométrica: Se a primeira letra é maiúscula, é Read-Only
            # Isso move o dado para uma área de memória protegida no Linux.
            is_static = coords[0].isupper()
            target_section_name = ".section .rodata" if is_static else ".section .data"
            
            # Limpa o conteúdo (remove aspas se já existirem)
            content = content.replace('"', '').replace("'", "")
            if asm_type == ".asciz":
                content = f'"{content}"' # Adiciona aspas apenas para strings
            
            # Cria o label único (Coordenada Z)
            label = f"z_{coords}"
            
            sections[target_section_name].append(f"    {label}: {asm_type} {content}\n")
            print(f"[*] Capturado {line_count}: {label} ({content}) -> {target_section_name}")

    # Montando o arquivo final .s
    output_lines = []
    
    # Adiciona seções de dados se tiverem conteúdo
    for sec_name, sec_content in sections.items():
        if sec_content:
            output_lines.append(f"{sec_name}\n")
            output_lines.extend(sec_content)
            output_lines.append("\n")

    output_lines.extend(asm_text)

    # Escreve o arquivo .s
    output_file = input_file.replace(".z", ".s").replace(".txt", ".s")
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.writelines(output_lines)
        print(f"--- Compilação Geométrica Concluída: {output_file} gerado ---")
    except Exception as e:
        print(f"Erro ao escrever o arquivo de saída: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        # Se o usuário não passar o arquivo, tenta ler o padrão zlang.txt
        # Como no seu terminal você usou zlang.txt, isso ajuda.
        try:
            print("[*] Nenhum arquivo fornecido, tentando zlang.txt...")
            compile_z_to_asm("zlang.txt")
        except:
            print("Uso: python3 z_compiler.py arquivo.z")
    else:
        compile_z_to_asm(sys.argv[1])

