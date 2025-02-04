import os
import sys
import subprocess
import yt_dlp

def verificar_dependencias():
    """
    Verifica se o yt-dlp está instalado e atualizado.
    Se não estiver instalado, ele será instalado automaticamente.
    Se estiver desatualizado, será atualizado.
    """
    try:
        print("Verificando dependências...")

        # Verifica se o yt-dlp está instalado
        subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "yt-dlp"], check=True)
        print("yt-dlp está instalado e atualizado.")

    except Exception as e:
        print(f"Erro ao verificar dependências: {e}")
        sys.exit(1)

def baixar_video_1080p(url, caminho_saida='./'):
    """
    Baixa um vídeo do YouTube na resolução máxima de 1080p com áudio.
    """
    try:
        # Configurações do yt-dlp
        ydl_opts = {
            'format': 'bestvideo[height<=1080]+bestaudio/best[height<=1080]',
            'outtmpl': f'{caminho_saida}/%(title)s.%(ext)s',
            'quiet': False,
            'no_warnings': False,
        }

        # Baixa o vídeo
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print(f"Baixando: {url}...")
            ydl.download([url])
            print("Download concluído!")
    except Exception as e:
        print(f"Ocorreu um erro ao baixar o vídeo: {e}")

if __name__ == "__main__":
    verificar_dependencias()
    url_video = input("Cole a URL do vídeo do YouTube: ")
    baixar_video_1080p(url_video)
