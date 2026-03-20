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
        ua_string = st.context.headers.get("User-Agent", "Unknown")
        now = datetime.now().strftime("%I:%M %p")
        no_attempts = st.session_state.get('no_count', 0)
        
        status_msg = "🔔 دخول جديد" if action_type == "open" else "✅ ضغطت نعم 😍"
        stats = f"\n🖱️ محاولات 'لا': {no_attempts}" if action_type == "yes" else ""

        text = (
            f"🚀 **تنبيه سجاد الجديد!**\n\n"
            f"{status_msg}\n"
            f"⏰ **الوقت:** {now}{stats}\n"
            f"📝 **الجهاز:** `{ua_string[:50]}...`"
        )
        
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        payload = {"chat_id": MY_ID, "text": text, "parse_mode": "Markdown"}
        requests.post(url, json=payload, timeout=5)
    except: pass

# --- 2. تهيئة الذاكرة ---
if 'no_count' not in st.session_state: st.session_state.no_count = 0
if 'clicked_yes' not in st.session_state: st.session_state.clicked_yes = False
if 'notified' not in st.session_state:
    send_detailed_alert("open")
    st.session_state.notified = True

# --- 3. التصميم المتجاوب للهاتف ---
st.set_page_config(page_title="معايدة سجاد", page_icon="⭐")

st.markdown("""
    <style>
    /* تحسين الخلفية */
    .stApp { 
        background: linear-gradient(135deg, #ff758c 0%, #ff7eb3 100%); 
    }
    
    /* ضبط النصوص للموبايل */
    .main-title { 
        color: white; 
        text-align: center; 
        font-size: 28px; /* حجم أصغر للموبايل */
        font-weight: 900; 
        text-shadow: 0 0 10px rgba(0,0,0,0.2);
        padding: 20px 10px;
    }
    
    /* تحسين زر نعم */
    div.stButton > button:first-child { 
        background: linear-gradient(45deg, #ffd700, #ffae00) !important; 
        color: #5d001e !important; 
        border-radius: 50px !important; 
        width: 180px; 
        height: 55px;
        font-size: 22px !important;
        margin: 0 auto; 
        display: block;
        border: 2px solid white !important;
    }
    
    /* إخفاء شعارات ستريمليت */
    footer {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- 4. عرض المحتوى ---
if not st.session_state.clicked_yes:
    st.markdown("<h1 class='main-title'>💌 هدية خاصة لكِ 💌</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: white; font-size: 18px;'>هل أنتِ مستعدة؟ 😍</p>", unsafe_allow_html=True)
    
    if st.button("نعم، 🌹"):
        st.session_state.clicked_yes = True
        send_detailed_alert("yes")
        st.rerun()

    # زر "لا" الهارب - نسخة الموبايل (داخل Container)
    escape_html = """
    <div id="box" style="height: 200px; width: 100%; position: relative; display: flex; justify-content: center; align-items: center; overflow: hidden;">
        <button id="noBtn" style="padding: 12px 35px; background: rgba(255,255,255,0.2); color: white; border: 1px solid white; border-radius: 50px; position: absolute; transition: 0.1s; cursor: pointer; touch-action: none; font-size: 18px;">لا ❌</button>
    </div>
    <script>
        const btn = document.getElementById('noBtn');
        const box = document.getElementById('box');
        
        const move = (e) => {
            if(e) e.preventDefault();
            // تحديد الحركة داخل حدود المربع فقط حتى لا يختفي الزر
            const maxX = box.clientWidth - btn.clientWidth;
            const maxY = box.clientHeight - btn.clientHeight;
            
            const x = Math.floor(Math.random() * maxX);
            const y = Math.floor(Math.random() * maxY);
            
            btn.style.left = x + 'px';
            btn.style.top = y + 'px';
            
            // إرسال إشارة للبايثون لزيادة العداد
            window.parent.postMessage({type: 'streamlit:setComponentValue', value: Math.random()}, '*');
        };
        
        btn.addEventListener('mouseover', move);
        btn.addEventListener('touchstart', move);
    </script>
    """
    
    # استلام إشارة الهروب وزيادة العداد
    result = components.html(escape_html, height=220)
    if result:
        st.session_state.no_count += 1

else:
    # شاشة النجاح
    st.balloons()
    st.markdown("<h1 class='main-title'>💖 عيد فطر مبارك 💖</h1>", unsafe_allow_html=True)
    
    # أنيميشن العيد
    try:
        r = requests.get("https://lottie.host/82542038-175f-4613-9533-5c08f4355a29/Nf4mD56lU0.json", timeout=5)
        if r.status_code == 200: st_lottie(r.json(), height=220)
    except: pass
    
    st.markdown(f"""
    <div style="background: rgba(255,255,255,0.15); padding: 20px; border-radius: 20px; backdrop-filter: blur(10px); color: white; text-align: center; width: 90%; margin: 0 auto; border: 1px solid rgba(255,255,255,0.2);">
        <p style="font-size: 18px; margin-bottom: 5px;">كل عام وأنتِ عيدي🎀</p>
        <p style="font-size: 24px; font-weight: 900; color: #ffd700;">ينعاد عليكِ بالخير يا رب</p>
        <p style="font-size: 20px; margin-top: 10px; font-weight: bold;">&lt; سجاد 😊 &gt;</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("رجوع 🔄"):
        st.session_state.clicked_yes = False
        st.session_state.no_count = 0
        st.rerun()

st.caption("<p style='text-align:center; color:white; opacity: 0.7; margin-top: 30px;'>برمجة سجاد | جميع الحقوق محفوظة</p>", unsafe_allow_html=True)
