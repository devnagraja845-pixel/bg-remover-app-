import streamlit as st
from rembg import remove
from PIL import Image, ImageEnhance, ImageOps
import io

# --- 1. UI & THEME SETUP ---
st.set_page_config(page_title="Pro Studio AI - Ravi Edition", layout="centered", initial_sidebar_state="expanded")

# Sidebar for Professional Settings
st.sidebar.title("🛠️ Studio Settings")
theme_choice = st.sidebar.selectbox("App Theme:", ["Classic Dark", "Oceanic Blue", "Clean White"])

# --- NEW FEATURES IN SIDEBAR ---
st.sidebar.markdown("---")
st.sidebar.subheader("📐 1. Auto-Resizer")
size_preset = st.sidebar.selectbox("Social Media Size:", 
    ["Original Size", "YouTube Thumbnail (16:9)", "Shorts/Reels (9:16)", "Instagram Post (1:1)"])

st.sidebar.markdown("---")
st.sidebar.subheader("📝 2. Bulk Renamer")
file_prefix = st.sidebar.text_input("File Naam Prefix:", "Ravi_Studio")

st.sidebar.markdown("---")
st.sidebar.subheader("🖼️ 3. Background Settings")
bg_type = st.sidebar.radio("Background Style:", ["Transparent", "Solid Color", "Custom Image"])
bg_color = st.sidebar.color_picker("Pick Color:", "#ffffff") if bg_type == "Solid Color" else None
bg_image_file = st.sidebar.file_uploader("Upload BG Image:", type=['jpg', 'png', 'jpeg']) if bg_type == "Custom Image" else None

# Theme CSS
if theme_choice == "Classic Dark":
    bg_c, txt_c, card_c, btn_c, acc = "#121212", "#e0e0e0", "#1e1e1e", "#4a5568", "#ff9f43"
elif theme_choice == "Oceanic Blue":
    bg_c, txt_c, card_c, btn_c, acc = "#0f172a", "#f1f5f9", "#1e293b", "#3b82f6", "#60a5fa"
else:
    bg_c, txt_c, card_c, btn_c, acc = "#ffffff", "#1a202c", "#f7fafc", "#3182ce", "#2b6cb0"

st.markdown(f"""
<style>
    html, body, [data-testid="stAppViewContainer"], .stApp {{ background-color: {bg_c} !important; color: {txt_c} !important; overscroll-behavior-y: contain !important; }}
    .stMarkdown p, h1, h2, h3, label {{ color: {txt_c} !important; text-align: center; }}
    .stButton>button {{ background-color: {acc}; color: {bg_c} !important; border-radius: 8px; width: 100%; font-weight: bold; border: none; padding: 12px; }}
    [data-testid="stFileUploader"] {{ background-color: {card_c}; border: 2px dashed {acc}; border-radius: 10px; }}
</style>
""", unsafe_allow_html=True)

# --- HELPER FUNCTIONS ---
def resize_image(img, preset):
    if preset == "Original Size": return img
    target_sizes = {"YouTube Thumbnail (16:9)": (1280, 720), "Shorts/Reels (9:16)": (1080, 1920), "Instagram Post (1:1)": (1080, 1080)}
    target_size = target_sizes[preset]
    # Resize keeping aspect ratio (fit/pad)
    img.thumbnail(target_size, Image.Resampling.LANCZOS)
    new_img = Image.new("RGBA", target_size, (0, 0, 0, 0))
    new_img.paste(img, ((target_size[0] - img.size[0]) // 2, (target_size[1] - img.size[1]) // 2))
    return new_img

def apply_background(subject, bg_type, color, bg_img_file):
    final_w, final_h = subject.size
    if bg_type == "Transparent": return subject
    
    if bg_type == "Solid Color":
        base = Image.new("RGBA", (final_w, final_h), color)
    else: # Custom Image
        if bg_img_file:
            bg_img = Image.open(bg_img_file).convert("RGBA").resize((final_w, final_h), Image.Resampling.LANCZOS)
            base = bg_img
        else:
            base = Image.new("RGBA", (final_w, final_h), (255, 255, 255, 255))
    
    base.paste(subject, (0, 0), subject)
    return base

# --- MAIN APP ---
st.title("🚀 Ravi Creator Studio")
st.markdown(f"<p style='text-align: center;'>All-in-One Image Production Tool</p>", unsafe_allow_html=True)

uploaded_files = st.file_uploader("Photos upload karein (Social Media ya Projects ke liye)", type=['png', 'jpg', 'jpeg'], accept_multiple_files=True)

if uploaded_files:
    edit_mode = st.checkbox("✂️ Remove Background", value=True)
    st.markdown("---")
    
    for index, file in enumerate(uploaded_files):
        with st.expander(f"🎬 Editing: {file.name}", expanded=True):
            img = Image.open(file)
            
            with st.spinner("Processing..."):
                # 1. Background Removal
                processed = remove(img) if edit_mode else img.convert("RGBA")
                
                # 2. Resize according to Preset
                resized = resize_image(processed, size_preset)
                
                # 3. Apply Background Style
                final = apply_background(resized, bg_type, bg_color, bg_image_file)
                
                # Show Preview
                st.image(final, use_container_width=True)
                
                # 4. Download with Custom Naming
                buf = io.BytesIO()
                final.save(buf, format='PNG')
                st.download_button(
                    label=f"💾 Save {file_prefix}_{index+1}.png",
                    data=buf.getvalue(),
                    file_name=f"{file_prefix}_{index+1}.png",
                    mime="image/png",
                    key=f"dl_{index}"
                )

# --- FOOTER ---
st.markdown(f"""
    <div style='text-align: center; margin-top: 50px; padding-top: 20px; border-top: 1px solid {acc}33;'>
        <p style='color: #888888; font-size: 14px;'>Made by <b style='color: {acc}; font-size: 18px;'>RAVI</b></p>
    </div>
""", unsafe_allow_html=True)
