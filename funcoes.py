import os
from win32com.client import Dispatch
import zipfile
import requests
import tkinter as tk
import subprocess
import py7zr

def create_folder_structure(version, log_box):
    base_directory = f"C:\\TOTVS"
    directories = [
        os.path.join(base_directory, f"{version}", "Apo"),
        os.path.join(base_directory, f"Protheus_{version}", "bin"),
        os.path.join(base_directory, f"Protheus_{version}", "bin", "Appserver"),
        os.path.join(base_directory, f"Protheus_{version}", "bin", "SmartClient"),
        #os.path.join(base_directory, f"{version}", "Protheus_Data"),
        os.path.join(base_directory, "TotvsDBAccess")
    ]
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        log_box.insert(tk.END, f"Pasta criada: {directory}\n")
        log_box.see(tk.END)
    log_box.insert(tk.END, "Estrutura de pastas criada com sucesso.\n")
    log_box.see(tk.END)

def get_download_url(appserver, build, version):
    base_url_appserver = "https://arte.engpro.totvs.com.br/tec/appserver/"
    base_url_smartclient = "https://arte.engpro.totvs.com.br/tec/smartclient/harpia/"
    base_url_dbaccess = "https://arte.engpro.totvs.com.br/tec/dbaccess/windows/64/latest/dbaccess.zip"
    base_url_dbapi = "https://arte.engpro.totvs.com.br/tec/dbaccess/windows/64/latest/dbapi.zip"
    base_url_smartclientwebapp = "https://arte.engpro.totvs.com.br/tec/smartclientwebapp/"
    base_url_protheus_data = "https://arte.engpro.totvs.com.br/engenharia/base_congelada/protheus/bra/"
    base_url_web_agent = "https://arte.engpro.totvs.com.br/tec/web-agent/windows/64/latest/"

    appserver_map = {
        "Harpia": "harpia",
        "Panthera Onça": "panthera_onca"
    }

    build_map = {
        "Latest": "latest",
        "Next": "next",
        "Published": "published"
    }

    smartclientwebapp_file = "smartclientwebapp.zip"  # Nome padrão
    if appserver == "Panthera Onça":
        smartclientwebapp_file = "webapp-10.0.2-windows-x64-release.zip"  # Nome específico para Panthera Onça

    urls = [
        f"{base_url_appserver}{appserver_map[appserver]}/windows/64/{build_map[build]}/appserver.zip",
        f"{base_url_smartclient}/windows/64/{build_map[build]}/smartclient.zip",
        f"{base_url_dbaccess}",
        f"{base_url_dbapi}",
        f"{base_url_smartclientwebapp}{appserver_map[appserver]}/windows/64/{build_map[build]}/{smartclientwebapp_file}",
        f"{base_url_protheus_data}{version}/exp_com_dic/latest/protheus_data.zip",
        f"{base_url_web_agent}web-agent.zip"
    ]
    return urls

def download_files(version, urls, log_box):
    base_directory = f"C:\\TOTVS\\Download\\{version}"
    os.makedirs(base_directory, exist_ok=True)
    
    # Adiciona um mapeamento para os nomes dos arquivos
    filename_map = {
        "appserver.zip": "appserver.zip",
        "smartclient.zip": "smartclient.zip",
        "dbaccess.zip": "dbaccess.zip",
        "dbapi.zip": "dbapi.zip",
        "smartclientwebapp.zip": "smartclientwebapp.zip",  # padrão
        "webapp-10.0.2-windows-x64-release.zip": "smartclientwebapp.zip",  # para Panthera Onça
        "protheus_data.zip": "protheus_data.zip",
        "web-agent.zip": "web-agent.zip"
    }

    for url in urls:
        try:
            file_name = url.split("/")[-1]
            file_path = os.path.join(base_directory, filename_map.get(file_name, file_name))
            
            log_box.insert(tk.END, f"Iniciando download de {file_name}...\n")
            log_box.see(tk.END)

            response = requests.get(url, stream=True)
            response.raise_for_status()

            total_size = int(response.headers.get('content-length', 0))
            downloaded_size = 0

            # Inicializa a mensagem de progresso
            progress_message = f"Baixado: 0 KB de {total_size / 1024:.2f} KB"
            progress_index = log_box.index(tk.END)
            log_box.insert(tk.END, progress_message + "\n")
            log_box.see(tk.END)

            with open(file_path, "wb") as file:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        file.write(chunk)
                        downloaded_size += len(chunk)

                        # Atualiza a linha de progresso atual
                        log_box.delete(progress_index + " linestart", progress_index + " lineend")
                        progress_message = f"Baixado: {downloaded_size / 1024:.2f} KB de {total_size / 1024:.2f} KB"
                        log_box.insert(progress_index + " linestart", progress_message)
                        log_box.see(tk.END)
                        log_box.update()  # Atualiza o log_box em tempo real

            log_box.insert(tk.END, f"Download de {file_name} concluído.\n")
            log_box.see(tk.END)
        except requests.exceptions.RequestException as e:
            log_box.insert(tk.END, f"Erro ao baixar {file_name}: {str(e)}\n")
            log_box.see(tk.END)
        except Exception as e:
            log_box.insert(tk.END, f"Ocorreu um erro inesperado ao baixar {file_name}: {str(e)}\n")
            log_box.see(tk.END)

