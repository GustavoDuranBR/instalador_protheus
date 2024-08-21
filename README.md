# Instalador Protheus
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)

Este é um programa desenvolvido para facilitar o processo de instalação e configuração do Protheus, permitindo o download de arquivos essenciais, configuração do `appserver.ini`, e a criação de uma estrutura de diretórios de maneira automatizada.

## Funcionalidades

- **Realizar Download**: Baixa os arquivos necessários para a instalação do Protheus (AppServer, SmartClient, DBAccess, e SmartClientWebApp) de acordo com a versão, AppServer e Build selecionados.
- **Baixar AppServer.ini**: Copia o arquivo `appserver.ini` correspondente à versão do Protheus selecionada, salvando-o no diretório apropriado.
- **Base Congelada**: Baixa a base congelada correspondente à versão do Protheus escolhida.
- **Criação Automática de Diretórios**: Cria automaticamente a estrutura de diretórios necessária para a instalação do Protheus.

## Requisitos

- **Python 3.11 ou superior**
- **Bibliotecas Python**:
  - `tkinter`: Interface gráfica
  - `requests`: Para realizar os downloads dos arquivos

## Estrutura do Projeto

O projeto possui a seguinte estrutura de diretórios:

```
Instalador_Protheus/
│
├── funcoes.py                # Funções principais do programa
├── gerar_appserver_ini.py    # Função para copiar o arquivo appserver.ini
├── instalador_protheus.py    # Arquivo principal que inicia a interface gráfica
├── icon.ico                  # Ícone do aplicativo
├── README.md                 # Documentação do projeto
└── venv/                     # Ambiente virtual com dependências do projeto
```

## Instruções de Instalação

1. Clone este repositório:

   ```bash
   git clone https://github.com/seuusuario/Instalador_Protheus.git
   cd Instalador_Protheus
   ```

2. Crie e ative um ambiente virtual:

   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/MacOS
   venv\Scripts\activate     # Windows
   ```

3. Instale as dependências:

   ```bash
   pip install -r requirements.txt
   ```

4. Execute o programa:

   ```bash
   python instalador_protheus.py
   ```

## Uso

- **Selecione a Versão**: Escolha a versão do Protheus que deseja instalar.
- **Selecione o AppServer**: Escolha o tipo de AppServer que deseja instalar (Harpia, Lobo Guara, ou Panthera Onça).
- **Selecione a Build**: Escolha a build que deseja instalar (Latest, Next, ou Published).
- **Clique em 'Realizar Download'**: Inicia o processo de download e criação de diretórios.
- **Clique em 'Baixar AppServer.ini'**: Copia o arquivo `appserver.ini` para o diretório correto.
- **Clique em 'Base Congelada'**: Baixa a base congelada para a versão selecionada.
- **Clique em 'Sair'**: Fecha o programa.

## Autor

Desenvolvido por Gustavo Duran.

## Licença

Este projeto está licenciado sob a Licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## Contato

Se tiver dúvidas ou precisar de ajuda, entre em contato através do email gustavoduran22@gmail.com
