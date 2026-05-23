class ZBlockException(Exception):
    """Exceção customizada para erros da Arquitetura Z."""
    pass

class MalhaContexto:
    def __init__(self):
        self.matriz = [[0.0 for _ in range(3)] for _ in range(3)]
        # Acumulador para guardar a soma dos cálculos negativos
        self.acumulador_negativo = 0.0
        # Limite crítico que o Z-Block suporta antes do erro 03FF
        self.limite_critico = -50.0
        
    def carregar_matriz(self, dados_9_elementos):
        if len(dados_9_elementos) != 9:
            raise ZBlockException("Erro: Entrada precisa de 9 elementos.")
        k = 0
        for i in range(3):
            for j in range(3):
                self.matriz[i][j] = dados_9_elementos[k]
                k += 1
                
    def verificar_balanco(self):
        a1 = self.matriz[0][0]
        a2 = self.matriz[0][1]
        a3 = self.matriz[0][2]
        
        # Cálculo do balanço bruto da linha
        balanco_linha_1 = (a1 + a2) - a3
        
        # Se quebrar a tolerância gerando um cálculo negativo
        if balanco_linha_1 < -0.01:
            self.acumulador_negativo += balanco_linha_1
            print(f"[Desvio] Adicionado: {balanco_linha_1:.2f} | Acumulador Atual: {self.acumulador_negativo:.2f}")
            
            # Se a soma quebrar o limite crítico determinado
            if self.acumulador_negativo < self.limite_critico:
                raise ZBlockException(
                    f"Erro [03FF]: Estouro de Malha por Acumulação Crítica ({self.acumulador_negativo:.2f})"
                )
            else:
                print("-> Estado: Amortecido pela geometria do bloco.")
                return True
        return True

# ====================================================
# BLOCO DE EXECUÇÃO FORÇADA (Para garantir o print na tela)
# ====================================================
if __name__ == "__main__":
    print("--- INICIANDO SIMULAÇÃO DE ACUMULAÇÃO NEGATIVA (Z-BLOCK 3) ---")
    malha = MalhaContexto()
    
    # Criamos uma entrada que gera um cálculo negativo de -15.0 por rodada
    # (1.0 + 2.0) - 18.0 = -15.0
    dados_teste = [1.0, 2.0, 18.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    
    malha.carregar_matriz(dados_teste)
    
    # Simulando loops de processamento jogando o cálculo negativo consecutivamente
    for rodada in range(1, 6):
        print(f"\n--- Processamento {rodada} ---")
        try:
            malha.verificar_balanco()
        except ZBlockException as e:
            print(f"\n[BLOQUEIO DE SEGURANÇA]: {e}")
            print("Ação: Dump evitado com sucesso pelo isolor do contexto.")
            break

