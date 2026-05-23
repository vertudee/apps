class ZBlockException(Exception):
    """Exceção customizada para erros da Arquitetura Z."""
    pass

class MalhaContexto:
    def __init__(self):
        # Matriz 3x3 de A até I
        self.matriz = [[0.0 for _ in range(3)] for _ in range(3)]
        # Novo: Acumulador de cálculos e resíduos negativos
        self.acumulador_negativo = 0.0
        # Limite crítico que o acumulador suporta antes do colapso
        self.limite_critico_negativo = -50.0
        
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
        
        # Cálculo bruto do balanço (sem aplicar abs() direto, para sabermos se é negativo)
        balanco_linha_1 = (a1 + a2) - a3
        
        # Se o balanço quebrou a tolerância padrão para o lado negativo
        if balanco_linha_1 < -0.01:
            # Somamos o cálculo negativo diretamente no acumulador
            self.acumulador_negativo += balanco_linha_1
            print(f"[Alerta de Desvio] Balanço negativo detectado: {balanco_linha_1:.2f}")
            print(f"-> Acumulador Z-Block atual: {self.acumulador_negativo:.2f}")
            
            # Verifica se a soma dos cálculos negativos quebrou o limite crítico
            if self.acumulador_negativo < self.limite_critico_negativo:
                raise ZBlockException(
                    f"Erro [03FF]: Colapso de Malha por Acumulação. "
                    f"Resíduo crítico atingido: {self.acumulador_negativo:.2f}"
                )
            else:
                print("-> Sistema tolerou o desvio temporariamente por amortecimento geométrico.")
                return True
        
        return True

    def aplicar_inversao_profundidade(self):
        self.matriz = [linha[::-1] for linha in self.matriz[::-1]]
        print("-> Janela de Profundidade Aplicada: Matriz Invertida Geometricamente.")

