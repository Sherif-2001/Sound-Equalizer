import numpy as np
import scipy.fft as fft
import plotly.express as px
import wave
import streamlit as st
from scipy.io.wavfile import write
import scipy.signal as sig
import plotly.graph_objs as go

def signalTransform():
    if st.session_state["uploaded_file"]:
        audio   =     wave.open(st.session_state["uploaded_file"], 'rb')
        sample_rate = audio.getframerate()
        n_samples   = audio.getnframes()
        duration    = n_samples / sample_rate
        signal_wave = audio.readframes(-1)   

        signal_y_axis = np.frombuffer(signal_wave, dtype=np.int16)
        signal_x_axis = np.arange(0,duration,1/(2*sample_rate))

        yf = fft.rfft(signal_y_axis)
        xf = fft.rfftfreq(len(yf),1/sample_rate)

        ranges = np.arange(0,np.abs(xf.max()),np.abs(xf.max())/10)

        for i in range(10):
            if i < 9:
                yf[int(duration*ranges[i]):int(duration* ranges[i+1])] *= st.session_state.get(f"slider{i+1}")
            else:
                yf[int(duration*ranges[-1]):int(duration* xf.max())] *= st.session_state.get(f"slider10")

        modified_signal = fft.irfft(yf)

        modified_signal_channel = np.int16(modified_signal)
        write("Modified.wav", sample_rate * 2, modified_signal_channel)
    
        return signal_x_axis,signal_y_axis,modified_signal,sample_rate
    else:
        return np.arange(0,1,0.1),np.zeros(10),np.zeros(10),1

def plotSignals():
    signal_x_axis,signal_y_axis,modified_signal,sample_rate = signalTransform()
    signal_figure = px.line(x = signal_x_axis,y = signal_y_axis)
    signal_figure['data'][0]['showlegend'] = True
    signal_figure['data'][0]['name'] = 'Original'
    signal_figure.add_scatter(name="Modified", x=signal_x_axis,y=modified_signal, line_color="#FF4B4B",visible="legendonly")
    signal_figure.update_layout(showlegend=True, margin=dict(l=0, r=0, t=0, b=0), legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01))
    signal_figure.update_xaxes(title="Time",showline=True, linewidth=2, linecolor='black',gridcolor='#5E5E5E', title_font=dict(size=24, family='Arial'))
    signal_figure.update_yaxes(title="Amplitude",showline=True, linewidth=2, linecolor='black',gridcolor='#5E5E5E', title_font=dict(size=24, family='Arial'))
 
    freqs, time, Pxx = sig.spectrogram(signal_y_axis, sample_rate*2)

    trace = [go.Heatmap(x= time[:len(time)//2], y= freqs, z= 10*np.log10(Pxx), colorscale='Jet')]
    layout = go.Layout(yaxis = dict(title = 'Frequency'), xaxis = dict(title = 'Time'), margin= dict(l=0, r=0, t=0, b=0))
    spec_figure = go.Figure(data=trace, layout=layout)
    spec_figure.update_xaxes(title_font=dict(size=24, family='Arial'))
    spec_figure.update_yaxes(title_font=dict(size=24, family='Arial'))

    return signal_figure, spec_figure