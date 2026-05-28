import streamlit as st
import google.generativeai as genai
from PIL import Image

# عنوان التطبيق
st.title("🛡️ Gluten Checker")
st.write("Upload a food product image to analyze gluten safety for celiac patients.")

# API KEY
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# اختيار الموديل
model = genai.GenerativeModel(
    model_name="gemini-1.5-pro",
    system_instruction="""
You are a clinical nutrition specialist and a Celiac Disease expert.

Analyze food product images for gluten safety with maximum caution.

Focus on:
- ingredients
- allergen warnings
- gluten-free logos
- E-numbers

Never assume safety when uncertain.

Final classifications:
🟢 Certified Safe
🟡 Ingredients Safe
🟠 Caution
🔴 Not Safe
"""
)

# رفع الصورة
uploaded_file = st.file_uploader(
    "Upload product image",
    type=["jpg", "jpeg", "png"]
)

if uploaded_file:
    image = Image.open(uploaded_file)

    st.image(image, caption="Uploaded Image", use_container_width=True)

    with st.spinner("Analyzing product..."):
        response = model.generate_content([
            "Analyze this product for celiac safety.",
            image
        ])

    st.markdown(response.text)
