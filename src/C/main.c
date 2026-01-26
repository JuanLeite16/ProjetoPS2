#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include "all.h"

int main(){
    Cliente Clientes[MAX_CLIENTE];
    Consumo Consumos[MAX_CONSUMO];
    Periodo Periodos[MAX_PERIODO];
    Cobranca Cobrancas[MAX_COBRANCA];
    int n_clientes = carregaClientes("../../../data/clientes.txt", Clientes);
    int n_consumos = carregaConsumos("../../../data/consumos.txt", Consumos);
    int n_periodos = carregaPeriodos("../../../data/periodos.txt", Periodos);

    if (n_clientes == 0 || n_consumos == 0 || n_periodos == 0) {
        printf("Erro crítico: Falha ao carregar ficheiros de dados.\n");
        return 0;
    }

    int ano, mes, ok = 0;
    do {
        printf("Introduza o ANO (ex: 2025): ");
        scanf("%d", &ano);
        if (ano < 1 || ano > 2026) {
            printf("Mês inválido!\n"); 
            ok = 0;
        } else ok = 1;
    } while(!ok);
    do {
        printf("Introduza o MES (1-12): ");
        scanf("%d", &mes);
        if (mes < 1 || mes > 12) {
            printf("Mês inválido!\n"); 
            ok = 0;
        } else ok = 1;
    } while(!ok);

    float preco = precoPeriodo(mes, ano, n_periodos, Periodos);
    int n_cobranca = processarDados(mes, ano, preco, n_consumos, n_clientes,
        Clientes, Consumos, Cobrancas);

    return 0;
}
