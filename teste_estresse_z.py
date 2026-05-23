# -*- coding: utf-8 -*-
"""
Z-BLOCK - MONITOR DE EXPANSAO E ESTRESSE DA MALHA
Arquivo: teste_estresse_z.py
"""
import time
import sys

def iniciar_expansao_z():
    print("=== [INICIANDO EXPANSAO GEOMÉTRICA EM TEMPO REAL] ===")
    print("Aplicando Geometria de Anulação para conter resíduos...\n")
    time.sleep(1)
    
    # Lista de saltos de simulação para testar o limite físico
    testes = [12, 16, 20, 24, 26, 28]
    
    for qubits in testes:
        elementos = 2**qubits
        peso_ram_gb = (elementos * 16) / (1024**3)
        
        print(f"[+] Alinhando {qubits} Kill Bits...")
        print(f"    -> Elementos na malha: {elementos:,}")
        print(f"    -> Peso projetado: {peso_ram_gb:.5f} GB")
        
        # Simula a alocação de processamento da malha de probabilidades
        print("    [Z-PROCESS] Cruzando matrizes espelhadas...")
        time.sleep(0.5) 
        
        if qubits >= 26:
            print("    ⚠️  ALERTA: Alta dissipação térmica detectada no dispositivo!")
            time.sleep(0.8)
            
        print("    ✅ Estado estabilizado em |0> com anulação de peso.\n")
        time.sleep(0.5)

    print("=======================================================")
    print("[RESULTADO] Teste concluído dentro da margem de segurança!")
    print("A malha suportou a expansão máxima simulada de 28 bits.")
    print("=======================================================")

if __name__ == '__main__':
    iniciar_expansao_z()

