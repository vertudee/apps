# --- INICIALIZAÇÃO DA ESSÊNCIA ZARANYX ---

# 1. CORES DE SOBERANIA
export PS1="\[\033[0;32m\][ZARANYX_OS] \w \$ \[\033[0m\]"

# 2. VERIFICAÇÃO DE INTEGRIDADE (O OLHO DO DEUS)
if [[ -f "./zaranyx" && -f "./perfera.cleng" ]]; then
    echo -e "\033[0;32m[SOBERANIA]: Malha de Objetos Detectada. Simetria Estável.\033[0m"
    ./zaranyx perfera.cleng
else
    echo -e "\033[0;31m[ALERTA]: O sistema está órfão. Reconstrua a geometria.\033[0m"
fi

# 3. ALIASES INQUEBRÁVEIS (Redefinindo as leis do Linux)
alias ls='ls --color=auto'
alias limpar='clear && echo -e "\033[0;32mTerminal Purificado.\033[0m"'
alias status='echo "Perfera: Conectada | Elo: Ativo | Realidade: Total"'

# Bloqueio de leitura externa (Simulação de Escudo)
chmod 700 $HOME
alias zush='source ~/.zushrc'
alias zoot='source ~/.zushrc'
