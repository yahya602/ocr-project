import streamlit as st
import cv2
import numpy as np
from PIL import Image

from src.preprocessing import full_pipeline
from src.ocr_engine import extract_text
from src.text_post_processing import fix_bullets

# ===============================
# PAGE CONFIG
# ===============================
st.set_page_config(
    page_title="Smart OCR Engine",
    page_icon="",
    layout="centered"
)

st.title("Smart OCR Engine")
st.caption("Extract high-quality text from images using OCR + preprocessing")

# ===============================
# UPLOAD SECTION
# ===============================
uploaded_file = st.file_uploader(
    "Upload Image (PNG / JPG / JPEG)",
    type=["png", "jpg", "jpeg"]
)

# ===============================
# PROCESS ONLY IF IMAGE UPLOADED
# ===============================
if uploaded_file is not None:

    # LOAD IMAGE
    image = Image.open(uploaded_file).convert("RGB")

    img = np.array(image)
    img_bgr = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

    # ===============================
    # MOBILE SAFE LAYOUT (NO FIXED COLUMNS)
    # ===============================
    st.subheader("Original Image")
    st.image(image, use_container_width=True)

    # ===============================
    # PROCESSING
    # ===============================
    with st.spinner("Extracting text... please wait"):

        # OCR 1 (raw)
        text1 = extract_text(img_bgr)

        # preprocessing + OCR 2
        processed = full_pipeline(img_bgr)
        text2 = extract_text(processed)

    # BEST RESULT SELECTION
    final_text = text1 if len(text1.strip()) > len(text2.strip()) else text2
    final_text = fix_bullets(final_text)

    # ===============================
    # OUTPUT SECTION
    # ===============================
    st.subheader("Extracted Text")

    if final_text.strip():
        st.success("Text extracted successfully")
    else:
        st.warning("No strong text detected")

    st.text_area("Result", final_text, height=300)

    # ===============================
    # DEBUG SECTION
    # ===============================
    with st.expander("Debug Info"):
        st.write("Raw OCR 1")
        st.code(text1)

        st.write("Raw OCR 2 (Processed)")
        st.code(text2)

    # ===============================
    # DOWNLOAD
    # ===============================
    st.download_button(
        label="Download Text",
        data=final_text,
        file_name="ocr_output.txt",
        mime="text/plain"
    )