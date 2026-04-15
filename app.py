import streamlit as st
from rembg import remove
from PIL import Image, ImageEnhance, ImageOps
import io

# --- 1. THEME & UI SETTINGS (Sidebar Enabled for Pro Look) ---
# initial_sidebar_state="collapsed" means sidebar exists but is closed by default
st.set_page_config(page_title="Pro Studio AI - Ravi Edition", layout="centered", initial_sidebar_state="collapsed")

# Theme Selection in Sidebar (Restored Pro Features)
st.sidebar.title("⚙️ Settings")
theme_choice = st.sidebar.selectbox("App Theme Select Karein:", ["Classic Dark", "Oceanic Blue", "Clean White"])

# Dynamic CSS for Professional Look (Restored V6 style)
if theme_choice == "Classic Dark":
    bg_color, text_color, card_bg, btn_color, accent = "#121212", "#e0e0e0", "#1e1e1e", "#4a5568", "#ff9f43"
elif theme_choice == "Oceanic Blue":
    bg_color, text_color, card_bg, btn_color, accent = "#0f172a", "#f1f5f9", "#1e293b", "#3b82f6", "#60a5fa"
else: # Clean White
    bg_color, text_color, card_bg, btn_color, accent = "#ffffff", "#1a202c", "#f7fafc", "#3182ce", "#2b6cb0"

st.markdown(f"""
<style>
    /* 🛑 Anti-Refresh for Android 🛑 */
    html, body, [data-testid="stAppViewContainer"], .stApp {{
        background-color: {bg_color} !important;
        color: {text_color} !important;
        overscroll-behavior-y: contain !important;
    }}
    
    /* Professional Layout */
    .stMarkdown p, h1, h2, h3, label, .stSelectbox {{ color: {text_color} !important; text-align: center; font-family: 'Poppins', sans-serif; }}
    
    /* File Uploader Box (Styled) */
    [data-testid="stFileUploader"] {{
        background-color: {card_bg};
        border: 2px dashed {accent};
        border-radius: 10px;
        padding: 10px;
    }}
    
    /* Elegant Buttons with Orange/Accent color */
    .stButton>button {{
        background-color: {accent};
        color: {bg_color} !important;
        border-radius: 8px;
        width: 100%;
        font-weight: bold;
        border: none;
        padding: 12px;
        transition: all 0.3s ease;
    }}
    .stButton>button:hover {{ transform: translateY(-2px); }}
    
    /* Expander/Card Styling */
    .stExpander {{ background-color: {card_bg}; border-radius: 10px; border: 1px solid {accent}33; }}
</style>
""", unsafe_allow_html=True)

# --- 2. COLOR GRAD DEEP ENGINE (Same as V7) ---
@st.cache_resource
def apply_filter(img, filter_name):
    if img.mode != 'RGBA':
        img = img.convert('RGBA')
    r, g, b, a = img.split()
    rgb_img = Image.merge("RGB", (r, g, b))
    enhancer_color = ImageEnhance.Color(rgb_img)
    enhancer_contrast = ImageEnhance.Contrast(rgb_img)
    enhancer_bright = ImageEnhance.Brightness(rgb_img)
    
    if "01" in filter_name: rgb_img = enhancer_contrast.enhance(1.2)
    elif "02" in filter_name: rgb_img = enhancer_color.enhance(1.4); rgb_img = enhancer_contrast.enhance(1.1)
    elif "03" in filter_name: rgb_img = ImageOps.grayscale(rgb_img).convert("RGB"); rgb_img = enhancer_contrast.enhance(1.3)
    elif "04" in filter_name: rgb_img = enhancer_color.enhance(1.5)
    
    return Image.merge("RGBA", (rgb_img.split()[0], rgb_img.split()[1], rgb_img.split()[2], a))

lut_list = ["00. Original", "01. Basic Crisp", "02. Cinematic Teal", "03. Moody Noir", "04. Bollywood Punch"]

# --- 3. MAIN APP LOGIC ---
st.title("✨ Pro Studio AI")
st.markdown("<p style='text-align: center; color: #a0aec0;'>HD Cutout + Color Grading - Ravi Edition</p>", unsafe_allow_html=True)

# User advice about limitations
st.info("Portait Photos par best results milega. Complex Graphics par AI struggling karega.")

uploaded_files = st.file_uploader("Photos upload karein", type=['png', 'jpg', 'jpeg'], accept_multiple_files=True)

if uploaded_files:
    edit_mode = st.radio("Editing Mode Select Karein:", ("✂️ Background Remove + LUT", "🎨 Sirf LUT Lagayein (No Cutout)"))
    selected_lut = st.selectbox("Select Color Filter:", options=lut_list)
    st.markdown("---")
    
    # Process Photos Centered
    col_l, col_m, col_r = st.columns([1,3,1])
    with col_m:
        st.subheader("Processing Your Photos")
        
    for index, file in enumerate(uploaded_files):
        with st.expander(f"📷 Photo {index+1}: {file.name}", expanded=True):
            img = Image.open(file)
            
            with st.spinner(f"Processing..."):
                try:
                    # RAM bachane ke liye simple, crash-proof logic
                    if "✂️" in edit_mode:
                        # Direct, fast, standard cutout. 
                        # HD features are disabled for stability on complex graphics.
                        processed = remove(img) 
                    else:
                        processed = img.convert("RGBA")
                    
                    # Apply Filter
                    final = apply_filter(processed, selected_lut)
                    
                    # Show Preview
                    st.image(final, use_container_width=True)
                    
                    # Direct PNG Download Button
                    buf = io.BytesIO()
                    final.save(buf, format='PNG')
                    st.download_button(label=f"💾 Save Ravi_Edit_{index+1}.png", data=buf.getvalue(), file_name=f"Ravi_Pro_Studio_{index+1}.png", mime="image/png", key=f"btn_{index}")
                except Exception as e:
                    st.error(f"Error in {file.name}: {e}")

# --- FOOTER (MADE BY RAVI) ---
# Footer with elegant design and Ravi name
st.markdown(f"""
    <div style='text-align: center; margin-top: 50px; padding-top: 20px; border-top: 1px solid {accent}33;'>
        <p style='color: #888888; font-size: 14px;'>Made by <b style='color: {accent}; font-size: 18px;'>RAVI</b></p>
    </div>
""", unsafe_allow_html=True)
