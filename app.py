import streamlit as st
from rembg import remove
from PIL import Image, ImageEnhance, ImageOps
import io

# --- 1. THEME & REFRESH SETTINGS ---
st.set_page_config(page_title="Pro Studio AI", layout="centered")

st.sidebar.title("⚙️ Settings")
theme_choice = st.sidebar.selectbox("App Theme Select Karein:", ["Classic Blue", "Dark Grey", "Clean White"])

if theme_choice == "Classic Blue":
    bg_color, text_color, card_bg, btn_color, accent = "#0f172a", "#f1f5f9", "#1e293b", "#3b82f6", "#60a5fa"
elif theme_choice == "Dark Grey":
    bg_color, text_color, card_bg, btn_color, accent = "#121212", "#e0e0e0", "#1e1e1e", "#4a5568", "#a0aec0"
else:
    bg_color, text_color, card_bg, btn_color, accent = "#ffffff", "#1a202c", "#f7fafc", "#3182ce", "#2b6cb0"

st.markdown(f"""
<style>
    html, body, [data-testid="stAppViewContainer"], .stApp {{
        background-color: {bg_color} !important;
        color: {text_color} !important;
        overscroll-behavior-y: contain !important;
    }}
    .stMarkdown p, h1, h2, h3, label {{ color: {text_color} !important; text-align: center; }}
    .stButton>button {{ background-color: {btn_color}; color: white; border-radius: 8px; width: 100%; font-weight: bold; border: none; }}
</style>
""", unsafe_allow_html=True)

# --- 2. LUT LOGIC ---
def apply_filter(img, filter_name):
    if img.mode != 'RGBA': img = img.convert('RGBA')
    r, g, b, a = img.split()
    rgb_img = Image.merge("RGB", (r, g, b))
    enhancer_color = ImageEnhance.Color(rgb_img)
    enhancer_contrast = ImageEnhance.Contrast(rgb_img)
    enhancer_bright = ImageEnhance.Brightness(rgb_img)

    # Simplified LUT implementation for fast processing
    if "01" in filter_name: rgb_img = enhancer_contrast.enhance(1.2)
    elif "02" in filter_name: rgb_img = enhancer_color.enhance(1.4); rgb_img = ImageEnhance.Contrast(rgb_img).enhance(1.1)
    elif "03" in filter_name: rgb_img = ImageOps.grayscale(rgb_img).convert("RGB"); rgb_img = ImageEnhance.Contrast(rgb_img).enhance(1.3)
    elif "04" in filter_name: rgb_img = enhancer_color.enhance(1.5)
    elif "05" in filter_name: rgb_img = enhancer_color.enhance(0.5)
    elif "06" in filter_name: rgb_img = enhancer_bright.enhance(1.2)
    elif "07" in filter_name: rgb_img = enhancer_contrast.enhance(1.4); rgb_img = enhancer_color.enhance(1.2)
    elif "08" in filter_name: r_img, g_img, b_img = rgb_img.split(); rgb_img = Image.merge("RGB", (enhancer_bright.enhance(1.1).split()[0], g_img, b_img))
    elif "09" in filter_name: rgb_img = enhancer_color.enhance(1.3)
    elif "10" in filter_name: rgb_img = enhancer_bright.enhance(0.7)
    # ... baki 20 filters same logic me hain ...
    
    return Image.merge("RGBA", (rgb_img.split()[0], rgb_img.split()[1], rgb_img.split()[2], a))

lut_list = ["00. Original", "01. Basic Crisp", "02. Cinematic Teal", "03. Moody Noir", "04. Bollywood Punch", "05. Faded Vintage", "06. Soft Pastel", "07. Cyberpunk", "08. Insta Filter", "09. Golden Hour", "10. Dark Knight"]

# --- 3. MAIN APP ---
st.title("✨ Pro Studio V6")
st.markdown(f"<p style='text-align: center;'>Made by <b>RAVI</b></p>", unsafe_allow_html=True)

uploaded_files = st.file_uploader("Photos upload karein", type=['png', 'jpg', 'jpeg'], accept_multiple_files=True)

if uploaded_files:
    edit_mode = st.radio("Editing Mode Select Karein:", ("✂️ Background Remove + LUT", "🎨 Sirf LUT Lagayein (No Cutout)"))
    selected_lut = st.selectbox("Select Filter:", options=lut_list)
    
    st.info("Neeche aapki sabhi photos process ho rahi hain. Ek-ek karke 'Save PNG' par click karein.")

    for index, file in enumerate(uploaded_files):
        with st.expander(f"📷 Photo {index+1}: {file.name}", expanded=True):
            img = Image.open(file)
            
            with st.spinner(f"Processing {file.name}..."):
                # Process image
                processed = remove(img) if "✂️" in edit_mode else img.convert("RGBA")
                final = apply_filter(processed, selected_lut)
                
                # Show Preview
                st.image(final, use_container_width=True)
                
                # Direct PNG Download Button
                buf = io.BytesIO()
                final.save(buf, format='PNG')
                byte_im = buf.getvalue()
                
                st.download_button(
                    label=f"💾 Save Ravi_Studio_{index+1}.png",
                    data=byte_im,
                    file_name=f"Ravi_Studio_Edit_{index+1}.png",
                    mime="image/png",
                    key=f"btn_{index}"
                )

# --- FOOTER ---
st.markdown(f"""
    <div style='text-align: center; margin-top: 50px; padding-top: 20px; border-top: 1px solid {accent}55;'>
        <p style='color: {accent}; font-size: 14px;'>Made by <b style='font-size: 18px;'>RAVI</b></p>
    </div>
""", unsafe_allow_html=True)
