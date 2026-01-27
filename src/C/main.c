/**
 * @file main.c
 * @author Juan Lucas Souza Leite
 * @brief Ponto de entrada do programa (leitura de inputs e execução do fluxo principal).
 * @date 2026-01-27
 *
 * @copyright Copyright (c) 2026
 */

#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include "all.h"

int main(){
    // Passo 1: Carregamento dos dados dos ficheiros para os arrays
    Cliente Clientes[MAX_CLIENTE];
    Consumo Consumos[MAX_CONSUMO];
    Periodo Periodos[MAX_PERIODO];
    Cobranca Cobrancas[MAX_COBRANCA];
    int n_clientes = carregaClientes("data/clientes.txt", Clientes);
    int n_consumos = carregaConsumos("data/consumos.txt", Consumos);
    int n_periodos = carregaPeriodos("data/periodos.txt", Periodos);

    if (n_clientes == 0 || n_consumos == 0 || n_periodos == 0) {
        printf("Erro crítico: Falha ao carregar ficheiros de dados.\n");
        return 0;
    }

    // Passo 2: Input do usuário com mês e ano desejados para cobrança
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

    // Passo 3: Ver o preço do kWh na data desejada e carregar os clientes para cobrança
    float preco = precoPeriodo(mes, ano, n_periodos, Periodos);
    int n_cobrancas = processarDados(mes, ano, preco, n_consumos, n_clientes,
        Clientes, Consumos, Cobrancas);
    
    // Passo 4: Validar e manipular dados
    criar_nif_valido(n_cobrancas, Cobrancas);
    criar_nib_valido(n_cobrancas, Cobrancas);

    // Passo 5: Estruturar e gerar arquivo PS2
    int valido = gerarPS2(mes, ano, n_cobrancas, Cobrancas);
    if(valido) printf("Ficheiro criado com sucesso!\n");
    else printf("Ficheiro não foi criado.\n");
    return 0;
}
