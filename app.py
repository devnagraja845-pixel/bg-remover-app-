import streamlit as st
from rembg import remove
from PIL import Image, ImageEnhance, ImageOps
import io

st.set_page_config(page_title="Ravi Studio AI", layout="centered")

# --- UI & ULTIMATE REFRESH LOCK SETUP ---
st.markdown("""
<style>
    /* 🛑 Heavy Duty Refresh Lock 🛑 */
    html, body, [data-testid="stAppViewContainer"], .stApp {
        overscroll-behavior-y: contain !important;
        background-color: #0e1117; 
        color: #ffffff;
    }
    h1, h2, h3, h4 { color: #ffffff !important; text-align: center; }
    .stButton>button { background-color: #ff4b4b; color: white; border-radius: 8px; width: 100%; font-weight: bold; }
    .stButton>button:hover { background-color: #ff3333; }
</style>
""", unsafe_allow_html=True)

st.title("✨ Ravi Studio AI V7")
st.markdown("<p style='text-align: center;'>Made by <b>RAVI</b></p>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #ff4b4b;'><b>Note: Complex Images par problem ho sakti hai. Ye app Portait Photos pe best kaam karegi.</b></p>", unsafe_allow_html=True)

# --- 20 PROFESSIONAL LUTS LOGIC ---
def apply_filter(img, filter_name):
    if img.mode != 'RGBA':
        img = img.convert('RGBA')
    r, g, b, a = img.split()
    rgb_img = Image.merge("RGB", (r, g, b))
    enhancer_color = ImageEnhance.Color(rgb_img)
    enhancer_contrast = ImageEnhance.Contrast(rgb_img)
    enhancer_bright = ImageEnhance.Brightness(rgb_img)
    if "01" in filter_name: rgb_img = enhancer_contrast.enhance(1.2)
    elif "02" in filter_name: rgb_img = enhancer_color.enhance(1.4); rgb_img = ImageEnhance.Contrast(rgb_img).enhance(1.1)
    elif "03" in filter_name: rgb_img = ImageOps.grayscale(rgb_img).convert("RGB"); rgb_img = ImageEnhance.Contrast(rgb_img).enhance(1.3)
    elif "04" in filter_name: rgb_img = enhancer_color.enhance(1.5)
    elif "05" in filter_name: rgb_img = enhancer_color.enhance(0.5); rgb_img = ImageEnhance.Contrast(rgb_img).enhance(0.8)
    elif "06" in filter_name: rgb_img = enhancer_bright.enhance(1.2); rgb_img = enhancer_color.enhance(0.8)
    elif "07" in filter_name: rgb_img = enhancer_contrast.enhance(1.4); rgb_img = enhancer_color.enhance(1.2)
    elif "08" in filter_name: r_img, g_img, b_img = rgb_img.split(); rgb_img = Image.merge("RGB", (enhancer_bright.enhance(1.1).split()[0], g_img, enhancer_bright.enhance(0.9).split()[2]))
    elif "09" in filter_name: rgb_img = enhancer_color.enhance(1.3); rgb_img = enhancer_bright.enhance(1.1)
    elif "10" in filter_name: rgb_img = enhancer_bright.enhance(0.8); rgb_img = enhancer_contrast.enhance(1.2)
    elif "11" in filter_name: rgb_img = enhancer_color.enhance(0.7); r_img, g_img, b_img = rgb_img.split(); rgb_img = Image.merge("RGB", (r_img, g_img, enhancer_bright.enhance(1.2).split()[2]))
    elif "12" in filter_name: rgb_img = ImageOps.grayscale(rgb_img).convert("RGB")
    elif "13" in filter_name: rgb_img = enhancer_contrast.enhance(0.8); rgb_img = enhancer_bright.enhance(1.1)
    elif "14" in filter_name: rgb_img = enhancer_color.enhance(1.2); r_img, g_img, b_img = rgb_img.split(); rgb_img = Image.merge("RGB", (enhancer_bright.enhance(1.1).split()[0], g_img, b_img))
    elif "15" in filter_name: rgb_img = enhancer_contrast.enhance(1.5)
    elif "16" in filter_name: rgb_img = enhancer_bright.enhance(1.3)
    elif "17" in filter_name: rgb_img = enhancer_color.enhance(0.3); rgb_img = enhancer_contrast.enhance(1.3)
    elif "18" in filter_name: rgb_img = enhancer_color.enhance(1.6); rgb_img = enhancer_contrast.enhance(1.2)
    elif "19" in filter_name: rgb_img = enhancer_contrast.enhance(1.1); r_img, g_img, b_img = rgb_img.split(); rgb_img = Image.merge("RGB", (r_img, enhancer_bright.enhance(1.1).split()[1], b_img))
    elif "20" in filter_name: rgb_img = enhancer_color.enhance(0.8); rgb_img = enhancer_contrast.enhance(1.2)
    return Image.merge("RGBA", (rgb_img.split()[0], rgb_img.split()[1], rgb_img.split()[2], a))

lut_list = ["00. Original", "01. Crisp", "02. Teal", "03. Noir", "04. Punch", "05. Vintage", "06. Pastel", "07. Cyber", "08. Insta", "09. Golden", "10. Dark", "11. Cool", "12. B&W Classic", "13. Matte", "14. Rich", "15. Hard", "16. Airy", "17. Bleach", "18. PopArt", "19. Emerald", "20. Winter"]

# --- UPLOAD ---
uploaded_files = st.file_uploader("Photos upload karein", type=['png', 'jpg', 'jpeg'], accept_multiple_files=True)

if uploaded_files:
    st.markdown("---")
    selected_lut = st.selectbox("Apna LUT (Filter) Select Karein:", options=lut_list)
    st.warning("Balanced Cutout processing ho rahi hai... Isme thoda time lag sakta hai.")
    
    # Simple direct PNG download framework
    for index, file in enumerate(uploaded_files):
        with st.expander(f"📷 Photo {index+1}: {file.name}", expanded=True):
            img = Image.open(file)
            
            with st.spinner(f"Processing Balanced HD: {file.name}..."):
                try:
                    # 🌟 Magic setting to fix edges with mask smoothing (Crash-Proof) 🌟
                    # Maine `post_process_mask=True` apply kiya hai jo edges ko smooth kar dega
                    # bina full alpha matting ke crash-heavy RAM ko use kiye.
                    processed = remove(img, post_process_mask=True)
                    
                    # Apply LUT
                    final = apply_filter(processed, selected_lut)
                    
                    # Show Preview
                    st.image(final, use_container_width=True)
                    
                    # Direct PNG Download Button
                    buf = io.BytesIO()
                    final.save(buf, format='PNG')
                    st.download_button(label=f"💾 Save Ravi_Edit_{index+1}.png", data=buf.getvalue(), file_name=f"Ravi_BalancedHD_{file.name.split('.')[0]}.png", mime="image/png", key=f"btn_{index}")
                except Exception as e:
                    st.error(f"Error in {file.name}: {e}")

# --- FOOTER ---
st.markdown("""
    <div style='text-align: center; margin-top: 50px; padding-top: 20px; border-top: 1px solid #333;'>
        <p style='color: #888888; font-size: 14px;'>Made by <b style='color: #ff4b4b; font-size: 16px;'>RAVI</b></p>
    </div>
""", unsafe_allow_html=True)
