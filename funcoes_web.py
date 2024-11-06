import os
from win32com.client import Dispatch
import zipfile
import requests
import time  
import streamlit as st

# Função para criar estrutura de pastas
def create_folder_structure(version):
    base_directory = f"C:\\TOTVS"
    directories = [
        os.path.join(base_directory, f"{version}", "Apo"),
        os.path.join(base_directory, f"Protheus_{version}", "bin"),
        os.path.join(base_directory, f"Protheus_{version}", "bin", "Appserver"),
        os.path.join(base_directory, f"Protheus_{version}", "bin", "SmartClient"),
        os.path.join(base_directory, f"{version}","Protheus_Data"),
        os.path.join(base_directory, "TotvsDBAccess")
    ]
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        st.write(f"Pasta criada: {directory}")
    st.write("Estrutura de pastas criada com sucesso.")

# Função para obter as URLs de download
def get_download_url(appserver, build):
    base_url_appserver = "https://arte.engpro.totvs.com.br/tec/appserver/"
    base_url_smartclient = "https://arte.engpro.totvs.com.br/tec/smartclient/harpia/"
    base_url_dbaccess = "https://arte.engpro.totvs.com.br/tec/dbaccess/windows/64/latest/dbaccess.zip"
    base_url_dbapi = "https://arte.engpro.totvs.com.br/tec/dbaccess/windows/64/latest/dbapi.zip"
    base_url_smartclientwebapp = "https://arte.engpro.totvs.com.br/tec/smartclientwebapp/"

    appserver_map = {
        "Harpia": "harpia",
        "Panthera Onça": "panthera_onca"
    }

    build_map = {
        "Latest": "latest",
        "Next": "next",
        "Published": "published"
    }

    urls = [
        f"{base_url_appserver}{appserver_map[appserver]}/windows/64/{build_map[build]}/appserver.zip",
        f"{base_url_smartclient}/windows/64/{build_map[build]}/smartclient.zip",
        f"{base_url_dbaccess}",
        f"{base_url_dbapi}",
        f"{base_url_smartclientwebapp}{appserver_map[appserver]}/windows/64/{build_map[build]}/smartclientwebapp.zip"
    ]
    return urls

# Função para download de arquivos com progresso
def download_files(version, urls):
    base_directory = f"C:\\TOTVS\\Download\\{version}"
    os.makedirs(base_directory, exist_ok=True)
    
    for url in urls:
        try:
            file_name = url.split("/")[-1]
            file_path = os.path.join(base_directory, file_name)
            
            st.write(f"Iniciando download de {file_name}...")
            response = requests.get(url, stream=True, timeout=60)
            response.raise_for_status()

            total_size = int(response.headers.get('content-length', 0))
            downloaded_size = 0

            progress_bar = st.progress(0)  # Barra de progresso no Streamlit

            with open(file_path, "wb") as file:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        file.write(chunk)
                        downloaded_size += len(chunk)
                        progress_bar.progress(downloaded_size / total_size)

            st.write(f"Download de {file_name} concluído.")
        except requests.exceptions.RequestException as e:
            st.write(f"Erro ao baixar {file_name}: {str(e)}")
        except Exception as e:
            st.write(f"Ocorreu um erro inesperado ao baixar {file_name}: {str(e)}")

# Função para criar atalhos
def create_shortcut(file_path, shortcut_name, additional_parameters):
    shortcut_path = os.path.join(os.path.dirname(file_path), f"{shortcut_name}.lnk")
    shell = Dispatch('WScript.Shell')
    shortcut = shell.CreateShortCut(shortcut_path)
    shortcut.Targetpath = file_path
    shortcut.Arguments = additional_parameters
    shortcut.WorkingDirectory = os.path.dirname(file_path)
    shortcut.save()

    st.write(f"Atalho criado: {shortcut_path}")

