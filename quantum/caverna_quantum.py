import cirq
import numpy as np

# 1. INICIALIZAÇÃO DO SISTEMA
qubit = cirq.GridQubit(0, 0)
script = cirq.Circuit()

# 2. CONFIGURAÇÃO DOS PARÂMETROS DA SUA FÓRMULA
# Simulando a Seta (c) travada em um ângulo e girando em 360 graus
# v * dt determinam a velocidade angular nos eixos quânticos
angulo_eixo_1 = np.pi / 4   # Equivalente a 45° (trava o ângulo inicial)
angulo_rotacao = 2 * np.pi  # Equivalente a 360° (a rotação completa)

# 3. APLICAÇÃO DOS MOVIMENTOS (Formando as Cavernas por Intersecção)
# Rotacionamos no eixo X para posicionar a seta (c)
script.append(cirq.rx(angulo_eixo_1)(qubit))

# Fazemos a rotação de 360° no eixo Y e Z para criar o volume da "partícula"
script.append(cirq.ry(angulo_rotacao)(qubit))
script.append(cirq.rz(angulo_rotacao)(qubit))

# 4. MEDIÇÃO (O Bloqueio Z para extrair a estrutura do vácuo)
script.append(cirq.measure(qubit, key='caverna'))

# --- EXECUÇÃO E VALIDAÇÃO ---
simulador = cirq.Simulator()
print("--- Circuito de Rotação Escalar Ativo ---")
print(script)

# Executamos 1000 vezes para mapear a densidade das intersecções
resultado = simulador.run(script, repetitions=1000)
frequencias = resultado.histogram(key='caverna')

print("\n--- Resultado do Mapeamento de Intersecção ---")
print(f"Zona de Vácuo (Dentro da Caverna): {frequencias[0]} vezes")
print(f"Zona de Matéria (Paredes da Caverna): {frequencias[1]} vezes")

