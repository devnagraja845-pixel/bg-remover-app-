import streamlit as st
from rembg import remove
from PIL import Image, ImageEnhance, ImageOps
import io
import zipfile

# --- 1. ULTIMATE REFRESH & SCROLL LOCK (CSS + JS) ---
st.set_page_config(page_title="Pro Studio AI", layout="centered")

# Yeh script phone ko refresh karne se rokega
st.components.v1.html(
    """
    <script>
    window.addEventListener('load', function() {
        var lastY = 0;
        var content = window.document.querySelector('.main');
        window.document.addEventListener('touchstart', function(e) {
            lastY = e.touches[0].clientY;
        }, {passive: false});

        window.document.addEventListener('touchmove', function(e) {
            var currY = e.touches[0].clientY;
            if (currY > lastY && window.scrollY <= 0) {
                // Agar user top par hai aur neeche khinch raha hai, toh block karo
                e.preventDefault();
            }
            lastY = currY;
        }, {passive: false});
    });
    </script>
    """,
    height=0,
)

# --- 2. THEME SELECTION ---
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
    /* Pull-to-refresh block karne ke liye CSS */
    html, body, [data-testid="stAppViewContainer"], .stApp {{
        background-color: {bg_color} !important;
        color: {text_color} !important;
        overscroll-behavior-y: contain !important;
        overscroll-behavior-x: none !important;
        position: fixed;
        width: 100%;
        height: 100%;
        overflow-y: auto;
        -webkit-overflow-scrolling: touch;
    }}
    .stMarkdown p, h1, h2, h3, label {{ color: {text_color} !important; text-align: center; }}
    [data-testid="stFileUploader"] {{ background-color: {card_bg}; border: 2px dashed {accent}; border-radius: 10px; }}
    .stButton>button {{ background-color: {btn_color}; color: white; border-radius: 8px; width: 100%; font-weight: bold; border: none; }}
</style>
""", unsafe_allow_html=True)

# --- 3. MAIN APP LOGIC ---
st.title("✨ Pro Studio V5")
st.markdown(f"<p style='text-align: center;'>Made by <b>RAVI</b></p>", unsafe_allow_html=True)

# --- LUT LOGIC ---
def apply_filter(img, filter_name):
    if img.mode != 'RGBA': img = img.convert('RGBA')
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

lut_list = ["00. Original", "01. Basic Crisp", "02. Cinematic Teal", "03. Moody Noir", "04. Bollywood Punch", "05. Faded Vintage", "06. Soft Pastel", "07. Cyberpunk", "08. Insta Filter", "09. Golden Hour", "10. Dark Knight", "11. Cool Breeze", "12. B&W Classic", "13. Matte Finish", "14. Rich Warmth", "15. Hard Contrast", "16. Bright & Airy", "17. Bleach Bypass", "18. Pop Art Bright", "19. Deep Emerald", "20. Crisp Winter"]

uploaded_files = st.file_uploader("Photos upload karein", type=['png', 'jpg', 'jpeg'], accept_multiple_files=True)

if uploaded_files:
    edit_mode = st.radio("Editing Mode:", ("✂️ Background Remove + LUT", "🎨 Sirf LUT Lagayein"))
    selected_lut = st.selectbox("Select Filter:", options=lut_list)
    
    # Preview
    with st.spinner("Loading Preview..."):
        img = Image.open(uploaded_files[0])
        res = remove(img) if "✂️" in edit_mode else img
        st.image(apply_filter(res, selected_lut), use_container_width=True)

    if st.button("🚀 Save & Download All"):
        zip_buffer = io.BytesIO()
        progress_bar = st.progress(0)
        with zipfile.ZipFile(zip_buffer, "w") as zip_file:
            for index, file in enumerate(uploaded_files):
                img = Image.open(file)
                processed = remove(img, alpha_matting=True) if "✂️" in edit_mode else img.convert("RGBA")
                final = apply_filter(processed, selected_lut)
                buf = io.BytesIO()
                final.save(buf, format='PNG')
                zip_file.writestr(f"Ravi_Edit_{file.name.split('.')[0]}.png", buf.getvalue())
                progress_bar.progress((index + 1) / len(uploaded_files))
        st.download_button("⬇️ Download ZIP", data=zip_buffer.getvalue(), file_name="Ravi_Pro_Studio.zip")

# --- FOOTER ---
st.markdown(f"""
    <div style='text-align: center; margin-top: 50px; padding-top: 20px; border-top: 1px solid {accent}55;'>
        <p style='color: {accent}; font-size: 14px;'>Made by <b style='font-size: 18px;'>RAVI</b></p>
    </div>
""", unsafe_allow_html=True)
