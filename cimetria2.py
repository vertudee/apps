import random

class MotorOrtogonalZ:
    def __init__(self):
        # As 9 coordenadas geométricas do seu caderno
        self.letras = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']
        
        # Polaridades estritas da raiz
        self.n = 7  # Sempre Positivo
        self.m = -7 # Jamais Positivo

    def gerar_e_verificar_malha(self):
        # 1. Injeção probabilística dos 3 zeros
        posicoes_zero = random.sample(range(9), 3)
        
        # Construção do estado linear da malha
        estado = [0 if i in posicoes_zero else self.letras[i] for i in range(9)]
        
        # Matriz 3x3 para visualização espacial
        matriz = [estado[0:3], estado[3:6], estado[6:9]]
        
        # 2. Mapeamento de todas as 8 ortogonalidades possíveis
        rotas_ortogonais = {
            "Linha 1 [A-B-C]": [0, 1, 2],
            "Linha 2 [D-E-F]": [3, 4, 5],
            "Linha 3 [G-H-I]": [6, 7, 8],
            "Coluna 1 [A-D-G]": [0, 3, 6],
            "Coluna 2 [B-E-H]": [1, 4, 7],
            "Coluna 3 [C-F-I]": [2, 5, 8],
            "Diagonal 1 [A-E-I]": [0, 4, 8],
            "Diagonal 2 [C-E-G]": [2, 4, 6]
        }
        
        # Exibição da Malha Atual
        print("="*60)
        print("🌌 MATRIZ ESPACIAL ATUAL")
        print("="*60)
        for linha in matriz:
            print("  " + "".join(f" [{x}] " for x in linha))
        print("-"*60)
        print("🔎 VERIFICAÇÃO DE ORTOGONALIDADE EM TEMPO REAL:")
        print("-"*60)
        
        # 3. Varredura (Scan) em tempo real de cada rota
        for nome_rota, indices in rotas_ortogonais.items():
            elementos_rota = [estado[i] for i in indices]
            qtd_zeros = elementos_rota.count(0)
            
            # Análise do comportamento do fluxo na rota
            if qtd_zeros == 0:
                status = "🔥 Fluxo Contínuo Total (Sem vácuo)"
            elif qtd_zeros == 1:
                status = "⚡ Transição Estável (1 Ponto de Anulação)"
            elif qtd_zeros == 2:
                status = "❄️ Bloqueio Temporário (Instabilidade de Peso)"
            else:
                status = "🕳️ Vácuo Absoluto (Eixo totalmente zerado)"
                
            # Exibe os elementos reais da rota substituindo os 0 por '0' visualmente
            rota_visual = [x if x != 0 else 0 for x in elementos_rota]
            print(f" -> {nome_rota}: {rota_visual} | Status: {status}")
            
        print("="*60 + "\n")

# Executando o motor de varredura instantânea
motor = MotorOrtogonalZ()

# Simula 2 estados rápidos de tempo real no terminal
for instante in range(2):
    print(f"INSTANTE DE TEMPO REAL #{instante + 1}")
    motor.gerar_e_verificar_malha()

