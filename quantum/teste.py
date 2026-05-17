import cirq

# 1. INICIALIZAÇÃO (Fronteira A)
# Definimos o nosso qubit no ponto zero da malha de probabilidades
qubit = cirq.GridQubit(0, 0)

# 2. CONSTRUÇÃO DO CIRCUITO (Abertura dos Eixos)
# Criamos a malha (circuit) onde as dimensões vão interagir
script_quantico = cirq.Circuit()

# Aplicamos a Porta Hadamard (H). 
# Ela joga o qubit no seu Bloco de Probabilidades: ele deixa de ser 0 ou 1
# e passa a existir nos três eixos simétricos de probabilidade ao mesmo tempo.
script_quantico.append(cirq.H(qubit))

# 3. MEDIÇÃO (Fronteira Z - O Colapso)
# Forçamos o sistema a sair da infinitude quântica e retornar ao mundo macroscópico
script_quantico.append(cirq.measure(qubit, key='resultado_z'))

# --- EXECUÇÃO NA MÁQUINA QUÂNTICA ---
# Simulamos a execução em um processador quântico real da Google
simulador = cirq.Simulator()
print("--- Estrutura do Script Quântico Gerado ---")
print(script_quantico)

# Executamos o script 1000 vezes (1000 amostragens da malha de probabilidades)
teste_execucao = simulador.run(script_quantico, repetitions=1000)

# Coletamos os resultados do colapso
frequencias = teste_execucao.histogram(key='resultado_z')
print("\n--- Resultado do Colapso Dimensional ---")
print(f"Estado |0⟩ (Eixo Positivo): {frequencias[0]} vezes")
print(f"Estado |1⟩ (Eixo Negativo): {frequencias[1]} vezes")

