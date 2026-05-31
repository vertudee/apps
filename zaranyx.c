#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <dirent.h>

// 🧩 Variável auxiliar para montar byte bit a bit
static unsigned char byte_atual = 0;
static int bit_pos = 7; // começa no bit mais significativo

// ✅ Escreve BIT REAL (0 ou 1), não caractere
void escrever_bit(int bit, FILE *out) {
    if (bit) byte_atual |= (1 << bit_pos); // liga bit
    bit_pos--;

    // quando completou 8 bits → grava 1 byte
    if (bit_pos < 0) {
        fputc(byte_atual, out);
        byte_atual = 0;
        bit_pos = 7;
    }
}

// ✅ Finaliza último byte (se incompleto) no fim do arquivo
void finalizar_bits(FILE *out) {
    if (bit_pos != 7) fputc(byte_atual, out);
}

// Extrai bloco de QUALQUER .libin
void extract_block(const char *name, const char *lib_filename, FILE *output) {
    FILE *libin = fopen(lib_filename, "r");
    if (!libin) return;

    char line[1024];
    int recording = 0;

    while (fgets(line, sizeof(line), libin)) {
        char pattern[128];
        sprintf(pattern, "%s();", name);

        // achou o bloco
        if (strstr(line, pattern)) {
            recording = 1;
            continue;
        }

        if (recording) {
            for (int i = 0; line[i] != '\0'; i++) {
                // ignora espaços, chaves, vírgulas
                if (line[i] == '{' || line[i] == '}' || line[i] == ' ' || line[i] == ';')
                    continue;

                // parou no fim do bloco
                if (line[i] == '}') {
                    fclose(libin);
                    return;
                }

                // ✅ AQUI É A MUDANÇA PRINCIPAL: grava BIT, não caractere
                if (line[i] == '0') escrever_bit(0, output);
                if (line[i] == '1') escrever_bit(1, output);
            }
        }
    }

    fclose(libin);
}

// Resolve hierarquia de blocos aninhados
void resolve_hierarchy(char *command, FILE *output) {
    char *open = strchr(command, '(');
    if (!open) return;

    // pega nome do bloco
    char block_name[64];
    strncpy(block_name, command, open - command);
    block_name[open - command] = '\0';

    // tem bloco dentro?
    char *next = strchr(open + 1, '(');
    if (next) {
        resolve_hierarchy(open + 1, output);
    } else {
        // pega conteúdo interno
        char *closed = strchr(open + 1, ')');
        if (closed) {
            char internal_name[64];
            strncpy(internal_name, open + 1, closed - (open + 1));
            internal_name[closed - (open + 1)] = '\0';

            // busca em TODOS os .libin
            struct dirent *entry;
            DIR *dp = opendir(".");
            while ((entry = readdir(dp))) {
                if (strstr(entry->d_name, ".libin"))
                    extract_block(internal_name, entry->d_name, output);
            }
            closedir(dp);
        }
    }

    // busca bloco atual
    struct dirent *entry;
    DIR *dp = opendir(".");
    while ((entry = readdir(dp))) {
        if (strstr(entry->d_name, ".libin"))
            extract_block(block_name, entry->d_name, output);
    }
    closedir(dp);
}

int main(int argc, char *argv[]) {
    if (argc < 4 || strcmp(argv[2], "-o") != 0) {
        printf("Uso: %s arquivo.main -o saida.bin\n", argv[0]);
        return 1;
    }

    FILE *main_file = fopen(argv[1], "r");
    FILE *output = fopen(argv[3], "wb"); // binário puro

    if (!main_file || !output) {
        printf("Erro ao abrir arquivos\n");
        return 1;
    }

    char line[256];
    while (fgets(line, sizeof(line), main_file)) {
        if (line[0] == '\n' || line[0] == ';') continue;

        char *end = strchr(line, ';');
        if (end) *end = '\0';

        resolve_hierarchy(line, output);
    }

    finalizar_bits(output); // garante que todos bits são gravados

    fclose(main_file);
    fclose(output);
    printf("✅ Binário PURO gerado: %s\n", argv[3]);
    return 0;
}

