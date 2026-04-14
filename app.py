import streamlit as st
from rembg import remove
from PIL import Image, ImageEnhance, ImageOps
import io
import zipfile

# --- UI & REFRESH LOCK SETUP ---
st.set_page_config(page_title="Pro Studio AI", layout="centered")

st.markdown("""
<style>
    /* 🛑 Yeh code mobile me page ko baar-baar refresh hone se rokega 🛑 */
    html, body, [data-testid="stAppViewContainer"], .main {
        overscroll-behavior-y: contain !important;
        background-color: #0e1117; 
        color: #ffffff;
    }
    h1, h2, h3 { color: #ffffff !important; text-align: center; }
    .stButton>button { background-color: #ff4b4b; color: white; border-radius: 8px; width: 100%; font-weight: bold; }
    .stButton>button:hover { background-color: #ff3333; }
</style>
""", unsafe_allow_html=True)

st.title("✨ Pro Studio V2")
st.markdown("<p style='text-align: center;'>AI Cutout + 20 Pro Color LUTs</p>", unsafe_allow_html=True)

# --- 20 PROFESSIONAL LUTS LOGIC ---
def apply_filter(img, filter_name):
    if img.mode != 'RGBA':
        img = img.convert('RGBA')
    r, g, b, a = img.split()
    rgb_img = Image.merge("RGB", (r, g, b))
    
    # Color Enhancers
    enhancer_color = ImageEnhance.Color(rgb_img)
    enhancer_contrast = ImageEnhance.Contrast(rgb_img)
    enhancer_bright = ImageEnhance.Brightness(rgb_img)

    if "01" in filter_name: rgb_img = enhancer_contrast.enhance(1.2) # Crisp
    elif "02" in filter_name: rgb_img = enhancer_color.enhance(1.4); rgb_img = ImageEnhance.Contrast(rgb_img).enhance(1.1) # Cinematic Vibrant
    elif "03" in filter_name: rgb_img = ImageOps.grayscale(rgb_img).convert("RGB"); rgb_img = ImageEnhance.Contrast(rgb_img).enhance(1.3) # Moody Noir
    elif "04" in filter_name: rgb_img = enhancer_color.enhance(1.5) # Bollywood Punch
    elif "05" in filter_name: rgb_img = enhancer_color.enhance(0.5); rgb_img = ImageEnhance.Contrast(rgb_img).enhance(0.8) # Faded Vintage
    elif "06" in filter_name: rgb_img = enhancer_bright.enhance(1.2); rgb_img = enhancer_color.enhance(0.8) # Soft Pastel
    elif "07" in filter_name: rgb_img = enhancer_contrast.enhance(1.4); rgb_img = enhancer_color.enhance(1.2) # Cyberpunk High Contrast
    elif "08" in filter_name: r_img, g_img, b_img = rgb_img.split(); rgb_img = Image.merge("RGB", (enhancer_bright.enhance(1.1).split()[0], g_img, enhancer_bright.enhance(0.9).split()[2])) # Teal & Orange Feel
    elif "09" in filter_name: rgb_img = enhancer_color.enhance(1.3); rgb_img = enhancer_bright.enhance(1.1) # Golden Hour
    elif "10" in filter_name: rgb_img = enhancer_bright.enhance(0.8); rgb_img = enhancer_contrast.enhance(1.2) # Dark Knight
    elif "11" in filter_name: rgb_img = enhancer_color.enhance(0.7); r_img, g_img, b_img = rgb_img.split(); rgb_img = Image.merge("RGB", (r_img, g_img, enhancer_bright.enhance(1.2).split()[2])) # Cool Breeze
    elif "12" in filter_name: rgb_img = ImageOps.grayscale(rgb_img).convert("RGB") # B&W Classic
    elif "13" in filter_name: rgb_img = enhancer_contrast.enhance(0.8); rgb_img = enhancer_bright.enhance(1.1) # Matte Finish
    elif "14" in filter_name: rgb_img = enhancer_color.enhance(1.2); r_img, g_img, b_img = rgb_img.split(); rgb_img = Image.merge("RGB", (enhancer_bright.enhance(1.1).split()[0], g_img, b_img)) # Rich Warmth
    elif "15" in filter_name: rgb_img = enhancer_contrast.enhance(1.5) # Hard Contrast
    elif "16" in filter_name: rgb_img = enhancer_bright.enhance(1.3) # Bright & Airy
    elif "17" in filter_name: rgb_img = enhancer_color.enhance(0.3); rgb_img = enhancer_contrast.enhance(1.3) # Bleach Bypass
    elif "18" in filter_name: rgb_img = enhancer_color.enhance(1.6); rgb_img = enhancer_contrast.enhance(1.2) # Pop Art
    elif "19" in filter_name: rgb_img = enhancer_contrast.enhance(1.1); r_img, g_img, b_img = rgb_img.split(); rgb_img = Image.merge("RGB", (r_img, enhancer_bright.enhance(1.1).split()[1], b_img)) # Deep Emerald
    elif "20" in filter_name: rgb_img = enhancer_color.enhance(0.8); rgb_img = enhancer_contrast.enhance(1.2) # Crisp Winter
    
    return Image.merge("RGBA", (rgb_img.split()[0], rgb_img.split()[1], rgb_img.split()[2], a))

