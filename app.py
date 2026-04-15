import streamlit as st
from rembg import remove
from PIL import Image, ImageEnhance, ImageOps
import io

# --- 1. THEME & UI SETTINGS (Sidebar Enabled) ---
st.set_page_config(page_title="Pro Studio AI - Ravi Edition", layout="centered", initial_sidebar_state="collapsed")

# Theme Selection in Sidebar
st.sidebar.title("⚙️ Settings")
theme_choice = st.sidebar.selectbox("App Theme Select Karein:", ["Classic Blue", "Dark Grey", "Clean White"])

# Dynamic CSS for Professional Look
if theme_choice == "Classic Blue":
    bg_color, text_color, card_bg, btn_color, accent = "#0f172a", "#f1f5f9", "#1e293b", "#3b82f6", "#60a5fa"
elif theme_choice == "Dark Grey":
    bg_color, text_color, card_bg, btn_color, accent = "#121212", "#e0e0e0", "#1e1e1e", "#4a5568", "#a0aec0"
else:
    bg_color, text_color, card_bg, btn_color, accent = "#ffffff", "#1a202c", "#f7fafc", "#3182ce", "#2b6cb0"

st.markdown(f"""
<style>
    /* Professional Layout */
    html, body, [data-testid="stAppViewContainer"], .stApp {{
        background-color: {bg_color} !important;
        color: {text_color} !important;
        overscroll-behavior-y: contain !important;
    }}
    .stMarkdown p, h1, h2, h3, label, .stSelectbox {{ color: {text_color} !important; text-align: center; font-family: 'Poppins', sans-serif; }}
    
    /* File Uploader Box */
    [data-testid="stFileUploader"] {{
        background-color: {card_bg};
        border: 2px dashed {accent};
        border-radius: 10px;
        padding: 10px;
    }}
    
    /* Elegant Buttons */
    .stButton>button {{
        background-color: {btn_color};
        color: white !important;
        border-radius: 8px;
        width: 100%;
        font-weight: bold;
        border: none;
        padding: 12px;
        transition: all 0.3s ease;
    }}
    .stButton>button:hover {{ background-color: {accent}; transform: translateY(-2px); }}
    
    /* Photo Card Styling */
    .stExpander {{ background-color: {card_bg}; border-radius: 10px; border: 1px solid {accent}33; }}
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {{ background-color: {card_bg} !important; border-right: 1px solid {accent}33; }}
</style>
""", unsafe_allow_html=True)

# --- 2. COLOR GRAD DEEP ENGINE (LUT Logic) ---
@st.cache_resource
def apply_filter(img, filter_name):
    if img.mode != 'RGBA':
        img = img.convert('RGBA')
    r, g, b, a = img.split()
    rgb_img = Image.merge("RGB", (r, g, b))
    
    enhancer_color = ImageEnhance.Color(rgb_img)
    enhancer_contrast = ImageEnhance.Contrast(rgb_img)
    enhancer_bright = ImageEnhance.Brightness(rgb_img)

    if filter_name == "00. Original": return img
    
    # Simple Color Matrices/Adjustments mimicking LUTs
    if "01" in filter_name: rgb_img = enhancer_contrast.enhance(1.2); rgb_img = enhancer_color.enhance(1.1)
    elif "02" in filter_name: rgb_img = enhancer_color.enhance(1.4); rgb_img = enhancer_contrast.enhance(1.1)
    elif "03" in filter_name: rgb_img = ImageOps.grayscale(rgb_img).convert("RGB"); rgb_img = enhancer_contrast.enhance(1.3)
    elif "04" in filter_name: rgb_img = enhancer_color.enhance(1.5)
    elif "05" in filter_name: rgb_img = enhancer_color.enhance(0.5); rgb_img = enhancer_contrast.enhance(0.8)
    elif "06" in filter_name: rgb_img = enhancer_bright.enhance(1.2); rgb_img = enhancer_color.enhance(0.8)
    elif "07" in filter_name: rgb_img = enhancer_contrast.enhance(1.4); rgb_img = enhancer_color.enhance(1.2)
    elif "08" in filter_name: 
        # Fake Teal & Orange
        r_img, g_img, b_img = rgb_img.split()
        r_img = ImageEnhance.Brightness(r_img).enhance(1.1)
        b_img = ImageEnhance.Brightness(b_img).enhance(0.9)
        rgb_img = Image.merge("RGB", (r_img, g_img, b_img))
        rgb_img = enhancer_color.enhance(1.3)
    elif "09" in filter_name: rgb_img = enhancer_color.enhance(1.3); rgb_img = enhancer_bright.enhance(1.1)
    elif "10" in filter_name: rgb_img = enhancer_bright.enhance(0.8); rgb_img = enhancer_contrast.enhance(1.2)
    
    # Reattach Alpha channel for transparency
    final_img = Image.merge("RGBA", (rgb_img.split()[0], rgb_img.split()[1], rgb_img.split()[2], a))
    return final_img

