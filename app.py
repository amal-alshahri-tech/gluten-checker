import streamlit as st
import google.generativeai as genai
from PIL import Image
# =========================
# Page Setup
# =========================
st.set_page_config(
    page_title="Gluten Checker",
    page_icon="🛡️",
    layout="centered"
)
# =========================
# Custom Title
# =========================
st.markdown(
    "<h1 style='font-size:36px;'>🛡️ فاحص الغلوتين | Gluten Checker</h1>",
    unsafe_allow_html=True
)
# =========================
# Warning Message
# =========================
st.warning("""
⚠️ هذا البرنامج أداة مساعدة تعتمد على الذكاء الاصطناعي وقد يخطئ أحيانًا.
يتحمل المستخدم مسؤولية القرار النهائي ويُنصح دائمًا بمراجعة الملصق الغذائي الرسمي والتواصل مع الشركة المصنعة عند وجود شك.
⚠️ This tool is AI-assisted and may occasionally make mistakes.
Users are responsible for final decisions and should always verify official product labels and contact manufacturers when uncertain.
""")
# =========================
# Description
# =========================
st.write("""
قم برفع صور المنتج الغذائي من جميع الجهات لتحليل سلامته لمرضى السيلياك والغلوتين.
Upload food product images from all sides to analyze gluten safety for celiac patients.
""")
st.divider()
# =========================
# API KEY
# =========================
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
# =========================
# SYSTEM PROMPT
# =========================
SYSTEM_PROMPT = """
أنت أخصائي تغذية سريرية وخبير في مرض السيلياك وتحليل المنتجات الغذائية عالميًا.
قم بتحليل صور المنتجات الغذائية بعناية لتحديد سلامتها لمرضى السيلياك والغلوتين.
حلل جميع الصور المرفوعة معًا على أنها لنفس المنتج.
لا تفترض الأمان عند وجود شك.
ركز على:
- المكونات
- تحذيرات الحساسية
- شعارات خالي من الغلوتين
- أرقام E
- النشا المعدل
- النكهات
- مصادر الغلوتين المخفية
- احتمالية التلوث التبادلي
التصنيفات النهائية:
🟢 آمن تمامًا
🟡 مكونات آمنة لكن غير معتمدة
🟠 يحتاج حذر
🔴 غير آمن / يحتوي على غلوتين
قواعد مهمة:
- يحتوي على قمح = غير آمن
- قد يحتوي على آثار قمح = غير آمن
- E1400 إلى E1451 = نشا معدل، إذا لم يُذكر المصدر فهو غير آمن
- E636 و E637 مشتقة من الشعير
- Wheat Free لا يعني Gluten Free
- Oat Free لا يعني Gluten Free
- لا تعتمد على الشعار وحده إذا كانت المكونات متعارضة
اكتب النتيجة بالعربية كاملة أولًا.
ثم الإنجليزية بعدها كاملة.
استخدم خطوط فاصلة بين الأقسام.
"""
# =========================
# MODEL
# =========================
model = genai.GenerativeModel(
    model_name="gemini-2.5-flash",
    system_instruction=SYSTEM_PROMPT
)
# =========================
# Upload Images
# =========================
uploaded_files = st.file_uploader(
    "📸 ارفع صور المنتج | Upload product images",
    type=["jpg", "jpeg", "png"],
    accept_multiple_files=True
)
# =========================
# Analyze Images
# =========================
if uploaded_files:
    images = []
    for file in uploaded_files:
        img = Image.open(file).convert("RGB")
        # Resize image
        img.thumbnail((1400, 1400))
        images.append(img)
    # Show uploaded images
    for i, image in enumerate(images, start=1):
        st.image(
            image,
            caption=f"الصورة {i}",
            use_container_width=True
        )
    st.divider()
    # Analyze Button
    if st.button("🔍 تحليل المنتج | Analyze Product"):
        try:
            with st.spinner("جاري تحليل المنتج... | Analyzing product..."):
                content = [
                    """
حلل هذه الصور معًا لنفس المنتج الغذائي.
اكتب النتيجة بالعربية كاملة أولًا ثم الإنجليزية بعدها.
استخدم هذا التنسيق:
---
# التحليل باللغة العربية
---
## 📊 الحالة
## 📋 الأسباب
---
## 🏷️ تحليل الشعارات
---
## 🧪 معلومات الحساسية
---
## 💡 التوصية
---
# English Analysis
---
## 📊 Status
## 📋 Reasons
---
## 🏷️ Label Analysis
---
## 🧪 Allergen Info
---
## 💡 Recommendation
"""
                ]
                content.extend(images)
                response = model.generate_content(content)
            st.success("✅ تم التحليل بنجاح | Analysis Completed")
            st.markdown(response.text)
        except Exception as e:
            st.error("""
❌ حدث خطأ أثناء التحليل.
قد يكون السبب:
- ضغط مؤقت على الخدمة
- انتهاء الحد المجاني
- صور كثيرة أو كبيرة جدًا
يرجى المحاولة لاحقًا.
---
❌ Analysis Error
Possible reasons:
- Temporary server overload
- Free quota exceeded
- Too many or very large images
Please try again later.
""")