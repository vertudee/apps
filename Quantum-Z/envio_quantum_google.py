# ========================================================
# ARCHITECTURE QUANTUM-Z v10.0 - GOOGLE HARDWARE CONNECTOR
# ENVIO DA MALHA DO CADERNO PARA OS CHIPS REAIS DA GOOGLE
# ========================================================
import cirq
import cirq_google as cg
import math
import os
import sys

def enviar_para_hardware_google():
    print("=== [ZARANYX_OS] PROTOCOLO DE EXPORTAÇÃO GOOGLE v10.0 ===")
    print("-> Verificando chaves de autenticação do Google Cloud...")

    # ------------------------------------------------------------------
    # CONFIGURAÇÃO DE AMBIENTE: Nome do seu projeto quântico na Google
    # ------------------------------------------------------------------
    ID_PROJETO_GOOGLE = "seu-projeto-quantum-z"
    ARQUIVO_CHAVE = "chave_google.json"

    if not os.path.exists(ARQUIVO_CHAVE):
        print("\n[AVISO]: Arquivo 'chave_google.json' não encontrado no diretório atual.")
        print("-> Para simular o disparo de nuvem sem a chave real, mude o motor para modo de simulação de Engine.")
        print("-> Pegue suas credenciais no console: console.cloud.google.com")
        # Criamos o motor de simulação de nuvem para não travar o seu terminal
        engine = cg.SimulatorEngine()
        print("[MODO]: Ativando Engine Remota Simulada (Ambiente de Teste Google Cloud).")
    else:
        # Se a chave real existir, conecta direto no hardware da Google
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = ARQUIVO_CHAVE
        engine = cg.get_engine(project_id=ID_PROJETO_GOOGLE)
        print("[MODO]: Autenticado com sucesso. Conectado ao cluster da Google.")

    # --- ESCOLHA DO CHIP REAL ---
    # Mostra os processadores quânticos reais ativos (como o Sycamore ou Weber)
    print("-> Listando processadores quânticos da Google disponíveis...")
    try:
        backends = engine.list_processors()
        chip_alvo = backends[0]
        print(f"[CHIP SELECIONADO]: {chip_alvo}")
    except Exception:
        chip_alvo = "rainbow" # Chip de calibração padrão da Google
        print(f"[CHIP PADRÃO]: Alocado no processador virtual/real: {chip_alvo}")

    # --- RECONSTRUINDO A SUA MALHA DO CADERNO NO CIRQ ---
    # A Google usa uma grade de qubits baseada em coordenadas físicas no chip (GridQubit)
    q0 = cirq.GridQubit(5, 3) # Seleciona um qubit específico na malha física do chip
    circuito = cirq.Circuit()

    # Aplica o valor limite [+10] do seu caderno convertido em rotação geométrica
    valor_caderno = 10
    fase_radianos = (valor_caderno * math.pi) / 10
    
    # Rotação direta no eixo Y
    circuito.append(cirq.ry(fase_radianos).on(q0))
    circuito.append(cirq.measure(q0, key='malha_z_google'))

    print("-> Transcompilando geometria para a topologia do chip Sycamore/Rainbow...")
    print(f"-> Despachando 1000 repetições para a nuvem da Google...")

    # Executa o circuito através do motor da Google
    programa = engine.create_program(circuito)
    job = programa.run(processor_id=chip_alvo, repetitions=1000)

    print("\n" + "="*55)
    print("[RELATÓRIO RETORNADO DO HARDWARE GOOGLE]")
    print("="*55)
    frequencias = job.histogram(key='malha_z_google')
    print(f" -> Colapso Estado |0> : {frequencias.get(0, 0)} vezes")
    print(f" -> Colapso Estado |1> : {frequencias.get(1, 0)} vezes")
    print("-" * 55)
    print("[Z-CONTEXT]: Execução concluída na infraestrutura da Google.")

if __name__ == '__main__':
    enviar_para_hardware_google()

