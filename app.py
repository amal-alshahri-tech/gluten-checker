import streamlit as st
import google.generativeai as genai
from PIL import Image
import io

st.set_page_config(
    page_title="Gluten Checker",
    page_icon="🛡️",
    layout="centered"
)

st.markdown("""
<style>
html, body, [class*="css"] {
    font-family: Arial, sans-serif;
}

.main-title {
    text-align: center;
    font-size: 46px;
    font-weight: 800;
    line-height: 1.3;
    margin-bottom: 10px;
    color: #2b2d42;
}

.warning-box {
    background-color: #f4f1d6;
    padding: 20px;
    border-radius: 12px;
    line-height: 1.9;
    font-size: 18px;
    margin-top: 15px;
    margin-bottom: 25px;
}

.description-box {
    text-align: center;
    line-height: 1.9;
    font-size: 20px;
    margin-bottom: 35px;
}

.arabic-text {
    direction: rtl;
    text-align: right;
    line-height: 2.1;
    font-size: 20px;
}

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

st.markdown("""
<div class="main-title">
🛡️ فاحص الغلوتين <br>
Gluten Checker
</div>
""", unsafe_allow_html=True)

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

st.markdown("""
<div class="description-box arabic-text">
قم برفع صور المنتج الغذائي من جميع الجهات لتحليل سلامته لمرضى السيلياك والغلوتين.

<br><br>

<div class="english-text">
Upload food product images from all sides to analyze gluten safety for celiac patients.
</div>
</div>
""", unsafe_allow_html=True)

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

SYSTEM_PROMPT = """
أنت خبير تغذية متخصص في تحليل المنتجات الغذائية لمرضى السيلياك وحساسية الغلوتين.

حلل جميع الصور المرفوعة على أنها لنفس المنتج الغذائي.

المطلوب:
1. اقرأ المكونات الظاهرة في الصورة.
2. استخرج قائمة المكونات كما هي قدر الإمكان.
3. استخرج أرقام E-numbers إن وجدت.
4. حلل معلومات الحساسية.
5. حلل الشعارات مثل Gluten Free / Wheat Free / Oat Free.
6. لا تعتمد على الشعار وحده إذا كانت المكونات متعارضة.
7. لا تفترض الأمان عند وجود شك.

قواعد مهمة:
- يحتوي على قمح = غير آمن.
- قد يحتوي على آثار قمح = غير آمن.
- قمح، شعير، جاودار، مالت، نشاء القمح، طحين، سميد، بقسماط = غير آمن.
- الشوفان غير آمن إلا إذا مكتوب بوضوح Gluten Free.
- النشا المعدل غير آمن إذا لم يتم ذكر مصدره.
- E1400 إلى E1451 = نشا معدل، إذا لم يذكر المصدر فهو غير آمن.
- E636 و E637 مشتقة من الشعير = غير آمنة.
- Wheat Free لا يعني Gluten Free.
- Oat Free لا يعني Gluten Free.

استخدم رموز التصنيف التالية فقط داخل خانة الحالة:
STATUS_SAFE
STATUS_INGREDIENTS_SAFE
STATUS_VERIFY
STATUS_UNSAFE

معنى التصنيفات:
STATUS_SAFE = آمن تمامًا / Certified Safe
STATUS_INGREDIENTS_SAFE = مكونات آمنة لكن غير معتمدة / Ingredients Safe But Not Certified
STATUS_VERIFY = يحتاج تحقق / Needs Verification
STATUS_UNSAFE = غير آمن / Unsafe

اكتب النتيجة بالعربية كاملة أولًا، ثم الإنجليزية كاملة بعدها.

استخدم هذا التنسيق فقط:

<hr>

<div dir="rtl" style="text-align:right; line-height:2.1; font-size:20px;">

<h2>التحليل باللغة العربية</h2>

<h3>📊 الحالة</h3>
<p>STATUS_SAFE أو STATUS_INGREDIENTS_SAFE أو STATUS_VERIFY أو STATUS_UNSAFE</p>

<hr>

<h3>🧾 المكونات المقروءة من الصورة</h3>
<p>اكتب قائمة المكونات التي استطعت قراءتها من الصور. إذا لم تكن واضحة، اذكر ذلك.</p>

<hr>

<h3>🔬 تحليل أرقام E</h3>
<p>اذكر أرقام E الموجودة، واشرح هل لها علاقة بالغلوتين أو لا. إذا لم توجد أرقام E، اكتب لا توجد أرقام E واضحة.</p>

<hr>

<h3>📋 الأسباب</h3>
<p>اشرح سبب التصنيف النهائي بوضوح.</p>

<hr>

<h3>⚠️ المكونات المشكوك فيها أو الخطرة</h3>
<p>اذكر أي مكونات ممنوعة أو مشكوك فيها مثل النشا المعدل، منكهات، شوفان، قمح، شعير، مالت.</p>

<hr>

<h3>🏷️ تحليل الشعارات</h3>
<p>اشرح الشعارات الموجودة، وهل هي Gluten Free أو Wheat Free أو Oat Free، ولا تخلط بينها.</p>

<hr>

<h3>🧪 معلومات الحساسية</h3>
<p>اذكر هل توجد عبارة يحتوي على قمح أو قد يحتوي على آثار قمح أو أي تحذير حساسية.</p>

<hr>

<h3>💡 التوصية</h3>
<p>اكتب توصية واضحة لمريض السيلياك.</p>

<hr>

<h3>⚠️ تنبيه مهم</h3>
<p>هذا التحليل يعتمد على الذكاء الاصطناعي وقد يحتوي على أخطاء. يجب دائمًا مراجعة الملصق الرسمي والتواصل مع الشركة المصنّعة عند الشك.</p>

</div>

<hr>

<div dir="ltr" style="text-align:left; line-height:1.8; font-size:18px;">

<h2>English Analysis</h2>

<h3>📊 Status</h3>
<p>STATUS_SAFE or STATUS_INGREDIENTS_SAFE or STATUS_VERIFY or STATUS_UNSAFE</p>

<hr>

<h3>🧾 Ingredients Read From Image</h3>
<p>List the ingredients you were able to read from the images. If unclear, say so.</p>

<hr>

<h3>🔬 E-number Analysis</h3>
<p>List detected E-numbers and explain whether they are gluten-related or not. If none are visible, say no clear E-numbers found.</p>

<hr>

<h3>📋 Reasons</h3>
<p>Clearly explain the reason for the final classification.</p>

<hr>

<h3>⚠️ Suspicious or Risky Ingredients</h3>
<p>Mention any forbidden or suspicious ingredients such as modified starch, flavorings, oats, wheat, barley, malt.</p>

<hr>

<h3>🏷️ Label Analysis</h3>
<p>Explain detected labels such as Gluten Free, Wheat Free, or Oat Free. Do not confuse them.</p>

<hr>

<h3>🧪 Allergen Info</h3>
<p>Mention whether there is contains wheat, may contain wheat, or any allergen warning.</p>

<hr>

<h3>💡 Recommendation</h3>
<p>Give a clear recommendation for celiac patients.</p>

<hr>

<h3>⚠️ Important Notice</h3>
<p>This analysis is AI-assisted and may contain mistakes. Always verify official labels and contact the manufacturer when uncertain.</p>

</div>

مهم جدًا:
- لا تخلط العربي والإنجليزي داخل نفس الجملة.
- العربي كامل أولًا، ثم الإنجليزي كامل بعده.
- لا تستخدم جداول.
- اجعل المكونات وأرقام E ظاهرة بوضوح في النتيجة.
"""

model = genai.GenerativeModel(
    model_name="gemini-2.5-flash",
    system_instruction=SYSTEM_PROMPT
)

uploaded_files = st.file_uploader(
    "📸 ارفع صور المنتج | Upload product images",
    type=["jpg", "jpeg", "png"],
    accept_multiple_files=True
)

def optimize_image(image):
    image.thumbnail((1200, 1200))
    buffer = io.BytesIO()
    image.save(buffer, format="JPEG", quality=75)
    buffer.seek(0)
    return Image.open(buffer)

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
                "حلل هذه الصور لنفس المنتج الغذائي. اقرأ المكونات، أرقام E، التحذيرات، الشعارات، ثم أعطِ التصنيف النهائي."
            ]

            content.extend(images)

            response = model.generate_content(content)

            result = response.text

            result = result.replace(
                "STATUS_INGREDIENTS_SAFE",
                "<span style='color:#65a30d; font-size:28px; font-weight:bold;'>🟡 مكونات آمنة لكن غير معتمدة | Ingredients Safe But Not Certified</span>"
            )

            result = result.replace(
                "STATUS_SAFE",
                "<span style='color:#16a34a; font-size:28px; font-weight:bold;'>🟢 آمن تمامًا | Certified Safe</span>"
            )

            result = result.replace(
                "STATUS_VERIFY",
                "<span style='color:#f97316; font-size:28px; font-weight:bold;'>🟠 يحتاج تحقق | Needs Verification</span>"
            )

            result = result.replace(
                "STATUS_UNSAFE",
                "<span style='color:#dc2626; font-size:28px; font-weight:bold;'>🔴 غير آمن | Unsafe</span>"
            )

            st.markdown(result, unsafe_allow_html=True)

        except Exception as e:
            st.error(
                "حدث خطأ مؤقت أثناء التحليل. حاول مرة أخرى لاحقًا. | Temporary analysis error. Please try again later."
            )
            st.code(str(e))