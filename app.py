import streamlit as st
import google.generativeai as genai
from PIL import Image

# =========================
# إعداد الصفحة
# =========================

st.set_page_config(
    page_title="Gluten Checker",
    page_icon="🛡️",
    layout="centered"
)

# =========================
# العنوان
# =========================

st.title("🛡️ Gluten Checker | فاحص الغلوتين")

st.markdown("""
### ⚠️ تنبيه مهم | Important Disclaimer

هذا البرنامج أداة مساعدة تعتمد على الذكاء الاصطناعي وقد يخطئ أحيانًا.  
يتحمل المستخدم مسؤولية القرار النهائي ويُنصح دائمًا بمراجعة الملصق الغذائي الرسمي والتواصل مع الشركة المصنعة عند وجود شك.

This tool is AI-assisted and may occasionally make mistakes.  
Users are responsible for final decisions and should always verify official labels and contact manufacturers when uncertain.
""")

st.divider()

# =========================
# API KEY
# =========================

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# =========================
# التعليمات الخاصة بالموديل
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

نظام التصنيف النهائي:

🟢 آمن تمامًا | Certified Safe

🟡 مكونات آمنة لكن غير معتمدة | Ingredients Safe But Not Certified

🟠 يحتاج حذر | Caution

🔴 غير آمن / يحتوي على غلوتين | Unsafe / Contains Gluten


يجب كتابة النتيجة بالعربية أولًا كاملة.
ثم الإنجليزية بعدها كاملة.

مهم جدًا:
- لا تستخدم أعلام الدول.
- أضف خط فاصل واضح بين كل قسم.
- اجعل التنسيق مرتبًا وسهل القراءة.
- لا تجعل العناوين ملتصقة بالنص.
- استخدم Markdown بشكل منظم.

استخدم هذا التنسيق حرفيًا:

---

# التحليل باللغة العربية

---

## 📊 الحالة

[اكتب التصنيف النهائي بالعربية]

---

## 📋 الأسباب

- شرح عربي مرتب وواضح
- نقاط مختصرة ومنظمة

---

## 🏷️ تحليل الشعارات

- شرح الشعارات الظاهرة
- توضيح أهميتها

---

## 🧪 معلومات الحساسية

- شرح تحذيرات الحساسية
- هل يوجد قمح أو آثار غلوتين

---

## 💡 التوصية

- توصية واضحة ومباشرة

---

## ⚠️ تنبيه مهم

هذا البرنامج أداة مساعدة تعتمد على الذكاء الاصطناعي وقد يخطئ أحيانًا.
يتحمل المستخدم مسؤولية القرار النهائي ويُنصح دائمًا بمراجعة الملصق الغذائي الرسمي والتواصل مع الشركة المصنعة عند وجود شك.

---

# English Analysis

---

## 📊 Status

[Final classification in English]

---

## 📋 Reasons

- Clear organized explanation
- Short readable points

---

## 🏷️ Label Analysis

- Explain labels found
- Explain their importance

---

## 🧪 Allergen Info

- Explain allergen warnings
- Mention wheat/gluten risk

---

## 💡 Recommendation

- Clear recommendation

---

## ⚠️ Important Disclaimer

This tool is AI-assisted and may occasionally make mistakes.
Users are responsible for final decisions and should always verify official labels and contact manufacturers when uncertain.
"""

# =========================
# اختيار الموديل
# =========================

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction=SYSTEM_PROMPT
)

# =========================
# رفع الصور
# =========================

uploaded_files = st.file_uploader(
    "📸 قم برفع صور المنتج من جميع الجهات | Upload product images from all sides",
    type=["jpg", "jpeg", "png"],
    accept_multiple_files=True
)

# =========================
# تحليل الصور
# =========================

if uploaded_files:

    images = [Image.open(file) for file in uploaded_files]

    # عرض الصور
    for i, image in enumerate(images, start=1):
        st.image(
            image,
            caption=f"Uploaded Image {i}",
            use_container_width=True
        )

    st.divider()

    # تقليل عدد الصور لتقليل الضغط على API
    images = images[:4]

    # تصغير الصور لتقليل الاستهلاك
    resized_images = []

    for image in images:
        img = image.copy()
        img.thumbnail((1200, 1200))
        resized_images.append(img)

    try:

        with st.spinner("🔍 جاري تحليل المنتج... | Analyzing product..."):

            content = [
                "حلل هذه الصور معًا لنفس المنتج الغذائي الخاص بمرضى السيلياك والغلوتين. Write Arabic first then English."
            ]

            content.extend(resized_images)

            response = model.generate_content(content)

        st.success("✅ تم التحليل بنجاح | Analysis Completed")

        st.markdown(response.text)

    except Exception as e:

        st.error("""
❌ حدث خطأ أثناء التحليل.

قد يكون السبب:
- عدد كبير من الطلبات
- انتهاء الحد المجاني لـ Gemini
- صور كبيرة جدًا
- ضغط مؤقت على الخدمة

يرجى المحاولة مرة أخرى بعد قليل.

---

❌ Analysis Error

Possible reasons:
- Too many requests
- Gemini free quota exceeded
- Images are too large
- Temporary server overload

Please try again later.
""")

        st.code(str(e))