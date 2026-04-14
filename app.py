import streamlit as st
from rembg import remove
from PIL import Image
import io
import zipfile

st.set_page_config(page_title="Pro BG Remover", layout="wide")
st.title("✂️ Bulk Background Remover")
st.write("Ek sath 1 se 100 images upload karein. AI automatically baalon (hair) aur edges ko clean kar dega.")

uploaded_files = st.file_uploader("Apni photos yahan upload karein (Max 100)", type=['png', 'jpg', 'jpeg'], accept_multiple_files=True)

if uploaded_files:
    if len(uploaded_files) > 100:
        st.error("Kripya ek baar me maximum 100 photos hi upload karein.")
    else:
        if st.button("✨ Background Remove Karein"):
            st.info("AI Processing start ho chuki hai... Isme thoda time lag sakta hai.")
            zip_buffer = io.BytesIO()
            progress_bar = st.progress(0)
            total_files = len(uploaded_files)
            
            with zipfile.ZipFile(zip_buffer, "w") as zip_file:
                for index, uploaded_file in enumerate(uploaded_files):
                    try:
                        image = Image.open(uploaded_file)
                        output_image = remove(image)
                        img_byte_arr = io.BytesIO()
                        output_image.save(img_byte_arr, format='PNG')
                        zip_file.writestr(f"no_bg_{uploaded_file.name}", img_byte_arr.getvalue())
                    except Exception as e:
                        st.error(f"Error processing {uploaded_file.name}: {e}")
                    progress_bar.progress((index + 1) / total_files)
            
            st.success("🎉 Tada! Sabhi photos successfully process ho gayi hain.")
            st.download_button(label="⬇️ Download Processed Photos (ZIP)", data=zip_buffer.getvalue(), file_name="Transparent_Photos.zip", mime="application/zip")
