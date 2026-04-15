import streamlit as st
from rembg import remove
from PIL import Image, ImageEnhance, ImageOps
import io

st.set_page_config(page_title="Ravi Studio AI", layout="centered")

st.markdown("""
<style>
    html, body, [data-testid="stAppViewContainer"] { background-color: #121212; color: #ffffff; overscroll-behavior-y: contain !important; }
    .stButton>button { background-color: #ff4b4b; color: white; border-radius: 8px; width: 100%; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

st.title("✨ Ravi Studio AI - Safe Mode")
st.markdown("<p style='text-align: center; color: #a0aec0;'>Crash-Proof Version</p>", unsafe_allow_html=True)

def apply_filter(img, filter_name):
    if img.mode != 'RGBA': img = img.convert('RGBA')
    r, g, b, a = img.split()
    rgb_img = Image.merge("RGB", (r, g, b))
    
    if "01" in filter_name: rgb_img = ImageEnhance.Contrast(rgb_img).enhance(1.2)
    elif "02" in filter_name: rgb_img = ImageEnhance.Color(rgb_img).enhance(1.4)
    elif "03" in filter_name: rgb_img = ImageOps.grayscale(rgb_img).convert("RGB")
    
    return Image.merge("RGBA", (rgb_img.split()[0], rgb_img.split()[1], rgb_img.split()[2], a))

lut_list = ["00. Original", "01. Basic Crisp", "02. Vibrant Color", "03. B&W Classic"]

uploaded_files = st.file_uploader("Photos upload karein", type=['png', 'jpg', 'jpeg'], accept_multiple_files=True)

if uploaded_files:
    edit_mode = st.radio("Mode:", ("✂️ Remove Background", "🎨 Sirf LUT Lagayein"))
    selected_lut = st.selectbox("Select Filter:", options=lut_list)
    
    for index, file in enumerate(uploaded_files):
        with st.expander(f"📷 Photo {index+1}", expanded=True):
            img = Image.open(file)
            with st.spinner("Processing safely..."):
                try:
                    # RAM bachane ke liye simple remove function (No heavy alpha matting)
                    if "✂️" in edit_mode:
                        processed = remove(img) 
                    else:
                        processed = img.convert("RGBA")
                        
                    final = apply_filter(processed, selected_lut)
                    st.image(final, use_container_width=True)
                    
                    buf = io.BytesIO()
                    final.save(buf, format='PNG')
                    st.download_button(label=f"💾 Download Edit {index+1}", data=buf.getvalue(), file_name=f"Ravi_SafeEdit_{index+1}.png", mime="image/png", key=f"btn_{index}")
                except Exception as e:
                    st.error("Error! Photo bahut heavy hai.")
