#include "all.h"
#include <stdlib.h>
#include <stdio.h>
#include <string.h>

int carregaClientes(const char *caminho, Cliente arrClientes[]){
    FILE *ficheiro = fopen(caminho, "r");
    if(ficheiro == NULL){
        printf("Erro ao abrir ficheiro clientes.\n");
        return 0;
    }

    char linha_atual[60];
    int n_clientes = 0;
    if(fgets(linha_atual, sizeof(linha_atual), ficheiro) == NULL){
        printf("Erro ao ler primeia linha do ficheiro.\n");
    }
    while(fgets(linha_atual, sizeof(linha_atual), ficheiro) != NULL){

        char *token = strtok(linha_atual, ";");
        if(!token) continue;
        arrClientes[n_clientes].id_cliente = atoi(token);

        token = strtok(NULL, ";");
        if(!token) continue;
        strcpy(arrClientes[n_clientes].nome, token);
        size_t tam = strlen(token);
        arrClientes[n_clientes].nome[tam] = '\0';

        token = strtok(NULL, ";");
        if(!token) continue;
        strncpy(arrClientes[n_clientes].nif, token, 9);
        arrClientes[n_clientes].nif[9] = '\0';

        token = strtok(NULL, ";");
        if(!token) continue;
        strncpy(arrClientes[n_clientes].nib, token, 21);
        arrClientes[n_clientes].nib[21] = '\0';

        n_clientes++;
    }
    return n_clientes;
}

int carregaConsumos(const char *caminho, Consumo arrConsumos[]){
    FILE * ficheiro = fopen(caminho, "r");
    if(ficheiro == NULL){
        printf("Erro ao abrir ficheiro consumos.\n");
        return 0;
    }
    char linha_atual[60];
    int n_consumos = 0;
    if(fgets(linha_atual, sizeof(linha_atual), ficheiro) == NULL){
        printf("Erro ao ler primeira linha do ficheiro.\n");
    }
    for(int i = 0; i < MAX_CONSUMO; i++){
        if(fgets(linha_atual, sizeof(linha_atual), ficheiro) == NULL) break;

        char * token = strtok(linha_atual, ";");
        if(!token) continue;
        arrConsumos[i].id_cliente = atoi(token);

        token = strtok(NULL, ";");
        if(!token) continue;
        arrConsumos[i].ano = atoi(token);

        token = strtok(NULL, ";");
        if(!token) continue;
        arrConsumos[i].mes = atoi(token);

        token = strtok(NULL, ";");
        if(!token) continue;
        arrConsumos[i].consumo = atof(token);

        n_consumos++;
    }

    return n_consumos;
}

int carregaPeriodos(const char *caminho, Periodo arrPeriodos[]){
    FILE * ficheiro = fopen(caminho, "r");
    if(ficheiro == NULL){
        printf("Erro ao abrir ficheiro periodos.\n");
        return 0;
    }
    char linha_atual[60];
    int n_periodos = 0;
    if(fgets(linha_atual, sizeof(linha_atual), ficheiro) == NULL){
        printf("Erro ao ler primeira linha do ficheiro.\n");
    }
    for(int i = 0; i < MAX_PERIODO; i++){
        if(fgets(linha_atual, sizeof(linha_atual), ficheiro) == NULL) break;

        char * token = strtok(linha_atual, ";");
        if(!token) continue;
        arrPeriodos[i].ano = atoi(token);

        token = strtok(NULL, ";");
        if(!token) continue;
        arrPeriodos[i].mes = atoi(token);

        token = strtok(NULL, ";");
        if(!token) continue;
        arrPeriodos[i].preco = atof(token);

        n_periodos++;
    }

    return n_periodos;
}

int processarDados(int mes, int ano, float preco, int n_consumos, Cliente arrClientes[], Consumo arrConsumos[]){
    for(int i = 0;i < n_consumos; i++){
        if(arrConsumos[i].mes == mes && arrConsumos[i].ano == ano){
            int kWh = arrConsumos[i].consumo;
        }
    }
}

float precoPeriodo(int mes, int ano, int n_periodos, Periodo arrPeriodos[]){
    for(int i = 0;i < n_periodos; i++){
        if(arrPeriodos[i].ano == ano && arrPeriodos[i].mes == mes){
            float preco = arrPeriodos[i].preco;
            return preco;
        }
    }
    return 0;
}
