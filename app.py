import streamlit as st
from rembg import remove
from PIL import Image
import io
import zipfile

st.set_page_config(page_title="Pro BG Remover HD", layout="wide")
st.title("✂️ Bulk Background Remover (HD Mode)")
st.write("Isme Alpha Matting ON hai - Baalon (hair) aur barik kinaro ki cutting ekdum smooth aur HD hogi.")

uploaded_files = st.file_uploader("Apni HD photos yahan upload karein", type=['png', 'jpg', 'jpeg'], accept_multiple_files=True)

if uploaded_files:
    if st.button("✨ HD Background Remove Karein"):
        st.info("High-Quality AI Processing chal rahi hai... Isme pehle se thoda zyada time lagega.")
        zip_buffer = io.BytesIO()
        progress_bar = st.progress(0)
        total_files = len(uploaded_files)
        
        with zipfile.ZipFile(zip_buffer, "w") as zip_file:
            for index, uploaded_file in enumerate(uploaded_files):
                try:
                    # Photo original size me open hogi
                    image = Image.open(uploaded_file)
                    
                    # 🌟 MAGIC HAPPENS HERE: Alpha Matting ON kar diya hai 🌟
                    output_image = remove(
                        image, 
                        alpha_matting=True,
                        alpha_matting_foreground_threshold=240,
                        alpha_matting_background_threshold=10,
                        alpha_matting_erode_size=10
                    )
                    
                    # Lossless PNG me save karega taaki quality kam na ho
                    img_byte_arr = io.BytesIO()
                    output_image.save(img_byte_arr, format='PNG')
                    zip_file.writestr(f"HD_nobg_{uploaded_file.name.split('.')[0]}.png", img_byte_arr.getvalue())
                except Exception as e:
                    st.error(f"Error processing {uploaded_file.name}: {e}")
                progress_bar.progress((index + 1) / total_files)
        
        st.success("🎉 HD Photos successfully process ho gayi hain!")
        st.download_button(label="⬇️ Download HD Photos (ZIP)", data=zip_buffer.getvalue(), file_name="HD_Transparent_Photos.zip", mime="application/zip")
