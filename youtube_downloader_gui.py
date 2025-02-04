import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
import requests
import yt_dlp
import sys
import subprocess

def atualizar_codigo():
    repo_url = "https://raw.githubusercontent.com/SEU_USUARIO/SEU_REPOSITORIO/main/youtube_downloader_gui.py"
    try:
        response = requests.get(repo_url)
        if response.status_code == 200:
            novo_codigo = response.text.strip()
            caminho_arquivo = os.path.abspath(sys.argv[0])

            if os.path.exists(caminho_arquivo):
                with open(caminho_arquivo, "r", encoding="utf-8") as file:
                    codigo_atual = file.read().strip()

                if novo_codigo != codigo_atual:
                    with open(caminho_arquivo, "w", encoding="utf-8") as file:
                        file.write(novo_codigo)

                    messagebox.showinfo("Atualização", "Código atualizado! Reinicie o programa para aplicar as mudanças.")
                    sys.exit()
    except Exception as e:
        messagebox.showerror("Erro", f"Falha ao verificar atualização: {e}")


atualizar_codigo()

def escolher_diretorio():
    diretorio = filedialog.askdirectory()
    if diretorio:
        entry_diretorio.delete(0, tk.END)
        entry_diretorio.insert(0, diretorio)

def verificar_suporte():
    url = entry_url.get()
    if not url:
        suporte_label.config(text="")
        return
    
    try:
        with yt_dlp.YoutubeDL() as ydl:
            info = ydl.extract_info(url, download=False)
            if info:
                suporte_label.config(text="✔", fg="green")
                mostrar_thumbnail(info.get('thumbnail', ''))
                return True
            else:
                suporte_label.config(text="✘", fg="red")
                mostrar_thumbnail(None)
                return False
    except:
        suporte_label.config(text="✘", fg="red")
        mostrar_thumbnail(None)
        return False

def mostrar_thumbnail(url):
    if url:
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            with open('thumbnail.jpg', 'wb') as file:
                file.write(response.content)
            img = Image.open('thumbnail.jpg')
            img = img.resize((160, 90), Image.ANTIALIAS)
            img = ImageTk.PhotoImage(img)
            thumbnail_label.config(image=img)
            thumbnail_label.image = img
    else:
        thumbnail_label.config(image='', text='')

def hook(d):
    if d['status'] == 'downloading':
        progresso = d.get('downloaded_bytes', 0) / d.get('total_bytes', 1) * 100
        progresso_bar['value'] = progresso
        progresso_label.config(text=f"Progresso: {progresso:.2f}%")
        root.update_idletasks()
    elif d['status'] == 'finished':
        progresso_label.config(text="Download concluído!")
        progresso_bar['value'] = 100

def baixar_video():
    url = entry_url.get()
    formato = opcao_formato.get()
    resolucao = opcao_resolucao.get()
    diretorio = entry_diretorio.get()
    
    if not url:
        messagebox.showerror("Erro", "Por favor, insira a URL do vídeo.")
        return
    
    if not diretorio:
        messagebox.showerror("Erro", "Escolha um diretório para salvar o arquivo.")
        return
    
    ydl_opts = {
        'outtmpl': os.path.join(diretorio, '%(title)s.%(ext)s'),
        'quiet': False,
        'no_warnings': False,
        'progress_hooks': [hook],
    }
    
    if formato == "MP3":
        ydl_opts['format'] = 'bestaudio/best'
        ydl_opts['postprocessors'] = [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }]
    elif formato == "MP4":
        ydl_opts['format'] = f'bestvideo[height<={resolucao}]+bestaudio/best[height<={resolucao}]'
        ydl_opts['merge_output_format'] = 'mp4'
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        messagebox.showinfo("Sucesso", "Download concluído!")
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro: {e}")

# Criando a janela principal
root = tk.Tk()
root.title("Video Downloader - Atualizado")
root.geometry("600x600")
root.configure(bg="#2E2E2E")

# Campo para inserir URL
tk.Label(root, text="URL do vídeo:", bg="#2E2E2E", fg="white").pack()
url_frame = tk.Frame(root, bg="#2E2E2E")
url_frame.pack()
entry_url = tk.Entry(url_frame, width=45)
entry_url.pack(side=tk.LEFT)
entry_url.bind("<KeyRelease>", lambda event: verificar_suporte())

suporte_label = tk.Label(url_frame, text="", font=("Arial", 14), bg="#2E2E2E")
suporte_label.pack(side=tk.LEFT, padx=5)

# Exibição da thumbnail
thumbnail_label = tk.Label(root, bg="#2E2E2E")
thumbnail_label.pack()

# Opção de formato
opcao_formato = tk.StringVar(value="MP4")
tk.Label(root, text="Formato:", bg="#2E2E2E", fg="white").pack()
tk.OptionMenu(root, opcao_formato, "MP4", "MP3").pack()

# Opção de resolução
opcao_resolucao = tk.StringVar(value="1080")
tk.Label(root, text="Resolução:", bg="#2E2E2E", fg="white").pack()
tk.OptionMenu(root, opcao_resolucao, "144", "240", "360", "480", "720", "1080").pack()

# Botão para escolher diretório
tk.Label(root, text="Diretório de Download:", bg="#2E2E2E", fg="white").pack()
entry_diretorio = tk.Entry(root, width=50)
entry_diretorio.pack()
tk.Button(root, text="Escolher Diretório", command=escolher_diretorio).pack()

# Barra de progresso
progresso_label = tk.Label(root, text="Progresso: 0%", font=("Arial", 12), bg="#2E2E2E", fg="white")
progresso_label.pack()
progresso_bar = ttk.Progressbar(root, orient="horizontal", length=300, mode="determinate")
progresso_bar.pack()

# Botão de download
tk.Button(root, text="Baixar", command=baixar_video).pack()

root.mainloop()
