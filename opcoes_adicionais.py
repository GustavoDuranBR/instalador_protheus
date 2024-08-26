import requests
from bs4 import BeautifulSoup
import os
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox

# URLs base para download e obtenção de versões
base_urls = {
    "AppServer": "https://arte.engpro.totvs.com.br/tec/appserver/panthera_onca/windows/64/builds/",
    "DbAccess": "https://arte.engpro.totvs.com.br/tec/dbaccess/windows/64/builds/",
    "SmartClient": "https://arte.engpro.totvs.com.br/tec/smartclient/harpia/windows/64/builds/",
    "SmartClientWebApp": "https://arte.engpro.totvs.com.br/tec/smartclientwebapp/panthera_onca/windows/64/builds/",
    "Web-Agent": "https://arte.engpro.totvs.com.br/tec/web-agent/windows/64/builds/"
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

    root_x = root.winfo_x()
    root_y = root.winfo_y()
    additional_window.geometry(f"+{root_x + 50}+{root_y + 50}")

    style = ttk.Style()
    style.theme_use('default')
    style.configure('TButton', background='#666666', foreground='#8bb7f7', font=('Arial', 10, 'italic'))
    style.map('TButton', background=[('active', '#555555')])

    label = tk.Label(additional_window, text="Opções Adicionais de Download", bg='#333333', fg='#8bb7f7', font=('Arial', 12, 'bold', 'italic'))
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
        version_combobox = ttk.Combobox(frame_options, textvariable=combo_var, values=options_dict[label], state="readonly")
        version_combobox.grid(row=idx, column=1, padx=10, pady=5, sticky='ew')
        combo_var.set("Selecione a Versão")

    download_button = ttk.Button(frame_options, text="Download", style='TButton', command=lambda: iniciar_download(options, log_box))
    download_button.grid(row=len(options) + 1, column=0, padx=10, pady=10, sticky='ew')

    close_button = ttk.Button(frame_options, text="Fechar", style='TButton', command=additional_window.destroy)
    close_button.grid(row=len(options) + 1, column=1, padx=10, pady=10, sticky='ew')

    log_box = scrolledtext.ScrolledText(additional_window, width=50, height=20, bg='#222222', fg='#8bb7f7', state='normal')
    log_box.pack(side=tk.RIGHT, fill=tk.BOTH, padx=10, pady=10, expand=True)
    log_box.insert(tk.END, "Pronto para iniciar o download...\n")

    additional_window.transient(root)
    additional_window.grab_set()
    root.wait_window(additional_window)

def iniciar_download(options, log_box):
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

    for label, (selected_var, version_var, _) in options.items():
        if selected_var.get():
            status = "Selecionado"
            version = version_var.get()
            if label == "DbAccess":
                urls = [
                    f"{base_urls[label]}{version}/{label.lower()}.zip",
                    f"{base_urls[label]}{version}/dbapi.zip"
                ]
                for url in urls:
                    update_log(f"{label}: {status}, Versão: {version}, URL: {url}")
                    realizar_download(url, f"C:\\TOTVS\\Download\\Download_Protheus\\{os.path.basename(url)}", log_box)
            else:
                url = f"{base_urls[label]}{version}/{label.lower()}.zip"
                update_log(f"{label}: {status}, Versão: {version}, URL: {url}")
                realizar_download(url, f"C:\\TOTVS\\Download\\Download_Protheus\\{label}_{version}.zip", log_box)
        else:
            status = "Não Selecionado"
            update_log(f"{label}: {status}")

    if extract_var.get():
        update_log("Iniciando a extração dos arquivos...")
        for file_name in downloaded_files:
            file_path = f"C:\\TOTVS\\Download\\Download_Protheus\\{file_name}"
            extract_files(file_path, log_box)  # Chama a função extract_files existente
        update_log("Extração concluída.")

    update_log("Todos os downloads foram concluídos.")

def realizar_download(url, destino, log_box):
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()

        total_size = int(response.headers.get('content-length', 0))
        downloaded_size = 0

        # Inicializa a mensagem de progresso
        progress_message = f"Baixando {os.path.basename(destino)}: 0 KB de {total_size / 1024:.2f} KB"
        log_box.insert(tk.END, progress_message)
        log_box.see(tk.END)
        log_box.update_idletasks()

        with open(destino, "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    file.write(chunk)
                    downloaded_size += len(chunk)

                    # Atualiza a linha de progresso
                    log_box.delete('end-1c linestart', 'end-1c lineend')
                    progress_message = f"\rBaixando {os.path.basename(destino)}: {downloaded_size / 1024:.2f} KB de {total_size / 1024:.2f} KB"
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

# Obter versões para cada URL
options_dict = {key: get_versions(url) for key, url in base_urls.items()}
