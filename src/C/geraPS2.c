#include "all.h"
#include <stdlib.h>
#include <stdio.h>

#define ENTIDADE_NOME "IPCA Energy"
#define ENTIDADE_NIF "503494933"

int gerarPS2(int mes, int ano, int n_cobrancas, Cobranca Cobrancas[]){
    char nome_ficheiro[30];
    int total_cent = 0, total_registros = 0;
    sprintf(nome_ficheiro, "data/DD_%4d_%02d.ps2", ano, mes);
    FILE *ficheiro = fopen(nome_ficheiro, "w+");
    if(!ficheiro){
        printf("Erro ao tentar criar ficheiro.\n");
        return 0;
    }
    long pos_cabecalho = ftell(ficheiro);
    fprintf(ficheiro, "1%04d%02d26%-26s%9s%014d%06d\n",
    ano, mes, ENTIDADE_NOME, ENTIDADE_NIF, 0, 0);
    for(int i = 0; i < n_cobrancas; i++){
        fprintf(ficheiro, "2%07d%03d%21s%9s%014d%-27s\n",
        Cobrancas[i].tipo_movimento, i+1, Cobrancas[i].nib, Cobrancas[i].nif,
        Cobrancas[i].valorPagar, Cobrancas[i].descricao);
        total_cent += Cobrancas[i].valorPagar;
        total_registros++;
    }
    fprintf(ficheiro, "9%014d%06d\n", total_cent, total_registros);
    fseek(ficheiro, pos_cabecalho, SEEK_SET);
    fprintf(ficheiro, "1%04d%02d26%-26s%9s%014d%06d\n",
    ano, mes, ENTIDADE_NOME, ENTIDADE_NIF, total_cent, total_registros);

    return 1;
}