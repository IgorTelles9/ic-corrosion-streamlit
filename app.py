import streamlit as st
from models import Image
import os

st.title("Image Database Management")

# Initialize MongoDB connection
image_db = Image()

# At the top of your form, before the form block
if "image_count" not in st.session_state:
    st.session_state["image_count"] = 1

# Create form
with st.form("image_form"):
    
    full_path = st.text_input(
        "Image Base Path (with extension)*",
        help="Enter the base path of the image (e.g. /path/to/image.jpg). For multiple images, numbers will be added before the extension."
    )
    
    # Image Details
    object_type = st.selectbox("Object Type*", ["tube", "ship", "plate", "mooring"])
    environment = st.selectbox("Environment*", ["underwater", "above water"])
    material = st.text_input("Material")
    
    # Multiple Images
    image_count = st.number_input(
        "Number of images to create",
        min_value=1,
        value=st.session_state["image_count"],
        step=1
    )

    # Augmentation
    is_augmented = st.checkbox("Is Augmented", value=False)

    # Resolution
    col1, col2 = st.columns(2)
    with col1:
        width = st.number_input("Width", min_value=0, step=1)
    with col2:
        height = st.number_input("Height", min_value=0, step=1)
    
    # Degradation
    col1, col2 = st.columns(2)
    with col1:
        degradation_level = st.number_input("Degradation Level", min_value=0, max_value=10, step=1)
    with col2:
        degradation_type = st.text_input("Degradation Type")
    
    
    submitted = st.form_submit_button("Submit")
    
    if submitted:
        st.session_state["image_count"] = image_count 
        
        # Prepare image data
        image_data = {
            "path": full_path,
            "resolution": {
                "width": width if width > 0 else None,
                "height": height if height > 0 else None
            },
            "details": {
                "object_type": object_type,
                "environment": environment,
                "material": material if material else None
            },
            "degradation": {
                "level": degradation_level if degradation_level > 0 else None,
                "type": degradation_type if degradation_type else None
            },
            "augmented": is_augmented
        }
        
        # Insert images
        if image_count == 1:
            result = image_db.insert_image(image_data)
            if result:
                st.success(f"Success: {full_path} - inserted with ID: {result.inserted_id}")
            else:
                st.error(f"Error: {full_path} - duplicated path")
        else:
            extension = os.path.splitext(full_path)[1]
            results = image_db.insert_multiple_images(image_data, image_count, full_path)
            st.success(f"Successfully inserted {len(results)} images!")
            st.write("Generated paths:")
            for i, _ in enumerate(results):
                if results[i]:
                    st.write(f"Success: {os.path.splitext(full_path)[0]}_{i}{extension}") 
                else:
                    st.error(f"Error: {os.path.splitext(full_path)[0]}_{i}{extension} - duplicated path")