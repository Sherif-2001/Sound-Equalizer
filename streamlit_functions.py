import numpy as np
import pandas as pd
import scipy.fft as fft
import plotly.express as px
import wave
import streamlit as st
from scipy.io.wavfile import write
import scipy.signal as sig
import plotly.graph_objs as go
import streamlit_vertical_slider as svs
from PIL import Image
import librosa

def signalTransform():
    if st.session_state["uploaded_file"]:
        audio = wave.open(st.session_state["uploaded_file"], 'rb')
        sample_rate = audio.getframerate()
        n_channels = audio.getnchannels()
        n_samples = audio.getnframes()
        duration = n_samples / sample_rate
        signal_wave = audio.readframes(-1)   

        signal_x_axis = np.arange(0,duration,1/sample_rate)
        signal_y_axis = np.frombuffer(signal_wave, dtype=np.int16)

        yf = fft.rfft(signal_y_axis)    
        xf = fft.rfftfreq(n_samples,1/sample_rate)

        equalizerModes(duration,yf,xf)

        modified_signal = fft.irfft(yf)
        
        male_modified_signal = librosa.effects.pitch_shift(modified_signal, sample_rate, n_steps= -5)
    
        modified_signal_channel = np.int16(male_modified_signal if (st.session_state["gender"] == "Male" and st.session_state["current_page"] == "VoiceChanger") else modified_signal)

        if n_channels == 1:
            write("Modified.wav", sample_rate, modified_signal_channel)
            return  signal_x_axis,signal_y_axis,modified_signal,sample_rate,duration
        
        else:
            write("Modified.wav", sample_rate*2, modified_signal_channel)
            return  signal_x_axis,signal_y_axis[:len(signal_x_axis)],modified_signal[:len(signal_x_axis)],sample_rate,duration

    else:
        return np.arange(0,1,0.1),np.zeros(10),np.zeros(10),1,1

def plotSignals():
    signal_x_axis,signal_y_axis,modified_signal,sample_rate,duration = signalTransform()
    signal_figure = px.line(x = signal_x_axis,y = modified_signal)
    signal_figure['data'][0]['showlegend'] = True
    signal_figure['data'][0]['name'] = 'Modified'
    signal_figure.add_scatter(name="Original", x=signal_x_axis,y=signal_y_axis, line_color="#FF4B4B",visible="legendonly")
    signal_figure.update_layout(margin=dict(l=0, r=0, t=0, b=0), legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01))
    signal_figure.update_xaxes(title="Time", linewidth=2, linecolor='black',gridcolor='#5E5E5E', title_font=dict(size=24, family='Arial'))
    signal_figure.update_yaxes(title="Amplitude", linewidth=2, linecolor='black',gridcolor='#5E5E5E', title_font=dict(size=24, family='Arial'))
 
    original_freqs, original_time, original_Pxx = sig.spectrogram(signal_y_axis, sample_rate)
    modified_freqs, modified_time, modified_Pxx = sig.spectrogram(modified_signal, sample_rate)

    traces = [go.Heatmap(x= modified_time, y= modified_freqs, z= 10*np.log10(modified_Pxx),name="Modified"),go.Heatmap(x= original_time, y= original_freqs, z= 10*np.log10(original_Pxx), visible="legendonly",name="Original")]
    layout = go.Layout(yaxis = dict(title = 'Frequency'), xaxis = dict(title = 'Time'), margin= dict(l=0, r=0, t=0, b=0))
    spec_figure = go.Figure(data=traces, layout=layout)
    spec_figure.update_traces(showlegend=True,colorscale='Jet')
    spec_figure.update_layout(showlegend=True,legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01))
    spec_figure.update_xaxes(title_font=dict(size=24, family='Arial'))
    spec_figure.update_yaxes(title_font=dict(size=24, family='Arial'))

    return signal_figure, spec_figure

