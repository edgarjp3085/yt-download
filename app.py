import streamlit as st
import yt_dlp
import os

DOWNLOAD_FOLDER = './downloads'
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

st.set_page_config(page_title="YT Download", page_icon="⬇️", layout="centered")


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


def download_video(link, output_path, index, use_cookies=False, browser='chrome'):
    try:
        ydl_opts = {
            **get_ydl_opts_base(use_cookies, browser),
            'format': 'best',
            'outtmpl': os.path.join(output_path, f'{index} - %(title)s.%(ext)s'),
            'noplaylist': True,
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(link, download=True)
        return info_dict.get('title', 'Video'), None
    except Exception as e:
        return None, str(e)


def download_audio(link, output_path, index, use_cookies=False, browser='chrome'):
    try:
        ydl_opts = {
            **get_ydl_opts_base(use_cookies, browser),
            'format': 'bestaudio[ext=m4a]/bestaudio[ext=mp3]/bestaudio',
            'outtmpl': os.path.join(output_path, f'{index} - %(title)s.%(ext)s'),
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'prefer_ffmpeg': True,
            'keepvideo': False,
            'noplaylist': True,
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(link, download=True)
        return info_dict.get('title', 'Audio'), None
    except Exception as e:
        return None, str(e)


def download_playlist(playlist_url, output_path, download_audio=False, use_cookies=False, browser='chrome'):
    try:
        base = get_ydl_opts_base(use_cookies, browser)
        if download_audio:
            ydl_opts = {
                **base,
                'format': 'bestaudio[ext=m4a]/bestaudio[ext=mp3]/bestaudio',
                'outtmpl': os.path.join(output_path, '%(playlist_index)s - %(title)s.%(ext)s'),
                'noplaylist': False,
                'ignoreerrors': True,
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'prefer_ffmpeg': True,
                'keepvideo': False,
            }
        else:
            ydl_opts = {
                **base,
                'format': 'best',
                'outtmpl': os.path.join(output_path, '%(playlist_index)s - %(title)s.%(ext)s'),
                'noplaylist': False,
                'ignoreerrors': True,
            }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(playlist_url, download=True)
        return info_dict.get('title', 'Playlist'), None
    except Exception as e:
        return None, str(e)


st.title("⬇️ YT Download")
st.caption("Baixe vídeos e áudios do YouTube")

with st.sidebar:
    st.markdown("### ⚙️ Configurações")
    use_cookies = st.checkbox("Usar cookies do navegador", value=False)
    browser = st.selectbox(
        "Navegador",
        ["chrome", "firefox", "edge", "brave", "opera"],
        disabled=not use_cookies,
    )
    st.caption("Ative se aparecer erro de vídeo indisponível. Requer estar logado no navegador.")
    st.divider()
    st.markdown("### 📋 Requisitos")
    st.code("choco install ffmpeg", language="bash")

option = st.selectbox(
    "Escolha uma opção",
    ["Baixar Vídeos", "Baixar Áudios", "Baixar Playlist"]
)

if option == "Baixar Vídeos":
    links = st.text_area("Cole os links dos vídeos (um por linha)")
    if st.button('⬇️ Baixar Vídeos', use_container_width=True):
        if links:
            links_list = [l.strip() for l in links.split('\n') if l.strip()]
            progress = st.progress(0, text="Baixando...")
            results = []
            for i, link in enumerate(links_list):
                progress.progress((i) / len(links_list), text=f"Baixando {i+1}/{len(links_list)}...")
                title, error = download_video(link, DOWNLOAD_FOLDER, i+1, use_cookies, browser)
                if error:
                    results.append(("❌", link, error))
                else:
                    results.append(("✅", link, title))
            progress.progress(1.0, text="Concluído!")
            st.divider()
            for icon, link, msg in results:
                st.write(f"{icon} **{msg}** — {link}")
        else:
            st.warning("Cole os links dos vídeos no campo acima.")

elif option == "Baixar Áudios":
    links = st.text_area("Cole os links dos vídeos (um por linha)")
    if st.button('⬇️ Baixar Áudios', use_container_width=True):
        if links:
            links_list = [l.strip() for l in links.split('\n') if l.strip()]
            progress = st.progress(0, text="Baixando...")
            results = []
            for i, link in enumerate(links_list):
                progress.progress((i) / len(links_list), text=f"Baixando {i+1}/{len(links_list)}...")
                title, error = download_audio(link, DOWNLOAD_FOLDER, i+1, use_cookies, browser)
                if error:
                    results.append(("❌", link, error))
                else:
                    results.append(("✅", link, title))
            progress.progress(1.0, text="Concluído!")
            st.divider()
            for icon, link, msg in results:
                st.write(f"{icon} **{msg}** — {link}")
        else:
            st.warning("Cole os links dos vídeos no campo acima.")

elif option == "Baixar Playlist":
    download_option = st.radio("Formato:", ["Vídeos", "Áudios"], horizontal=True)
    playlist_url = st.text_input("Cole o link da playlist")
    if st.button('⬇️ Baixar Playlist', use_container_width=True):
        if playlist_url:
            with st.spinner("Baixando playlist..."):
                title, error = download_playlist(
                    playlist_url, DOWNLOAD_FOLDER,
                    download_audio=(download_option == "Áudios"),
                    use_cookies=use_cookies,
                    browser=browser,
                )
            if error:
                st.error(f"Erro: {error}")
            else:
                st.success(f"Playlist baixada: {title}")
        else:
            st.warning("Cole o link da playlist no campo acima.")
