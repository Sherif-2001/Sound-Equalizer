import streamlit as st
import streamlit_functions as functions

# ---------------------- Websites Options -------------------------------- #
st.set_page_config(page_title="Equalizer",layout="wide",page_icon="🎚",initial_sidebar_state="expanded")

# ---------------------- Variables States -------------------------------- #
if "current_page" not in st.session_state:
    st.session_state["current_page"] = "Default"

# ---------------------- Elements Styling -------------------------------- #
with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# ---------------------- Uploading Files --------------------------------- #

uploaded_file = st.sidebar.file_uploader("uploader",key="uploaded_file",label_visibility="hidden",type="wav")

# ---------------------- Original Audio ---------------------------------- #

st.sidebar.markdown("# Original Signal")
st.sidebar.audio(st.session_state["uploaded_file"] if st.session_state["uploaded_file"] else None,"wav")

if st.session_state["current_page"] == "Default":
    functions.defaultPage()
elif st.session_state["current_page"] == "Music":
    functions.musicPage()
elif st.session_state["current_page"] == "Vowels":
    functions.vowelsPage()
elif st.session_state["current_page"] == "lastone":
    functions.lastPage()

# ---------------------- Line Break -------------------------------------- #
st.markdown("***")
# ---------------------- Plots ------------------------------------------- #
signal_figure,spec_figure = functions.plotSignals()
signal_plot_col, spectrogram_col = st.columns(2,gap="large")

with signal_plot_col:
    st.plotly_chart(signal_figure,use_container_width=True)

with spectrogram_col:
    st.plotly_chart(spec_figure,use_container_width=True)

# ---------------------- Modified Signal --------------------------------- #
st.sidebar.markdown("# Modified Signal")
st.sidebar.audio("Modified.wav" if st.session_state["uploaded_file"] else None,"wav")

# ---------------------- Pages ------------------------------------------- #

st.sidebar.markdown("# Pages")
current_page = st.sidebar.radio("pages",["Default","Music","Vowels","lastone"],key="current_page",label_visibility="collapsed")