#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <stdlib.h>
#include "all.h"

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
