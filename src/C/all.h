#ifndef ALL_H
#define ALL_H

#include <stdbool.h>

#define MAX_CLIENTE 100
#define MAX_CONSUMO 500
#define MAX_PERIODO 120

typedef struct {
    int id_cliente;
    char nome[100];
    char nif[10];
    char nib[22];
    bool nif_valido;
    bool nib_valido;

} Cliente;

typedef struct {
    int id_cliente;
    int ano;
    int mes;
    float consumo;
} Consumo;

typedef struct {
    int ano;
    int mes;
    float preco;
} Periodo;

typedef struct {
    int id_cliente;
    char nif[10];
    char nib[22];
    float valorPagar;
    char descricao[27];
} Cobranca;

#endif