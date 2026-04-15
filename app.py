import streamlit as st
from rembg import remove
from PIL import Image, ImageEnhance, ImageOps, ImageFilter, ImageDraw, ImageFont
import urllib.request
import io
import os

# --- 1. UI SETUP ---
st.set_page_config(page_title="Pro Studio", layout="centered", initial_sidebar_state="expanded")

st.markdown("""
<style>
    html, body, [data-testid="stAppViewContainer"], .stApp { background-color: #0e1117 !important; color: #ffffff !important; overscroll-behavior-y: contain !important; }
    .stMarkdown p, h1, h2, h3, label { color: #ffffff !important; text-align: center; }
    .stButton>button { background-color: #ff4b4b; color: white !important; border-radius: 8px; width: 100%; font-weight: bold; border: none; padding: 12px; }
    [data-testid="stFileUploader"] { background-color: #1e1e1e; border: 2px dashed #ff4b4b; border-radius: 10px; }
</style>
""", unsafe_allow_html=True)

# 🌟 Main App Name Changed as Requested 🌟
st.title("🚀 Pro Studio")
st.markdown("<p style='text-align: center; color: #a0aec0;'>The Ultimate YouTube Thumbnail Maker</p>", unsafe_allow_html=True)

# --- FONT DOWNLOADER (For Professional Text) ---
@st.cache_resource
def get_font(size):
    font_path = "Roboto-Black.ttf"
    if not os.path.exists(font_path):
        try:
            url = "https://github.com/googlefonts/roboto/raw/main/src/hinted/Roboto-Black.ttf"
            urllib.request.urlretrieve(url, font_path)
        except: pass
    try: return ImageFont.truetype(font_path, size)
    except: return ImageFont.load_default()

# --- LUTS LOGIC ---
def apply_filter(img, filter_name):
    if img.mode != 'RGBA': img = img.convert('RGBA')
    if "00" in filter_name: return img
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

# --- SIDEBAR SETTINGS ---
st.sidebar.title("🛠️ Project Settings")
selected_lut = st.sidebar.selectbox("🎨 Global Filter (LUT):", options=lut_list)
st.sidebar.markdown("---")
size_preset = st.sidebar.selectbox("📏 Canvas Size:", ["YouTube Thumbnail (16:9)", "Shorts/Reels (9:16)", "Instagram Post (1:1)", "Original Size"])
st.sidebar.markdown("---")
bg_type = st.sidebar.radio("🖼️ Background Style:", ["Transparent", "Solid Color", "Custom Image"])
bg_color = st.sidebar.color_picker("Pick Color:", "#121212") if bg_type == "Solid Color" else None
bg_image_file = st.sidebar.file_uploader("Upload BG Image:", type=['jpg', 'png']) if bg_type == "Custom Image" else None

# --- CORE ADVANCED COMPOSE LOGIC ---
def get_target_size(original_size, preset):
    if preset == "Original Size": return original_size
    sizes = {"YouTube Thumbnail (16:9)": (1280, 720), "Shorts/Reels (9:16)": (1080, 1920), "Instagram Post (1:1)": (1080, 1080)}
    return sizes[preset]

def advanced_compose(subject, bg_type, color, bg_img_file, target_size, scale, offset_x, offset_y, bright, shadow, flip, stroke, stroke_color, text, txt_color, txt_size, txt_x, txt_y, txt_stroke_w, txt_stroke_c):
    W, H = target_size
    
    # 1. Background
    if bg_type == "Solid Color": base = Image.new("RGBA", (W, H), color)
    elif bg_type == "Custom Image" and bg_img_file: base = Image.open(bg_img_file).convert("RGBA").resize((W, H), Image.Resampling.LANCZOS)
    else: base = Image.new("RGBA", (W, H), (255, 255, 255, 0))
        
    # 2. Subject Edits
    if flip: subject = ImageOps.mirror(subject)
    if bright != 100: subject = ImageEnhance.Brightness(subject).enhance(bright / 100.0)

    # 3. Add Stroke (Subject Outline)
    if stroke:
        alpha = subject.split()[3]
        stroke_mask = alpha.filter(ImageFilter.MaxFilter(9))
        stroke_img = Image.new('RGBA', subject.size, stroke_color)
        stroke_img.putalpha(stroke_mask)
        stroke_img.paste(subject, (0,0), subject)
        subject = stroke_img

    # 4. Resize Subject
    ratio = min(W * 0.8 / subject.width, H * 0.8 / subject.height)
    new_w, new_h = int(subject.width * ratio * scale), int(subject.height * ratio * scale)
    if new_w <= 0 or new_h <= 0: return base 
    subject_resized = subject.resize((new_w, new_h), Image.Resampling.LANCZOS)
    
    paste_x = (W - new_w) // 2 + offset_x
    paste_y = (H - new_h) // 2 + offset_y
    
    # 5. Drop Shadow
    if shadow:
        r, g, b, a = subject_resized.split()
        black = Image.new('L', a.size, 0)
        shadow_img = Image.merge('RGBA', (black, black, black, a)).filter(ImageFilter.GaussianBlur(15))
        base.paste(shadow_img, (paste_x + 15, paste_y + 15), shadow_img) 

    # 6. Paste Subject
    base.paste(subject_resized, (paste_x, paste_y), subject_resized)

    # 7. ADD TEXT (With Outline & Shadow) 🌟
    if text:
        draw = ImageDraw.Draw(base)
        font = get_font(txt_size)
        # Text Shadow (Drop Shadow for extra depth)
        draw.text((txt_x + 5, txt_y + 5), text, font=font, fill="black")
        # Main Text with Stroke (Outline)
        draw.text((txt_x, txt_y), text, font=font, fill=txt_color, stroke_width=txt_stroke_w, stroke_fill=txt_stroke_c)

    return base

