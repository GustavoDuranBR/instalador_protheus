# Documentação: Instalador Protheus e Inicializador Protheus

## Índice

1. [Introdução](#introdução)
2. [Instalador Protheus](#instalador-protheus)
    - [Criação da Estrutura de Pastas](#criação-da-estrutura-de-pastas)
    - [Download de Arquivos](#download-de-arquivos)
    - [Extração de Arquivos](#extração-de-arquivos)
    - [Criação de Atalhos](#criação-de-atalhos)
    - [Instalação do Web Agent](#instalação-do-web-agent)
3. [Inicializador Protheus](#inicializador-protheus)
    - [Inicialização do DbAccess](#inicialização-do-dbaccess)
    - [Inicialização do AppServer](#inicialização-do-appserver)
    - [Logs de Execução](#logs-de-execução)
    - [Controle de Terminais](#controle-de-terminais)
    - [Finalização e Fechamento](#finalização-e-fechamento)
4. [Fluxo de Funcionamento](#fluxo-de-funcionamento)
5. [Conclusão](#conclusão)
6. [Configuração de Diretórios](#configuração-de-diretórios)
7. [Instruções de Uso](#instruções-de-uso)
    - [Executando o Instalador Protheus](#executando-o-instalador-protheus)
    - [Executando o Inicializador Protheus](#executando-o-inicializador-protheus)
8. [Contribuições](#contribuições)

---

## Introdução

Os programas **Instalador Protheus** e **Inicializador Protheus** são fundamentais para o processo de instalação e inicialização do ambiente Protheus da TOTVS. O **Instalador Protheus** é responsável pela criação de toda a estrutura de pastas e pela obtenção dos arquivos necessários, enquanto o **Inicializador Protheus** facilita o lançamento dos componentes necessários (como DbAccess e AppServer) de forma automatizada.

## Instalador Protheus

### Criação da Estrutura de Pastas
O instalador cria a estrutura de diretórios necessária para a instalação do Protheus, incluindo pastas como:
- `C:\TOTVS\<versao>\Apo`
- `C:\TOTVS\Protheus_<versao>\bin`
- `C:\TOTVS\TotvsDBAccess`

### Download de Arquivos
O instalador baixa os arquivos necessários para o Protheus, como:
- Appserver
- SmartClient
- DBAccess
- Base Congelada (dependendo da versão)
   
Estes arquivos são obtidos a partir de URLs pré-definidas.

### Extração de Arquivos
Após o download, os arquivos ZIP são extraídos para os diretórios correspondentes.

### Criação de Atalhos
O instalador cria atalhos para os executáveis essenciais, como:
- AppServer
- SmartClient
- DBAccess

### Instalação do Web Agent
O programa também instala o Web Agent, necessário para o funcionamento do Protheus em ambientes web.

## Inicializador Protheus

### Inicialização do DbAccess
Inicia o DbAccess, que é essencial para o funcionamento do banco de dados no Protheus.

### Inicialização do AppServer
Lança o AppServer, que é responsável por realizar o processamento do Protheus no servidor.

### Logs de Execução
O Inicializador mantém logs detalhados de cada etapa do processo, como a execução do DbAccess e AppServer, incluindo informações de sucesso ou falha.

### Controle de Terminais
A interface do Inicializador pode ser configurada para abrir terminais externos para o DbAccess e o AppServer, proporcionando uma visualização separada dos logs.

### Finalização e Fechamento
Após a execução bem-sucedida do processo, o Inicializador Protheus exibe uma mensagem de sucesso. Os terminais podem ser fechados automaticamente ao final.

## Fluxo de Funcionamento

O funcionamento conjunto dos dois programas ocorre da seguinte forma:

1. O **Instalador Protheus** é executado primeiro para garantir que todas as pastas e arquivos necessários estão corretamente configurados no sistema.
2. Após a instalação, o **Inicializador Protheus** pode ser executado para iniciar os processos do DbAccess e AppServer, garantindo que o ambiente Protheus esteja pronto para uso.

## Conclusão

Esses programas são essenciais para a automatização e simplificação do processo de instalação e inicialização do ambiente Protheus, garantindo que todas as etapas sejam realizadas corretamente.

---

## Configuração de Diretórios

- **Diretórios de Instalação:**
  - `C:\TOTVS\`: Pasta base para a instalação.
  - `C:\TOTVS\Protheus_<versao>\`: Contém os arquivos binários do Protheus.
  - `C:\TOTVS\TotvsDBAccess\`: Contém o banco de dados e o DbAccess.

- **Diretórios de Download:**
  - `C:\TOTVS\Download\<versao>\`: Pasta onde os arquivos serão baixados temporariamente.

---

## Instruções de Uso

### Executando o Instalador Protheus

1. Inicie o **Instalador Protheus**.
2. Insira a versão do Protheus desejada.
3. Clique em "Iniciar Instalação". O programa irá automaticamente criar a estrutura de pastas e baixar os arquivos necessários.

### Executando o Inicializador Protheus

1. Após a instalação do Protheus, inicie o **Inicializador Protheus**.
2. O programa iniciará automaticamente o DbAccess e o AppServer.
3. Os logs da execução serão exibidos na interface, e você será notificado quando a inicialização for concluída com sucesso.

---

## Contribuições

Se você deseja contribuir com o projeto ou fazer melhorias, siga as instruções abaixo:

1. Faça um fork deste repositório.
2. Crie uma branch para sua contribuição.
3. Faça as alterações e envie um pull request.