# Função para extrair arquivos
def extract_files(version):
    base_directory = f"C:\\TOTVS\\Download\\{version}"
    extraction_map = {
        "appserver.zip": f"C:\\TOTVS\\Protheus_{version}\\bin\\Appserver",
        "dbaccess.zip": f"C:\\TOTVS\\TotvsDBAccess",
        "dbapi.zip": f"C:\\TOTVS\\Protheus_{version}\\bin\\Appserver",
        "smartclient.zip": f"C:\\TOTVS\\Protheus_{version}\\bin\\SmartClient",
        "smartclientwebapp.zip": f"C:\\TOTVS\\Protheus_{version}\\bin\\SmartClient"
    }

    for file_name, dest_dir in extraction_map.items():
        zip_path = os.path.join(base_directory, file_name)

        if os.path.exists(zip_path):
            st.write(f"Extraindo {file_name} para {dest_dir}...")
            try:
                with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                    zip_ref.extractall(dest_dir)
                st.write(f"Extração de {file_name} concluída.")
            except zipfile.BadZipFile:
                st.error(f"O arquivo {file_name} está corrompido ou não é um arquivo zip válido.")
            except Exception as e:
                st.error(f"Ocorreu um erro ao extrair {file_name}: {str(e)}")
        else:
            st.warning(f"Arquivo {file_name} não encontrado para extração.")

# Função principal de download
def download_protheus(version, appserver, build, update_log_func):
    steps = 8
    current_step = 0
    
    def update_log(message):
        nonlocal current_step
        current_step += 1
        update_log_func(f"[{current_step}/{steps}] {message}")
    
    update_log("Iniciando o processo de download...")
    download_urls = get_download_url(appserver, build)
    
    create_folder_structure(version)
    
    update_log("Baixando AppServer...")
    download_files(version, [download_urls[0]], update_log)  # AppServer 

    update_log("Baixando SmartClient...")
    download_files(version, [download_urls[1]], update_log)  # SmartClient   
    time.sleep(1)  
    
    update_log("Baixando DBAccess...")
    download_files(version, [download_urls[2]], update_log)  # DBAccess   
    time.sleep(1)

    update_log("Baixando DbApi...")
    download_files(version, [download_urls[3]], update_log)  # DBApi  
    time.sleep(1)    

    update_log("Baixando SmartClient WebApp...")
    download_files(version, [download_urls[4]], update_log)  # SmartClient WebApp
    
    update_log("Todos os downloads foram concluídos com sucesso.")
    update_log("Extraindo arquivos...")
    extract_files(version, update_log_func)
    update_log("Extração de arquivos concluída.")

def download_base_congelada(version, update_log_func):
    # Verificação da versão para definir a URL correspondente
    if version == "12.1.2210":
        url = "https://arte.engpro.totvs.com.br/engenharia/base_congelada/protheus/bra/12.1.2210/exp_com_dic/latest/mssql_bak.zip"
    elif version == "12.1.2310":
        url = "https://arte.engpro.totvs.com.br/engenharia/base_congelada/protheus/bra/12.1.2310/exp_com_dic/latest/mssql_bak.zip"
    elif version == "12.1.2410":
        url = "https://arte.engpro.totvs.com.br/engenharia/base_congelada/protheus/bra/12.1.2410/exp_com_dic/latest/mssql_bak.zip"
    else:
        update_log_func("Versão inválida selecionada.")
        return

    try:
        # Notificação de início do download
        update_log_func(f"Baixando base congelada para a versão {version}...")
        
        # Requisição de download
        response = requests.get(url, stream=True, timeout=60)
        response.raise_for_status()

        # Configuração do diretório de download
        base_directory = f"C:\\TOTVS\\Download\\{version}"
        os.makedirs(base_directory, exist_ok=True)
        file_path = os.path.join(base_directory, "mssql_bak.zip")

        # Determina o tamanho total do arquivo para o progresso
        total_size = int(response.headers.get('content-length', 0))
        downloaded_size = 0

        # Processo de download com atualização de log de progresso
        with open(file_path, "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    file.write(chunk)
                    downloaded_size += len(chunk)
                    progress_percent = (downloaded_size / total_size) * 100
                    # Atualiza o log com a porcentagem de download em tempo real
                    update_log_func(
                        f"Progresso: {progress_percent:.2f}% ({downloaded_size}/{total_size} bytes)",
                        is_progress=True
                    )

        # Mensagem de sucesso ao finalizar o download
        update_log_func(f"Base congelada baixada com sucesso em: {file_path}")
        
    except requests.exceptions.RequestException as e:
        update_log_func(f"Erro ao baixar a base congelada: {str(e)}")
    except Exception as e:
        update_log_func(f"Ocorreu um erro inesperado: {str(e)}")