import streamlit as st
import streamlit_vertical_slider as svs

columns = st.columns(10)
for column in columns:
    with column:
        svs.vertical_slider(key = f"{columns.index(column)}",min_value=0,max_value=10,step=0.5,default_value=5,thumb_color="#FF4B4B",slider_color="#AA4B4B",track_color="#FFFFFF")