# --- MAIN UPLOAD AREA ---
uploaded_files = st.file_uploader("Photos upload karein", type=['png', 'jpg', 'jpeg'], accept_multiple_files=True)

if uploaded_files:
    edit_mode = st.checkbox("✂️ Remove Background", value=True)
    
    for index, file in enumerate(uploaded_files):
        st.markdown("---")
        st.subheader(f"🎬 Editing: {file.name}")
        
        img = Image.open(file)
        target_size = get_target_size(img.size, size_preset)
        
        with st.spinner("Preparing AI Canvas..."):
            processed_subject = remove(img) if edit_mode else img.convert("RGBA")
        
        # --- TABBED INTERFACE ---
        tab1, tab2, tab3 = st.tabs(["📸 Subject Tools", "✨ Effects", "📝 Add Text"])
        
        with tab1: # Position & Size
            c1, c2 = st.columns(2)
            with c1: scale_val = st.slider(f"🔍 Size (%)", 10, 200, 100, key=f"s_{index}") / 100.0
            with c2: flip_val = st.checkbox(f"↔️ Flip Subject (Mirror)", key=f"f_{index}")
            
            c3, c4 = st.columns(2)
            with c3: x_val = st.slider(f"↔️ Left/Right", -1000, 1000, 0, key=f"x_{index}")
            with c4: y_val = st.slider(f"↕️ Up/Down", -1000, 1000, 0, key=f"y_{index}")
                
        with tab2: # Magic Effects
            c5, c6 = st.columns(2)
            with c5: bright_val = st.slider(f"☀️ Brightness", 50, 150, 100, key=f"b_{index}")
            with c6: shadow_val = st.checkbox(f"🌑 Add Drop Shadow", value=True, key=f"sh_{index}")
            
            stroke_val = st.checkbox("🔥 Add Thumbnail Outline (Stroke)", key=f"str_{index}")
            stroke_color = st.color_picker("Outline Color", "#ffffff", key=f"strc_{index}") if stroke_val else "#ffffff"

        with tab3: # Text Tool 🌟
            user_text = st.text_input("✍️ Yahan Text Likhein:", "", key=f"t_{index}")
            if user_text:
                tc1, tc2 = st.columns(2)
                with tc1: txt_color = st.color_picker("Text Color", "#ffd700", key=f"tc_{index}")
                with tc2: txt_size = st.slider("Text Size", 20, 300, 100, key=f"ts_{index}")
                
                # New Outline Features
                tc3, tc4 = st.columns(2)
                with tc3: txt_stroke_w = st.slider("Text Outline Motaai", 0, 15, 4, key=f"tsw_{index}")
                with tc4: txt_stroke_c = st.color_picker("Text Outline Color", "#000000", key=f"tsc_{index}")
                
                tx_val = st.slider("↔️ Text Left/Right", 0, target_size[0], int(target_size[0]/4), key=f"tx_{index}")
                ty_val = st.slider("↕️ Text Up/Down", 0, target_size[1], int(target_size[1]/8), key=f"ty_{index}")
            else:
                txt_color, txt_size, tx_val, ty_val = "#ffffff", 50, 0, 0
                txt_stroke_w, txt_stroke_c = 0, "#000000"

        # Composition & Render
        composed_img = advanced_compose(processed_subject, bg_type, bg_color, bg_image_file, target_size, scale_val, x_val, y_val, bright_val, shadow_val, flip_val, stroke_val, stroke_color, user_text, txt_color, txt_size, tx_val, ty_val, txt_stroke_w, txt_stroke_c)
        final_img = apply_filter(composed_img, selected_lut)
        
        st.markdown("### 👁️ Live Preview")
        st.image(final_img, use_container_width=True)
        
        # Download
        buf = io.BytesIO()
        final_img.save(buf, format='PNG')
        st.download_button(label="💾 Download Final Thumbnail", data=buf.getvalue(), file_name=f"ProStudio_Thumbnail_{index+1}.png", mime="image/png", key=f"dl_{index}")

st.markdown("""
    <div style='text-align: center; margin-top: 50px; padding-top: 20px; border-top: 1px solid #333;'>
        <p style='color: #888888; font-size: 14px;'>Made by <b style='color: #ff4b4b; font-size: 18px;'>RAVI</b></p>
    </div>
""", unsafe_allow_html=True)
