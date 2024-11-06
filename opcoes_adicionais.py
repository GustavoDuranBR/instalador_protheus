import requests
from bs4 import BeautifulSoup
import os
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox

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
        soup = BeautifulSoup(response.text, 'html.parser')
        rows = soup.select('tr.file')
        versions = []
        for row in rows:
            version_tag = row.select_one('td:nth-child(2) span.name')
            if version_tag:
                version_name = version_tag.get_text(strip=True)
                versions.append(version_name)
        return versions
    except Exception as e:
        print(f"Erro ao obter versões de {url}: {str(e)}")
        return []

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

    root_x = root.winfo_x()
    root_y = root.winfo_y()
    additional_window.geometry(f"+{root_x + 50}+{root_y + 50}")

    style = ttk.Style()
    style.theme_use('default')
    style.configure('TButton', background='#666666', foreground='#8bb7f7', font=('Arial', 10, 'italic'))
    style.map('TButton', background=[('active', '#555555')])

    label = tk.Label(additional_window, text="Opções Adicionais de Download", bg='#333333', 
                     fg='#8bb7f7', font=('Arial', 12, 'bold', 'italic'))
    label.pack(pady=10)

    frame_options = tk.Frame(additional_window, bg='#333333')
    frame_options.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

    checkbox_style = {
        'bg': '#333333',
        'fg': '#ffffff',
        'font': ('Arial', 10, 'italic'),
        'selectcolor': '#333333'
    }

    # Adicionar a combobox para selecionar a build (Panthera ou Harpia)
    selected_build = tk.StringVar(value="Panthera Onça")
    build_label = tk.Label(frame_options, text="Selecione a Build:", bg='#333333', fg='#ffffff', font=('Arial', 10, 'italic'))
    build_label.grid(row=0, column=0, padx=10, pady=5, sticky='w')
    build_combobox = ttk.Combobox(frame_options, textvariable=selected_build, values=["Panthera Onça", "Harpia"], state="readonly")
    build_combobox.grid(row=0, column=1, padx=10, pady=5, sticky='ew')

    # Variáveis e opções de download
    options = {
        "AppServer": (tk.BooleanVar(), tk.StringVar(), []),
        #"DbAccess": (tk.BooleanVar(), tk.StringVar(), []),
        #"SmartClient": (tk.BooleanVar(), tk.StringVar(), []),
        "SmartClientWebApp": (tk.BooleanVar(), tk.StringVar(), []),
        #"Web-Agent": (tk.BooleanVar(), tk.StringVar(), [])
    }

    # Função para preencher a combobox de versão quando o checkbox for marcado
    def on_option_selected(option, selected_var, version_var, combo_box, build_var):
        if selected_var.get():
            build = build_mapping.get(build_var.get(), build_var.get()).lower()
            url = base_urls[option].format(build) if '{}' in base_urls[option] else base_urls[option]
            versions = get_versions(url)
            if versions:
                combo_box['values'] = versions
                version_var.set(versions[0])
            else:
                messagebox.showwarning("Erro", f"Não foi possível obter as versões de {option}.")
        else:
            version_var.set("Selecione a Versão")
            combo_box['values'] = []

    # Adicionando as opções de download com checkboxes e comboboxes
    for idx, (label, (selected_var, version_var, _)) in enumerate(options.items(), start=1):
        tk.Checkbutton(frame_options, text=label, variable=selected_var, **checkbox_style).grid(row=idx, column=0, sticky='w', pady=5)
        version_combobox = ttk.Combobox(frame_options, textvariable=version_var, values=[], state="readonly")
        version_combobox.grid(row=idx, column=1, padx=10, pady=5, sticky='ew')
        version_var.set("Selecione a Versão")
        selected_var.trace('w', lambda *args, label=label, var=selected_var, version=version_var, combo=version_combobox, build=selected_build: 
                           on_option_selected(label, var, version, combo, build))

    download_button = ttk.Button(frame_options, text="Download", style='TButton', 
                                 command=lambda: iniciar_download(options, log_box, selected_build))
    download_button.grid(row=len(options) + 1, column=0, padx=10, pady=10, sticky='ew')

    close_button = ttk.Button(frame_options, text="Fechar", style='TButton', 
                              command=additional_window.destroy)
    close_button.grid(row=len(options) + 1, column=1, padx=10, pady=10, sticky='ew')

    log_box = scrolledtext.ScrolledText(additional_window, width=50, height=20, 
                                        bg='#222222', fg='#8bb7f7', state='normal')
    log_box.pack(side=tk.RIGHT, fill=tk.BOTH, padx=10, pady=10, expand=True)
    log_box.insert(tk.END, "Pronto para iniciar o download...\n")

    additional_window.transient(root)
    additional_window.grab_set()
    root.wait_window(additional_window)

