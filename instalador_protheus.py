import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from funcoes import download_protheus, download_base_congelada
from arquivos_adicionais import copiar_appserver_ini, copiar_atualiar_rpo
from opcoes_adicionais import open_additional_options

def validate_selections(version=None, appserver=None, build=None):
    if version and (not version or version == "Selecione a versão"):
        messagebox.showerror("Erro", "Por favor, selecione a versão do Protheus.")
        return False
    if appserver is not None and (not appserver or appserver == "Selecione o AppServer"):
        messagebox.showerror("Erro", "Por favor, selecione o AppServer.")
        return False
    if build is not None and (not build or build == "Selecione a Build"):
        messagebox.showerror("Erro", "Por favor, selecione a Build.")
        return False
    return True

def on_download_button_click():
    version = version_var.get()
    appserver = appserver_var.get()
    build = build_var.get()

    if validate_selections(version, appserver, build):
        log_box.insert(tk.END, "Espere enquanto realizo o download...\n")
        log_box.see(tk.END)
        log_box.update_idletasks()  # Atualiza o log imediatamente

        download_protheus(version, appserver, build, log_box)

def on_baixar_appserver_ini_button_click():
    version = version_var.get()
    if validate_selections(version=version):
        log_box.insert(tk.END, "Copiando o arquivo appserver.ini...\n")
        log_box.see(tk.END)
        copiar_appserver_ini(version, log_box)

def on_baixar_atualizador_rpo_click():
    version = version_var.get()
    if validate_selections(version=version):
        log_box.insert(tk.END, f"Copiando Atualizar_RPO_{version}.bat...\n")
        log_box.see(tk.END)
        copiar_atualiar_rpo(version, log_box)

def on_base_congelada_button_click():
    version = version_var.get()
    if validate_selections(version, None, None):
        log_box.insert(tk.END, "Espere enquanto realizo o download da Base Congelada...\n")
        log_box.see(tk.END)
        log_box.update_idletasks()  # Atualiza o log imediatamente

        download_base_congelada(version, log_box)

def quit_app():
    if messagebox.askokcancel("Sair", "Você tem certeza que deseja sair?"):
        root.quit()
        root.destroy()

root = tk.Tk()
root.title("Instalador Protheus")
root.iconbitmap("icon.ico")
root.geometry("700x500")
root.configure(bg='#333333')

# Estilo para tema dark e botões padronizados
style = ttk.Style()
style.theme_use('default')
style.configure('TButton', background='#666666', foreground='#8bb7f7', font=('Arial', 10), width=20)
style.map('TButton', background=[('active', '#555555')])

label = tk.Label(root, text="Instalador Protheus", bg='#333333', 
                 fg='#8bb7f7', font=('Arial', 14, 'bold','italic'))
label.pack(pady=10)

# Frame para os botões, alinhado à esquerda
frame_buttons = tk.Frame(root, bg='#333333')
frame_buttons.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

# Caixa de diálogo para log
log_box = scrolledtext.ScrolledText(root, width=50, height=20, 
                                    bg='#222222', fg='#8bb7f7', state='normal')
log_box.pack(side=tk.RIGHT, fill=tk.BOTH, padx=10, pady=10, expand=True)
log_box.insert(tk.END, "Pronto para iniciar o download...\n")

# Label e Seletor de versão
version_label = tk.Label(frame_buttons, text="Selecione a versão do Protheus:", 
                         bg='#333333', fg='#8bb7f7', 
                         font=('Arial', 10, 'bold','italic'))
version_label.pack(pady=2, anchor=tk.W)
version_var = tk.StringVar()
version_selector = ttk.Combobox(frame_buttons, 
                                textvariable=version_var, 
                                values=["12.1.2210", "12.1.2310"], state="readonly")
version_selector.set("Selecione a versão")
version_selector.pack(pady=5, anchor=tk.W)

# Label e Seletor do AppServer
appserver_var = tk.StringVar()
appserver_selector = ttk.Combobox(frame_buttons, 
                                  textvariable=appserver_var, 
                                  values=["Harpia", "Panthera Onça"], state="readonly")
appserver_selector.set("Selecione o AppServer")
appserver_selector.pack(pady=5, anchor=tk.W)

# Label e Seletor do Build
build_var = tk.StringVar()
build_selector = ttk.Combobox(frame_buttons, 
                              textvariable=build_var, 
                              values=["Latest", "Next", "Published"], state="readonly")
build_selector.set("Selecione a Build")
build_selector.pack(pady=5, anchor=tk.W)

# Botão de Download
download_button = ttk.Button(frame_buttons, text="Realizar Download", 
                            command=on_download_button_click)
download_button.pack(pady=5, anchor=tk.W)

# Botão para Baixar AppServer.ini
baixar_ini_button = ttk.Button(frame_buttons, 
                              text="Baixar AppServer.ini", 
                              command=on_baixar_appserver_ini_button_click)
baixar_ini_button.pack(pady=5, anchor=tk.W)

# Botão para Baixar Atualizador RPO
baixar_rpo_button = ttk.Button(frame_buttons, 
                              text="Baixar Atualizador RPO", 
                              command=on_baixar_atualizador_rpo_click)
baixar_rpo_button.pack(pady=5, anchor=tk.W)

# Botão de Base Congelada
base_congelada_button = ttk.Button(frame_buttons, text="Base Congelada", 
                                  command=on_base_congelada_button_click)
base_congelada_button.pack(pady=5, anchor=tk.W)

# Botão Opções Adicionais
additional_button = ttk.Button(frame_buttons, text="Opções Adicionais", 
                              command=lambda: open_additional_options(root))
additional_button.pack(pady=5, anchor=tk.W)

# Botão de Sair
exit_button = ttk.Button(frame_buttons, text="Sair", command=quit_app)
exit_button.pack(pady=5, anchor=tk.W)

# Informações do desenvolvedor e versão, alinhadas à esquerda junto com os botões
dev_label = tk.Label(
    frame_buttons, 
    text="Desenvolvedor: Gustavo Duran\nVersão: 2.0", 
    bg='#333333', 
    fg='#8bb7f7', 
    font=('Arial', 10,'bold','italic'), 
    justify='left'
)
dev_label.pack(pady=1, anchor=tk.W)

root.protocol("WM_DELETE_WINDOW", quit_app)
root.mainloop()
