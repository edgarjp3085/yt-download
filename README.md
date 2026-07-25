# ⬇️ YT Download

Baixador de vídeos e áudios do YouTube com interface moderna e elegante.

![Interface](https://img.shields.io/badge/Interface-Modern-dark?style=for-the-badge&color=667eea)
![Python](https://img.shields.io/badge/Python-3.9+-blue?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.30+-red?style=for-the-badge&logo=streamlit&logoColor=white)

---

## ✨ Funcionalidades

| Feature | Descrição |
|---------|-----------|
| 🎬 **Vídeos** | Baixe em até 1080p com seleção de qualidade |
| 🎵 **Áudios** | Extraia e converta para MP3 (128-320 kbps) |
| 📑 **Playlists** | Baixe playlists completas de uma vez |
| 👁️ **Preview** | Veja thumbnail, duração e views antes de baixar |
| 📜 **Histórico** | Acompanhe seus downloads recentes |
| 🍪 **Cookies** | Suporte a vídeos com restrição de idade |
| 🎨 **UI Moderna** | Interface com gradientes, cards e animações |
| 📊 **Estatísticas** | Contador de downloads em tempo real |

---

## 🚀 Instalação

### Pré-requisitos

- Python 3.9+
- [FFmpeg](https://ffmpeg.org/) instalado e no PATH

### Passo a passo

```bash
# Clone o repositório
git clone https://github.com/edgarjp3085/yt-download.git
cd yt-download

# Instale as dependências
pip install -r requirements.txt

# Execute o app
streamlit run app.py
```

Ou execute `iniciar.bat` no Windows (instala dependências automaticamente).

---

## 🎨 Interface

O app possui um design moderno com:

- **Tema escuro** com gradientes roxos
- **Cards** com efeitos de hover
- **Preview** de vídeos com thumbnail
- **Barra de progresso** em tempo real
- **Layout responsivo** com abas

---

## 📋 Uso

1. **Baixar Vídeos**: Cole os links (um por linha), selecione a qualidade e clique em baixar
2. **Baixar Áudios**: Cole os links, escolha o bitrate (128-320 kbps) e extraia o áudio
3. **Baixar Playlists**: Cole o link da playlist, escolha entre vídeo ou áudio

### Dicas

- Use o **Preview rápido** para verificar o vídeo antes de baixar
- Ative **Cookies do navegador** se encontrar erro de restrição
- A barra lateral mostra suas **estatísticas** de download

---

## 🔧 Instalando o FFmpeg

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

---

## 📁 Estrutura

```
yt-download/
├── app.py              # Aplicação principal
├── requirements.txt    # Dependências Python
├── iniciar.bat         # Iniciador Windows
├── .gitignore          # Arquivos ignorados
├── .streamlit/
│   └── config.toml     # Configuração do tema
└── README.md           # Este arquivo
```

---

## 🛠️ Tecnologias

- **Python** - Linguagem principal
- **Streamlit** - Interface web
- **yt-dlp** - Download do YouTube
- **FFmpeg** - Conversão de áudio

---

## 📄 Licença

MIT License - veja o arquivo [LICENSE](LICENSE) para mais detalhes.

---

## 👤 Autor

**Edgar Pereira** - [GitHub](https://github.com/edgarjp3085)
