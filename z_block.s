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
