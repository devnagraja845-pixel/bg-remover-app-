import streamlit as st
from rembg import remove
from PIL import Image
import io
import zipfile

# Website ki setting
st.set_page_config(page_title="Bulk BG Remover - Pro Studio", layout="wide")
st.title("✂️ Bulk Background Remover")
st.write("Ek sath 1 se 100 images upload karein. Deep Learning AI automatically baalon (hair) aur complex edges ko clean kar dega.")

# File uploader (Multiple files allow karne ke liye)
uploaded_files = st.file_uploader(
    "Apni wedding photos yahan drag & drop karein (Max 100)", 
    type=['png', 'jpg', 'jpeg'], 
    accept_multiple_files=True
)

if uploaded_files:
    # Limit check karna (taaki memory overload na ho)
    if len(uploaded_files) > 100:
        st.error("Kripya ek baar me maximum 100 photos hi upload karein.")
    else:
        if st.button("✨ Background Remove Karein"):
            st.info("AI Processing start ho chuki hai... Isme thoda time lag sakta hai.")
            
            # Processed images ko ek ZIP file me pack karne ke liye buffer
            zip_buffer = io.BytesIO()
            
            # Progress bar
            progress_bar = st.progress(0)
            total_files = len(uploaded_files)
            
            with zipfile.ZipFile(zip_buffer, "w") as zip_file:
                for index, uploaded_file in enumerate(uploaded_files):
                    try:
                        # Original image read karein
                        image = Image.open(uploaded_file)
                        
                        # Background remove karein (Rembg uses U-2-Net for perfect hair masking)
                        output_image = remove(image)
                        
                        # Output image ko bytes me convert karein
                        img_byte_arr = io.BytesIO()
                        output_image.save(img_byte_arr, format='PNG')
                        
                        # Image ko ZIP file me add karein
                        zip_file.writestr(f"no_bg_{uploaded_file.name.split('.')[0]}.png", img_byte_arr.getvalue())
                        
                    except Exception as e:
                        st.error(f"Error processing {uploaded_file.name}: {e}")
                    
                    # Progress update
                    progress_bar.progress((index + 1) / total_files)
            
            st.success(f"🎉 Tada! Sabhi {total_files} photos successfully process ho gayi hain.")
            
            # ZIP file download karne ka button
            st.download_button(
                label="⬇️ Download All Processed Photos (ZIP)",
                data=zip_buffer.getvalue(),
                file_name="Wedding_Transparent_Photos.zip",
                mime="application/zip"
           ))
