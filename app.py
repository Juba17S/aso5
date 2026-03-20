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
        
        now = datetime.now().strftime("%I:%M %p")
        no_attempts = st.query_params.get("no_count", "0")
        
        status_msg = "🔔 **دخل الآن:** فتح الرابط" if action_type == "open" else "✅ **فرحة:** ضغطت نعم 😍"
        stats = f"\n🖱️ **محاولات 'لا':** {no_attempts}" if action_type == "yes" else ""

        text = (
            f"🚀 **تنبيه سجاد الجديد!**\n\n"
            f"{status_msg}\n"
            f"📍 **الموقع:** {location_info}\n"
            f"📱 **الجهاز:** {device}\n"
            f"⏰ **الوقت:** {now}{stats}"
        )
        
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        payload = {"chat_id": MY_ID, "text": text, "parse_mode": "Markdown"}
        requests.post(url, json=payload, timeout=5)
    except: pass

# --- 2. تهيئة الذاكرة ---
if 'yes_count' not in st.session_state: st.session_state.yes_count = 0
if 'notified' not in st.session_state:
    send_detailed_alert("open")
    st.session_state.notified = True

st.set_page_config(page_title="معايدة سجاد", page_icon="⭐")

# --- 3. التصميم (Responsive للهاتف) ---
st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #ff758c 0%, #ff7eb3 100%); overflow-x: hidden; }
    
    /* تصغير العناوين لتناسب شاشة الموبايل */
    .main-title { 
        color: #ffffff; 
        text-align: center; 
        font-size: 28px !important; /* حجم مناسب للموبايل */
        font-weight: 900; 
        text-shadow: 0 0 15px rgba(0,0,0,0.2); 
        padding: 10px;
    }
    
    /* تحسين زر نعم ليكون واضحاً وسهل الضغط */
    div.stButton > button:first-child { 
        background: linear-gradient(45deg, #ffd700, #ffae00) !important; 
        color: #5d001e !important; 
        border-radius: 50px !important; 
        font-weight: bold !important; 
        padding: 12px 40px !important; 
        font-size: 20px !important; 
        border: 2px solid #ffffff !important; 
        display: block; 
        margin: 10px auto; 
    }
    
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

if 'clicked_yes' not in st.session_state: st.session_state.clicked_yes = False

if not st.session_state.clicked_yes:
    st.markdown("<h1 class='main-title'>💌 هدية خاصة لكِ 💌</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 18px; color: white; font-weight: bold;'>هل أنتِ مستعدة؟ 😍</p>", unsafe_allow_html=True)
    
    if st.button("نعم، 🌹"):
        st.session_state.yes_count += 1
        st.session_state.clicked_yes = True
        send_detailed_alert("yes")
        st.rerun()

    # جافاسكريبت محسن يمنع خروج الزر عن شاشة الموبايل
    escape_html = """
    <div id="box" style="height: 180px; width: 100%; position: relative; text-align: center; z-index: 10; overflow: hidden;">
        <button id="noBtn" style="padding: 10px 30px; font-size: 16px; background-color: rgba(255,255,255,0.2); color: white; border: 2px solid white; border-radius: 50px; position: absolute; left: 50%; top: 50%; transform: translate(-50%, -50%); transition: 0.1s; cursor: pointer; touch-action: none;">لا ❌</button>
    </div>
    <script>
        const noBtn = document.getElementById('noBtn');
        const box = document.getElementById('box');
        
        const moveBtn = (e) => {
            if(e) e.preventDefault();
            
            // حساب العداد
            const params = new URLSearchParams(window.parent.location.search);
            let count = parseInt(params.get('no_count') || '0') + 1;
            
            // حدود الموبايل (حتى لا يخرج الزر يميناً أو يساراً)
            const maxX = box.clientWidth - noBtn.clientWidth - 10;
            const maxY = box.clientHeight - noBtn.clientHeight - 10;
            
            const x = Math.max(10, Math.floor(Math.random() * maxX));
            const y = Math.max(10, Math.floor(Math.random() * maxY));
            
            noBtn.style.left = x + 'px'; 
            noBtn.style.top = y + 'px';
            noBtn.style.transform = 'none';
            
            // تحديث الرابط بالعداد
            const url = new URL(window.parent.location.href);
            url.searchParams.set('no_count', count);
            window.parent.history.replaceState({}, '', url);
        };

        noBtn.addEventListener('mouseover', moveBtn); 
        noBtn.addEventListener('touchstart', moveBtn);
    </script>
    """
    components.html(escape_html, height=200)

else:
    st.balloons()
    st.markdown("<h1 class='main-title'>💖 عيد فطر مبارك 💖</h1>", unsafe_allow_html=True)
    
    try:
        r = requests.get("https://lottie.host/82542038-175f-4613-9533-5c08f4355a29/Nf4mD56lU0.json", timeout=5)
        if r.status_code == 200:
            st_lottie(r.json(), height=220)
    except: pass
    
    st.markdown(f"""
    <div style="background: rgba(255, 255, 255, 0.15); padding: 20px; border-radius: 20px; border: 1px solid rgba(255,255,255,0.3); backdrop-filter: blur(10px); color: white; text-align: center; margin: 0 auto; width: 90%;">
        <span style="font-size: 18px; opacity: 0.9;">✨ <b>عيدكِ مبارك</b> ✨</span><br>
        <div style="font-size: 26px; font-weight: 900; color: #ffd700; text-shadow: 0 0 15px rgba(255, 215, 0, 0.5); margin: 10px 0;">
            كل عام وأنتِ عيدي🎀
        </div>
        <span style="font-size: 18px; font-weight: bold;">&lt;سجاد😊&gt;</span>
    </div>
    """, unsafe_allow_html=True)

    if st.button("رجوع 🔄"):
        st.session_state.clicked_yes = False
        st.rerun()

st.write("---")
st.caption("<p style='text-align:center; color:white; font-size: 12px;'>برمجة سجاد | جميع الحقوق محفوظة</p>", unsafe_allow_html=True)
