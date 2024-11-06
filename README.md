# Instalador Protheus
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)

Este programa facilita a instalação e configuração do Protheus, automatizando o download de arquivos essenciais, configuração do `appserver.ini`, e a criação de diretórios necessários.

## Funcionalidades

- **Realizar Download**: 
  - O programa baixa os arquivos necessários para a instalação do Protheus, como AppServer, SmartClient, DBAccess, e SmartClientWebApp, conforme a versão, AppServer e Build selecionados.
  - **Código Relevante**: `get_download_url` para construir URLs de download, `download_files` para realizar o download dos arquivos.

- **Baixar AppServer.ini**: 
  - Copia o arquivo `appserver.ini` correspondente à versão selecionada para o diretório apropriado.
  - **Código Relevante**: `copiar_appserver_ini` realiza a cópia do arquivo `appserver.ini`.

- **Base Congelada**:
  - Baixa a base congelada específica para a versão do Protheus escolhida.
  - **Código Relevante**: `download_base_congelada` cuida do download da base congelada.

- **Criação Automática de Diretórios**:
  - Cria a estrutura de diretórios necessária para a instalação do Protheus.
  - **Código Relevante**: `create_folder_structure` para criar a estrutura de diretórios.

- **Atualização do RPO**:
  - Copia o script para atualizar o RPO para o diretório de destino.
  - **Código Relevante**: `copiar_atualiar_rpo` realiza a cópia do script de atualização do RPO.

---
### Documentação de Configurações

Para mais informações sobre as configurações de diretórios e como configurar corretamente o sistema, consulte a [documentação de configurações](docs/CONFIGURACOES_DIRETORIOS.md).

---

## Estrutura do Projeto

O projeto está organizado da seguinte forma:

```
Instalador_Protheus/
│
├── funcoes.py                # Funções principais do programa, como download e criação de diretórios
├── gerar_appserver_ini.py    # Função para copiar o arquivo appserver.ini
├── instalador_protheus.py    # Arquivo principal com a interface gráfica e a lógica do programa
├── icon.ico                  # Ícone do aplicativo
├── README.md                 # Documentação do projeto
└── venv/                     # Ambiente virtual com dependências do projeto
```

## Instruções de Instalação

1. **Clone este repositório**:
   ```bash
   git clone https://github.com/seuusuario/Instalador_Protheus.git
   cd Instalador_Protheus
   ```

2. **Crie e ative um ambiente virtual**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/MacOS
   venv\Scripts\activate     # Windows
   ```

3. **Instale as dependências**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Execute o programa**:
   ```bash
   python instalador_protheus.py
   ```

## Uso

- **Selecione a Versão**: Escolha a versão do Protheus desejada.
- **Selecione o AppServer**: Escolha o tipo de AppServer (Harpia, Lobo Guara, Panthera Onça).
- **Selecione a Build**: Escolha a build (Latest, Next, Published).
- **Clique em 'Realizar Download'**: Inicia o processo de download e criação de diretórios.
- **Clique em 'Baixar AppServer.ini'**: Copia o arquivo `appserver.ini` para o diretório correto.
- **Clique em 'Baixar Atualizador RPO'**: Copia o script de atualização do RPO específico para a versão selecionada.
- **Clique em 'Base Congelada'**: Baixa a base congelada para a versão selecionada.
- **Clique em 'Opções Adicionais'**: Acessa uma janela com opções de download adicionais e configurações extras.
- **Clique em 'Sair'**: Fecha o programa.

## Configuração do `appserver.ini`

Após a instalação, edite o arquivo `appserver.ini` conforme as suas necessidades:

```
DBServer=localhost
```

### Como Encontrar o Host Name da Sua Máquina

- **Windows**:
  1. Abra o Prompt de Comando (cmd).
  2. Digite `hostname` e pressione Enter.

- **Linux/MacOS**:
  1. Abra o Terminal.
  2. Digite `hostname` e pressione Enter.

## Autor

Desenvolvido por Gustavo Duran.

## Licença

Este projeto está licenciado sob a Licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## Contato

Para dúvidas ou ajuda, entre em contato por email: gustavoduran22@gmail.com
