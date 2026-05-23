import os

# Criar a pasta de testes visuais
os.makedirs("z_visual_tests", exist_ok=True)

# 1. Matriz de TV Antiga Pura (Passa no teste de brilho)
pure_matrix = b"\\\\\x00\\\\\x00" + b"\x00\x01" * 32
with open("z_visual_tests/Tv_Estatica_Pura.z", "wb") as f:
    f.write(pure_matrix)

# 2. Matriz Hackeada (Força o brilho artificial com bits 1 - Bloqueada pela Zero Security)
hacked_matrix = b"\\\\\x00\\\\\x01" + b"\x01\x01" * 32
with open("z_visual_tests/Tv_Estatica_Hacked.z", "wb") as f:
    f.write(hacked_matrix)

print("[Z-SYSTEM]: Simulacros de TV binária gerados com sucesso!")

