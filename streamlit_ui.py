import streamlit as st
import streamlit_functions as functions
import plotly.express as px
import streamlit_vertical_slider as svs

import librosa.display
import matplotlib.pyplot as plt

# ---------------------- Elements Styling -------------------------------- #

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# ---------------------- Declaring Variables State ----------------------- #
if "play_state" not in st.session_state:
    st.session_state["play_state"] = False

# ---------------------- Uploading Files --------------------------------- #

st.sidebar.markdown("# Upload")
uploaded_file = st.sidebar.file_uploader("uploader",key="uploaded_file",label_visibility="hidden")

# ---------------------- Play/Pause Button ------------------------------- #

play_button = st.sidebar.button(label= "PLAY" if not st.session_state["play_state"] else "PAUSE",
                                disabled= not st.session_state["uploaded_file"], 
                                on_click= functions.onPlayButtonClick)
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

# ------------------------------------------------------------------------ #
st.markdown("***")
# ---------------------- Heat map ---------------------------------------- #

# s = [[1,2,3],[2,8,6],[8,2,8]]
# figure = px.line(s)
# figure.update_layout(showlegend=True, margin=dict(l=0, r=0, t=0, b=0), legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01),height = 350)
# figure.update_xaxes(showline=True, linewidth=2, linecolor='black',gridcolor='#5E5E5E', title_font=dict(size=24, family='Arial'))
# figure.update_yaxes(showline=True, linewidth=2, linecolor='black',gridcolor='#5E5E5E', title_font=dict(size=24, family='Arial'))

# st.plotly_chart(figure, use_container_width=True)

x, sr = librosa.load('Crash-Cymbal-3.wav', sr=None)
X = librosa.stft(x)
Xdb = librosa.amplitude_to_db(abs(X))
fig = plt.figure() 
librosa.display.specshow(Xdb, sr=sr, x_axis='time', y_axis='hz')
plt.colorbar()
plt.show()

st.pyplot(fig)
