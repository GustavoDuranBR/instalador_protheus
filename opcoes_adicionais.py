import requests
from bs4 import BeautifulSoup
import os
import tkinter as tk
from tkinter import ttk, scrolledtext

# URLs base para download e obtenção de versões
base_urls = {
    "AppServer": "https://arte.engpro.totvs.com.br/tec/appserver/panthera_onca/windows/64/builds/",
    "DbAccess": "https://arte.engpro.totvs.com.br/tec/dbaccess/windows/64/builds/",
    "SmartClient": "https://arte.engpro.totvs.com.br/tec/smartclient/harpia/windows/64/builds/",
    "SmartClientWebApp": f"https://arte.engpro.totvs.com.br/tec/smartclientwebapp/panthera_onca/windows/64/builds/",
    "Web-Agent": f"https://arte.engpro.totvs.com.br/tec/web-agent/windows/64/builds/"
}

def get_versions(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    rows = soup.select('tr.file')
    versions = []

    for row in rows:
        version_tag = row.select_one('td:nth-child(2) span.name')
        if version_tag:
            version_name = version_tag.get_text(strip=True)
            versions.append(version_name)
        else:
            print("Elemento de versão não encontrado na linha:", row.prettify())

    return versions

def verificar_e_criar_diretorio():
    base_directory = "C:\\TOTVS\\Download\\Download_Protheus"
    if not os.path.exists(base_directory):
        os.makedirs(base_directory)
        return f"Diretório {base_directory} criado com sucesso.\n"
    else:
        return f"Diretório {base_directory} já existe.\n"

def open_additional_options(root):
    additional_window = tk.Toplevel(root)
    additional_window.title("Opções Adicionais de Download")
    additional_window.iconbitmap("icon.ico")
    additional_window.geometry("700x400")
    additional_window.configure(bg='#333333')

    style = ttk.Style()
    style.theme_use('default')
    style.configure('TButton', background='#666666', foreground='#8bb7f7', font=('Arial', 10, 'italic'))
    style.map('TButton', background=[('active', '#555555')])

    label = tk.Label(additional_window, text="Opções Adicionais de Download", 
                     bg='#333333', fg='#8bb7f7', font=('Arial', 12, 'bold', 'italic'))
    label.pack(pady=10)

    frame_options = tk.Frame(additional_window, bg='#333333')
    frame_options.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

    checkbox_style = {
        'bg': '#333333',
        'fg': '#ffffff',
        'font': ('Arial', 10, 'italic'),
        'selectcolor': '#333333'
    }

    options = {
        "AppServer": (tk.BooleanVar(), tk.StringVar(), []),
        "DbAccess": (tk.BooleanVar(), tk.StringVar(), []),
        "SmartClient": (tk.BooleanVar(), tk.StringVar(), []),
        "SmartClientWebApp": (tk.BooleanVar(), tk.StringVar(), []),
        "Web-Agent": (tk.BooleanVar(), tk.StringVar(), [])
    }

    for idx, (label, (var, combo_var, _)) in enumerate(options.items()):
        tk.Checkbutton(frame_options, text=label, variable=var, **checkbox_style) \
            .grid(row=idx, column=0, sticky='w', pady=5)
        version_combobox = ttk.Combobox(frame_options, textvariable=combo_var, 
                                        values=options_dict[label], state="readonly")
        version_combobox.grid(row=idx, column=1, padx=10, pady=5, sticky='ew')
        combo_var.set("Selecione a Versão")

    download_button = ttk.Button(frame_options, text="Download", style='TButton', 
                                 command=lambda: iniciar_download(options, log_box))
    download_button.grid(row=len(options) + 1, column=0, padx=10, pady=10, sticky='ew')

    close_button = ttk.Button(frame_options, text="Fechar", style='TButton', 
                              command=additional_window.destroy)
    close_button.grid(row=len(options) + 1, column=1, padx=10, pady=10, sticky='ew')

    log_box = scrolledtext.ScrolledText(additional_window, width=40, height=15, 
                                        bg='#222222', fg='#8bb7f7', state='normal')
    log_box.pack(side=tk.RIGHT, fill=tk.BOTH, padx=10, pady=10, expand=True)
    log_box.insert(tk.END, "Pronto para iniciar o download...\n")

def iniciar_download(options, log_box):
    log_message = verificar_e_criar_diretorio()
    log_box.insert(tk.END, log_message)

    log_box.insert(tk.END, "Iniciando downloads...\n")
    for label, (selected_var, version_var, _) in options.items():
        if selected_var.get():
            status = "Selecionado"
            version = version_var.get()
            if label == "DbAccess":
                # Download do arquivo principal e do dbapi.zip para DbAccess
                urls = [
                    f"{base_urls[label]}{version}/{label.lower()}.zip",
                    f"{base_urls[label]}{version}/dbapi.zip"
                ]
                for url in urls:
                    log_box.insert(tk.END, f"{label}: {status}, Versão: {version}, URL: {url}\n")
                    realizar_download(url, f"C:\\TOTVS\\Download\\Download_Protheus\\{os.path.basename(url)}")
            else:
                url = f"{base_urls[label]}{version}/{label.lower()}.zip"
                log_box.insert(tk.END, f"{label}: {status}, Versão: {version}, URL: {url}\n")
                realizar_download(url, f"C:\\TOTVS\\Download\\Download_Protheus\\{label}_{version}.zip")
        else:
            status = "Não Selecionado"
            log_box.insert(tk.END, f"{label}: {status}\n")
    log_box.insert(tk.END, "Todos os downloads foram concluídos.\n")
    log_box.yview(tk.END)

def realizar_download(url, destino):
    response = requests.get(url)
    with open(destino, 'wb') as file:
        file.write(response.content)

# Obter versões para cada URL
options_dict = {key: get_versions(url) for key, url in base_urls.items()}
