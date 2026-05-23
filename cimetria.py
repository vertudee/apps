import random

class MalhaZ3x3:
    def __init__(self):
        # Definição das 9 letras principais divididas nos blocos do seu caderno
        self.letras = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']
        
        # Estado dinâmico dos operadores de peso (valores de 0 a 9)
        # Garantindo a regra: m e n precisam estar alinhados em simetria
        self.m = {"m1": 5, "m2": 3, "m3": 7}
        self.n = {"n1": -self.m["m1"], "n2": -self.m["m2"], "n3": -self.m["m3"]}

    def gerar_malha_probabilistica(self):
        """
        Gera a matriz 3x3 injetando 3 zeros aleatórios (random) 
        que rodam entre as 9 posições principais da operação.
        """
        # Criamos uma cópia das letras para manipular nesta rodada
        posicoes_disponiveis = list(range(9))
        
        # Escolhe de forma probabilística 3 posições únicas para virarem ZERO
        posicoes_zero = random.sample(posicoes_disponiveis, 3)
        
        # Monta a estrutura linear da malha substituindo por 0 onde o random definiu
        estado_linear = []
        for idx, letra in enumerate(self.letras):
            if idx in posicoes_zero:
                estado_linear.append(" 0 ") # O zero quântico/probabilístico rodando
            else:
                estado_linear.append(f" {letra} ")

        # Transforma a estrutura linear em uma matriz geométrica 3x3
        malha_3x3 = [
            estado_linear[0:3],
            estado_linear[3:6],
            estado_linear[6:9]
        ]
        return malha_3x3, posicoes_zero

    def processar_ciclo(self):
        """
        Executa um ciclo da malha aplicando as regras de n e m do caderno
        """
        malha, zeros_atuais = self.gerar_malha_probabilistica()
        
        print("="*45)
        print("🔄 NOVO CICLO DA MALHA ORTOGONAL")
        print("="*45)
        print(f"Alinhamento de Pesos (0 a 9):")
        print(f"  n1 = {self.n['n1']}  <-->  -m1 = {-self.m['m1']}")
        print(f"  n2 = {self.n['n2']}  <-->  -m2 = {-self.m['m2']}")
        print(f"  n3 = {self.n['n3']}  <-->  -m3 = {-self.m['m3']}")
        print(f"Sinal do Ciclo: n_barra_1 -> -m1 = -1")
        print("-"*45)
        print("Geometria do Bloco com 3 Zeros Aleatórios:")
        
        for linha in malha:
            print("  " + "".join(linha))
            
        print("-"*45)
        print(f"Índices das Letras anuladas neste fluxo: {zeros_atuais}")
        print("="*45 + "\n")

# Inicializando o motor geométrico Z-Block
interpretador_z = MalhaZ3x3()

# Simulando 3 ciclos seguidos para ver os zeros rodando aleatoriamente
for ciclo in range(3):
    interpretador_z.processar_ciclo()

