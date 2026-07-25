# YT Download

Baixador de vídeos e áudios do YouTube com interface web.

## Funcionalidades

- Baixar vídeos individuais (múltiplos links)
- Baixar áudios individuais (converte para MP3)
- Baixar playlists completas (vídeo ou áudio)
- Suporte a cookies do navegador para vídeos com restrição

## Requisitos

- Python 3.9+
- [FFmpeg](https://ffmpeg.org/) instalado e no PATH

## Instalação

```bash
# Clonar o repositório
git clone https://github.com/edgarjp3085/yt-download.git
cd yt-download

# Instalar dependências
pip install -r requirements.txt
```

## Uso

```bash
streamlit run app.py
```

Ou execute `iniciar.bat` no Windows.

## Instalando o FFmpeg

**Windows (Chocolatey):**
```bash
choco install ffmpeg
```

**Ubuntu/Debian:**
```bash
sudo apt install ffmpeg
```

**macOS (Homebrew):**
```bash
brew install ffmpeg
```

## Licença

MIT
