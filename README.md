<p align="center">
  <img src="./docs/logo.png" alt="Logo PS2" width="200">
</p>

# Análise de arquivos PS2
**Licenciatura em Engenharia de Sistemas Informáticos** (Pós-Laboral) 2025-26 Escola Superior de Tecnologia - IPCA

---
## Descrição do Projeto
PS2 é um formato bancário estruturado usado para débitos diretos, composto por registos padronizados que garantem a validação, integridade e processamento automático das transações financeiras.
O principal objetivo desse projeto é gerarmos esse tipo de arquivo através de dados guardados em ficheiros e depois analisarmos os dados em uma Dashboard.

Para a realização e cumprimento dos objetivos foram utilizadas as seguintes linguagens de programção:
* **C**: Ler ficheiros e gerar o arquivo PS2 estruturado.
* **Python**: Validação e manipulação de dados e visualização de métricas.

## Descrição do Problema
A empresa "IPCA Energy" fornece eletricidade aos seus clientes e pretende automatizar o processo de cobrança mensal.

A empresa dispõe de ficheiros de texto com a informação dos seus clientes, os consumos mensais registados e o preçário
em vigor para cada período.

O sistema a desenvolver deverá ler estes ficheiros, processar a informação, calcular o valor a faturar a cada cliente e, por
fim, gerar um único ficheiro de texto no formato PS2 (simplificado). Este ficheiro será posteriormente enviado ao banco
para efetuar a cobrança automática na conta dos clientes que têm o serviço de débito direto ativo.

Uma etapa crucial do processo é a validação dos dados dos clientes. O sistema deve verificar se o NIF e o NIB de cada
cliente são válidos antes de o incluir no ficheiro de débitos diretos. 

## Documentação
A documentação foi gerada a partir do Doxygen.

## Organização do Repositório
A estrutura do projeto segue as boas práticas de modularização exigidas:

| Diretoria | Descrição |
| :--- | :--- |
| **[`data/`](./data/)** | Contém os ficheiros de entrada para testes e processamento. |
| **[`docs/`](./docs/)** | Documentação académica, incluindo o relatório final em LaTeX. |
| **[`ref/`](./ref/)** | Documentação técnica gerada automaticamente via Doxygen (HTML/PDF). |
| **[`src/`](./src/)** | Código-fonte da aplicação (`app.py`, `cli.py`, `parser.py`, etc.). |

## Como Executar
### **Pré-requisitos**
Antes de executar o programa via CLI ou shiny é necessário a criação de uma venv e a instalação das bibliotecas usada no projeto. 

**ATENÇÃO**: Para instalar e rodar tudo corretamente é PRECISO sempre estar na pasta raiz do projeto.

### Venv e Bibliotecas:
Para instalar a venv e as bibliotecas necessárias para o projeto é funcionar, é preciso executar esse dois comandos:
```
make venv
make install
```

### CLI:
Para rodar o programa via CLI(Command Line Interface) é preciso executar o seguinte comando:
```
make cli
```

### Shiny:
Para rodar o programa via shiny é preciso executar o seguinte comando:
```
make shiny
```
