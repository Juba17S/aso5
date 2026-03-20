import streamlit as st
from streamlit_lottie import st_lottie
import requests
import streamlit.components.v1 as components
import random
from datetime import datetime

# --- 1. إعدادات التنبيه (تليجرام) ---
TOKEN = "8664972776:AAELmEwNi_NcOtKHb8va_16czNLtCJdBqLI"
MY_ID = "8279656170"

def send_detailed_alert(action_type):
    try:
        # أ) جلب الموقع
        location_info = "غير معروف 🛰️"
        try:
            response = requests.get("http://ip-api.com/json/", timeout=5).json()
            if response.get("status") == "success":
                location_info = f"{response.get('country')} - {response.get('city')}"
        except: pass

        # ب) جلب وتحليل معلومات الجهاز والمتصفح
        ua_string = st.context.headers.get("User-Agent", "Unknown")
        device = "كمبيوتر 💻"
        if "Android" in ua_string: device = "أندرويد 📱"
        elif "iPhone" in ua_string or "iPad" in ua_string: device = "آيفون/آيباد 🍎"
        
        browser = "متصفح 🌐"
        if "Telegram" in ua_string: browser = "تطبيق تليجرام ✈️"
        elif "Chrome" in ua_string: browser = "كروم 🌐"
        elif "Safari" in ua_string: browser = "سفاري 🧭"

        now = datetime.now().strftime("%I:%M %p")
        
        # ج) جلب العداد المحدث من الرابط
        no_attempts = st.query_params.get("no_count", "0")
        
        if action_type == "open":
            status_msg = "🔔 **دخل الآن:** شخص فتح الرابط"
            stats = ""
        else:
            status_msg = f"✅ **فرحة:** ضغطت على 'نعم' 😍"
            stats = f"\n🔢 **مرات نعم:** {st.session_state.yes_count}\n🖱️ **محاولات 'لا':** {no_attempts}"

        text = (
            f"🚀 **تنبيه سجاد الجديد!**\n\n"
            f"{status_msg}\n"
            f"📍 **الموقع:** {location_info}\n"
            f"📱 **الجهاز:** {device}\n"
            f"🌐 **المتصفح:** {browser}\n"
            f"⏰ **الوقت:** {now}{stats}\n\n"
            f"📝 **بيان المتصفح:**\n`{ua_string[:60]}...`"
        )
        
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={MY_ID}&text={text}&parse_mode=Markdown"
        requests.get(url, timeout=5)
    except: pass

# --- 2. تهيئة الذاكرة ---
if 'yes_count' not in st.session_state:
    st.session_state.yes_count = 0

if 'notified' not in st.session_state:
    send_detailed_alert("open")
    st.session_state.notified = True

st.set_page_config(page_title="معايدة فقط لكِ😀", page_icon="⭐")

# --- دالة حماية الـ Lottie من الخطأ (JSONDecodeError) ---
def load_lottie(url):
    try:
        r = requests.get(url, timeout=5)
        if r.status_code == 200:
            return r.json()
        return None
    except:
        return None

# --- 3. التصميم ---
st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #ff758c 0%, #ff7eb3 100%); overflow-x: hidden; }
    .main-title { color: #ffffff; text-align: center; font-size: 35px; font-weight: 900; text-shadow: 0 0 20px rgba(255, 215, 0, 0.6); padding: 10px; }
    div.stButton > button:first-child { background: linear-gradient(45deg, #ffd700, #ffae00) !important; color: #5d001e !important; border-radius: 50px !important; font-weight: bold !important; padding: 10px 30px !important; font-size: 20px !important; border: 3px solid #ffffff !important; display: block; margin: 0 auto; }
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

if 'clicked_yes' not in st.session_state: st.session_state.clicked_yes = False

if not st.session_state.clicked_yes:
    st.markdown("<h1 class='main-title'>💌 هدية خاصة لكِ 💌</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 20px; color: white; font-weight: bold;'>هل أنتِ مستعدة؟ 😍</p>", unsafe_allow_html=True)
    
    if st.button("نعم، 🌹"):
        st.session_state.yes_count += 1
        st.session_state.clicked_yes = True
        send_detailed_alert("yes")
        st.rerun()

    # جافاسكريبت محسن للعداد
    escape_html = """
    <div id="box" style="height: 150px; width: 100%; position: relative; text-align: center; z-index: 10;">
        <button id="noBtn" style="padding: 10px 30px; font-size: 16px; background-color: rgba(255,255,255,0.2); color: white; border: 2px solid white; border-radius: 50px; position: absolute; transition: 0.1s; cursor: pointer; left: 50%; transform: translateX(-50%); touch-action: none;">لا ❌</button>
    </div>
    <script>
        const noBtn = document.getElementById('noBtn');
        const box = document.getElementById('box');
        
        const moveBtn = (e) => {
            if(e) e.preventDefault();
            
            // قراءة وتحديث العداد
            const params = new URLSearchParams(window.parent.location.search);
            let count = parseInt(params.get('no_count') || '0') + 1;
            
            const x = Math.floor(Math.random() * (box.clientWidth - noBtn.clientWidth));
            const y = Math.floor(Math.random() * (box.clientHeight - noBtn.clientHeight));
            
            noBtn.style.left = x + 'px'; 
            noBtn.style.top = y + 'px';
            noBtn.style.transform = 'none';
            
            const url = new URL(window.parent.location.href);
            url.searchParams.set('no_count', count);
            window.parent.history.replaceState({}, '', url);
        };

        noBtn.addEventListener('mouseover', moveBtn); 
        noBtn.addEventListener('touchstart', moveBtn);
    </script>
    """
    components.html(escape_html, height=180)

else:
    st.balloons()
    st.markdown("<h1 class='main-title'>💖 عيد فطر مبارك 💖</h1>", unsafe_allow_html=True)
    
    # تحميل الأنيميشن مع الحماية من الخطأ
    lottie_eid = load_lottie("https://lottie.host/82542038-175f-4613-9533-5c08f4355a29/Nf4mD56lU0.json")
    if lottie_eid:
        st_lottie(lottie_eid, height=250)
    
    st.markdown(f"""
    <div style="background: rgba(255, 255, 255, 0.15); padding: 25px; border-radius: 20px; border: 1px solid rgba(255,255,255,0.3); backdrop-filter: blur(10px); color: white; text-align: center; margin: 0 auto; width: 85%;">
        <span style="font-size: 20px; opacity: 0.9;">✨ <b>عيدكِ مبارك</b> ✨</span><br>
        <div style="font-size: 32px; font-weight: 900; color: #ffd700; text-shadow: 0 0 15px rgba(255, 215, 0, 0.5); margin: 15px 0;">
            كل عام وأنتِ عيدي🎀
        </div>
        <span style="font-size: 22px; font-weight: bold; color: #ffffff;">&lt;سجاد😊&gt;</span>
    </div>
    """, unsafe_allow_html=True)

    if st.button("رجوع 🔄"):
        st.session_state.clicked_yes = False
        st.rerun()

st.write("---")
st.caption("<p style='text-align:center; color:white;'>برمجة سجاد | جميع الحقوق محفوظة</p>", unsafe_allow_html=True)
