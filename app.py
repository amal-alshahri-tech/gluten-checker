import streamlit as st
import google.generativeai as genai
from PIL import Image

# إعداد الصفحة
st.set_page_config(
    page_title="Gluten Checker | فاحص الغلوتين",
    page_icon="🛡️"
)

# عنوان التطبيق
st.title("🛡️ فاحص الغلوتين | Gluten Checker")

# تنبيه مهم
st.warning("""
⚠️ هذا البرنامج أداة مساعدة تعتمد على الذكاء الاصطناعي وقد يخطئ أحيانًا. 
يتحمل المستخدم مسؤولية القرار النهائي ويُنصح دائمًا بمراجعة الملصق الغذائي الرسمي والتواصل مع الشركة المصنعة عند وجود شك.

⚠️ This tool is AI-assisted and may occasionally make mistakes.
Users are responsible for final decisions and should always verify official product labels and contact manufacturers when uncertain.
""")

# وصف التطبيق
st.write("""
قم برفع صور المنتج الغذائي من جميع الجهات لتحليل سلامته لمرضى السيلياك والغلوتين.

Upload food product images from all sides to analyze gluten safety for celiac patients.
""")

# API KEY
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# البرومبت الرئيسي
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
يستخدم فقط إذا:
- المنتج يحمل اعتماد رسمي خالي من الغلوتين
أو
- جميع المكونات واضحة وآمنة بدون أي شكوك.

🟡 مكونات آمنة لكن غير معتمدة | Ingredients Safe But Not Certified
يستخدم إذا:
- المكونات تبدو آمنة
لكن
- لا يوجد اعتماد رسمي خالي من الغلوتين
أو
- توجد شكوك بسيطة.

🟠 يحتاج حذر | Caution
يستخدم إذا:
- توجد معلومات ناقصة
- الصور غير واضحة
- توجد مكونات أو نكهات مشكوك بها
- لا يمكن التأكد الكامل من المصدر

🔴 غير آمن / يحتوي على غلوتين | Unsafe / Contains Gluten
يستخدم إذا:
- وُجد قمح
- أو شعير
- أو جاودار
- أو مالت
- أو نشا قمح
- أو طحين
- أو سميد
- أو بقسماط
- أو شوفان غير مكتوب عليه Gluten Free
- أو نشا معدل بدون ذكر المصدر
- أو أي مصدر واضح للغلوتين

قواعد E-numbers:
- لا يوجد رقم E يدل مباشرة على الغلوتين.
- من E1400 إلى E1451 تعني نشا معدل. إذا لم يتم ذكر المصدر، صنّف المنتج 🔴 غير آمن / يحتوي على غلوتين.
- E636 و E637 مشتقة من الشعير. صنّف المنتج 🔴 غير آمن / يحتوي على غلوتين.
- بقية أرقام E ليست مرتبطة بالغلوتين بشكل مباشر إلا إذا وُجدت مؤشرات أخرى.

قواعد الشعارات:
- شعار Gluten Free أو السنبلة المشطوبة مؤشر إيجابي فقط.
- Wheat Free أو Oat Free لا يعني خالي من الغلوتين.
- لا تعتمد على الشعارات وحدها إذا كانت المكونات متعارضة.

قواعد الحساسية:
- يحتوي على قمح = 🔴 غير آمن / يحتوي على غلوتين.
- قد يحتوي على آثار قمح = 🔴 غير آمن / يحتوي على غلوتين.
- إذا لم يتم ذكر القمح أو الغلوتين، فهذا عامل دعم فقط وليس دليلًا نهائيًا.

IMPORTANT:
يجب كتابة النتيجة العربية كاملة أولًا.
ثم كتابة النتيجة الإنجليزية كاملة بعدها.
لا تخلط اللغتين داخل نفس القسم.

Use this exact structure:

━━━━━━━━━━━━━━━━━━━
🇸🇦 التحليل باللغة العربية
━━━━━━━━━━━━━━━━━━━

📊 الحالة:
[التصنيف النهائي بالعربية فقط]

📋 الأسباب:
- شرح عربي مرتب وواضح

🏷️ تحليل الشعارات:
- شرح عربي

🧪 معلومات الحساسية:
- شرح عربي

💡 التوصية:
- توصية عربية واضحة

⚠️ تنبيه مهم:
هذا البرنامج أداة مساعدة تعتمد على الذكاء الاصطناعي وقد يخطئ أحيانًا.
يتحمل المستخدم مسؤولية القرار النهائي ويُنصح دائمًا بمراجعة الملصق الغذائي الرسمي والتواصل مع الشركة المصنعة عند وجود شك.

━━━━━━━━━━━━━━━━━━━
🇺🇸 English Analysis
━━━━━━━━━━━━━━━━━━━

📊 Status:
[Final classification in English only]

📋 Reasons:
- Clear English explanation

🏷️ Label Analysis:
- English explanation

🧪 Allergen Info:
- English explanation

💡 Recommendation:
- Clear English recommendation

⚠️ Important Disclaimer:
This tool is AI-assisted and may occasionally make mistakes.
Users are responsible for final decisions and should always verify official labels and contact manufacturers when uncertain.
"""

# اختيار الموديل
model = genai.GenerativeModel(
    model_name="gemini-2.5-flash",
    system_instruction=SYSTEM_PROMPT
)

# رفع الصور
uploaded_files = st.file_uploader(
    "ارفع صور المنتج | Upload product images",
    type=["jpg", "jpeg", "png"],
    accept_multiple_files=True
)

# عند رفع الصور
if uploaded_files:

    images = []

    for file in uploaded_files:

        img = Image.open(file).convert("RGB")

        # تصغير ذكي للحفاظ على الأداء
        img.thumbnail((1400, 1400))

        images.append(img)

    # عرض الصور
    for i, image in enumerate(images, start=1):

        st.image(
            image,
            caption=f"الصورة {i} | Uploaded Image {i}",
            use_container_width=True
        )

    # زر التحليل
    if st.button("تحليل المنتج | Analyze Product"):

        with st.spinner("جاري تحليل المنتج... | Analyzing product..."):

            try:

                content = [
                    """
حلل هذه الصور معًا على أنها لنفس المنتج لتحديد سلامته لمرضى السيلياك.

اكتب النتيجة العربية كاملة أولًا.
ثم اكتب النتيجة الإنجليزية كاملة بعدها.

Analyze these images together as ONE product for celiac safety.

Write the full Arabic result first.
Then write the full English result after it.
"""
                ]

                content.extend(images)

                response = model.generate_content(content)

                st.markdown(response.text)

            except Exception as e:

                st.error("""
⚠️ تم الوصول إلى الحد المسموح أو يوجد ضغط على الخادم.
يرجى المحاولة لاحقًا.

⚠️ API usage limit reached or server overloaded.
Please try again later.
""")

                st.code(str(e))