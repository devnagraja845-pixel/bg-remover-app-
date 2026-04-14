import streamlit as st
from rembg import remove
from PIL import Image, ImageEnhance, ImageOps
import io
import zipfile

# --- CLEAN UI SETUP ---
st.set_page_config(page_title="AI Photo Studio", layout="centered")

st.markdown("""
<style>
    /* Clean Minimalist Theme */
    .stApp { background-color: #0e1117; color: #ffffff; }
    h1, h2, h3 { color: #ffffff !important; text-align: center; font-family: sans-serif; }
    .stButton>button { background-color: #2b313e; color: white; border: 1px solid #4a5568; border-radius: 6px; width: 100%; }
    .stButton>button:hover { background-color: #3b4252; border-color: #63b3ed; }
</style>
""", unsafe_allow_html=True)

st.title("✨ AI Photo Studio")
st.markdown("<p style='text-align: center; color: #a0aec0;'>Background Remover & Color LUTs</p>", unsafe_allow_html=True)

# --- UPLOAD SECTION ---
uploaded_files = st.file_uploader("Photos upload karein (Max 100)", type=['png', 'jpg', 'jpeg'], accept_multiple_files=True)

# Filter Logic (Simulated LUTs)
def apply_filter(img, filter_name):
    if img.mode != 'RGBA':
        img = img.convert('RGBA')
    r, g, b, a = img.split()
    rgb_img = Image.merge("RGB", (r, g, b))
    
    if "Cinematic" in filter_name:
        rgb_img = ImageEnhance.Color(rgb_img).enhance(1.2)
        rgb_img = ImageEnhance.Contrast(rgb_img).enhance(1.1)
    elif "Noir" in filter_name:
        rgb_img = ImageOps.grayscale(rgb_img).convert("RGB")
        rgb_img = ImageEnhance.Contrast(rgb_img).enhance(1.3)
    elif "Vibrant" in filter_name:
        rgb_img = ImageEnhance.Color(rgb_img).enhance(1.5)
        
    return Image.merge("RGBA", (rgb_img.split()[0], rgb_img.split()[1], rgb_img.split()[2], a))

lut_options = ["00. Original", "01. Cinematic Teal", "02. Moody Noir", "03. Bollywood Vibrant"]

if uploaded_files:
    st.markdown("---")
    st.subheader("🎨 Live LUT Preview")
    
    # Live preview ke liye pehli image ka use
    preview_img = Image.open(uploaded_files[0])
    
    # Layout for Preview
    col1, col2 = st.columns(2)
    with col1:
        st.write("Original Photo")
        st.image(preview_img, use_container_width=True)
        
    with col2:
        st.write("LUT Preview (After BG Removal)")
        selected_lut = st.selectbox("LUT Select Karein:", options=lut_options, label_visibility="collapsed")
        
        # Temp background removal just for preview
        with st.spinner("Preview loading..."):
            preview_nobg = remove(preview_img)
            preview_final = apply_filter(preview_nobg, selected_lut)
            st.image(preview_final, use_container_width=True)

    st.markdown("---")
    
    # --- BULK PROCESS BUTTON ---
    if st.button("🚀 Process All & Download (HD)"):
        st.info("Processing Started...")
        zip_buffer = io.BytesIO()
        progress_bar = st.progress(0)
        
        with zipfile.ZipFile(zip_buffer, "w") as zip_file:
            for index, file in enumerate(uploaded_files):
                img = Image.open(file)
                transparent_img = remove(img, alpha_matting=True, alpha_matting_foreground_threshold=240, alpha_matting_background_threshold=10, alpha_matting_erode_size=10)
                
                final_img = apply_filter(transparent_img, selected_lut) if "00" not in selected_lut else transparent_img
                
                img_byte_arr = io.BytesIO()
                final_img.save(img_byte_arr, format='PNG')
                zip_file.writestr(f"Edit_{file.name.split('.')[0]}.png", img_byte_arr.getvalue())
                
                progress_bar.progress((index + 1) / len(uploaded_files))
                
        st.success("✅ Done!")
        st.download_button(label="⬇️ Download ZIP", data=zip_buffer.getvalue(), file_name="Edited_Photos.zip", mime="application/zip")
