# app.py
import streamlit as st
import os
from PIL import Image
from train import train_model
from predict import make_predictions

# Define the directory to save uploaded images
UPLOAD_DIR = './cloud_classification/images'

def save_uploaded_file(uploaded_file):
    try:
        os.makedirs(UPLOAD_DIR, exist_ok=True)
        with open(os.path.join(UPLOAD_DIR, uploaded_file.name), "wb") as f:
            f.write(uploaded_file.getbuffer())
        return True
    except Exception as e:
        st.error(f"Error saving file: {e}")
        return False

def main():
    st.title("Cloud Detection with DETR")

    # File uploader for images
    uploaded_files = st.file_uploader("Upload Images", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

    if uploaded_files:
        for uploaded_file in uploaded_files:
            if save_uploaded_file(uploaded_file):
                st.success(f"Saved file: {uploaded_file.name}")

    # Button to start training
    if st.button("Start Training"):
        if os.listdir(UPLOAD_DIR):
            st.write("Starting training...")
            train_model()
            st.success("Training completed!")
        else:
            st.error("Please upload images before starting training.")

    # File uploader for prediction
    uploaded_image = st.file_uploader("Upload Image for Prediction", type=["jpg", "jpeg", "png"])

    if uploaded_image:
        image_path = os.path.join(UPLOAD_DIR, uploaded_image.name)
        if save_uploaded_file(uploaded_image):
            st.success(f"Saved file: {uploaded_image.name}")
            if st.button("Make Prediction"):
                st.write("Making prediction...")
                make_predictions(image_path)
                st.success("Prediction completed!")

if __name__ == "__main__":
    main()