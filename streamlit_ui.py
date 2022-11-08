import streamlit as st
import streamlit_functions as functions
import streamlit_vertical_slider as svs
import librosa
import wave
import numpy as np
import scipy.fft as fft
import plotly.express as px

# ---------------------- Websites Options -------------------------------- #
st.set_page_config(page_title="Equalizer",layout="wide",page_icon="🎚",initial_sidebar_state="expanded")

# ---------------------- Elements Styling -------------------------------- #
with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# ---------------------- Declaring Variables State ----------------------- #
if "play_state" not in st.session_state:
    st.session_state["play_state"] = False

# ---------------------- Uploading Files --------------------------------- #

st.sidebar.markdown("# Upload")
uploaded_file = st.sidebar.file_uploader("uploader",key="uploaded_file",label_visibility="hidden",type="wav")


if st.session_state["uploaded_file"]:
# ---------------------- Play/Pause Audio -------------------------------- #

    st.sidebar.audio(st.session_state["uploaded_file"],"wav")

# ---------------------- Sliders ----------------------------------------- #

    columns = st.columns(10)
    for column in columns:
        with column:
            svs.vertical_slider(key = f"slider{columns.index(column)}", 
                                min_value=-100,
                                max_value=100,
                                step=1,
                                default_value=0,
                                thumb_color="#2481ce",
                                slider_color="#061724",
                                track_color="lightgray")

# -----------------------line break -------------------------------------- #
    st.markdown("***")
# ---------------------- Plots ------------------------------------------- #

    signal_plot_col, spectrogram_col = st.columns(2)
    with signal_plot_col:
        audio         = wave.open(st.session_state["uploaded_file"], 'rb')
        sample_rate = audio.getframerate()
        n_samples   = audio.getnframes()
        duration    = n_samples / sample_rate
        signal_wave = audio.readframes(-1)

        signal_y_axis = np.frombuffer(signal_wave, dtype=np.int16)
        signal_x_axis = np.arange(0,duration,1/(2*sample_rate))

        yf = fft.rfft(signal_y_axis)
        xf = fft.rfftfreq(round(sample_rate*duration),1/sample_rate)

        modified_signal = fft.irfft(yf)

        modified_signal_channel = np.int16(modified_signal * (32767 / modified_signal.max()))

        fig = px.line(x = signal_x_axis,y = signal_y_axis)
        fig['data'][0]['showlegend'] = True
        fig['data'][0]['name'] = 'Original'
        fig.add_scatter(name="Modified", x=signal_x_axis,y=modified_signal, line_color="#FF4B4B",visible="legendonly")
        fig.update_layout(showlegend=True, margin=dict(l=0, r=0, t=0, b=0), legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01))
        fig.update_xaxes(title="Time",showline=True, linewidth=2, linecolor='black',gridcolor='#5E5E5E', title_font=dict(size=24, family='Arial'))
        fig.update_yaxes(title="Amplitude",showline=True, linewidth=2, linecolor='black',gridcolor='#5E5E5E', title_font=dict(size=24, family='Arial'))
        st.plotly_chart(fig,use_container_width=True)
    with spectrogram_col:
        st.plotly_chart(fig,use_container_width=True)
