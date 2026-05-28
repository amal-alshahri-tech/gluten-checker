import streamlit as st
import google.generativeai as genai
from PIL import Image
import io

# =====================================
# إعداد الصفحة
# =====================================

st.set_page_config(
    page_title="Gluten Checker",
    page_icon="🛡️",
    layout="centered"
)

# =====================================
# تنسيق CSS
# =====================================

st.markdown("""
<style>

html, body, [class*="css"] {
    font-family: Arial, sans-serif;
}

/* العنوان الرئيسي */
.main-title {
    text-align: center;
    font-size: 46px;
    font-weight: 800;
    line-height: 1.3;
    margin-bottom: 10px;
    color: #2b2d42;
}

/* صندوق التنبيه */
.warning-box {
    background-color: #f4f1d6;
    padding: 20px;
    border-radius: 12px;
    line-height: 1.9;
    font-size: 18px;
    margin-top: 15px;
    margin-bottom: 25px;
}

/* النص التعريفي */
.description-box {
    text-align: center;
    line-height: 1.9;
    font-size: 20px;
    margin-bottom: 35px;
}

/* النص العربي */
.arabic-text {
    direction: rtl;
    text-align: right;
    line-height: 2.1;
    font-size: 20px;
}

/* النص الإنجليزي */
.english-text {
    direction: ltr;
    text-align: left;
    line-height: 1.8;
    font-size: 18px;
}

hr {
    margin-top: 30px;
    margin-bottom: 30px;
}

</style>
""", unsafe_allow_html=True)

# =====================================
# العنوان
# =====================================

st.markdown("""
<div class="main-title">
🛡️ فاحص الغلوتين <br>
Gluten Checker
</div>
""", unsafe_allow_html=True)

# =====================================
# التنبيه
# =====================================

st.markdown("""
<div class="warning-box arabic-text">
⚠️ هذا البرنامج أداة مساعدة تعتمد على الذكاء الاصطناعي وقد يخطئ أحيانًا.
يتحمّل المستخدم مسؤولية القرار النهائي وينصح دائمًا بمراجعة الملصق الغذائي الرسمي والتواصل مع الشركة المصنّعة عند وجود شك.

<br><br>

<div class="english-text">
⚠️ This tool is AI-assisted and may occasionally make mistakes.
Users are responsible for final decisions and should always verify official product labels and contact manufacturers when uncertain.
</div>

</div>
""", unsafe_allow_html=True)

# =====================================
# وصف التطبيق
# =====================================

st.markdown("""
<div class="description-box arabic-text">

قم برفع صور المنتج الغذائي من جميع الجهات لتحليل سلامته لمرضى السيلياك والغلوتين.

<br><br>

<div class="english-text">
Upload food product images from all sides to analyze gluten safety for celiac patients.
</div>

</div>
""", unsafe_allow_html=True)

# =====================================
# API KEY
# =====================================

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# =====================================
# SYSTEM PROMPT
# =====================================

