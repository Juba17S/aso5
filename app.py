import streamlit as st
from streamlit_lottie import st_lottie
import requests
import streamlit.components.v1 as components
import random
from datetime import datetime
import pytz

# --- 1. إعدادات التنبيه (تليجرام) ---
TOKEN = "8664972776:AAELmEwNi_NcOtKHb8va_16czNLtCJdBqLI"
MY_ID = "8279656170"

def send_detailed_alert(action_type):
    try:
        location_info = "غير معروف 🛰️"
        try:
            response = requests.get("http://ip-api.com/json/", timeout=5).json()
            if response.get("status") == "success":
                location_info = f"{response.get('country')} - {response.get('city')}"
        except: pass

        ua_string = st.context.headers.get("User-Agent", "Unknown")
        device = "كمبيوتر 💻"
        if "Android" in ua_string: device = "أندرويد 📱"
        elif "iPhone" in ua_string or "iPad" in ua_string: device = "آيفون/آيباد 🍎"
        
        browser = "متصفح 🌐"
        if "Telegram" in ua_string: browser = "تطبيق تليجرام ✈️"
        elif "Chrome" in ua_string: browser = "كروم 🌐"
        elif "Safari" in ua_string: browser = "سفاري 🧭"

        # ضبط الوقت المباشر بتوقيت بغداد 🇮🇶
        iq_tz = pytz.timezone('Asia/Baghdad')
        now_iq = datetime.now(iq_tz).strftime("%I:%M:%S %p") 
        
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
            f"⏰ **توقيت بغداد:** {now_iq}{stats}\n\n"
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

def load_lottie(url):
    try:
        r = requests.get(url, timeout=5)
        if r.status_code == 200: return r.json()
        return None
    except: return None

# --- 3. التصميم (تركيز كامل على توافق الموبايل) ---
st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #ff758c 0%, #ff7eb3 100%); overflow-x: hidden; }
    
    /* ضبط العنوان ليكون مرن جداً على الشاشات الصغيرة */
    .main-title { 
        color: #ffffff; 
        text-align: center; 
        font-size: clamp(22px, 7vw, 32px); /* يصغر آلياً للموبايل */
        font-weight: 900; 
        text-shadow: 0 0 15px rgba(255, 215, 0, 0.4); 
        padding: 15px 5px;
        line-height: 1.3;
    }
    
    /* ضبط حجم البطاقة البيضاء الشفافة */
    .wish-card {
        background: rgba(255, 255, 255, 0.15); 
        padding: 20px; 
        border-radius: 20px; 
        border: 1px solid rgba(255,255,255,0.3); 
        backdrop-filter: blur(10px); 
        color: white; 
        text-align: center; 
        margin: 0 auto; 
        width: 90%; /* عرض مناسب جداً للموبايل */
    }

    /* زر نعم - كبسة مريحة للإصبع */
    div.stButton > button:first-child { 
        background: linear-gradient(45deg, #ffd700, #ffae00) !important; 
        color: #5d001e !important; 
        border-radius: 50px !important; 
        font-weight: bold !important; 
        padding: 12px 0 !important; 
        width: 160px; /* عرض ثابت ليكون متناسق */
        font-size: 18px !important; 
        border: 2px solid #ffffff !important; 
        display: block; 
        margin: 10px auto !important; 
    }
    
    .sub-text {
        text-align: center; 
        font-size: clamp(16px, 5vw, 19px); 
        color: white; 
        font-weight: 500;
        margin-bottom: 20px;
    }

    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

if 'clicked_yes' not in st.session_state: st.session_state.clicked_yes = False

if not st.session_state.clicked_yes:
    st.markdown("<h1 class='main-title'>💌 هدية خاصة لكِ 💌</h1>", unsafe_allow_html=True)
    st.markdown("<p class='sub-text'>هل أنتِ مستعدة؟ 😍</p>", unsafe_allow_html=True)
    
    if st.button("نعم، 🌹"):
        st.session_state.yes_count += 1
        st.session_state.clicked_yes = True
        send_detailed_alert("yes")
        st.rerun()

    # جافاسكريبت العداد
    escape_html = """
    <div id="box" style="height: 120px; width: 100%; position: relative; text-align: center;">
        <button id="noBtn" style="padding: 10px 25px; font-size: 16px; background-color: rgba(255,255,255,0.2); color: white; border: 1.5px solid white; border-radius: 50px; position: absolute; transition: 0.1s; cursor: pointer; left: 50%; transform: translateX(-50%); touch-action: none;">لا ❌</button>
    </div>
    <script>
        const noBtn = document.getElementById('noBtn');
        const box = document.getElementById('box');
        const moveBtn = (e) => {
            if(e) e.preventDefault();
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
    components.html(escape_html, height=150)

else:
    st.balloons()
    st.markdown("<h1 class='main-title'>💖 عيد فطر مبارك 💖</h1>", unsafe_allow_html=True)
    
    lottie_eid = load_lottie("https://lottie.host/82542038-175f-4613-9533-5c08f4355a29/Nf4mD56lU0.json")
    if lottie_eid:
        st_lottie(lottie_eid, height=220)
    
    st.markdown(f"""
    <div class="wish-card">
        <span style="font-size: 18px; opacity: 0.9;">✨ <b>عيدكِ مبارك</b> ✨</span><br>
        <div style="font-size: clamp(20px, 6vw, 28px); font-weight: 900; color: #ffd700; text-shadow: 0 0 10px rgba(255, 215, 0, 0.4); margin: 15px 0;">
            كل عام وأنتِ عيدي🎀
        </div>
        <span style="font-size: 18px; font-weight: bold; color: #ffffff;">&lt;سجاد😊&gt;</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("رجوع 🔄"):
        st.session_state.clicked_yes = False
        st.rerun()

st.write("---")
st.caption("<p style='text-align:center; color:white; font-size:12px;'>برمجة سجاد | جميع الحقوق محفوظة</p>", unsafe_allow_html=True)
