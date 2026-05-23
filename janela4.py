# janela4.py - Experimento de Estouro de Malha e Propriedades Ocultas
# Arquitetura: Z-Block (Foco em Amortecimento de Fluxo de Dados)

class ZBlockContext:
    def __init__(self, limite_buffer):
        self.limite = limite_buffer
        self.acumulador_pressao = 0.0
        self.malha_ativa = True
        
    def injetar_sequencia(self, string_dados):
        if not self.malha_ativa:
            print("[Isolador Ativo] Fluxo bloqueado preventivamente.")
            return

        # Medindo a magnitude dos dados injetados
        tamanho_dados = len(string_dados)
        print(f"\n-> Injetando: '{string_dados}' (Tamanho: {tamanho_dados})")

        # Se ultrapassar o limite físico do buffer, calculamos o desvio geométrico
        if tamanho_dados > self.limite:
            excedente = tamanho_dados - self.limite
            
            # Amortecimento: O desvio gera uma pressão negativa acumulada
            # Simula a dissipação da energia do estouro na malha
            self.acumulador_pressao -= (excedente * 15.0) 
            print(f"[Aviso de Malha] Pressão Acumulada: {self.acumulador_pressao}")

            # Condição de Disparo do Isolador de Contexto (ex: bateu -60.0)
            if self.acumulador_pressao <= -60.0:
                print(f"[BLOQUEIO] Limite crítico atingido ({self.acumulador_pressao}). Desarmando malha antes do crash!")
                self.malha_ativa = False
        else:
            # Estabilização se os dados estiverem na tolerância
            if self.acumulador_pressao < 0:
                self.acumulador_pressao += 5.0 # Recuperação gradual da malha
            print(f"[Estável] Buffer operando com folga. Pressão: {self.acumulador_pressao}")

# --- Execução do Fluxo de Teste ---
if __name__ == "__main__":
    # Inicializa o bloco de contexto com um limite de buffer arbitrário (ex: 8 caracteres)
    contexto_z = ZBlockContext(limite_buffer=8)

    # Sequência de testes injetando strings progressivamente maiores (simulando o "shar")
    testes_sequencia = [
        "AAAA",          # Dentro do limite
        "AAAABBBBCCCC",  # Estouro leve -> Gera desvio de -15.0 ou -30.0
        "AAAABBBBCCCCDDDD", # Estouro médio
        "SUPER_ESTOURO_DE_BUFFER_STRING_MÁXIMO" # Estouro crítico -> Dispara o isolador (-60.0)
    ]

    for dado in testes_sequencia:
        contexto_z.injetar_sequencia(dado)
        if not contexto_z.malha_ativa:
            print("\n[Resultado] Propriedade desconhecida mapeada com sucesso. Sistema salvo.")
            break

