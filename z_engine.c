#include <stdio.h>
#include <string.h>
#include <stdbool.h>

// Definição da estrutura do Z-Block
typedef struct {
    char identity[32];
    bool is_open;
} ZBlock;

void handle_logic(ZBlock *block, char *content) {
    // Se o bloco for 'print', ele joga pra saída
    if (strcmp(block->identity, "print") == 0) {
        printf("[Saída Z]: %s\n", content);
    }
    // Se for '##', o sistema de 0-bytes apenas ignora (comentário)
    else if (strcmp(block->identity, "##") == 0) {
        // Silêncio absoluto
    }
}

int main() {
    printf("=== Z-SYSTEM CORE : INDEPENDÊNCIA UNIVERSAL ===\n");

    // Simulando o fluxo de dados que entra no bloco
    // Na sua lógica: IDENTIDADE -> CONTEÚDO -> IDENTIDADE
    char *stream[] = {"print", "Calculando sequências infinitas...", "print", 
                      "##", "Isso é um comentário e será ignorado", "##",
                      "print", "22 333 4444", "print"};

    ZBlock current_block;
    current_block.is_open = false;

    for (int i = 0; i < 9; i++) {
        if (!current_block.is_open) {
            // Abre o bloco com a primeira identidade que encontrar
            strcpy(current_block.identity, stream[i]);
            current_block.is_open = true;
            printf("\n[SISTEMA] Abrindo bloco: %s\n", current_block.identity);
        } else {
            // Se já está aberto, verifica se o próximo é o fechamento (espelho)
            if (strcmp(current_block.identity, stream[i]) == 0) {
                printf("[SISTEMA] Fechando bloco: %s (Simetria confirmada)\n", current_block.identity);
                current_block.is_open = false;
            } else {
                // Se não é o fechamento, é o código/conteúdo lá dentro
                handle_logic(&current_block, stream[i]);
            }
        }
    }

    printf("\n=== PROCESSO CONCLUÍDO EM ESTADO Z ===\n");
    return 0;
}

