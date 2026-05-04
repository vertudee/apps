#!/bin/bash
# ZASM 777 - O COMPILADOR DE SOBERANIA

ARQUIVO_Z=$1
NOME_SAIDA="${ARQUIVO_Z%.*}"

if [ -z "$1" ]; then
    echo "ERRO: Forneça um arquivo .z ou .s para o Z-777 processar."
    exit 1
fi

echo "--- APLICANDO REGRAS Z-777 NO HARDWARE ---"

# 1. Montagem (AS)
as $ARQUIVO_Z -o temp_z.o

# 2. Linkagem (LD) - Flag -s e --nmagic para anular peso
ld temp_z.o -o $NOME_SAIDA -s --nmagic

# 3. Limpeza de Entropia (Strip brutal)
strip -R .comment -R .note -R .note.ABI-tag $NOME_SAIDA

rm temp_z.o

echo "=== SISTEMA 777 CONCLUÍDO ==="
printf "STATUS: Binário Soberano [%s] gerado com %s bytes.\n" "$NOME_SAIDA" "$(stat -c%s $NOME_SAIDA)"

