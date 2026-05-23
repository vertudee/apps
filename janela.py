class ZBlockException(Exception):
    """Exceção customizada para erros da Arquitetura Z."""
    pass

class MalhaContexto:
    def __init__(self):
        # Matriz 3x3 de A até I
        self.matriz = [[0.0 for _ in range(3)] for _ in range(3)]
        
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
        tolerancia = 0.01
        balanco_linha_1 = abs((a1 + a2) - a3)
        
        if balanco_linha_1 > tolerancia:
            raise ZBlockException(f"Erro [03FF]: Estouro de Malha. Balanço violado na linha 1 ({balanco_linha_1}).")
        return True

    def aplicar_inversao_profundidade(self):
        self.matriz = [linha[::-1] for linha in self.matriz[::-1]]
        print("-> Janela de Profundidade Aplicada: Matriz Invertida Geometricamente.")

# ==========================================
# IMPORTANTE: Bloco de Execução (O que faz aparecer no terminal)
# ==========================================
if __name__ == "__main__":
    print("--- Teste 1: Fluxo Perfeito ---")
    malha1 = MalhaContexto()
    dados_validos = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0]
    
    try:
        malha1.carregar_matriz(dados_validos)
        if malha1.verificar_balanco():
            print("Sucesso: Dados alinhados com a geometria do Z-Block.")
            malha1.aplicar_inversao_profundidade()
    except ZBlockException as e:
        print(f"Janela bloqueada: {e}")

    print("\n" + "-"*40 + "\n")

    print("--- Teste 2: Disparando Erro 03FF ---")
    malha2 = MalhaContexto()
    dados_invalidos = [5.0, 10.0, 3.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    
    try:
        malha2.carregar_matriz(dados_invalidos)
        malha2.verificar_balanco()
    except ZBlockException as e:
        print(f"Aviso do Sistema: {e}")
        print("Ação: Dump de memória evitado. O contexto isolou o z-block defeituoso.")

