import os
import subprocess
from datetime import datetime

# Garante que estamos na pasta correta dos scripts quânticos
diretorio_quantum = os.path.expanduser("~/apps/Quantum-Z")
os.chdir(diretorio_quantum)

# Lista todos os arquivos de teste em Python
arquivos_py = [f for f in os.listdir('.') if f.endswith('.py') and f.startswith('teste_quantum_')]

print(f"🤖 [Engine Z] Encontrados {len(arquivos_py)} arquivos de teste para validação quântica.\n")

for arquivo in arquivos_py:
    nome_base = arquivo.replace('.py', '')
    nome_relatorio = f"relatorio_{nome_base}.txt"
    
    print(f"⏳ Executando e analisando a malha de: {arquivo}...")
    
    # Executa o script quântico e captura a saída do terminal
    try:
        resultado = subprocess.run(
            ['python', arquivo], 
            capture_output=True, 
            text=True, 
            timeout=30
        )
        saida_terminal = resultado.stdout if resultado.returncode == 0 else resultado.stderr
    except subprocess.TimeoutExpired:
        saida_terminal = "ERRO: O teste excedeu o tempo limite de execução (Timeout de 30s)."
    except Exception as e:
        saida_terminal = f"ERRO NA EXECUÇÃO: {str(e)}"

    # Estrutura o relatório automatizado
    conteúdo_relatorio = f"""==================================================
📊 RELATÓRIO DE VALIDAÇÃO GEOMÉTRICA - QUANTUM-Z
==================================================
Data da Execução: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Módulo Analisado: {arquivo}
Status da Malha: Sincronizado via Termux
--------------------------------------------------

📝 DESCRIÇÃO TEÓRICA DO PROJETO:
Este relatório documenta o comportamento estatístico do algoritmo '{arquivo}' 
sob condições de ruído quântico simulado. O objetivo do teste é demonstrar 
a eficiência da arquitetura Z na mitigação e anulação aleatória de erros 
de superposição e decoerência de fase.

--------------------------------------------------
🔬 RESULTADOS DOS TESTES DE RUÍDO (SAÍDA DA ENGINE):
--------------------------------------------------
{saida_terminal if saida_terminal.strip() else "O arquivo executou com sucesso, mas não retornou saídas de texto no terminal."}

--------------------------------------------------
Fim do Relatório - Propriedade Intelectual da Conta 'vertudee'
=================================================="""

    # Escreve o relatório no arquivo txt correspondente
    with open(nome_relatorio, "w", encoding="utf-8") as f:
        f.write(conteúdo_relatorio)
        
    print(f"✅ Relatório gerado com sucesso: {nome_relatorio}\n")

print("🌌 Todos os relatórios foram gerados na malha estrutural!")

