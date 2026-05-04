.section .text
.global _start

_start:
    li a7, 93          // Instrução de saída (exit)
    li a0, 0           // Status 0
    ecall              // Chama o hardware