SYSTEM_PROMPT = """
أنت خبير تغذية متخصص في تحليل المنتجات الغذائية لمرضى السيلياك وحساسية الغلوتين.

قم بتحليل جميع الصور لنفس المنتج الغذائي.

ركز على:
- المكونات
- التحذيرات
- الشعارات
- احتمالية التلوث التبادلي
- أرقام E

إذا لم تكن متأكدًا اذكر ذلك بوضوح.

اكتب النتيجة بهذا التنسيق فقط:

<hr>

<div dir="rtl" style="text-align:right; line-height:2.1; font-size:20px;">

<h2>التحليل باللغة العربية</h2>

<h3>📊 الحالة</h3>
<p>SAFE أو CAUTION أو UNSAFE أو VERIFY</p>

<hr>

<h3>📋 الأسباب</h3>
<p>...</p>

<hr>

<h3>🏷️ تحليل الشعارات</h3>
<p>...</p>

<hr>

<h3>🧪 معلومات الحساسية</h3>
<p>...</p>

<hr>

<h3>💡 التوصية</h3>
<p>...</p>

<hr>

<h3>⚠️ تنبيه مهم</h3>
<p>
هذا التحليل يعتمد على الذكاء الاصطناعي وقد يحتوي على أخطاء.
يجب دائمًا مراجعة الملصق الرسمي والتواصل مع الشركة المصنّعة عند الشك.
</p>

</div>

<hr>

<div dir="ltr" style="text-align:left; line-height:1.8; font-size:18px;">

<h2>English Analysis</h2>

<h3>📊 Status</h3>
<p>SAFE أو CAUTION أو UNSAFE أو VERIFY</p>

<hr>

<h3>📋 Reasons</h3>
<p>...</p>

<hr>

<h3>🏷️ Label Analysis</h3>
<p>...</p>

<hr>

<h3>🧪 Allergen Info</h3>
<p>...</p>

<hr>

<h3>💡 Recommendation</h3>
<p>...</p>

<hr>

<h3>⚠️ Important Notice</h3>
<p>
This analysis is AI-assisted and may contain mistakes.
Always verify official labels and contact the manufacturer when uncertain.
</p>

</div>

مهم جدًا:
- لا تخلط العربي والإنجليزي داخل نفس الجملة.
- اجعل العربي كامل أولًا ثم الإنجليزي كامل بعده.
- لا تستخدم جداول.
- اجعل التنسيق مرتب وواضح.
"""

# =====================================
# اختيار الموديل
# =====================================

model = genai.GenerativeModel(
    model_name="gemini-2.5-flash",
    system_instruction=SYSTEM_PROMPT
)

# =====================================
# رفع الصور
# =====================================

uploaded_files = st.file_uploader(
    "📸 ارفع صور المنتج | Upload product images",
    type=["jpg", "jpeg", "png"],
    accept_multiple_files=True
)

# =====================================
# تحسين الصور
# =====================================

def optimize_image(image):

    max_size = (1200, 1200)

    image.thumbnail(max_size)

    buffer = io.BytesIO()

    image.save(buffer, format="JPEG", quality=75)

    buffer.seek(0)

    return Image.open(buffer)

# =====================================
# التحليل
# =====================================

if uploaded_files:

    images = []

    for file in uploaded_files:

        img = Image.open(file).convert("RGB")

        optimized = optimize_image(img)

        images.append(optimized)

    for i, image in enumerate(images, start=1):

        st.image(
            image,
            caption=f"Uploaded Image {i}",
            use_container_width=True
        )

    with st.spinner("جاري تحليل المنتج... | Analyzing product..."):

        try:

            content = [
                "حلل هذه الصور لنفس المنتج الغذائي وحدد مدى أمانه لمرضى السيلياك والغلوتين."
            ]

            content.extend(images)

            response = model.generate_content(content)

            result = response.text

            # =====================================
            # تلوين التصنيفات
            # =====================================

            result = result.replace(
                "SAFE",
                "<span style='color:#16a34a; font-size:30px; font-weight:bold;'>🟢 آمن تمامًا | SAFE</span>"
            )

            result = result.replace(
                "CAUTION",
                "<span style='color:#eab308; font-size:30px; font-weight:bold;'>🟡 يحتاج حذر | CAUTION</span>"
            )

            result = result.replace(
                "UNSAFE",
                "<span style='color:#dc2626; font-size:30px; font-weight:bold;'>🔴 غير آمن | UNSAFE</span>"
            )

            result = result.replace(
                "VERIFY",
                "<span style='color:#f97316; font-size:30px; font-weight:bold;'>🟠 يحتاج تحقق | VERIFY</span>"
            )

            st.markdown(result, unsafe_allow_html=True)

        except Exception as e:

            st.error(
                "حدث خطأ مؤقت أثناء التحليل. حاول مرة أخرى لاحقًا. | Temporary analysis error. Please try again later."
            )

            st.code(str(e))