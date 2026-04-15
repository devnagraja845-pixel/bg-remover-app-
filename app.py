import streamlit as st
from rembg import remove
from PIL import Image
import io

# --- 1. UI SETUP ---
st.set_page_config(page_title="Ravi Pro Editor", layout="centered", initial_sidebar_state="expanded")

# Theme CSS
st.markdown("""
<style>
    html, body, [data-testid="stAppViewContainer"], .stApp { background-color: #0e1117 !important; color: #ffffff !important; overscroll-behavior-y: contain !important; }
    .stMarkdown p, h1, h2, h3, label { color: #ffffff !important; text-align: center; }
    .stButton>button { background-color: #ff4b4b; color: white !important; border-radius: 8px; width: 100%; font-weight: bold; border: none; padding: 12px; }
    [data-testid="stFileUploader"] { background-color: #1e1e1e; border: 2px dashed #ff4b4b; border-radius: 10px; }
</style>
""", unsafe_allow_html=True)

st.title("🚀 Ravi Pro Editor")
st.markdown("<p style='text-align: center;'>Advanced Size & Position Control</p>", unsafe_allow_html=True)

# --- 2. SIDEBAR SETTINGS ---
st.sidebar.title("🛠️ Project Settings")

st.sidebar.subheader("📏 1. Canvas Size")
size_preset = st.sidebar.selectbox("Social Media Size:", 
    ["YouTube Thumbnail (16:9)", "Shorts/Reels (9:16)", "Instagram Post (1:1)", "Original Size"])

st.sidebar.markdown("---")
st.sidebar.subheader("🖼️ 2. Background")
bg_type = st.sidebar.radio("Background Style:", ["Transparent", "Solid Color", "Custom Image"])
bg_color = st.sidebar.color_picker("Pick Color:", "#ff4b4b") if bg_type == "Solid Color" else None
bg_image_file = st.sidebar.file_uploader("Upload BG Image:", type=['jpg', 'png']) if bg_type == "Custom Image" else None

# --- CORE LOGIC ---
def get_target_size(original_size, preset):
    if preset == "Original Size": return original_size
    sizes = {"YouTube Thumbnail (16:9)": (1280, 720), "Shorts/Reels (9:16)": (1080, 1920), "Instagram Post (1:1)": (1080, 1080)}
    return sizes[preset]

def advanced_compose(subject, bg_type, color, bg_img_file, target_size, scale, offset_x, offset_y):
    W, H = target_size
    
    # 1. Create Canvas Background
    if bg_type == "Solid Color":
        base = Image.new("RGBA", (W, H), color)
    elif bg_type == "Custom Image" and bg_img_file:
        bg = Image.open(bg_img_file).convert("RGBA")
        # Resize BG to fill canvas
        bg = bg.resize((W, H), Image.Resampling.LANCZOS)
        base = bg
    else:
        base = Image.new("RGBA", (W, H), (255, 255, 255, 0)) # Transparent
        
    # 2. Resize Subject Foreground (with Slider Scale)
    # Default scale is calculated to fit 80% of canvas
    ratio = min(W * 0.8 / subject.width, H * 0.8 / subject.height)
    new_w = int(subject.width * ratio * scale)
    new_h = int(subject.height * ratio * scale)
    
    # Prevent crashing on 0 size
    if new_w <= 0 or new_h <= 0: return base 
    
    subject_resized = subject.resize((new_w, new_h), Image.Resampling.LANCZOS)
    
    # 3. Calculate Position (Center + Slider Offsets)
    paste_x = (W - new_w) // 2 + offset_x
    paste_y = (H - new_h) // 2 + offset_y
    
    # 4. Paste Subject
    base.paste(subject_resized, (paste_x, paste_y), subject_resized)
    return base

# --- MAIN UPLOAD AREA ---
uploaded_files = st.file_uploader("Photos upload karein", type=['png', 'jpg', 'jpeg'], accept_multiple_files=True)

if uploaded_files:
    edit_mode = st.checkbox("✂️ Remove Background", value=True)
    
    for index, file in enumerate(uploaded_files):
        st.markdown("---")
        st.subheader(f"🎬 Studio Editor: {file.name}")
        
        img = Image.open(file)
        target_size = get_target_size(img.size, size_preset)
        
        # Initial Processing (Heavy task done once)
        with st.spinner("Cutting Background..."):
            processed_subject = remove(img) if edit_mode else img.convert("RGBA")
        
        # 🎛️ ADVANCED EDITOR PANEL (Sliders)
        st.write("🎛️ **Position & Size Controller**")
        col1, col2, col3 = st.columns(3)
        with col1:
            scale_val = st.slider(f"🔍 Size (%)", 10, 200, 100, key=f"scale_{index}") / 100.0
        with col2:
            x_val = st.slider(f"↔️ Left/Right", -1000, 1000, 0, key=f"x_{index}")
        with col3:
            y_val = st.slider(f"↕️ Up/Down", -1000, 1000, 0, key=f"y_{index}")
            
        # Real-time Composition
        final_img = advanced_compose(processed_subject, bg_type, bg_color, bg_image_file, target_size, scale_val, x_val, y_val)
        
        # Show Preview
        st.image(final_img, use_container_width=True)
        
        # Download
        buf = io.BytesIO()
        final_img.save(buf, format='PNG')
        st.download_button(
            label=f"💾 Save Final Image",
            data=buf.getvalue(),
            file_name=f"Ravi_Masterpiece_{index+1}.png",
            mime="image/png",
            key=f"dl_{index}"
        )

# --- FOOTER ---
st.markdown("""
    <div style='text-align: center; margin-top: 50px; padding-top: 20px; border-top: 1px solid #333;'>
        <p style='color: #888888; font-size: 14px;'>Made by <b style='color: #ff4b4b; font-size: 18px;'>RAVI</b></p>
    </div>
""", unsafe_allow_html=True)
