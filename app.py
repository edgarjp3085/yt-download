import streamlit as st
import yt_dlp
import os
import time
from datetime import datetime

DOWNLOAD_FOLDER = './downloads'
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

st.set_page_config(page_title="YT Download", page_icon="⬇️", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    * { font-family: 'Inter', sans-serif !important; }

    /* não sobrescrever a fonte de ícones (Material Symbols), senão o
       botão de abrir/fechar a sidebar e outros ícones viram texto cru */
    [data-testid="stIconMaterial"],
    [data-testid="stIconMaterial"] *,
    [data-testid="baseButton-headerNoPadding"] span,
    span[class*="material-icons"],
    span[class*="material-symbols"] {
        font-family: 'Material Symbols Rounded', 'Material Icons' !important;
    }

    .stApp { background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%); }

    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem 2.5rem;
        border-radius: 16px;
        margin-bottom: 2rem;
        box-shadow: 0 10px 40px rgba(102, 126, 234, 0.3);
    }
    .main-header h1 {
        color: white !important;
        font-size: 2.2rem !important;
        font-weight: 700 !important;
        margin: 0 !important;
    }
    .main-header p {
        color: rgba(255,255,255,0.8) !important;
        font-size: 1rem !important;
        margin: 0.3rem 0 0 0 !important;
    }

    /* ===== SIDEBAR ===== */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #17142b 0%, #201c3d 100%) !important;
        border-right: 1px solid rgba(255,255,255,0.08);
    }
    section[data-testid="stSidebar"] > div {
        padding-top: 1.5rem;
    }
    section[data-testid="stSidebar"] * {
        color: rgba(255,255,255,0.85) !important;
    }
    section[data-testid="stSidebar"] h3 {
        color: #fff !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
        letter-spacing: 0.3px;
    }
    section[data-testid="stSidebar"] hr {
        border-color: rgba(255,255,255,0.1) !important;
        margin: 1.2rem 0 !important;
    }

    /* checkbox */
    section[data-testid="stSidebar"] div[data-testid="stCheckbox"] label span {
        color: rgba(255,255,255,0.85) !important;
    }

    /* selectbox */
    section[data-testid="stSidebar"] div[data-testid="stSelectbox"] > div {
        background: rgba(255,255,255,0.06) !important;
        border: 1px solid rgba(255,255,255,0.12) !important;
        border-radius: 10px !important;
        color: #fff !important;
    }
    section[data-testid="stSidebar"] div[data-testid="stSelectbox"] svg {
        fill: rgba(255,255,255,0.7) !important;
    }

    /* metric cards */
    section[data-testid="stSidebar"] div[data-testid="stMetric"] {
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 12px;
        padding: 0.8rem 0.5rem;
        text-align: center;
    }
    section[data-testid="stSidebar"] div[data-testid="stMetricValue"] {
        color: #fff !important;
        font-weight: 700 !important;
    }
    section[data-testid="stSidebar"] div[data-testid="stMetricLabel"] {
        color: rgba(255,255,255,0.55) !important;
        font-size: 0.75rem !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    /* info box */
    section[data-testid="stSidebar"] div[data-testid="stAlert"] {
        background: rgba(102,126,234,0.15) !important;
        border: 1px solid rgba(102,126,234,0.3) !important;
        border-radius: 10px !important;
    }
    section[data-testid="stSidebar"] div[data-testid="stAlert"] * {
        color: rgba(255,255,255,0.9) !important;
    }

    /* expander */
    section[data-testid="stSidebar"] details {
        background: rgba(255,255,255,0.04) !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
        border-radius: 10px !important;
    }
    section[data-testid="stSidebar"] summary {
        color: rgba(255,255,255,0.85) !important;
    }
    section[data-testid="stSidebar"] summary svg {
        fill: rgba(255,255,255,0.7) !important;
    }

    /* code block */
    section[data-testid="stSidebar"] pre, section[data-testid="stSidebar"] code {
        background: rgba(0,0,0,0.35) !important;
        color: #a5d6ff !important;
        border-radius: 8px !important;
    }

    /* caption */
    section[data-testid="stSidebar"] [data-testid="stCaptionContainer"] {
        color: rgba(255,255,255,0.55) !important;
    }
    /* botão de abrir a sidebar quando ela está fechada (fica sobre o fundo escuro) */
    [data-testid="stSidebarCollapsedControl"] button,
    [data-testid="stSidebarCollapsedControl"] svg,
    [data-testid="stSidebarCollapsedControl"] span {
        color: rgba(255,255,255,0.85) !important;
        fill: rgba(255,255,255,0.85) !important;
    }
    /* botão de fechar a sidebar (dentro dela) */
    [data-testid="stSidebar"] [data-testid="baseButton-headerNoPadding"] svg,
    [data-testid="stSidebar"] [data-testid="baseButton-headerNoPadding"] span {
        color: rgba(255,255,255,0.85) !important;
        fill: rgba(255,255,255,0.85) !important;
    }
    /* ===== FIM SIDEBAR ===== */

    .feature-card {
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 16px;
        padding: 1.5rem;
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
        height: 100%;
    }
    .feature-card:hover {
        border-color: rgba(102, 126, 234, 0.5);
        box-shadow: 0 8px 32px rgba(102, 126, 234, 0.2);
        transform: translateY(-2px);
    }
    .feature-card h3 { color: #fff !important; font-size: 1.1rem !important; margin-bottom: 0.5rem !important; }
    .feature-card p { color: rgba(255,255,255,0.6) !important; font-size: 0.85rem !important; }

    .stat-card {
        background: linear-gradient(135deg, rgba(102,126,234,0.15) 0%, rgba(118,75,162,0.15) 100%);
        border: 1px solid rgba(102,126,234,0.2);
        border-radius: 12px;
        padding: 1.2rem;
        text-align: center;
    }
    .stat-card .stat-number {
        font-size: 1.8rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea, #764ba2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .stat-card .stat-label {
        color: rgba(255,255,255,0.5);
        font-size: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    .success-card {
        background: linear-gradient(135deg, rgba(0,210,106,0.1) 0%, rgba(0,180,90,0.1) 100%);
        border: 1px solid rgba(0,210,106,0.3);
        border-radius: 12px;
        padding: 1rem 1.5rem;
        margin: 0.5rem 0;
    }
    .error-card {
        background: linear-gradient(135deg, rgba(255,71,87,0.1) 0%, rgba(255,50,60,0.1) 100%);
        border: 1px solid rgba(255,71,87,0.3);
        border-radius: 12px;
        padding: 1rem 1.5rem;
        margin: 0.5rem 0;
    }

    .download-item {
        background: rgba(255,255,255,0.03);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
        display: flex;
        align-items: center;
        gap: 1rem;
    }

    .quality-badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    div[data-testid="stButton"] > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.8rem 2rem !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        width: 100% !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 20px rgba(102, 126, 234, 0.3) !important;
    }
    div[data-testid="stButton"] > button:hover {
        box-shadow: 0 6px 30px rgba(102, 126, 234, 0.5) !important;
        transform: translateY(-2px) !important;
    }

    div[data-testid="stTextInput"] > div > div > input,
    div[data-testid="stTextArea"] > div > div > textarea {
        background: rgba(255,255,255,0.05) !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
        border-radius: 10px !important;
        color: white !important;
    }
    div[data-testid="stTextInput"] > div > div > input:focus,
    div[data-testid="stTextArea"] > div > div > textarea:focus {
        border-color: #667eea !important;
        box-shadow: 0 0 0 2px rgba(102,126,234,0.2) !important;
    }

    div[data-testid="stSelectbox"] > div > div {
        background: rgba(255,255,255,0.05) !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
        border-radius: 10px !important;
        color: white !important;
    }

    div[data-testid="stRadio"] > div { gap: 0.5rem !important; }
    div[data-testid="stRadio"] > div > label {
        background: rgba(255,255,255,0.05) !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
        border-radius: 10px !important;
        padding: 0.6rem 1rem !important;
    }
    div[data-testid="stRadio"] > div > label[data-checked="true"] {
        background: linear-gradient(135deg, rgba(102,126,234,0.2), rgba(118,75,162,0.2)) !important;
        border-color: #667eea !important;
    }

    .stTabs [data-baseweb="tab-list"] { gap: 0.5rem !important; }
    .stTabs [data-baseweb="tab"] {
        background: rgba(255,255,255,0.05) !important;
        border-radius: 10px !important;
        border: 1px solid rgba(255,255,255,0.08) !important;
        padding: 0.6rem 1.5rem !important;
        color: rgba(255,255,255,0.6) !important;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border-color: transparent !important;
    }

    .progress-bar > div > div {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
    }

    footer { text-align: center; padding: 2rem; color: rgba(255,255,255,0.3); font-size: 0.8rem; }
</style>
""", unsafe_allow_html=True)


def get_ydl_opts_base(use_cookies=False, browser='chrome'):
    opts = {
        'retries': 10,
        'retry_sleep': 10,
        'socket_timeout': 60,
        'extractor_args': {
            'youtube': {
                'player_client': ['android', 'ios', 'web'],
            }
        },
    }
    if use_cookies:
        opts['cookiesfrombrowser'] = (browser,)
    return opts


def get_video_info(url, use_cookies=False, browser='chrome'):
    try:
        opts = {**get_ydl_opts_base(use_cookies, browser), 'skip_download': True}
        with yt_dlp.YoutubeDL(opts) as ydl:
            info = ydl.extract_info(url, download=False)
        return info, None
    except Exception as e:
        return None, str(e)


def download_video(link, output_path, index, quality='best', use_cookies=False, browser='chrome'):
    try:
        fmt = {'best': 'best', '1080': 'bestvideo[height<=1080]+bestaudio/best[height<=1080]', '720': 'bestvideo[height<=720]+bestaudio/best[height<=720]', '480': 'bestvideo[height<=480]+bestaudio/best[height<=480]'}.get(quality, 'best')
        ydl_opts = {
            **get_ydl_opts_base(use_cookies, browser),
            'format': fmt,
            'outtmpl': os.path.join(output_path, f'{index} - %(title)s.%(ext)s'),
            'merge_output_format': 'mp4',
            'noplaylist': True,
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(link, download=True)
        return info_dict.get('title', 'Video'), info_dict.get('thumbnail'), info_dict.get('duration'), None
    except Exception as e:
        return None, None, None, str(e)


def download_audio(link, output_path, index, audio_quality='192', use_cookies=False, browser='chrome'):
    try:
        ydl_opts = {
            **get_ydl_opts_base(use_cookies, browser),
            'format': 'bestaudio[ext=m4a]/bestaudio[ext=mp3]/bestaudio',
            'outtmpl': os.path.join(output_path, f'{index} - %(title)s.%(ext)s'),
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': audio_quality,
            }],
            'prefer_ffmpeg': True,
            'keepvideo': False,
            'noplaylist': True,
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(link, download=True)
        return info_dict.get('title', 'Audio'), info_dict.get('thumbnail'), info_dict.get('duration'), None
    except Exception as e:
        return None, None, None, str(e)


def download_playlist(playlist_url, output_path, download_audio=False, quality='best', audio_quality='192', use_cookies=False, browser='chrome'):
    try:
        base = get_ydl_opts_base(use_cookies, browser)
        if download_audio:
            ydl_opts = {
                **base,
                'format': 'bestaudio[ext=m4a]/bestaudio[ext=mp3]/bestaudio',
                'outtmpl': os.path.join(output_path, '%(playlist_index)s - %(title)s.%(ext)s'),
                'noplaylist': False,
                'ignoreerrors': True,
                'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': audio_quality}],
                'prefer_ffmpeg': True,
                'keepvideo': False,
            }
        else:
            fmt = {'best': 'best', '1080': 'bestvideo[height<=1080]+bestaudio/best[height<=1080]', '720': 'bestvideo[height<=720]+bestaudio/best[height<=720]', '480': 'bestvideo[height<=480]+bestaudio/best[height<=480]'}.get(quality, 'best')
            ydl_opts = {
                **base,
                'format': fmt,
                'outtmpl': os.path.join(output_path, '%(playlist_index)s - %(title)s.%(ext)s'),
                'noplaylist': False,
                'ignoreerrors': True,
                'merge_output_format': 'mp4',
            }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(playlist_url, download=True)
        return info_dict.get('title', 'Playlist'), info_dict.get('entries', []), None
    except Exception as e:
        return None, [], str(e)


def format_duration(seconds):
    if not seconds: return "--:--"
    h, r = divmod(int(seconds), 3600)
    m, s = divmod(r, 60)
    return f"{h:02d}:{m:02d}:{s:02d}" if h else f"{m:02d}:{s:02d}"


def format_views(views):
    if not views: return "N/A"
    if views >= 1_000_000: return f"{views/1_000_000:.1f}M"
    if views >= 1_000: return f"{views/1_000:.1f}K"
    return str(views)


if 'history' not in st.session_state:
    st.session_state.history = []
if 'total_downloads' not in st.session_state:
    st.session_state.total_downloads = 0


with st.sidebar:
    st.markdown("### ⚙️ Configurações")
    use_cookies = st.checkbox("🍪 Usar cookies do navegador", value=False)
    browser = st.selectbox("Navegador", ["chrome", "firefox", "edge", "brave", "opera"], disabled=not use_cookies, index=0)
    if use_cookies:
        st.info("Requer estar logado no navegador selecionado.")

    st.divider()

    st.markdown("### 📊 Estatísticas")
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="Downloads", value=st.session_state.total_downloads)
    with col2:
        st.metric(label="Arquivos", value=len(st.session_state.history))

    st.divider()

    st.markdown("### 📋 Requisitos")
    st.caption("FFmpeg necessário para conversão de áudio")
    with st.expander("Instalar FFmpeg"):
        st.code("# Windows\nchoco install ffmpeg\n\n# Ubuntu\nsudo apt install ffmpeg\n\n# macOS\nbrew install ffmpeg", language="bash")


st.markdown("""
<div class="main-header">
    <h1>⬇️ YT Download</h1>
    <p>Baixe vídeos e áudios do YouTube com qualidade e estilo</p>
</div>
""", unsafe_allow_html=True)


col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("""<div class="feature-card"><h3>🎬 Vídeos</h3><p>Baixe em até 1080p com qualidade selecionável</p></div>""", unsafe_allow_html=True)
with col2:
    st.markdown("""<div class="feature-card"><h3>🎵 Áudios</h3><p>Extraia e converta para MP3 em alta qualidade</p></div>""", unsafe_allow_html=True)
with col3:
    st.markdown("""<div class="feature-card"><h3>📑 Playlists</h3><p>Baixe playlists completas de uma vez</p></div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)


tab1, tab2, tab3 = st.tabs(["🎬 Baixar Vídeos", "🎵 Baixar Áudios", "📑 Baixar Playlist"])


with tab1:
    col_a, col_b = st.columns([3, 2])

    with col_a:
        links = st.text_area("Cole os links dos vídeos (um por linha)", height=150, key="video_links", placeholder="https://www.youtube.com/watch?v=...\nhttps://youtu.be/...")
        quality = st.selectbox("Qualidade do vídeo", ["Melhor", "1080p", "720p", "480p"], key="video_quality")

    with col_b:
        preview_url = st.text_input("Preview rápido", key="preview_url", placeholder="Cole um link para ver detalhes...")
        if preview_url:
            info, err = get_video_info(preview_url, use_cookies, browser)
            if info:
                thumb = info.get('thumbnail', '')
                if thumb:
                    st.image(thumb, use_container_width=True, caption="")
                st.markdown(f"**{info.get('title', 'Sem título')}**")
                meta_col1, meta_col2, meta_col3 = st.columns(3)
                with meta_col1:
                    st.caption(f"⏱️ {format_duration(info.get('duration'))}")
                with meta_col2:
                    st.caption(f"👁️ {format_views(info.get('view_count'))} views")
                with meta_col3:
                    uploader = info.get('uploader', 'N/A')
                    st.caption(f"👤 {uploader[:15]}")
            elif err:
                st.error(f"Erro: {err}")

    if st.button('⬇️ Baixar Vídeos', key="btn_video", use_container_width=True):
        if links:
            links_list = [l.strip() for l in links.split('\n') if l.strip()]
            q = {'Melhor': 'best', '1080p': '1080', '720p': '720', '480p': '480'}[quality]
            progress = st.progress(0, text="Preparando...")
            status_area = st.container()

            for i, link in enumerate(links_list):
                progress.progress((i) / len(links_list), text=f"Baixando {i+1}/{len(links_list)}...")
                title, thumb, duration, error = download_video(link, DOWNLOAD_FOLDER, i+1, q, use_cookies, browser)
                with status_area:
                    if error:
                        st.markdown(f"""<div class="error-card">❌ <strong>Erro:</strong> {error[:80]}</div>""", unsafe_allow_html=True)
                    else:
                        st.session_state.history.append({"title": title, "type": "video", "time": datetime.now().strftime("%H:%M")})
                        st.session_state.total_downloads += 1
                        st.markdown(f"""<div class="success-card">✅ <strong>{title[:60]}</strong> ({format_duration(duration)})</div>""", unsafe_allow_html=True)
            progress.progress(1.0, text="Concluído!")
        else:
            st.warning("Cole pelo menos um link.")


with tab2:
    col_a, col_b = st.columns([3, 2])

    with col_a:
        links = st.text_area("Cole os links dos vídeos (um por linha)", height=150, key="audio_links", placeholder="https://www.youtube.com/watch?v=...\nhttps://youtu.be/...")
        audio_quality = st.selectbox("Qualidade do áudio", ["128 kbps", "192 kbps", "256 kbps", "320 kbps"], key="audio_quality")

    with col_b:
        preview_url = st.text_input("Preview rápido", key="preview_url_audio", placeholder="Cole um link para ver detalhes...")
        if preview_url:
            info, err = get_video_info(preview_url, use_cookies, browser)
            if info:
                thumb = info.get('thumbnail', '')
                if thumb:
                    st.image(thumb, use_container_width=True, caption="")
                st.markdown(f"**{info.get('title', 'Sem título')}**")
                meta_col1, meta_col2 = st.columns(2)
                with meta_col1:
                    st.caption(f"⏱️ {format_duration(info.get('duration'))}")
                with meta_col2:
                    st.caption(f"👤 {info.get('uploader', 'N/A')[:15]}")
            elif err:
                st.error(f"Erro: {err}")

    if st.button('⬇️ Baixar Áudios', key="btn_audio", use_container_width=True):
        if links:
            links_list = [l.strip() for l in links.split('\n') if l.strip()]
            aq = audio_quality.split()[0]
            progress = st.progress(0, text="Preparando...")
            status_area = st.container()

            for i, link in enumerate(links_list):
                progress.progress((i) / len(links_list), text=f"Baixando {i+1}/{len(links_list)}...")
                title, thumb, duration, error = download_audio(link, DOWNLOAD_FOLDER, i+1, aq, use_cookies, browser)
                with status_area:
                    if error:
                        st.markdown(f"""<div class="error-card">❌ <strong>Erro:</strong> {error[:80]}</div>""", unsafe_allow_html=True)
                    else:
                        st.session_state.history.append({"title": title, "type": "audio", "time": datetime.now().strftime("%H:%M")})
                        st.session_state.total_downloads += 1
                        st.markdown(f"""<div class="success-card">🎵 <strong>{title[:60]}</strong> ({format_duration(duration)})</div>""", unsafe_allow_html=True)
            progress.progress(1.0, text="Concluído!")
        else:
            st.warning("Cole pelo menos um link.")


with tab3:
    col_a, col_b = st.columns([3, 2])

    with col_a:
        playlist_url = st.text_input("Link da playlist", key="playlist_url", placeholder="https://www.youtube.com/playlist?list=...")
        dl_format = st.radio("Formato", ["Vídeos", "Áudios"], horizontal=True, key="pl_format")

        if dl_format == "Vídeos":
            quality = st.selectbox("Qualidade", ["Melhor", "1080p", "720p", "480p"], key="pl_quality")
        else:
            audio_quality = st.selectbox("Qualidade do áudio", ["128 kbps", "192 kbps", "256 kbps", "320 kbps"], key="pl_audio_quality")

    with col_b:
        preview_url = st.text_input("Preview rápido", key="preview_url_pl", placeholder="Cole o link da playlist...")
        if preview_url:
            info, err = get_video_info(preview_url, use_cookies, browser)
            if info:
                entries = info.get('entries', [])
                st.markdown(f"**{info.get('title', 'Playlist')}**")
                st.caption(f"📋 {len(entries)} vídeos")
                st.markdown("---")
                for entry in entries[:5]:
                    if entry:
                        st.caption(f"▶ {entry.get('title', 'Video')[:40]} ({format_duration(entry.get('duration'))})")
                if len(entries) > 5:
                    st.caption(f"... e mais {len(entries)-5} vídeos")
            elif err:
                st.error(f"Erro: {err}")

    if st.button('⬇️ Baixar Playlist', key="btn_playlist", use_container_width=True):
        if playlist_url:
            da = dl_format == "Áudios"
            aq = audio_quality.split()[0] if da else None
            q = {'Melhor': 'best', '1080p': '1080', '720p': '720', '480p': '480'}.get(quality if not da else 'Melhor', 'best')

            with st.spinner("Carregando playlist..."):
                title, entries, error = download_playlist(playlist_url, DOWNLOAD_FOLDER, da, q, aq, use_cookies, browser)

            if error:
                st.error(f"Erro: {error}")
            else:
                st.session_state.history.append({"title": title, "type": "playlist", "time": datetime.now().strftime("%H:%M")})
                st.session_state.total_downloads += 1
                st.success(f"Playlist baixada: {title}")
        else:
            st.warning("Cole o link da playlist.")


if st.session_state.history:
    st.markdown("---")
    with st.expander("📜 Histórico de Downloads", expanded=False):
        for item in reversed(st.session_state.history[-10:]):
            icon = "🎬" if item["type"] == "video" else "🎵" if item["type"] == "audio" else "📑"
            st.caption(f"{icon} {item['title'][:50]} — {item['time']}")


st.markdown("""
<footer>
    <p>YT Download © 2026 | Feito com Streamlit + yt-dlp</p>
</footer>
""", unsafe_allow_html=True)