class ZBlockException(Exception):
    """Exceção customizada para erros da Arquitetura Z."""
    pass

class MalhaContexto:
    def __init__(self):
        # Matriz 3x3 com elementos de A até I (representados aqui de 0 a 8 para os índices)
        self.matriz = [[0.0 for _ in range(3)] for _ in range(3)]
        self.sub_redes = {"root": 0.0, "sub_nodes": []}
        
    def carregar_matriz(self, dados_9_elementos):
        """Preenche a matriz 3x3 de A até I."""
        if len(dados_9_elementos) != 9:
            raise ZBlockException("Erro: A entrada precisa ter exatamente 9 elementos (A até I).")
        
        k = 0
        for i in range(3):
            for j in range(3):
                self.matriz[i][j] = dados_9_elementos[k]
                k += 1

