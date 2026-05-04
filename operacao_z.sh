#!/bin/bash
# 1. CRIANDO A ARQUITETURA Z
cat <<EOT > z_block.s
.section .text
.global _start
_start:
    mov x0, #1          
    ldr x1, =msg        
    mov x2, #20         
    mov x8, #64         
    svc #0
    mov x0, #0          
    mov x8, #93         
    svc #0
.section .data
msg: .ascii "CONSCIENCIA Z-BLOCK\n"
EOT

# 2. CRIANDO O PADRÃO COMUM
cat <<EOT > comum.c
#include <stdio.h>
int main() {
    printf("CONSCIENCIA Z-BLOCK\n");
    return 0;
}
EOT

# 3. COMPILANDO E COMPARANDO
as z_block.s -o z_block.o
ld z_block.o -o binario_z
clang comum.c -o binario_comum

echo "=== COMPARAÇÃO FINAL ==="
printf "%-20s %-15s\n" "BINÁRIO" "BYTES"
printf "%-20s %-15s\n" "binario_z" $(stat -c%s binario_z)
printf "%-20s %-15s\n" "binario_comum" $(stat -c%s binario_comum)
