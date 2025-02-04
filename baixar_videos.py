import os
import sys
import subprocess
import requests

# URL do código atualizado no GitHub
GITHUB_RAW_URL = "https://raw.githubusercontent.com/SEU_USUARIO/baixar_videos_youtube/main/baixar_videos.py"

def atualizar_codigo():
    """
    Verifica se há uma versão mais recente do código no GitHub e substitui o script local.
    """
    try:
        print("Verificando atualizações...")

        response = requests.get(GITHUB_RAW_URL)
        if response.status_code == 200:
            novo_codigo = response.text

            # Lê o código atual
            with open(__file__, "r", encoding="utf-8") as arquivo:
                codigo_atual = arquivo.read()

            # Se houver diferença, atualiza
            if novo_codigo.strip() != codigo_atual.strip():
                with open(__file__, "w", encoding="utf-8") as arquivo:
                    arquivo.write(novo_codigo)
                print("Código atualizado! Reinicie o script para aplicar as mudanças.")
                sys.exit()
            else:
                print("Nenhuma atualização encontrada.")
        else:
            print("Falha ao verificar atualizações.")
    except Exception as e:
        print(f"Erro ao atualizar código: {e}")

def verificar_dependencias():
    """
    Verifica se o yt-dlp está instalado e atualizado.
    """
    try:
        print("Verificando dependências...")
        subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "yt-dlp", "requests"], check=True)
        print("Dependências verificadas!")
    except Exception as e:
        print(f"Erro ao verificar dependências: {e}")
        sys.exit(1)

def baixar_video_1080p(url, caminho_saida='./'):
    """
    Baixa um vídeo do YouTube na resolução máxima de 1080p com áudio.
    """
    try:
        ydl_opts = {
            'format': 'bestvideo[height<=1080]+bestaudio/best[height<=1080]',
            'outtmpl': f'{caminho_saida}/%(title)s.%(ext)s',
            'quiet': False,
            'no_warnings': False,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print(f"Baixando: {url}...")
            ydl.download([url])
            print("Download concluído!")
    except Exception as e:
        print(f"Ocorreu um erro ao baixar o vídeo: {e}")

if __name__ == "__main__":
    atualizar_codigo()
    verificar_dependencias()
    url_video = input("Cole a URL do vídeo do YouTube: ")
    baixar_video_1080p(url_video)
