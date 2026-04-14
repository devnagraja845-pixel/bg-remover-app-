import streamlit as st
from rembg import remove
from PIL import Image, ImageEnhance, ImageOps
import io
import zipfile
import numpy as np

# --- PAGE CONFIGURATION (UI Setup) ---
st.set_page_config(page_title="Pro Studio AI - Indian Wedding Editor", layout="wide", initial_sidebar_state="collapsed")

# --- CUSTOM CSS (Making it Beautiful like Editor Apps) ---
# Forced Dark Theme, Styled Buttons, Clean Layout
st.markdown("""
<style>
    /* Main Background */
    [data-testid="stAppViewContainer"] {
        background-color: #121212;
        color: #e0e0e0;
    }
    /* Headers */
    h1, h2, h3, h4 {
        color: #ff9f43 !important; /* Elegant Orange Header */
        font-family: 'Poppins', sans-serif;
        text-align: center;
    }
    /* Paragraphs */
    .stMarkdown p {
        color: #b0b0b0;
        text-align: center;
    }
    /* Buttons */
    .stButton>button {
        background-color: #ff9f43;
        color: #121212;
        font-weight: bold;
        border-radius: 8px;
        border: none;
        width: 100%;
        padding: 12px;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #ffaa5a;
        transform: scale(1.02);
    }
    /* File Uploader Box */
    [data-testid="stFileUploader"] {
        background-color: #1e1e1e;
        border: 2px dashed #ff9f43;
        border-radius: 12px;
        padding: 20px;
    }
    /* Download Button */
    .stDownloadButton>button {
        background-color: #2ecc71; /* Green for download */
        color: white;
    }
    /* Expanders & Other Elements */
    .stExpander {
        background-color: #1e1e1e;
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)

# --- HEADER SECTION ---
st.title("✂️ Pro Studio AI: Background Remover & Color Editor")
st.markdown("Designed for Indian Wedding Photos with perfect hair edges & Professional LUTs.")

# --- STEP 1: IMAGE UPLOAD ---
st.markdown("---")
st.subheader("📸 Step 1: Upload Photos (Max 100)")
uploaded_files = st.file_uploader("", type=['png', 'jpg', 'jpeg'], accept_multiple_files=True)

# --- COLOR FILTER ENGINE (SIMULATED LUTs) ---
# Dictionary defining filter logic (categories of popular looks)
@st.cache_resource
def apply_color_grade(img, filter_name):
    # Convert RGBA (from BG Remover) to RGB temporarily for filtering
    r, g, b, a = img.split()
    rgb_img = Image.merge("RGB", (r, g, b))
    
    if filter_name == "00. Original":
        return img
    
    # --- CINEMATIC & MOODY ---
    elif filter_name == "01. Cinematic Teal & Orange":
        rgb_img = ImageEnhance.Color(rgb_img).enhance(1.2)
        r_img, g_img, b_img = rgb_img.split()
        r_img = ImageEnhance.Contrast(r_img).enhance(1.1)
        b_img = ImageEnhance.Contrast(b_img).enhance(1.0)
        rgb_img = Image.merge("RGB", (r_img, g_img, b_img))
        
    elif filter_name == "02. Moody Noir":
        rgb_img = ImageOps.grayscale(rgb_img)
        rgb_img = ImageEnhance.Contrast(rgb_img).enhance(1.3)
        rgb_img = rgb_img.convert("RGB")
        
    # --- WEDDING & VIBRANT ---
    elif filter_name == "10. Bollywood Punch (Vibrant)":
        rgb_img = ImageEnhance.Color(rgb_img).enhance(1.5)
        rgb_img = ImageEnhance.Contrast(rgb_img).enhance(1.1)
        
    elif filter_name == "11. Soft Pastel Wedding":
        rgb_img = ImageEnhance.Color(rgb_img).enhance(0.9)
        rgb_img = ImageEnhance.Brightness(rgb_img).enhance(1.1)
        
    # --- VINTAGE & RETRO ---
    elif filter_name == "20. Sepia 1970s":
        sepia_matrix = (
            0.393, 0.769, 0.189, 0,
            0.349, 0.686, 0.168, 0,
            0.272, 0.534, 0.131, 0
        )
        rgb_img = rgb_img.convert("RGB", matrix=sepia_matrix)
        rgb_img = ImageEnhance.Contrast(rgb_img).enhance(0.8)

    elif filter_name == "21. Instamatic Retro":
        r_img, g_img, b_img = rgb_img.split()
        r_img = ImageEnhance.Brightness(r_img).enhance(1.1)
        b_img = ImageEnhance.Brightness(b_img).enhance(0.9)
        rgb_img = Image.merge("RGB", (r_img, g_img, b_img))
        rgb_img = ImageEnhance.Color(rgb_img).enhance(1.3)
        
    # --- HIGH-END EDITING ---
    elif filter_name == "30. Classic B&W Portait":
        rgb_img = ImageOps.grayscale(rgb_img)
        rgb_img = rgb_img.convert("RGB")
        
    elif filter_name == "31. Modern Matt":
        rgb_img = ImageEnhance.Contrast(rgb_img).enhance(0.8)
        rgb_img = ImageEnhance.Brightness(rgb_img).enhance(1.05)

    # Reattach original Alpha channel (transparency)
    final_img = Image.merge("RGBA", (rgb_img.split()[0], rgb_img.split()[1], rgb_img.split()[2], a))
    return final_img

# --- LUT DROPDOWN LIST (FRAMEWORK FOR 100+) ---
lut_options = [
    "00. Original",
    "--- CINEMATIC ---", "01. Cinematic Teal & Orange", "02. Moody Noir", "03. Desert Gold", "04. Oceanic Chill",
    "--- WEDDING PRO ---", "10. Bollywood Punch (Vibrant)", "11. Soft Pastel Wedding", "12. Golden Hour Glo", "13. Elegant Blush",
    "--- VINTAGE ---", "20. Sepia 1970s", "21. Instamatic Retro", "22. Faded Film", "23. 1950s Kodachrome",
    "--- BLACK & WHITE ---", "30. Classic B&W Portait", "31. Modern Matt", "32. Silver Gelatin", "33. Heavy Grain"
]

# (Developer Note: 100 filter logic can be added in the `apply_color_grade` function above following these categories.)

if uploaded_files:
    # --- STEP 2: LUT SELECTOR ---
    st.markdown("---")
    st.subheader("🎨 Step 2: Choose Color LUT (Filter)")
    # Column for centering the dropdown
    col_l, col_m, col_r = st.columns([1,2,1])
    with col_m:
        selected_lut = st.selectbox("", options=lut_options, index=0, label_visibility="collapsed")

    # --- MAIN ACTION BUTTON ---
    st.markdown("---")
    if st.button("🚀 Process & Download HD Transparents"):
        
        st.info("AI Hair Cutting (HD) + Color Grading... Isme thoda time lag sakta hai.")
        zip_buffer = io.BytesIO()
        progress_bar = st.progress(0)
        total_files = len(uploaded_files)
        
        with zipfile.ZipFile(zip_buffer, "w") as zip_file:
            for index, uploaded_file in enumerate(uploaded_files):
                try:
                    image = Image.open(uploaded_file)
                    
                    # ✂️ Step A: Background Removal (HD Alpha Matting Mode ON)
                    transparent_image = remove(
                        image, 
                        alpha_matting=True,
                        alpha_matting_foreground_threshold=240,
                        alpha_matting_background_threshold=10,
                        alpha_matting_erode_size=10
                    )
                    
                    # 🎨 Step B: Color Grading (Applying LUT if not original)
                    if selected_lut and "---" not in selected_lut:
                         final_image = apply_color_grade(transparent_image, selected_lut)
                    else:
                         final_image = transparent_image
                    
                    # Save as Lossless PNG
                    img_byte_arr = io.BytesIO()
                    final_image.save(img_byte_arr, format='PNG')
                    zip_file.writestr(f"Pro_{selected_lut.replace(' ','_')}_{uploaded_file.name.split('.')[0]}.png", img_byte_arr.getvalue())
                    
                except Exception as e:
                    st.error(f"Error processing {uploaded_file.name}: {e}")
                progress_bar.progress((index + 1) / total_files)
        
        # --- SUCCESS & DOWNLOAD ---
        st.markdown("---")
        st.success("🎉 HD Photos successfully process ho gayi hain!")
        # Column for centered download button
        dl_l, dl_m, dl_r = st.columns([1,2,1])
        with dl_m:
            st.download_button(label="⬇️ Download All Editor ZIP", data=zip_buffer.getvalue(), file_name="Wedding_HD_Transparent_Photos.zip", mime="application/zip")
