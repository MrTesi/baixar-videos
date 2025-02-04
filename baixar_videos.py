import os
import sys
import requests
import hashlib

# 🔹 URL do arquivo no GitHub (Substitua pelo seu link correto)
GITHUB_RAW_URL = "https://raw.githubusercontent.com/MrTesi/baixar-videos/refs/heads/main/baixar_videos.py"

def calcular_hash(conteudo):
    """Calcula um hash SHA256 do conteúdo para comparação precisa."""
    return hashlib.sha256(conteudo.encode("utf-8")).hexdigest()

def atualizar_codigo():
    """Verifica se há uma versão mais recente do código no GitHub e substitui o script local."""
    try:
        print("🔄 Verificando atualizações...")

        # Baixa o código mais recente do GitHub
        response = requests.get(GITHUB_RAW_URL)
        if response.status_code == 200:
            novo_codigo = response.text.strip()

            # Lê o código atual
            with open(__file__, "r", encoding="utf-8") as arquivo:
                codigo_atual = arquivo.read().strip()

            # Compara os hashes dos códigos
            if calcular_hash(novo_codigo) != calcular_hash(codigo_atual):
                with open(__file__, "w", encoding="utf-8") as arquivo:
                    arquivo.write(novo_codigo)
                print("✅ Código atualizado! Reinicie o script para aplicar as mudanças.")
                sys.exit()
            else:
                print("✅ Nenhuma atualização necessária. Código já está atualizado.")
        else:
            print("⚠️ Erro ao verificar atualizações no GitHub.")
    except Exception as e:
        print(f"⚠️ Erro ao atualizar código: {e}")

# 🔹 Executa a verificação de atualização antes de rodar o código principal
atualizar_codigo()

# 🔹 Código principal (exemplo: baixar vídeos do YouTube)
import yt_dlp

def baixar_video_1080p(url, caminho_saida='./'):
    try:
        ydl_opts = {
            'format': 'bestvideo[height<=1080]+bestaudio/best[height<=1080]',
            'outtmpl': f'{caminho_saida}/%(title)s.%(ext)s',
            'quiet': False,
            'no_warnings': False,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print(f"📥 Baixando: {url}...")
            ydl.download([url])
            print("✅ Download concluído!")
    except Exception as e:
        print(f"⚠️ Ocorreu um erro: {e}")

# 🔹 Exemplo de uso
url_video = input("🎥 Cole a URL do vídeo do YouTube: ")
baixar_video_1080p(url_video)