lut_list = [
    "00. Original", "01. Basic Crisp", "02. Cinematic Teal", "03. Moody Noir", "04. Bollywood Punch", 
    "05. Faded Vintage", "06. Soft Pastel", "07. Cyberpunk", "08. Insta Filter", "09. Golden Hour",
    "10. Dark Knight", "11. Cool Breeze", "12. B&W Classic", "13. Matte Finish", "14. Rich Warmth",
    "15. Hard Contrast", "16. Bright & Airy", "17. Bleach Bypass", "18. Pop Art Bright", "19. Deep Emerald", "20. Crisp Winter"
]

# --- UPLOAD ---
uploaded_files = st.file_uploader("Photos upload karein", type=['png', 'jpg', 'jpeg'], accept_multiple_files=True)

if uploaded_files:
    # --- EDITING MODE SELECTOR (NEW FEATURE) ---
    st.markdown("---")
    edit_mode = st.radio("Aap kya karna chahte hain?", 
                         ("✂️ Background Remove + LUT (Wedding Photos ke liye)", 
                          "🎨 Sirf LUT Lagayein, BG mat hatayein (Thumbnails ke liye)"))
    
    st.markdown("---")
    
    # LIVE PREVIEW
    preview_img = Image.open(uploaded_files[0])
    selected_lut = st.selectbox("Apna LUT (Filter) Select Karein:", options=lut_list)
    
    col1, col2 = st.columns(2)
    with col1:
        st.write("Original")
        st.image(preview_img, use_container_width=True)
        
    with col2:
        st.write("Live Preview")
        with st.spinner("Applying..."):
            if "✂️ Background Remove" in edit_mode:
                # Agar user BG hatana chahta hai (Thoda time lega preview me)
                temp_nobg = remove(preview_img)
                preview_final = apply_filter(temp_nobg, selected_lut)
            else:
                # Agar sirf color filter lagana hai (Fast hoga)
                preview_final = apply_filter(preview_img, selected_lut)
                
            st.image(preview_final, use_container_width=True)

    st.markdown("---")
    
    # --- PROCESSING ---
    if st.button("🚀 Save & Download All"):
        st.info("Processing Started...")
        zip_buffer = io.BytesIO()
        progress_bar = st.progress(0)
        
        with zipfile.ZipFile(zip_buffer, "w") as zip_file:
            for index, file in enumerate(uploaded_files):
                img = Image.open(file)
                
                # Check mode
                if "✂️ Background Remove" in edit_mode:
                    processed_img = remove(img, alpha_matting=True, alpha_matting_foreground_threshold=240, alpha_matting_background_threshold=10, alpha_matting_erode_size=10)
                else:
                    processed_img = img.convert("RGBA")
                
                # Apply Filter
                final_img = apply_filter(processed_img, selected_lut) if "00" not in selected_lut else processed_img
                
                # Save
                img_byte_arr = io.BytesIO()
                final_img.save(img_byte_arr, format='PNG')
                zip_file.writestr(f"Edited_{file.name.split('.')[0]}.png", img_byte_arr.getvalue())
                
                progress_bar.progress((index + 1) / len(uploaded_files))
                
        st.success("✅ Sabhi Photos Edit ho gayi!")
        st.download_button(label="⬇️ Download ZIP", data=zip_buffer.getvalue(), file_name="Pro_Edited_Photos.zip", mime="application/zip")