def equalizerModes(duration,yf,xf):

    if st.session_state["current_page"] == "Default":
        ranges = np.arange(0,np.abs(xf.max()),np.abs(xf.max())/10)
        for i in range(10):
            if i < 9:
                yf[int(duration*ranges[i]):int(duration* ranges[i+1])] *= st.session_state.get(f"slider{i+1}")
            else:
                yf[int(duration*ranges[-1]):int(duration* xf.max())] *= st.session_state.get(f"slider10")

    if st.session_state["current_page"] == "Music":
        yf[int(duration*0):int(duration* 1000)] *= st.session_state["drum_value"]
        yf[int(duration*1000):int(duration* 5000)] *= st.session_state["piano_value"]
        yf[int(duration*5000):int(duration* 10000)] *= st.session_state["violin_value"]

    if st.session_state["current_page"] == "Vowels":
        yf[int(duration*0):int(duration* 1000)] *= st.session_state["letterA_value"]
        yf[int(duration*1000):int(duration* 5000)] *= st.session_state["letterB_value"]
        yf[int(duration*5000):int(duration* 10000)] *= st.session_state["letterT_value"]
        yf[int(duration*10000):int(duration* 20000)] *= st.session_state["letterK_value"]

    if st.session_state["current_page"] == "Medical":
        yf[int(duration*60):int(duration*90)] *= st.session_state["Arrhythmia1"]
        yf[int(duration*90):int(duration*250)] *=st.session_state["Arrhythmia2"]
        yf[int(duration*250):int(duration*300)] *= st.session_state["Arrhythmia3"]

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
    instrument1_col,instrument2_col,instrument3_col = st.columns(3)
    with instrument1_col:
        drum_image = Image.open('icons/drum.png')
        st.image(drum_image,width=200)
        st.slider("Drum Sound",0,5,1,1,key="drum_value",label_visibility="collapsed")
    with instrument2_col:
        violin_image = Image.open('icons/violin.png')
        st.image(violin_image,width=200)
        st.slider("Violin Sound",0,5,1,1,key="violin_value",label_visibility="collapsed")
    with instrument3_col:
        piano_image = Image.open('icons/piano.png')
        st.image(piano_image,width=200)
        st.slider("Piano Sound",0,5,1,1,key="piano_value",label_visibility="collapsed")

def vowelsPage():
    letters = ["A","B","T","K"]
    letters_columns = st.columns(4)
    for column in letters_columns:
        i = letters_columns.index(column)
        with column:
            st.slider(f"letter {letters[i]}",0,5,1,1,key=f"letter{letters[i]}_value")

def voiceChangerPage():
    female_col,selectbox_col,male_col = st.columns((1,2,1))
    with female_col:
        female_image = Image.open('icons/female.png')
        st.image(female_image,width=200)
   
    with selectbox_col:
        for _ in range(4):
            st.markdown("")
        st.select_slider("Change Voice to:",options=["Female","Male"],key="gender",label_visibility="collapsed")

    with male_col:
        male_image = Image.open('icons/male.png')
        st.image(male_image,width=200)

def medicalPage():
    columns = st.columns(3)
    for column in columns:
        i = columns.index(column)+1
        with column:
            st.slider(f"Arrhythmia{i}",0,5,1,1,key=f"Arrhythmia{i}_value")

def dynamicPlot():
    signal_x_axis,signal_y_axis,modified_signal,sample_rate,duration = signalTransform()
    df = pd.DataFrame({"amplitude":signal_y_axis,"time":signal_x_axis})
    if len(df) != 0:
        df = df[::(len(df)//1000)]
    Frame_1 = []
    time_list=[0]
    amplitude_list=[df["amplitude"][0]]
    for ind,df_r in df.iterrows():
        time_list.append(df_r["time"])
        amplitude_list.append(df_r["amplitude"])
        Frame_1.append(go.Frame(data=[go.Scatter(x=time_list,y=amplitude_list,mode="lines")])) #1
    fig = go.Figure(
        data=[go.Scatter(x=[0, 0], y=[0, 0])],
        layout=go.Layout(
            xaxis=dict(range=[0, df["time"].max()], autorange=False),
            yaxis=dict(range=[df["amplitude"].min()*1.5, df["amplitude"].max()*1.5], autorange=False),
            margin= dict(l=0, r=0, t=0, b=0)
    ),
        frames=Frame_1
    ) #2

    fig["layout"]["updatemenus"] = [
        {
            "buttons": [
                {
                    "args": [None, {"frame": {"duration": 1, "redraw": False},
                                    "fromcurrent": True, "transition": {"duration": 0}}],
                    "label": "Play",
                    "method": "animate"
                },
                {
                    "args": [[None], {"frame": {"duration": 0, "redraw": False},
                                    "mode": "immediate",
                                    "transition": {"duration": 0}}],
                    "label": "Pause",
                    "method": "animate"
                }
            ],
            "direction": "left",
            "pad": {"t": 50},
            "showactive": False,
            "type": "buttons",
            "x": 0.1,
            "xanchor": "right",
            "y": 0,
            "yanchor": "top"
        }
    ]

    # sliders_dict = {
    #     "active": 0,
    #     "yanchor": "top",
    #     "xanchor": "left",
    #     "currentvalue": {
    #         "font": {"size": 20},
    #         "prefix": "Time:",
    #         "visible": True,
    #         "xanchor": "right"
    #     },
    #     "transition": {"duration": 0},
    #     "pad": {"b": 10, "t": 50},
    #     "len": 0.9,
    #     "x": 0.1,
    #     "y": 0,
    #     "steps": []
    # }
    # slider_step = {"args": [
    #     {"frame": {"duration": 300, "redraw": False},
    #      "mode": "immediate",
    #      "transition": {"duration": 300}}
    # ],
    #     "method": "animate"}
    # sliders_dict["steps"].append(slider_step)
    # fig1["layout"]["sliders"] = [sliders_dict]

    st.plotly_chart(fig)