lut_list = ["00. Original", "01. Basic Crisp", "02. Cinematic Teal", "03. Moody Noir", "04. Bollywood Punch", "05. Faded Vintage", "06. Soft Pastel", "07. Cyberpunk", "08. Insta Filter", "09. Golden Hour", "10. Dark Knight"]

# --- 3. MAIN APP LOGIC ---
st.title("✨ Pro Studio AI")
st.markdown(f"<p style='text-align: center; color: #a0aec0;'>HD Cutout + Color Grading - {theme_choice}</p>", unsafe_allow_html=True)

# Important Note for User
st.warning("Note: Complex edges (baalon) ko smooth karne ke liye AI 'HD mode' use kar raha hai. Processing mein har photo par 5-10 second extra lag sakte hain. Please wait karein.")

uploaded_files = st.file_uploader("Photos upload karein (High Quality Photos par best result milega)", type=['png', 'jpg', 'jpeg'], accept_multiple_files=True)

if uploaded_files:
    edit_mode = st.radio("Editing Mode Select Karein:", ("✂️ HD Background Remove + LUT (Clean Edges)", "🎨 Sirf LUT Lagayein (No Cutout)"))
    selected_lut = st.selectbox("Select Color Filter:", options=lut_list)
    
    # Layout with columns for centered processing info
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.markdown("---")
        st.subheader("Processing Photos")
        
    for index, file in enumerate(uploaded_files):
        with st.expander(f"📷 Photo {index+1}: {file.name}", expanded=True):
            img = Image.open(file)
            
            with st.spinner(f"HD Processing: {file.name} (Waiting for clean hair edges)..."):
                try:
                    if "✂️" in edit_mode:
                        # 🌟 MAGIC HAPPENS HERE: HD ALPHA MATTING ENABLED & FINE-TUNED 🌟
                        # foreground_threshold=240, background_threshold=10, erode_size=10
                        # These specific parameters force the AI to smoothly handle complex edges like hair.
                        processed = remove(
                            img, 
                            alpha_matting=True,
                            alpha_matting_foreground_threshold=240,
                            alpha_matting_background_threshold=10,
                            alpha_matting_erode_size=10
                        )
                    else:
                        processed = img.convert("RGBA")
                    
                    # Apply Filter
                    final = apply_filter(processed, selected_lut)
                    
                    # Show Preview
                    st.image(final, use_container_width=True)
                    
                    # Direct PNG Download Button
                    buf = io.BytesIO()
                    final.save(buf, format='PNG')
                    byte_im = buf.getvalue()
                    
                    st.download_button(
                        label=f"💾 Save Ravi_Edit_{index+1}.png",
                        data=byte_im,
                        file_name=f"Ravi_Studio_HD_{index+1}.png",
                        mime="image/png",
                        key=f"btn_{index}"
                    )
                except Exception as e:
                    st.error(f"Error processing {file.name}: {e}")

# --- FOOTER (MADE BY RAVI) ---
st.markdown(f"""
    <div style='text-align: center; margin-top: 50px; padding-top: 20px; border-top: 1px solid {accent}55;'>
        <p style='color: #888888; font-size: 14px;'>Made by <b style='color: #ff4b4b; font-size: 18px;'>RAVI</b></p>
    </div>
""", unsafe_allow_html=True)
