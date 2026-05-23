import random

class MotorOrtogonalZ2:
    def __init__(self):
        self.letras = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']
        # Polaridades estritas definidas na raiz
        self.n = 7   # Sempre Positivo
        self.m = -7  # Jamais Positivo

    def simular_instante_real(self, numero_instante):
        posicoes_zero = random.sample(range(9), 3)
        estado = [0 if i in posicoes_zero else self.letras[i] for i in range(9)]
        matriz = [estado[0:3], estado[3:6], estado[6:9]]
        
        rotas = {
            "Linha 1 [A-B-C]": [0, 1, 2],
            "Linha 2 [D-E-F]": [3, 4, 5],
            "Linha 3 [G-H-I]": [6, 7, 8],
            "Coluna 1 [A-D-G]": [0, 3, 6],
            "Coluna 2 [B-E-H]": [1, 4, 7],
            "Coluna 3 [C-F-I]": [2, 5, 8],
            "Diagonal 1 [A-E-I]": [0, 4, 8],
            "Diagonal 2 [C-E-G]": [2, 4, 6]
        }
        
        print("="*65)
        print(f"⚡ INSTANTE REAL DE MATRIZ #{numero_instante} ⚡")
        print("="*65)
        for linha in matriz:
            print("  " + "".join(f" [{x}] " for x in linha))
        print("-"*65)
        print("📊 DECISÃO DO ROTEADOR QUÂNTICO (POLARIDADE):")
        print("-"*65)
        
        for nome_rota, indices in rotas.items():
            elementos = [estado[i] for i in indices]
            qtd_zeros = elementos.count(0)
            
            # Decisão de transferência de peso baseado na geometria
            if qtd_zeros == 0:
                # Fluxo máximo: n e m operam em equivalência direta
                calculo_canal = f"Carga Ativa: n({self.n}) + m({self.m}) = 0 (Estabilidade Perfeita)"
                status_visual = "🔥 FLUXO TOTAL"
            elif qtd_zeros == 1:
                # Ponto de salto: o zero serve de ponte reflexiva
                calculo_canal = f"Salto Quântico: n({self.n}) -> [0] -> m({self.m})"
                status_visual = "⚡ PONTE ATIVA"
            elif qtd_zeros == 2:
                # Bloqueio: desvia o sinal para poupar processamento
                calculo_canal = "Fluxo Suspenso -> Roteando para Eixo Secundário"
                status_visual = "❄️ DESVIADO"
            else:
                # Vácuo: canal desligado da malha
                calculo_canal = "Consumo Zero -> Canal em Repouso Dimensional"
                status_visual = "🕳️ ISOLADO"
                
            print(f" -> {nome_rota.ljust(18)}: {status_visual} | {calculo_canal}")
        print("="*65 + "\n")

# Rodando o novo motor de teste
motor = MotorOrtogonalZ2()
motor.simular_instante_real(1)