def create_shortcut(file_path, shortcut_name, additional_parameters, log_box):
    shortcut_path = os.path.join(os.path.dirname(file_path), f"{shortcut_name}.lnk")
    shell = Dispatch('WScript.Shell')
    shortcut = shell.CreateShortCut(shortcut_path)
    shortcut.Targetpath = file_path
    shortcut.Arguments = additional_parameters
    shortcut.WorkingDirectory = os.path.dirname(file_path)
    shortcut.save()

    log_box.insert(tk.END, f"Atalho criado: {shortcut_path}\n")
    log_box.see(tk.END)

def extract_files(version, log_box):
    base_directory = f"C:\\TOTVS\\Download\\{version}"
    extraction_map = {
        "appserver.zip": f"C:\\TOTVS\\Protheus_{version}\\bin\\Appserver",
        "dbaccess.zip": f"C:\\TOTVS\\TotvsDBAccess",
        "dbapi.zip": f"C:\\TOTVS\\TotvsDBAccess",
        "smartclient.zip": f"C:\\TOTVS\\Protheus_{version}\\bin\\SmartClient",
        "smartclientwebapp.zip": f"C:\\TOTVS\\Protheus_{version}\\bin\\Appserver",
        "web-agent.zip": f"C:\\TOTVS\\Download\\{version}\\web-agent",
        "protheus_data.zip": f"C:\\TOTVS\\{version}"  
    }

    for file_name, dest_dir in extraction_map.items():
        zip_path = os.path.join(base_directory, file_name)
        os.makedirs(dest_dir, exist_ok=True)  # Garante que o diretório existe

        if os.path.exists(zip_path):
            log_box.insert("end", f"Verificando {file_name}...\n")
            log_box.see("end")

            if os.path.getsize(zip_path) > 0:
                try:
                    if file_name == "protheus_data.zip":
                        # Lógica específica para protheus_data.zip com py7zr
                        log_box.insert("end", f"Extraindo {file_name} para {dest_dir} com py7zr...\n")
                        log_box.see("end")

                        with py7zr.SevenZipFile(zip_path, 'r') as archive:
                            archive.extractall(path=dest_dir)

                        log_box.insert("end", f"Extração de {file_name} concluída.\n")
                        log_box.see("end")
                    else:
                        # Lógica padrão para arquivos ZIP comuns
                        log_box.insert("end", f"Extraindo {file_name} para {dest_dir}...\n")
                        log_box.see("end")

                        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                            zip_ref.extractall(dest_dir)

                        log_box.insert("end", f"Extração de {file_name} concluída.\n")
                        log_box.see("end")

                except zipfile.BadZipFile:
                    log_box.insert("end", f"Erro: {file_name} não é um arquivo ZIP válido.\n")
                    log_box.see("end")
                except Exception as e:
                    log_box.insert("end", f"Erro ao extrair {file_name}: {str(e)}\n")
                    log_box.see("end")
            else:
                log_box.insert("end", f"Erro: {file_name} está vazio ou corrompido.\n")
                log_box.see("end")
        else:
            log_box.insert("end", f"Arquivo {file_name} não encontrado para extração.\n")
            log_box.see("end")

def install_web_agent(log_box, version):
    base_directory = f"C:\\TOTVS\\Download\\{version}"
    web_agent_path = os.path.join(base_directory, "web-agent")

    try:
        # Verifica se o diretório existe
        if not os.path.exists(web_agent_path):
            log_box.insert(tk.END, f"Caminho não encontrado: {web_agent_path}\n")
            return
        
        # Lista todos os arquivos no diretório web-agent e filtra arquivos .exe
        files = os.listdir(web_agent_path)
        exe_files = [file for file in files if file.endswith('.exe')]

        if exe_files:
            setup_file = os.path.join(web_agent_path, exe_files[0])
            log_box.insert(tk.END, f"Arquivo de instalação encontrado: {setup_file}\n")
            log_box.see(tk.END)

            # Executa o comando de instalação de forma silenciosa
            log_box.insert(tk.END, f"Iniciando a instalação do {setup_file}...\n")
            log_box.see(tk.END)
            subprocess.run([setup_file, "/silent"], check=True)

            log_box.insert(tk.END, f"Instalação do {setup_file} concluída com sucesso!\n")
            log_box.see(tk.END)
        else:
            log_box.insert(tk.END, "Nenhum arquivo de instalação (.exe) encontrado no diretório web-agent.\n")
            log_box.see(tk.END)
    except Exception as e:
        log_box.insert(tk.END, f"Erro durante a instalação: {str(e)}\n")
        log_box.see(tk.END)

