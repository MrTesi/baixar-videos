import yt_dlp

def baixar_video_1080p(url, caminho_saida='./'):
    try:
        # Configurações do yt-dlp
        ydl_opts = {
            'format': 'bestvideo[height<=1080]+bestaudio/best[height<=1080]',  # Baixa o vídeo em 1080p
            'outtmpl': f'{caminho_saida}/%(title)s.%(ext)s',  # Define o nome do arquivo de saída
            'quiet': False,  # Exibe informações no terminal
            'no_warnings': False,  # Exibe avisos
        }

        # Baixa o vídeo
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print(f"📥 Baixando: {url}...")
            ydl.download([url])
            print("✅ Download concluído!")
    except Exception as e:
        print(f"⚠️ Ocorreu um erro: {e}")

# Exemplo de uso
url_video = input("🎥 Cole a URL do vídeo do YouTube: ")
baixar_video_1080p(url_video)
