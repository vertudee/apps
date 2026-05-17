// Definição da Malha de Anulação Simétrica
[Z-CONTEXT: MALHA_ESTÁVEL]
{
    // Fluxo Direto: Entrada e processamento do motor pulsado
    -> [MOTOR: PULSAÇÃO(1000000)]
    {
        q = 10 * q * i * (2 * i - 1);
        r = 10 * u * (q * (5 * i - 2) + r - y * t);
    }

    // Fluxo Reverso: Contra-força negativa operando na borda do bloco
    <- [ANULAÇÃO: ESPELHO]
    {
        // Operação inversa que colide o peso de 'q' e 'r'
        descomputar(q, r); 
    }
}

