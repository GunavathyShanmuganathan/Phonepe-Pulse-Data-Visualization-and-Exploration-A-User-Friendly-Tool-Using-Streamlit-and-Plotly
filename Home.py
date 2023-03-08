import streamlit as st
st.title("Phonepe Pulse Data Analysis")
from PIL import Image

image = Image.open(r'C:\Users\User\images.jpg')

st.image(image, caption='Phonepe',width=600)