def iniciar_download(options, log_box, build_var):
    total_steps = sum(1 for selected_var, _, _ in options.values() if selected_var.get()) * 2 + 2
    current_step = 0

    def update_log(message):
        nonlocal current_step
        current_step += 1
        log_box.insert(tk.END, f"[{current_step}/{total_steps}] {message}\n")
        log_box.see(tk.END)
        log_box.update_idletasks()

    for label, (selected_var, version_var, _) in options.items():
        if selected_var.get() and version_var.get() == "Selecione a Versão":
            messagebox.showwarning("Erro de Seleção", f"Por favor, selecione a versão para {label}.")
            return

    if not any(var.get() for var, _, _ in options.values()):
        messagebox.showwarning("Erro de Seleção", "Por favor, marque pelo menos uma das opções de download.")
        return

    log_message = verificar_e_criar_diretorio()
    update_log(log_message)
    update_log("Iniciando downloads...")

    build = build_mapping.get(build_var.get(), build_var.get()).lower()

    for label, (selected_var, version_var, _) in options.items():
        if selected_var.get():
            version = version_var.get()
            if label == "AppServer":
                file_name = "appserver.zip"
            elif label == "SmartClientWebApp":
                file_name = "smartclientwebapp.zip"
            url = base_urls[label].format(build) + f"{version}/{file_name}"
            build_dir = f"C:\\TOTVS\\Download\\Download_Protheus\\{build}"
            if not os.path.exists(build_dir):
                os.makedirs(build_dir)
            destino = os.path.join(build_dir, file_name)            
            update_log(f"Baixando {label} - Versão {version}...")
            realizar_download(url, destino, log_box)
    update_log("Todos os downloads foram concluídos.")

def realizar_download(url, destino, log_box):
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()

        total_size = int(response.headers.get('content-length', 0))
        downloaded_size = 0

        progress_message = f"Baixando {os.path.basename(destino)}: 0 KB de {total_size / 1024:.2f} KB"
        log_box.insert(tk.END, progress_message)
        log_box.see(tk.END)
        log_box.update_idletasks()

        with open(destino, "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    file.write(chunk)
                    downloaded_size += len(chunk)

                    progress_message = f"\rBaixando {os.path.basename(destino)}: {downloaded_size / 1024:.2f} KB de {total_size / 1024:.2f} KB"
                    log_box.delete('end-1c linestart', 'end-1c lineend')
                    log_box.insert(tk.END, progress_message)
                    log_box.see(tk.END)
                    log_box.update_idletasks()

        log_box.insert(tk.END, f"\nDownload de {os.path.basename(destino)} concluído.\n")
        log_box.see(tk.END)
    except requests.exceptions.RequestException as e:
        log_box.insert(tk.END, f"Erro ao baixar {os.path.basename(destino)}: {str(e)}\n")
        log_box.see(tk.END)
    except Exception as e:
        log_box.insert(tk.END, f"Ocorreu um erro inesperado ao baixar {os.path.basename(destino)}: {str(e)}\n")
        log_box.see(tk.END)
