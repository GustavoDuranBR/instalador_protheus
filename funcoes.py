import os
import requests
import tkinter as tk

def create_folder_structure(version, log_box):
    base_directory = f"C:\\TOTVS"
    directories = [
        os.path.join(base_directory, f"{version}", "Apo"),
        os.path.join(base_directory, "Protheus", "bin"),
        os.path.join(base_directory, "Protheus", "bin", "Appserver"),
        os.path.join(base_directory, "Protheus", "bin", "SmartClient"),
        os.path.join(base_directory, f"{version}","Protheus_Data"),
        os.path.join(base_directory, "TotvsDBAccess")
    ]
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        log_box.insert(tk.END, f"Pasta criada: {directory}\n")
        log_box.see(tk.END)
    log_box.insert(tk.END, "Estrutura de pastas criada com sucesso.\n")
    log_box.see(tk.END)

def get_download_url(build, appserver):
    base_url_appserver = "https://arte.engpro.totvs.com.br/tec/appserver/"
    base_url_smartclient = "https://arte.engpro.totvs.com.br/tec/smartclient/"
    base_url_dbaccess = "https://arte.engpro.totvs.com.br/tec/dbaccess/windows/64/latest/dbaccess.zip"
    base_url_dbapi = "https://arte.engpro.totvs.com.br/tec/dbaccess/windows/64/latest/dbapi.zip"
    base_url_smartclientwebapp = "https://arte.engpro.totvs.com.br/tec/smartclientwebapp/"

    appserver_map = {
        "Harpia": "harpia",
        "Lobo Guara": "lobo_guara",
        "Panthera Onça": "panthera_onca"
    }

    build_map = {
        "Latest": "latest",
        "Next": "next",
        "Published": "published"
    }

    urls = [
        f"{base_url_appserver}{appserver_map[appserver]}/windows/64/{build_map[build]}/appserver.zip",
        f"{base_url_smartclient}{appserver_map[appserver]}/windows/64/{build_map[build]}/smartclient.zip",
        f"{base_url_dbaccess}",
        f"{base_url_dbapi}",
        f"{base_url_smartclientwebapp}{appserver_map[appserver]}/windows/64/{build_map[build]}/smartclientwebapp.zip"
    ]
    return urls

def download_files(version, urls, log_box):
    base_directory = f"C:\\TOTVS\\Download\\{version}"

    if not os.path.exists(base_directory):
        os.makedirs(base_directory)

    for url in urls:
        file_name = os.path.join(base_directory, url.split("/")[-1])
        log_box.insert(tk.END, f"Iniciando download de {url.split('/')[-1]}...\n")
        log_box.see(tk.END)
        
        response = requests.get(url)
        with open(file_name, 'wb') as file:
            file.write(response.content)
        
        log_box.insert(tk.END, f"Download de {file_name} concluído!\n")
        log_box.see(tk.END)

def download_protheus(version, appserver, build, log_box):
    log_box.insert(tk.END, "Iniciando o processo de download...\n")
    log_box.see(tk.END)
    
    # Obtém as URLs para download
    download_urls = get_download_url(build, appserver)
    
    # Cria a estrutura de pastas
    create_folder_structure(version, log_box)
    
    # Realiza os downloads um por vez
    log_box.insert(tk.END, "Baixando AppServer...\n")
    log_box.see(tk.END)
    download_files(version, [download_urls[0]], log_box)  # AppServer
    
    log_box.insert(tk.END, "Baixando SmartClient...\n")
    log_box.see(tk.END)
    download_files(version, [download_urls[1]], log_box)  # SmartClient
    
    log_box.insert(tk.END, "Baixando DBAccess...\n")
    log_box.see(tk.END)
    download_files(version, [download_urls[2]], log_box)  # DBAccess
    
    log_box.insert(tk.END, "Baixando SmartClient WebApp...\n")
    log_box.see(tk.END)
    download_files(version, [download_urls[3]], log_box)  # SmartClient WebApp
    
    log_box.insert(tk.END, "Todos os downloads foram concluídos com sucesso.\n")
    log_box.see(tk.END)

def download_base_congelada(version, log_box):
    if version == "12.1.2210":
        url = "https://arte.engpro.totvs.com.br/engenharia/base_congelada/protheus/bra/12.1.2210/exp_com_dic/latest/mssql_bak.zip"
    elif version == "12.1.2310":
        url = "https://arte.engpro.totvs.com.br/engenharia/base_congelada/protheus/bra/12.1.2310/exp_com_dic/latest/mssql_bak.zip"
    else:
        log_box.insert(tk.END, "Versão inválida selecionada.\n")
        log_box.see(tk.END)
        return

    log_box.insert(tk.END, f"Iniciando o download da Base Congelada para a versão {version}...\n")
    log_box.see(tk.END)
    download_files(version, [url], log_box)
    log_box.insert(tk.END, "Download da Base Congelada concluído.\n")
    log_box.see(tk.END)
