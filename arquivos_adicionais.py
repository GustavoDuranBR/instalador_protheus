import os
import shutil
import tkinter as tk
from tkinter import ttk  # Adicionar essa linha
from funcoes import create_folder_structure

def copiar_appserver_ini(version, log_box):
    # Diretório de origem com base na versão selecionada
    if version == "12.1.2210":
        source_dir = "AppServer_ini_2210"
    elif version == "12.1.2310":
        source_dir = "AppServer_ini_2310"
    else:
        log_box.insert(tk.END, "Versão selecionada não reconhecida!\n")
        log_box.see(tk.END)
        return

    # Caminho do arquivo appserver.ini de origem
    ini_file = os.path.join(source_dir, "appserver.ini")

    # Caminho de destino
    dest_dir = f'C:\\TOTVS\\Protheus\\bin\\AppServer'
    dest_file = os.path.join(dest_dir, "appserver.ini")

    # Criar diretório de destino se não existir
    os.makedirs(dest_dir, exist_ok=True)

    # Copiar o arquivo
    try:
        shutil.copy(ini_file, dest_file)
        log_box.insert(tk.END, f"Arquivo appserver.ini copiado para {dest_file}.\n")
    except Exception as e:
        log_box.insert(tk.END, f"Erro ao copiar o arquivo: {str(e)}.\n")

    log_box.see(tk.END)


def copiar_atualiar_rpo(version, log_box):
    # Diretório de origem com base na versão selecionada
    if version == "12.1.2210":
        source_dir = "Atualizar_RPO\\RPO_12.1.2210\\"
    elif version == "12.1.2310":
        source_dir = "Atualizar_RPO\\RPO_12.1.2310\\"
    else:
        log_box.insert(tk.END, "Versão selecionada não reconhecida!\n")
        log_box.see(tk.END)
        return

    # Caminho do arquivo appserver.ini de origem
    ini_file = os.path.join(source_dir, f"Atualizar_RPO_{version}.bat")

    # Caminho de destino
    dest_dir = f'C:\\TOTVS\\'
    dest_file = os.path.join(dest_dir, f"Atualizar_RPO_{version}.bat")

    # Criar diretório de destino se não existir
    os.makedirs(dest_dir, exist_ok=True)

    # Copiar o arquivo
    try:
        shutil.copy(ini_file, dest_file)
        log_box.insert(tk.END, f"Arquivo Atualizar_RPO_{version}.bat copiado para {dest_file}.\n")
    except Exception as e:
        log_box.insert(tk.END, f"Erro ao copiar o arquivo: {str(e)}.\n")

    log_box.see(tk.END)