def create_appserver_shortcut(log_box, version):
    appserver_path = r"C:\\TOTVS\\Protheus_{}\bin\\Appserver\\appserver.exe".format(version)
    create_shortcut(appserver_path, "appserver.exe - Atalho", "-console", log_box)

def create_smartclient_shortcut(log_box, version):
    smartclient_path = r"C:\\TOTVS\\Protheus_{}\bin\\SmartClient\\smartclient.exe".format(version)
    create_shortcut(smartclient_path, "smartclient.exe - Atalho", " -m", log_box)

def create_dbaccess_shortcut(log_box):
    dbaccess_path = r"C:\\TOTVS\\TotvsDBAccess\\dbaccess64.exe"
    create_shortcut(dbaccess_path, "dbaccess64.exe - Atalho", "-debug", log_box)

def download_protheus(version, appserver, build, log_box):
    steps = 6
    current_step = 0
    
    def update_log(message):
        nonlocal current_step
        current_step += 1
        log_box.insert(tk.END, f"Passo {current_step}/{steps}: {message}\n")
        log_box.see(tk.END)

    update_log("Criando estrutura de pastas...")
    create_folder_structure(version, log_box)

    update_log("Obtendo URLs de download...")
    urls = get_download_url(appserver, build, version)

    update_log("Iniciando download dos arquivos...")
    download_files(version, urls, log_box)

    update_log("Extraindo arquivos...")
    extract_files(version, log_box)

    update_log("Criando atalhos...")
    create_appserver_shortcut(log_box, version)
    create_smartclient_shortcut(log_box, version)
    create_dbaccess_shortcut(log_box)

    update_log("Download e configuração do Protheus concluídos com sucesso!")

def download_base_congelada(version, log_box):
    if version == "12.1.2210":
        url = "https://arte.engpro.totvs.com.br/engenharia/base_congelada/protheus/bra/12.1.2210/exp_com_dic/latest/mssql_bak.zip"
    elif version == "12.1.2310":
        url = "https://arte.engpro.totvs.com.br/engenharia/base_congelada/protheus/bra/12.1.2310/exp_com_dic/latest/mssql_bak.zip"
    elif version == "12.1.2410":
        url = "https://arte.engpro.totvs.com.br/engenharia/base_congelada/protheus/bra/12.1.2410/exp_com_dic/latest/mssql_bak.zip"
    else:
        log_box.insert(tk.END, "Versão inválida selecionada.\n")
        log_box.see(tk.END)
        return

    try:
        log_box.insert(tk.END, f"Baixando base congelada para a versão {version}...\n")
        log_box.see(tk.END)

        # Fazendo o download do arquivo
        response = requests.get(url, stream=True)
        response.raise_for_status()  # Levanta uma exceção se o download falhar

        # Caminho para salvar o arquivo
        base_directory = f"C:\\TOTVS\\Download\\{version}"
        os.makedirs(base_directory, exist_ok=True)
        file_path = os.path.join(base_directory, "mssql_bak.zip")

        # Obtendo o tamanho total do arquivo
        total_size = int(response.headers.get('content-length', 0))
        downloaded_size = 0

        # Salvando o arquivo em chunks e exibindo progresso
        progress_message = f"Baixado: 0 KB de {total_size / 1024:.2f} KB"
        progress_index = log_box.index(tk.END)
        log_box.insert(tk.END, progress_message + "\n")
        log_box.see(tk.END)
        
        with open(file_path, "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:  # Filtrando keep-alive chunks
                    file.write(chunk)
                    downloaded_size += len(chunk)
                    # Atualizando o log_box com o progresso do download na mesma linha
                    log_box.delete(progress_index + " linestart", progress_index + " lineend")
                    progress_message = f"Baixado: {downloaded_size / 1024:.2f} KB de {total_size / 1024:.2f} KB"
                    log_box.insert(progress_index + " linestart", progress_message)
                    log_box.see(tk.END)
                    log_box.update()  # Atualiza o log_box em tempo real

        log_box.insert(tk.END, f"Base congelada baixada com sucesso em: {file_path}\n")
        log_box.see(tk.END)
    except requests.exceptions.RequestException as e:
        log_box.insert(tk.END, f"Erro ao baixar a base congelada: {str(e)}\n")
        log_box.see(tk.END)
    except Exception as e:
        log_box.insert(tk.END, f"Ocorreu um erro inesperado: {str(e)}\n")
        log_box.see(tk.END)