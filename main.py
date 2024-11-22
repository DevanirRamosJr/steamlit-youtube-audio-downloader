import streamlit as st
from pytube.exceptions import RegexMatchError
from streamlit.runtime.media_file_storage import MediaFileStorageError

from youtube_downloader import YoutubeAudioDownloader

yad = YoutubeAudioDownloader()

st.title("Video Audio Donwloader")

left_column, right_column = st.columns([5, 1], vertical_alignment="bottom")

left_column.text_input("Video URL", key="video_url")

if st.session_state.video_url is not None and st.session_state.video_url != "":
    try:
        st.video(st.session_state.video_url)
        if right_column.button(label="Generate Download"):
            _, center_column, _ = st.columns(3, vertical_alignment="center")
            with st.spinner(f"Generating audio file for..."):
                yad.video_audio_download(st.session_state.video_url)
            with st.spinner(f"Generating audio file for...{yad.title} with size {yad.size}mb"):
                audio_content = yad.audio_converter()
            center_column.download_button(label="Download Audio", data=audio_content, file_name=f"{yad.title}.mp3", mime="audio/mpeg")
            #yad.clean_routine()
    except (MediaFileStorageError, RegexMatchError):
        st.error("Not a valid video URL")
