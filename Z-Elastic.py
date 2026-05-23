import random
import time

class MotorZElastic:
    def __init__(self):
        self.cadeia_base = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']
        # Polaridades estritas da raiz
        self.n = 99  # Elevando a intensidade da carga útil para aguentar a expansão
        self.m = -99 # Jamais positivo

    def pulsar_malha(self, clock):
        # 1. Rotatividade probabilística dos 3 zeros na cadeia
        posicoes_zero = random.sample(range(9), 3)
        cadeia_instante = [0 if i in posicoes_zero else self.cadeia_base[i] for i in range(9)]
        
        # 2. O SISTEMA SE MEXE SOZINHO: Escolha aleatória do tamanho do bloco (5 a 8)
        # E definição dinâmica de onde o bloco começa e termina na cadeia
        tamanho_bloco = random.randint(5, 8)
        ponto_inicio = random.randint(0, 9 - tamanho_bloco)
        ponto_fim = ponto_inicio + tamanho_bloco
        
        # Extração do bloco elétrico atual
        elementos_bloco = cadeia_instante[ponto_inicio:ponto_fim]
        qtd_zeros = elementos_bloco.count(0)
        
        # 3. Diagnóstico de Condutividade Ortogonal da Janela Dinâmica
        if qtd_zeros == 0:
            status = "🔥 FLUXO CRÍTICO ABSOLUTO (Hiper-Condutor)"
            eficiencia = "100% - Carga máxima trafegando."
        elif qtd_zeros == 1:
            status = "⚡ PONTE DE SALTO DINÂMICA"
            eficiencia = "75% - Dados tunelando pelo ponto zero."
        elif qtd_zeros == 2:
            status = "❄️ COMPRESSÃO GEOMÉTRICA (Fluxo Lento)"
            eficiencia = "40% - Malha estreitando e recalibrando pesos."
        else:
            status = "🕳️ ISOLAMENTO POR VÁCUO (Auto-Proteção)"
            eficiencia = "10% - Rota blindada contra estouro de memória."

        # Impressão do pulso no Terminal
        print("="*75)
        print(f"🌀 PULSO DE CLOCK Z-BLOCK: #{clock}")
        print("="*75)
        print(f" Cadeia Linear Atual : {['0' if x == 0 else x for x in cadeia_instante]}")
        print(f" Raiz de Polaridade   : n(+{self.n}) <---> m({self.m})")
        print("-"*75)
        print(f" 📐 GEOMETRIA ELÁSTICA DO BLOCO ATUAL:")
        print(f" -> Escala da Janela : {tamanho_bloco} em {tamanho_bloco} letras")
        print(f" -> Escopo Ativo     : Posição [{ponto_inicio} até {ponto_fim-1}]")
        print(f" -> Elementos Físicos: {[0 if x == 0 else x for x in elementos_bloco]}")
        print("-"*75)
        print(f" 📊 DIAGNÓSTICO EM TEMPO REAL:")
        print(f" -> Status de Rota   : {status}")
        print(f" -> Eficiência Útil  : {eficiencia}")
        print("="*75 + "\n")

# Inicializa o motor flutuante
motor_fluido = MotorZElastic()

print("🚀 Ativando Motor Z-Elastic... Pressione CTRL+C no Termux para pausar.")
time.sleep(1.5)

# Loop contínuo fazendo a malha se mexer sozinha em tempo real
clock = 1
try:
    while True:
        motor_fluido.pulsar_malha(clock)
        clock += 1
        time.sleep(0.8) # Ritmo de pulso do clock (quase 1 segundo por mudança)
except KeyboardInterrupt:
    print("\n[Aviso] Fluxo pausado pelo operador. Geometria congelada com sucesso.")
