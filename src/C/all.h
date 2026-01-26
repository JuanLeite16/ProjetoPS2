#ifndef ALL_H
#define ALL_H

#define MAX_CLIENTE 100
#define MAX_CONSUMO 500
#define MAX_PERIODO 120
#define MAX_COBRANCA 500

typedef struct {
    int id_cliente;
    char nome[100];
    char nif[10];
    char nib[22];
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
    int valorPagar;
    int tipo_movimento;
    char descricao[28];
} Cobranca;

int carregaClientes(const char *caminho, Cliente arrClientes[]);

int carregaConsumos(const char *caminho, Consumo arrConsumos[]);

int carregaPeriodos(const char *caminho, Periodo arrPeriodos[]);

float precoPeriodo(int mes, int ano, int n_periodos, Periodo arrPeriodos[]);

int processarDados(int mes, int ano, float preco, int n_consumos, int n_clientes,
    Cliente arrClientes[], Consumo arrConsumos[], Cobranca arrCobrancas[]);

int calcularDebito(float preco, int kWh);

int gerarPS2(int mes, int ano, int n_cobrancas, Cobranca Cobrancas[]);

void criar_nif_valido(int n_cobrancas, Cobranca Cobrancas[]);

#endif