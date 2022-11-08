import streamlit as st

def onPlayButtonClick():
    st.session_state["play_state"] = not st.session_state["play_state"]



