/**
 * @file all.h
 * @author Juan Lucas Souza Leite
 * @brief Declarações de estruturas, constantes e protótipos de funções do projeto.
 * @date 2026-01-27
 * 
 * @copyright Copyright (c) 2026
 */

#ifndef ALL_H
#define ALL_H

// DImensões definidas nos requesitos técnicos
#define MAX_CLIENTE 100
#define MAX_CONSUMO 500
#define MAX_PERIODO 120
#define MAX_COBRANCA 500

/**
 * @struct Cliente
 * @brief Estrutura que representa um cliente.
 */
typedef struct {
    int id_cliente;   /**< Identificador do cliente */
    char nome[100];   /**< Nome do cliente */
    char nif[10];     /**< NIF do cliente */
    char nib[22];     /**< NIB do cliente */
} Cliente;

/**
 * @struct Consumo
 * @brief Estrutura que representa um registo de consumo de energia.
 */
typedef struct {
    int id_cliente;   /**< Identificador do cliente */
    int ano;          /**< Ano do consumo */
    int mes;          /**< Mês do consumo */
    float consumo;    /**< Consumo de energia (kWh) */
} Consumo;

/**
 * @struct Periodo
 * @brief Estrutura que representa um período com o respetivo preço.
 */
typedef struct {
    int ano;        /**< Ano do período */
    int mes;        /**< Mês do período */
    float preco;    /**< Preço associado ao período */
} Periodo;

/**
 * @struct Cobranca
 * @brief Estrutura que representa uma cobrança de um cliente.
 */
typedef struct {
    int id_cliente;      /**< Identificador do cliente */
    char nif[10];        /**< NIF do cliente */
    char nib[22];        /**< NIB do cliente */
    int valorPagar;      /**< Valor a pagar em cêntimos */
    int tipo_movimento;  /**< Tipo de movimento */
    char descricao[28];  /**< Descrição da cobrança */
} Cobranca;

/**
 * @brief Carrega os dados dos clientes a partir de um ficheiro de texto.
 * @details Lê um ficheiro CSV separado por ';', ignora a primeira linha
 * (cabeçalho) e armazena os dados de cada cliente no array fornecido.
 * 
 * @param caminho Caminho para o ficheiro de clientes.
 * @param arrClientes Array onde os clientes serão armazenados.
 * @return int Número de clientes carregados ou 0 em caso de erro.
 */
int carregaClientes(const char *caminho, Cliente arrClientes[]);

/**
 * @brief Carrega os registos de consumo a partir de um ficheiro de texto.
 * @details Lê um ficheiro CSV separado por ';', ignora o cabeçalho e armazena
 * os consumos no array fornecido, até ao limite definido por MAX_CONSUMO.
 * 
 * @param caminho Caminho para o ficheiro de consumos.
 * @param arrConsumos Array onde os consumos serão armazenados.
 * @return int Número de registos carregados ou 0 em caso de erro.
 */
int carregaConsumos(const char *caminho, Consumo arrConsumos[]);

/**
 * @brief Carrega os períodos tarifários a partir de um ficheiro de texto.
 * @details Lê um ficheiro CSV separado por ';', ignora o cabeçalho e armazena
 * os períodos no array fornecido, até ao limite definido por MAX_PERIODO.
 * 
 * @param caminho Caminho para o ficheiro de períodos.
 * @param arrPeriodos Array onde os períodos serão armazenados.
 * @return int Número de períodos carregados ou 0 em caso de erro.
 */
int carregaPeriodos(const char *caminho, Periodo arrPeriodos[]);

/**
 * @brief Obtém o preço de um período específico.
 * @details Procura no array de períodos o registo correspondente ao mês e ano
 * indicados e devolve o respetivo preço.
 * 
 * @param mes Mês do período.
 * @param ano Ano do período.
 * @param n_periodos Número de períodos disponíveis.
 * @param arrPeriodos Array de períodos.
 * @return float Preço do período ou 0 se não existir.
 */
float precoPeriodo(int mes, int ano, int n_periodos, Periodo arrPeriodos[]);

/**
 * @brief Processa os consumos e gera as cobranças dos clientes.
 * @details Filtra os consumos pelo mês e ano indicados, calcula o valor a pagar
 * e cria os registos de cobrança correspondentes.
 * 
 * @param mes Mês de referência.
 * @param ano Ano de referência.
 * @param preco Preço por kWh.
 * @param n_consumos Número de consumos disponíveis.
 * @param n_clientes Número de clientes disponíveis.
 * @param arrClientes Array de clientes.
 * @param arrConsumos Array de consumos.
 * @param arrCobrancas Array onde as cobranças serão armazenadas.
 * @return int Número de cobranças geradas.
 */
int processarDados(int mes, int ano, float preco, int n_consumos, int n_clientes,
    Cliente arrClientes[], Consumo arrConsumos[], Cobranca arrCobrancas[]);

/**
 * @brief Calcula o valor do débito a pagar.
 * @details Calcula o valor em cêntimos com base no preço por kWh e no consumo.
 * 
 * @param preco Preço por kWh.
 * @param kWh Consumo de energia em kWh.
 * @return int Valor a pagar em cêntimos.
 */
int calcularDebito(float preco, int kWh);    

/**
 * @brief Gera um ficheiro PS2 para um mês/ano com base nas cobranças.
 * @details Cria o ficheiro em "data/DD_AAAA_MM.ps2", escreve cabeçalho, registos
 * e rodapé, e atualiza o cabeçalho com os totais calculados.
 * 
 * @param mes Mês de referência.
 * @param ano Ano de referência.
 * @param n_cobrancas Número de cobranças a escrever.
 * @param Cobrancas Array de cobranças.
 * @return int 1 se o ficheiro foi gerado com sucesso, 0 em caso de erro.
 */
int gerarPS2(int mes, int ano, int n_cobrancas, Cobranca Cobrancas[]);

/**
 * @brief Gera e corrige NIFs válidos para as cobranças.
 * @details Ajusta o NIF de cada cobrança para garantir 9 dígitos válidos,
 * recalculando o dígito de controlo segundo o módulo 11.
 * 
 * @param n_cobrancas Número de cobranças a processar.
 * @param Cobrancas Array de cobranças a atualizar.
 */
void criar_nif_valido(int n_cobrancas, Cobranca Cobrancas[]);

/**
 * @brief Gera e corrige NIBs válidos para as cobranças.
 * @details Ajusta o NIB de cada cobrança para garantir 21 dígitos válidos,
 * recalculando os dígitos de controlo segundo o módulo 97.
 * 
 * @param n_cobrancas Número de cobranças a processar.
 * @param Cobrancas Array de cobranças a atualizar.
 */
void criar_nib_valido(int n_cobrancas, Cobranca Cobrancas[]);

#endif