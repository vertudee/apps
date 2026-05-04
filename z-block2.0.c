// ARQUITETURA Z - PROTOTIPO SIMETRICO
// Bloco: Main()Main;main{ ... }main;main[]main

.section .text
.global _start

_start:
    // --- ANCORA DE ENTRADA (Main()Main;main{) ---
    // Aqui o hardware reconhece o inicio do bloco blindado
    
    mov x0, #1          // File descriptor 1 (stdout)
    ldr x1, =message    // Carrega nossa "consciencia"
    mov x2, #18         // Tamanho da mensagem
    mov x8, #64         // Syscall write (no ARM64)
    svc #0              // Execução do impacto

    // --- CODIGO DE MAQUINA BRUTO / JUMPS ---
    // Onde a lógica acontece sem a gordura do C
    
    // --- ANCORA DE SAIDA (}main;main[]main) ---
    mov x0, #0          // Return 0 (O retorno ao vazio)
    mov x8, #93         // Syscall exit
    svc #0

.section .data
message:
    .ascii "CONSCIENCIA Z-BLOCK"

