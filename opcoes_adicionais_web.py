import streamlit as st
from bs4 import BeautifulSoup
import requests
import os

# URLs base para download e obtenção de versões
base_urls = {
    "AppServer": "https://arte.engpro.totvs.com.br/tec/appserver/{}/windows/64/builds/",
    "SmartClientWebApp": "https://arte.engpro.totvs.com.br/tec/smartclientwebapp/{}/windows/64/builds/",
}

build_mapping = {
    "Panthera Onça": "panthera_onca",
    "Harpia": "harpia"
}

def get_versions(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        rows = soup.select('tr.file')
        versions = []
        for row in rows:
            version_tag = row.select_one('td:nth-child(2) span.name')
            if version_tag:
                version_name = version_tag.get_text(strip=True)
                versions.append(version_name)
        return versions
    except requests.exceptions.RequestException as e:
        st.error(f"Erro ao obter versões de {url}: {str(e)}")
        return []

def verificar_e_criar_diretorio():
    base_directory = "C:\\TOTVS\\Download\\Download_Protheus"
    if not os.path.exists(base_directory):
        os.makedirs(base_directory)
        return f"Diretório {base_directory} criado com sucesso."
    return f"Diretório {base_directory} já existe."

def realizar_download(url, destino, update_log):
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        total_size = int(response.headers.get('content-length', 0))
        downloaded_size = 0
        with open(destino, "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    file.write(chunk)
                    downloaded_size += len(chunk)
                    progress_message = f"Baixando {os.path.basename(destino)}: {downloaded_size / 1024:.2f} KB de {total_size / 1024:.2f} KB"
                    update_log(progress_message)
        update_log(f"Download de {os.path.basename(destino)} concluído.")
    except Exception as e:
        update_log(f"Erro ao baixar {os.path.basename(destino)}: {str(e)}")

def open_additional_options():
    st.sidebar.title("Opções Adicionais de Download")

    # Seleção da Build
    selected_build = st.sidebar.selectbox("Selecione a Build:", list(build_mapping.keys()))
    build = build_mapping[selected_build]

    # Opções de download com versões dinâmicas
    options = {}
    for label in base_urls.keys():
        if st.sidebar.checkbox(f"Baixar {label}"):
            # Obter versões automaticamente
            url = base_urls[label].format(build)
            versions = get_versions(url)
            if versions:
                options[label] = {
                    "version": st.sidebar.selectbox(f"Escolha a versão para {label}", versions),
                    "url": url
                }
            else:
                st.sidebar.write(f"Não há versões disponíveis para {label}.")

    if st.sidebar.button("Iniciar Download"):
        iniciar_download(options)

def iniciar_download(options):
    update_log = st.empty()
    def log(message):
        update_log.write(message)

    # Verificar e criar diretório
    log(verificar_e_criar_diretorio())

    # Iniciar download para cada opção selecionada
    for label, info in options.items():
        version = info['version']
        url = info['url'] + version  # URL completa para a versão específica
        destino = f"C:\\TOTVS\\Download\\Download_Protheus\\{label}_{version}.zip"
        log(f"Iniciando download de {label} - Versão {version}...")
        realizar_download(url, destino, log)
