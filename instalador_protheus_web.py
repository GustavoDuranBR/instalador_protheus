import streamlit as st
from funcoes_web import download_protheus, download_base_congelada
from arquivos_adicionais_web import copiar_appserver_ini, copiar_atualiar_rpo
from opcoes_adicionais_web import open_additional_options

# Inicializa log_content e progress_content no session_state se não existir
if 'log_content' not in st.session_state:
    st.session_state.log_content = []
if 'progress_content' not in st.session_state:
    st.session_state.progress_content = ""

# Função para atualizar o log
def update_log(message, is_progress=False):
    if is_progress:
        st.session_state.progress_content = message
    else:
        st.session_state.log_content.append(message)
    display_logs()

# Exibe todos os logs no painel de log
def display_logs():
    log_content = '\n'.join(st.session_state.log_content)
    full_log_content = log_content + "\n" + st.session_state.progress_content
    log_box.markdown(
        f"""
        <div style="background-color: black; color: #00FF00; font-family: monospace; padding: 10px; 
                    border-radius: 5px; height: 350px; width: 700px; overflow-y: auto; margin-top: 20px;">
            {full_log_content}
        </div>
        """,
        unsafe_allow_html=True
    )

# Função para validar as seleções
def validate_selections(version=None, appserver=None, build=None):
    if version and (not version or version == "Selecione a versão"):
        update_log("Por favor, selecione a versão do Protheus.")
        return False
    if appserver is not None and (not appserver or appserver == "Selecione o AppServer"):
        update_log("Por favor, selecione o AppServer.")
        return False
    if build is not None and (not build or build == "Selecione a Build"):
        update_log("Por favor, selecione a Build.")
        return False
    return True

# Função para manipular ações dos botões
def on_download_button_click(version, appserver, build):
    if validate_selections(version, appserver, build):
        update_log("Espere enquanto realizo o download...")
        download_protheus(version, appserver, build, update_log)  # Passa a função de log

def on_baixar_appserver_ini_button_click(version):
    if validate_selections(version=version):
        update_log("Copiando o arquivo appserver.ini...")
        copiar_appserver_ini(version)
        update_log(f"Arquivo appserver.ini copiado para C:\\TOTVS\\Protheus_{version}\\bin\\AppServer\\appserver.ini.")

def on_baixar_atualizador_rpo_click(version):
    if validate_selections(version=version):
        update_log(f"Copiando Atualizar_RPO_{version}.bat...")
        copiar_atualiar_rpo(version)
        update_log(f"Arquivo Atualizar_RPO copiado com sucesso para a versão {version}.")

def on_base_congelada_button_click(version):
    if validate_selections(version=version):
        update_log("Iniciando o download da base congelada...")
        download_base_congelada(version, update_log)

# Layout da interface
st.title("Instalador Protheus")

# Seletor de versão
version = st.selectbox("Selecione a versão do Protheus:", ["Selecione a versão", "12.1.2210", "12.1.2310", "12.1.2410"], key="version_selectbox")

# Seletor de AppServer
appserver = st.selectbox("Selecione o AppServer:", ["Selecione o AppServer", "Harpia", "Panthera Onça"], key="appserver_selectbox")

# Seletor de Build
build = st.selectbox("Selecione a Build:", ["Selecione a Build", "Latest", "Next", "Published"], key="build_selectbox")

# Colunas para os botões
col3, col4, col5, col6, col7 = st.columns(5)

# Placeholder para o painel de log
log_box = st.empty()

# Botões
with col3:
    if st.button("Realizar Download"):
        on_download_button_click(version, appserver, build)

with col4:
    if st.button("Baixar AppServer.ini"):
        on_baixar_appserver_ini_button_click(version)

with col5:
    if st.button("Atualizador RPO"):
        on_baixar_atualizador_rpo_click(version)

with col6:
    if st.button("Base Congelada"):
        on_base_congelada_button_click(version)

with col7:
    if st.button("Opções Adicionais"):
        open_additional_options()

# Exibe os logs após os botões
display_logs()

# Informações do desenvolvedor
st.sidebar.markdown(f"**Dev**: Gustavo Duran  \n**Versão**: 1.0")
