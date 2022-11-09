import streamlit as st
import streamlit_functions as functions
import streamlit_vertical_slider as svs
import plotly.express as px

# ---------------------- Websites Options -------------------------------- #
st.set_page_config(page_title="Equalizer",layout="wide",page_icon="🎚",initial_sidebar_state="expanded")

# ---------------------- Elements Styling -------------------------------- #
with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# ---------------------- Uploading Files --------------------------------- #

uploaded_file = st.sidebar.file_uploader("uploader",key="uploaded_file",label_visibility="hidden",type="wav")

# ---------------------- Original Audio ---------------------------------- #

st.sidebar.markdown("# Original Signal")
st.sidebar.audio(st.session_state["uploaded_file"] if st.session_state["uploaded_file"] else None,"wav")

# ---------------------- Sliders ----------------------------------------- #

columns = st.columns(10)
for column in columns:
    if f"slider{columns.index(column)+1}" not in st.session_state:
        st.session_state[f"slider{columns.index(column)+1}"] = 1

for column in columns:
    with column:
        svs.vertical_slider(key = f"slider{columns.index(column)+1}", 
                            min_value=0,
                            max_value=5,
                            step=1,
                            default_value=1,
                            thumb_color="#2481ce",
                            slider_color="#061724",
                            track_color="lightgray")

# -----------------------line break -------------------------------------- #
st.markdown("***")
# ---------------------- Plots ------------------------------------------- #

signal_figure,spec_figure = functions.plotSignals()
signal_plot_col, spectrogram_col = st.columns(2)

with signal_plot_col:
    st.plotly_chart(signal_figure,use_container_width=True)

with spectrogram_col:
    st.plotly_chart(spec_figure,use_container_width=True)

# ---------------------- Modified Signal --------------------------------- #
st.sidebar.markdown("# Modified Signal")
st.sidebar.audio("Modified.wav" if st.session_state["uploaded_file"] else None,"wav")
