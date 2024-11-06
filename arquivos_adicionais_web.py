import os
import shutil
import streamlit as st

def copiar_appserver_ini(version):
    # Diretório de origem com base na versão selecionada
    if version == "12.1.2210":
        source_dir = "AppServer_ini_2210"
    elif version == "12.1.2310":
        source_dir = "AppServer_ini_2310"
    elif version == "12.1.2410":
        source_dir = "AppServer_ini_2410"
    else:
        return

    # Caminho do arquivo appserver.ini de origem
    ini_file = os.path.join(source_dir, "appserver.ini")

    # Caminho de destino
    dest_dir = f'C:\\TOTVS\\Protheus_{version}\\bin\\AppServer'
    dest_file = os.path.join(dest_dir, "appserver.ini")

    # Criar diretório de destino se não existir
    os.makedirs(dest_dir, exist_ok=True)

    # Copiar o arquivo
    try:
        shutil.copy(ini_file, dest_file)
    except Exception:
        return

def copiar_atualiar_rpo(version):
    # Diretório de origem com base na versão selecionada
    if version == "12.1.2210":
        source_dir = "Atualizar_RPO\\RPO_12.1.2210\\"
    elif version == "12.1.2310":
        source_dir = "Atualizar_RPO\\RPO_12.1.2310\\"
    elif version == "12.1.2410":
        source_dir = "Atualizar_RPO\\RPO_12.1.2410\\"
    else:
        return

    # Caminho do arquivo de origem
    ini_file = os.path.join(source_dir, f"Atualizar_RPO_{version}.bat")

    # Caminho de destino
    dest_dir = f'C:\\TOTVS\\'
    dest_file = os.path.join(dest_dir, f"Atualizar_RPO_{version}.bat")

    # Criar diretório de destino se não existir
    os.makedirs(dest_dir, exist_ok=True)

    # Copiar o arquivo
    try:
        shutil.copy(ini_file, dest_file)
    except Exception:
        return
