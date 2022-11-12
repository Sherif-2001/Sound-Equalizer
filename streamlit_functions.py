import numpy as np
import scipy.fft as fft
import plotly.express as px
import wave
import streamlit as st
from scipy.io.wavfile import write
import scipy.signal as sig
import plotly.graph_objs as go
import streamlit_vertical_slider as svs
from PIL import Image

def signalTransform():
    if st.session_state["uploaded_file"]:
        audio   =     wave.open(st.session_state["uploaded_file"], 'rb')
        sample_rate = audio.getframerate()
        n_channels = audio.getnchannels()
        n_samples   = audio.getnframes()
        duration    = n_samples / sample_rate
        signal_wave = audio.readframes(-1)   

        signal_y_axis = np.frombuffer(signal_wave, dtype=np.int16)
        signal_x_axis = np.arange(0,duration,1/(2*sample_rate))

        yf = fft.rfft(signal_y_axis)
        xf = fft.rfftfreq(len(yf),1/sample_rate)

        rangesMode(duration,yf,xf)

        modified_signal = fft.irfft(yf)
        modified_signal_channel = np.int16(modified_signal)

        if n_channels == 1:
            write("Modified.wav", sample_rate, modified_signal_channel)
            return  signal_x_axis[:len(signal_x_axis)//2],signal_y_axis,modified_signal,sample_rate
        
        else:
            write("Modified.wav", sample_rate*2, modified_signal_channel)
            return  signal_x_axis,signal_y_axis,modified_signal,sample_rate

    else:
        return np.arange(0,1,0.1),np.zeros(10),np.zeros(10),1

def plotSignals():
    signal_x_axis,signal_y_axis,modified_signal,sample_rate = signalTransform()
    signal_figure = px.line(x = signal_x_axis,y = modified_signal)
    signal_figure['data'][0]['showlegend'] = True
    signal_figure['data'][0]['name'] = 'Modified'
    signal_figure.add_scatter(name="Original", x=signal_x_axis,y=signal_y_axis, line_color="#FF4B4B",visible="legendonly")
    signal_figure.update_layout(margin=dict(l=0, r=0, t=0, b=0), legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01))
    signal_figure.update_xaxes(title="Time", linewidth=2, linecolor='black',gridcolor='#5E5E5E', title_font=dict(size=24, family='Arial'))
    signal_figure.update_yaxes(title="Amplitude", linewidth=2, linecolor='black',gridcolor='#5E5E5E', title_font=dict(size=24, family='Arial'))
 
    original_freqs, original_time, original_Pxx = sig.spectrogram(signal_y_axis, sample_rate*2)
    modified_freqs, modified_time, modified_Pxx = sig.spectrogram(modified_signal, sample_rate*2)

    traces = [go.Heatmap(x= modified_time, y= modified_freqs, z= 10*np.log10(modified_Pxx),name="Modified"),go.Heatmap(x= original_time, y= original_freqs, z= 10*np.log10(original_Pxx), visible="legendonly",name="Original")]
    layout = go.Layout(yaxis = dict(title = 'Frequency'), xaxis = dict(title = 'Time'), margin= dict(l=0, r=0, t=0, b=0))
    spec_figure = go.Figure(data=traces, layout=layout)
    spec_figure.update_traces(showlegend=True,colorscale='Jet')
    spec_figure.update_layout(showlegend=True,legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01))
    spec_figure.update_xaxes(title_font=dict(size=24, family='Arial'))
    spec_figure.update_yaxes(title_font=dict(size=24, family='Arial'))

    return signal_figure, spec_figure

def rangesMode(duration,yf,xf):
    ranges = np.arange(0,np.abs(xf.max()),np.abs(xf.max())/10)

    if st.session_state["current_page"] == "Music":
        if not st.session_state["drum_check"]:
            yf[int(duration*0):int(duration* 1000)] *= 0
        if not st.session_state["piano_check"]:
            yf[int(duration*1000):int(duration* 5000)] *= 0
        if not st.session_state["violin_check"]:
            yf[int(duration*5000):int(duration* 10000)] *= 0

    if st.session_state["current_page"] == "Default":
        for i in range(10):
            if i < 9:
                yf[int(duration*ranges[i]):int(duration* ranges[i+1])] *= st.session_state.get(f"slider{i+1}")
            else:
                yf[int(duration*ranges[-1]):int(duration* xf.max())] *= st.session_state.get(f"slider10")

    if st.session_state["current_page"] == "Vowels":
        if not st.session_state["letterA"]:
            yf[int(duration*0):int(duration* 1000)] *= 0
        if not st.session_state["letterB"]:
            yf[int(duration*1000):int(duration* 5000)] *= 0
        if not st.session_state["letterT"]:
            yf[int(duration*5000):int(duration* 10000)] *= 0
        if not st.session_state["letterK"]:
            yf[int(duration*10000):int(duration* 20000)] *= 0

    if st.session_state["current_page"] == "VoiceChanger":
        if st.session_state["gender"] == "Male":
            print("male")
        elif st.session_state["gender"] == "Female":
            print("Female")

def defaultPage():
    columns = st.columns(10)
    
    for index in range(len(columns)):
        if f"slider{index+1}" not in st.session_state:
            st.session_state[f"slider{index+1}"] = 1

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

def musicPage():
    instrument1_col,instrument2_col,instrument3_col = st.columns((2,2,1))
    with instrument1_col:
        drum_image = Image.open('icons/drum.png')
        st.image(drum_image,width=200)
        st.checkbox("Drum Sound",value=True,key="drum_check")
    with instrument2_col:
        violin_image = Image.open('icons/violin.png')
        st.image(violin_image,width=200)
        st.checkbox("Violin Sound",value=True,key="violin_check")
    with instrument3_col:
        piano_image = Image.open('icons/piano.png')
        st.image(piano_image,width=200)
        st.checkbox("Piano Sound",value=True,key="piano_check")

def vowelsPage():
    letters = ["A","B","T","K"]
    letters_columns = st.columns((2,2,2,1))
    for column in letters_columns:
        i = letters_columns.index(column)
        with column:
            st.checkbox(label=f"letter {letters[i]}",value=True,key=f"letter{letters[i]}")

def voiceChangerPage():
    male_col,selectbox_col, female_col = st.columns((1,2,1))
    with male_col:
        male_image = Image.open('icons/male.png')
        st.image(male_image,width=200)
    
    with selectbox_col:
        for _ in range(4):
            st.markdown("")
        st.select_slider("Change Voice to:",options=["Male","Female"],key="gender",value="Male",label_visibility="collapsed")

    with female_col:
        female_image = Image.open('icons/female.png')
        st.image(female_image,width=200)