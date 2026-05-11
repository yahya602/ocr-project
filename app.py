import streamlit as st
import cv2
import numpy as np
from PIL import Image

from src.preprocessing import full_pipeline
from src.ocr_engine import extract_text
from src.text_post_processing import fix_bullets

# ===============================
# PAGE CONFIG (PRO LOOK)
# ===============================
st.set_page_config(
    page_title="Smart OCR Engine",
    page_icon="",
    layout="wide"
)

st.title("Smart OCR Engine")
st.caption("Extract high-quality text from images using advanced OCR and preprocessing techniques.")

# ===============================
# UPLOAD SECTION
# ===============================
uploaded_file = st.file_uploader(
    "Upload Image (PNG / JPG / JPEG)",
    type=["png", "jpg", "jpeg"]
)

if uploaded_file is not None:

    # ===============================
    # LOAD IMAGE
    # ===============================
    image = Image.open(uploaded_file).convert("RGB")
    img = np.array(image)
    img_bgr = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

    # ===============================
    # LAYOUT (SIDE BY SIDE)
    # ===============================
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Original Image")
        st.image(image, use_column_width=True)

    # ===============================
    # PROCESSING INDICATOR
    # ===============================
    with st.spinner("Extracting text... please wait"):
        text1 = extract_text(img_bgr)
        processed = full_pipeline(img_bgr)
        text2 = extract_text(processed)

    # ===============================
    # BEST RESULT SELECTION
    # ===============================
    final_text = text1 if len(text1.strip()) > len(text2.strip()) else text2
    final_text = fix_bullets(final_text)

    with col2:
        st.subheader("Extracted Text")

        if final_text.strip():
            st.success("Text extracted successfully")
        else:
            st.warning("No strong text detected")

        st.text_area("", final_text, height=350)

    # ===============================
    # DEBUG SECTION (OPTIONAL)
    # ===============================
    with st.expander("🔍 Debug Info"):
        st.write("Raw OCR 1:")
        st.code(text1)

        st.write("Raw OCR 2 (Processed Image):")
        st.code(text2)

    # ===============================
    # DOWNLOAD BUTTON
    # ===============================
    st.download_button(
        label="⬇ Download Text",
        data=final_text,
        file_name="ocr_output.txt",
        mime="text/plain"
    )