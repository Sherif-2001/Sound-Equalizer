import streamlit as st
import pandas as pd
import pandas as ps
from scipy.io import wavfile
from scipy.io.wavfile import read
import wave, struct
import matplotlib.pyplot as plt
import plotly_express as px
import numpy as np
from numpy import tile, dot, sinc, newaxis
import plotly.graph_objects as go
import streamlit_vertical_slider as svs
st.title('Audio Equalizer')
st.sidebar.title("Navigation")
uploaded_file = st.sidebar.file_uploader("Upload your file here")
Fig = go.Figure()
st.plotly_chart(Fig, use_container_width=True)
columns = st.columns(10)
for column in columns:
    with column:
        svs.vertical_slider(key = f"{columns.index(column)}", 
                            min_value=0,
                            max_value=100,step=1,
                            default_value=30,
                            thumb_color="#2481ce",
                            slider_color="#061724",
                            track_color="lightgray")

st.button('Play')

