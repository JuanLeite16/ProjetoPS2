/**
 * @file validacoes.c
 * @brief Implementação das funções de validação e criação de NIF e NIB do projeto.
 * @date 2026-01-27
 *
 * @copyright Copyright (c) 2026
 */

#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <stdlib.h>
#include <math.h>
#include "all.h"

// Gera e corrige NIFs válidos para as cobranças.
void criar_nif_valido(int n_cobrancas, Cobranca Cobrancas[]){
    int soma, tamanho;
    char nif[10];
    for(int j = 0; j < n_cobrancas; j++){
        strcpy(nif, Cobrancas[j].nif);
        soma = 0;
        tamanho = abs((int)strlen(nif) - 9);
        if(tamanho != 0) strncat(nif, "123456789", tamanho);
        for(int i = 0; i < (int)strlen(nif); i++){
            if(!isdigit((unsigned char)nif[i])){
                nif[i] = '1';
            }
        }
        for(int i = 0; i < (int)strlen(nif)-1; i++){
            soma += (nif[i] - '0')*(9-i);
        }
        int resto = soma % 11;
        if(resto == 0 || resto == 1){
            nif[((int)strlen(nif))-1] = '0';
        } else {
            nif[((int)strlen(nif))-1] = (11 - resto) + '0';
        }
        strncpy(Cobrancas[j].nif, nif, 9);
        Cobrancas[j].nif[9] = '\0';
    }
}

// Gera e corrige NIBs válidos para as cobranças.
void criar_nib_valido(int n_cobrancas, Cobranca Cobrancas[]){
    char nib[22];
    int tamanho, resto, dc = 0;
    for(int j = 0;j < n_cobrancas;j++){
        strncpy(nib, Cobrancas[j].nib, 21);
        nib[21] = '\0';
        tamanho = ((int)strlen(nib)) - 21;
        if(tamanho < 0) strncat(nib, "123456789012345678901", abs(tamanho));
        nib[21] = '\0';
        for(int i = 0;i < 21;i++) if(!isdigit((unsigned char)nib[i])) nib[i] = '1';
        nib[20] = '0';
        nib[19] = '0';
        resto = 0;
        for (int i = 0; i < 21; i++) {
            resto = (resto * 10 + (nib[i] - '0')) % 97;
        }
        dc = 98 - resto;
        if (dc == 98) dc = 0;
        nib[19] = '0' + (dc / 10);
        nib[20] = '0' + (dc % 10);
        nib[21] = '\0';
        strncpy(Cobrancas[j].nib, nib, 21);
        Cobrancas[j].nib[21] = '\0';
    }
}
