import streamlit as st
import os
from io import BytesIO
from utils import ai_generator, meme_renderer

st.set_page_config(page_title="MemeCraft", page_icon="M", layout="wide")

def main():
    # Custom CSS for better styling
    st.markdown("""
    <style>
    div.stButton > button {
        width: 100%;
        font-weight: bold;
        height: 3rem;
    }
    .main-header {
        font-size: 3rem;
        font-weight: 800;
        background: -webkit-linear-gradient(45deg, #FF4B4B, #FF914D);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        margin-bottom: 2rem;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<p class="main-header">MemeCraft</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Create viral memes in seconds using advanced AI.</p>', unsafe_allow_html=True)
    
    # Check for API Key
    if not os.getenv("REPLICATE_API_TOKEN"):
        st.error("API Token missing! Please check your .env file.")
        st.stop()

    # Step 1: Generate Template
    with st.container():
        st.markdown("#### 1. Dream Up a Template")
        
        # Use columns to center and constrain width (middle column is 50% width)
        _, col_center, _ = st.columns([1, 2, 1])
        
        with col_center:
            # Stacked layout: Input first, then button below
            template_desc = st.text_input("Describe the scene:", placeholder="e.g., A futuristic city where everyone rides giant hamsters")
            generate_btn = st.button("Generate Template")

    if "generated_image" not in st.session_state:
        st.session_state.generated_image = None

    if generate_btn:
        if not template_desc.strip():
            st.warning("Please describe your meme idea first!")
        else:
            with st.spinner("Painting your meme canvas..."):
                try:
                    img = ai_generator.generate_meme_image(template_desc)
                    st.session_state.generated_image = img
                    # Reset final meme when new template is generated
                    if "final_meme" in st.session_state:
                        del st.session_state.final_meme
                except Exception as e:
                    st.error(f"Oops! Something went wrong: {e}")

    st.divider()

    # Step 2: Customize Text
    if st.session_state.generated_image:
        st.markdown("#### 2. Add Your Captions")
        
        col_preview, col_controls = st.columns([1, 1])
        
        with col_controls:
            with st.form("caption_form"):
                st.subheader("Text Editor")
                top_text = st.text_input("Top Text", placeholder="WHEN YOU REALIZE...")
                bottom_text = st.text_input("Bottom Text", placeholder="IT'S MONDAY AGAIN")
                
                st.subheader("Styling")
                c1, c2 = st.columns(2)
                with c1:
                    font_size = st.slider("Font Size", 20, 150, 80)
                    padding = st.slider("Vertical Padding", 0, 150, 50)
                with c2:
                    text_color = st.color_picker("Text Color", "#FFFFFF")
                    outline_color = st.color_picker("Outline Color", "#000000")
                    outline_width = st.slider("Outline Width", 0, 15, 3)
                
                render_btn = st.form_submit_button("Render Final Meme")

        with col_preview:
            # Logic to handle rendering
            if render_btn:
                final_img = st.session_state.generated_image.copy()
                st.session_state.final_meme = meme_renderer.render_meme(
                    final_img, 
                    top_text, 
                    bottom_text, 
                    font_size=font_size,
                    text_color=text_color,
                    outline_color=outline_color,
                    outline_width=outline_width,
                    padding=padding
                )
            
            # Display logic
            if "final_meme" in st.session_state:
                 st.image(st.session_state.final_meme, caption="Your Masterpiece", use_column_width=True)
                 
                 # Download button for the final meme
                 buf = BytesIO()
                 st.session_state.final_meme.save(buf, format="JPEG")
                 byte_im = buf.getvalue()
                 
                 st.download_button(
                    label="Download Meme",
                    data=byte_im,
                    file_name="memecraft_creation.jpg",
                    mime="image/jpeg"
                 )
            else:
                 st.image(st.session_state.generated_image, caption="Raw Template", use_column_width=True)

if __name__ == "__main__":
    main()
