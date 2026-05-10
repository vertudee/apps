.section .data
    z_price_: .asciz "p 500 p"
    z_counter_: .long 1
    z_limit_: .long 777

.section .text
.global _start
_start:
    mov $60, %rax
    xor %rdi, %rdi
    syscall
