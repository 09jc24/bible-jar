import streamlit as st
import random
import json
import os
import urllib.parse

# 1. Page Configuration
st.set_page_config(
    page_title="TGFHL Kids & Teens | Bible Jar",
    page_icon="static/icon.png" if os.path.exists("static/icon.png") else "🫙",
    layout="centered"
)

# 1B. Inject Custom Mobile Home Screen Icon & Web App Meta Tags
st.iframe("""
<script>
    const doc = window.parent.document;
    const head = doc.head;

    let appleIcon = doc.querySelector("link[rel='apple-touch-icon']");
    if (!appleIcon) {
        appleIcon = doc.createElement("link");
        appleIcon.rel = "apple-touch-icon";
        head.appendChild(appleIcon);
    }
    appleIcon.href = "/app/static/icon.png";

    const metaTags = [
        { name: "apple-mobile-web-app-capable", content: "yes" },
        { name: "apple-mobile-web-app-title", content: "Bible Jar" },
        { name: "application-name", content: "Bible Jar" },
        { name: "theme-color", content: "#EBF5FF" }
    ];
    metaTags.forEach(tag => {
        let el = doc.querySelector(`meta[name='${tag.name}']`);
        if (!el) {
            el = doc.createElement("meta");
            el.name = tag.name;
            head.appendChild(el);
        }
        el.content = tag.content;
    });
</script>
""", height=1)

# 2. Custom CSS for Uniform Buttons, Big Emojis & Soft Pastel Background
st.markdown("""
<style>
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(160deg, #FFFDF7 0%, #EBF5FF 50%, #F3E8FF 100%) !important;
    }
    [data-testid="stHeader"] {
        background: transparent !important;
    }
    h1 {
        color: #1E293B !important;
        text-align: center;
        font-family: 'Trebuchet MS', sans-serif !important;
        font-size: 2.3rem !important;
        margin-bottom: 0.2rem !important;
    }
    /* Force dark readable text on Language Toggle & Expander even in Dark Mode */
    [data-testid="stRadio"] label,
    [data-testid="stRadio"] p,
    [data-testid="stExpander"] summary,
    [data-testid="stExpander"] summary p,
    [data-testid="stExpander"] div p,
    [data-testid="stExpander"] li {
        color: #1E293B !important;
    }

    /* Style the bottom expander so it looks like a clean pill card */
    [data-testid="stExpander"] {
        background-color: rgba(255, 255, 255, 0.85) !important;
        border-radius: 16px !important;
        border: 1px solid #CBD5E1 !important;
    }

    /* Uniform size for all 10 buttons */
    div.stButton {
        width: 100% !important;
    }
    div.stButton > button {
        width: 100% !important;
        height: 84px !important;
        min-height: 84px !important;
        max-height: 84px !important;
        border-radius: 20px !important;
        border: none !important;
        padding: 10px 14px !important;
        margin-bottom: 8px !important;
        box-shadow: 0 6px 14px rgba(0, 0, 0, 0.12) !important;
        transition: all 0.15s ease-in-out !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
    }
    div.stButton > button p {
        font-size: 18px !important;
        font-weight: 800 !important;
        color: #FFFFFF !important;
        line-height: 1.25 !important;
        margin: 0 !important;
    }
    div.stButton > button p::first-letter {
        font-size: 28px !important;
        margin-right: 6px !important;
    }
    div.stButton > button:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 10px 18px rgba(0, 0, 0, 0.18) !important;
    }
    div.stButton > button:active {
        transform: scale(0.96) !important;
    }

    /* Left Column (5 Buttons) */
    div[data-testid="stHorizontalBlock"] > div:nth-child(1) div[data-testid="stVerticalBlock"] > div:nth-of-type(1) button {
        background: linear-gradient(135deg, #FF5252 0%, #D32F2F 100%) !important; /* Red - Angry */
    }
    div[data-testid="stHorizontalBlock"] > div:nth-child(1) div[data-testid="stVerticalBlock"] > div:nth-of-type(2) button {
        background: linear-gradient(135deg, #FFB300 0%, #F57C00 100%) !important; /* Amber - Anxious */
    }
    div[data-testid="stHorizontalBlock"] > div:nth-child(1) div[data-testid="stVerticalBlock"] > div:nth-of-type(3) button {
        background: linear-gradient(135deg, #AB47BC 0%, #6A1B9A 100%) !important; /* Purple - Lonely */
    }
    div[data-testid="stHorizontalBlock"] > div:nth-child(1) div[data-testid="stVerticalBlock"] > div:nth-of-type(4) button {
        background: linear-gradient(135deg, #26A69A 0%, #00695C 100%) !important; /* Teal - Insecure */
    }
    div[data-testid="stHorizontalBlock"] > div:nth-child(1) div[data-testid="stVerticalBlock"] > div:nth-of-type(5) button {
        background: linear-gradient(135deg, #5C6BC0 0%, #283593 100%) !important; /* Indigo - Guilty */
    }

    /* Right Column (5 Buttons) */
    div[data-testid="stHorizontalBlock"] > div:nth-child(2) div[data-testid="stVerticalBlock"] > div:nth-of-type(1) button {
        background: linear-gradient(135deg, #42A5F5 0%, #1565C0 100%) !important; /* Blue - Sad */
    }
    div[data-testid="stHorizontalBlock"] > div:nth-child(2) div[data-testid="stVerticalBlock"] > div:nth-of-type(2) button {
        background: linear-gradient(135deg, #66BB6A 0%, #2E7D32 100%) !important; /* Green - Happy */
    }
    div[data-testid="stHorizontalBlock"] > div:nth-child(2) div[data-testid="stVerticalBlock"] > div:nth-of-type(3) button {
        background: linear-gradient(135deg, #FF7043 0%, #D84315 100%) !important; /* Coral - Overwhelmed */
    }
    div[data-testid="stHorizontalBlock"] > div:nth-child(2) div[data-testid="stVerticalBlock"] > div:nth-of-type(4) button {
        background: linear-gradient(135deg, #EC407A 0%, #AD1457 100%) !important; /* Rose Pink - Unloved */
    }
    div[data-testid="stHorizontalBlock"] > div:nth-child(2) div[data-testid="stVerticalBlock"] > div:nth-of-type(5) button {
        background: linear-gradient(135deg, #78909C 0%, #37474F 100%) !important; /* Slate Blue - Tired */
    }

    /* Styled Scripture Card */
    .verse-card {
        background-color: #FFFFFF;
        padding: 24px;
        border-radius: 22px;
        box-shadow: 0 8px 24px rgba(15, 23, 42, 0.08);
        border-left: 8px solid #3B82F6;
        margin-top: 14px;
        margin-bottom: 15px;
    }
    .verse-ref {
        font-size: 22px;
        font-weight: 800;
        color: #1E293B;
        margin-bottom: 10px;
    }
    .verse-text {
        font-size: 19px;
        font-style: italic;
        color: #0F172A;
        background-color: #F8FAFC;
        padding: 14px;
        border-radius: 12px;
        margin-bottom: 14px;
    }
    .verse-note {
        font-size: 17px;
        color: #334155;
        margin-bottom: 12px;
        line-height: 1.5;
    }
    .verse-prayer {
        font-size: 17px;
        color: #1D4ED8;
        background-color: #EFF6FF;
        padding: 12px;
        border-radius: 12px;
        line-height: 1.5;
    }

    /* Share Action Bar */
    .share-row {
        display: flex;
        gap: 12px;
        margin-top: 8px;
        margin-bottom: 16px;
        flex-wrap: wrap;
    }
    .share-btn {
        flex: 1;
        min-width: 210px;
        display: inline-flex !important;
        align-items: center !important;
        justify-content: center !important;
        gap: 10px !important;
        padding: 14px 18px !important;
        border-radius: 16px !important;
        font-weight: 800 !important;
        font-size: 18px !important;
        text-decoration: none !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.12) !important;
        transition: transform 0.15s ease-in-out !important;
    }
    .share-btn:hover {
        transform: translateY(-2px) !important;
        opacity: 0.95 !important;
    }
    .btn-whatsapp {
        background-color: #25D366 !important;
        color: #FFFFFF !important;
    }
    .btn-sms {
        background-color: #3B82F6 !important;
        color: #FFFFFF !important;
    }
</style>
""", unsafe_allow_html=True)

# 3. Language Toggle
lang = st.radio("Language / Idioma:", ["English 🇺🇸", "Español 🇲🇽"], horizontal=True)
is_es = "Español" in lang

# 4. Header
icon_path = os.path.join(os.path.dirname(__file__), "static", "icon.png")

if os.path.exists(icon_path):
    _, center_col, _ = st.columns([2, 1, 2])
    with center_col:
        st.image(icon_path, width=84)
    title_prefix = ""
else:
    title_prefix = "🫙 "
if is_es:
    st.title(f"{title_prefix}Tu Frasco Bíblico")
    st.markdown("<p style='text-align:center; font-size:18px; color:#475569;'>¿Cómo te sientes hoy? Toca tu emoción para abrir un mensaje de Dios para ti.</p>", unsafe_allow_html=True)
else:
    st.title(f"{title_prefix}Your Bible Jar")
    st.markdown("<p style='text-align:center; font-size:18px; color:#475569;'>How are you feeling right now? Tap your emotion to pull a Bible message just for you.</p>", unsafe_allow_html=True)

# 5. Database of Passages (Expand each list to 15 passages to reach 90 total!)
json_path = os.path.join(os.path.dirname(__file__), "passages.json")
with open(json_path, "r", encoding="utf-8") as f:
    passages = json.load(f)

# 6. Emotion Buttons Grid
if "selected_emotion" not in st.session_state:
    st.session_state.selected_emotion = None
if "current_choice" not in st.session_state:
    st.session_state.current_choice = None
if "seen_passages" not in st.session_state:
    st.session_state.seen_passages = {}

def pick_verse(emotion_key):
    st.session_state.selected_emotion = emotion_key
    all_items = passages[emotion_key]
    seen_indices = st.session_state.seen_passages.get(emotion_key, [])
    available_indices = [i for i in range(len(all_items)) if i not in seen_indices]
    if not available_indices:
        seen_indices = []
        available_indices = list(range(len(all_items)))
    chosen_idx = random.choice(available_indices)
    seen_indices.append(chosen_idx)
    st.session_state.seen_passages[emotion_key] = seen_indices
    st.session_state.current_choice = all_items[chosen_idx]

col1, col2 = st.columns(2)

with col1:
    if st.button("😠 Enojado" if is_es else "😠 Angry", use_container_width=True):
        pick_verse("angry")
    if st.button("😰 Ansioso / Con Miedo" if is_es else "😰 Anxious / Scared", use_container_width=True):
        pick_verse("anxious")
    if st.button("🥺 Solo / Rechazado" if is_es else "🥺 Lonely / Left Out", use_container_width=True):
        pick_verse("lonely")
    if st.button("🪞 Inseguro / No Suficiente" if is_es else "🪞 Insecure / Not Enough", use_container_width=True):
        pick_verse("insecure")
    if st.button("😔 Culpable / Avergonzado" if is_es else "😔 Guilty / Ashamed", use_container_width=True):
        pick_verse("guilty")

with col2:
    if st.button("😢 Triste" if is_es else "😢 Sad", use_container_width=True):
        pick_verse("sad")
    if st.button("🥳 Feliz / Agradecido" if is_es else "🥳 Happy / Thankful", use_container_width=True):
        pick_verse("happy")
    if st.button("🤯 Abrumado / Confundido" if is_es else "🤯 Overwhelmed / Confused", use_container_width=True):
        pick_verse("overwhelmed")
    if st.button("💔 No Amado / Herido" if is_es else "💔 Unloved / Hurt", use_container_width=True):
        pick_verse("unloved")
    if st.button("😩 Cansado / Agotado" if is_es else "😩 Tired / Burned Out", use_container_width=True):
        pick_verse("tired")

# 7. Display the Drawn Passage + One-Tap Share Buttons
if st.session_state.current_choice:
    choice = st.session_state.current_choice

    if is_es:
        st.markdown(f"""
        <div class="verse-card">
            <div class="verse-ref">📖 {choice['ref_es']}</div>
            <div class="verse-text">"{choice['verse_es']}"</div>
            <div class="verse-note"><strong>💬 Jesús te dice:</strong> {choice['note_es']}</div>
            <div class="verse-prayer"><strong>🙏 Hablemos con Él:</strong> <em>{choice['prayer_es']}</em></div>
        </div>
        """, unsafe_allow_html=True)

        share_text = (
            f"🫙 Tu Frasco Bíblico\n\n"
            f"📖 {choice['ref_es']}\n"
            f"\"{choice['verse_es']}\"\n\n"
            f"💬 {choice['note_es']}\n\n"
            f"🙏 {choice['prayer_es']}"
        )
        encoded = urllib.parse.quote(share_text)
        st.markdown(f"""
        <div class="share-row">
            <a class="share-btn btn-whatsapp" href="https://whatsapp.com{encoded}" target="_blank">
                <svg width="24" height="24" viewBox="0 0 32 32" fill="#FFFFFF" xmlns="http://w3.org">
                    <path d="M16.004 3.2c-7.06 0-12.8 5.74-12.8 12.8 0 2.256.59 4.46 1.71 6.402L3.1 28.8l6.564-1.722a12.74 12.74 0 0 0 6.34 1.682h.006c7.058 0 12.796-5.74 12.796-12.8 0-3.42-1.332-6.636-3.75-9.054A12.716 12.716 0 0 0 16.004 3.2zm0 23.404h-.004a10.6 10.6 0 0 1-5.404-1.48l-.388-.23-3.896 1.022 1.04-3.798-.252-.402a10.575 10.575 0 0 1-1.622-5.636c0-5.858 4.766-10.624 10.628-10.624 2.838 0 5.506 1.106 7.512 3.114a10.556 10.556 0 0 1 3.11 7.516c0 5.86-4.768 10.618-10.624 10.618zm5.828-7.954c-.32-.16-1.89-.932-2.182-1.038-.294-.106-.508-.16-.72.16-.214.32-.826 1.038-1.012 1.252-.186.214-.374.24-.694.08-.32-.16-1.35-.498-2.572-1.588-.95-.848-1.592-1.894-1.778-2.214-.186-.32-.02-.492.14-.652.144-.144.32-.374.48-.56.16-.186.214-.32.32-.534.106-.214.054-.4-.026-.56-.08-.16-.72-1.734-.986-2.374-.26-.624-.524-.54-.72-.55l-.614-.01c-.214 0-.56.08-.854.4-.294.32-1.12 1.094-1.12 2.668s1.146 3.094 1.306 3.308c.16.214 2.256 3.444 5.466 4.83.764.33 1.36.526 1.824.674.766.244 1.464.21 2.016.126.614-.092 1.89-.772 2.156-1.518.266-.746.266-1.386.186-1.518-.08-.134-.294-.214-.614-.374z"/>
                </svg>
                Compartir por WhatsApp
            </a>
            <a class="share-btn btn-sms" href="sms:?&body={encoded}">💬 Enviar por Mensaje</a>
        </div>
        """, unsafe_allow_html=True)


        with st.expander("📋 Copiar texto para pegar en Instagram / TikTok / Notas"):
            st.code(share_text, language=None)

    else:
        st.markdown(f"""
        <div class="verse-card">
            <div class="verse-ref">📖 {choice['ref_en']}</div>
            <div class="verse-text">"{choice['verse_en']}"</div>
            <div class="verse-note"><strong>💬 Jesus shares with you:</strong> {choice['note_en']}</div>
            <div class="verse-prayer"><strong>🙏 Let's pray together:</strong> <em>{choice['prayer_en']}</em></div>
        </div>
        """, unsafe_allow_html=True)

        share_text = (
            f"🫙 Your Bible Jar\n\n"
            f"📖 {choice['ref_en']}\n"
            f"\"{choice['verse_en']}\"\n\n"
            f"💬 {choice['note_en']}\n\n"
            f"🙏 {choice['prayer_en']}"
        )
        encoded = urllib.parse.quote(share_text)
        st.markdown(f"""
        <div class="share-row">
            <a class="share-btn btn-whatsapp" href="https://whatsapp.com{encoded}" target="_blank">
                <svg width="24" height="24" viewBox="0 0 32 32" fill="#FFFFFF" xmlns="http://w3.org">
                    <path d="M16.004 3.2c-7.06 0-12.8 5.74-12.8 12.8 0 2.256.59 4.46 1.71 6.402L3.1 28.8l6.564-1.722a12.74 12.74 0 0 0 6.34 1.682h.006c7.058 0 12.796-5.74 12.796-12.8 0-3.42-1.332-6.636-3.75-9.054A12.716 12.716 0 0 0 16.004 3.2zm0 23.404h-.004a10.6 10.6 0 0 1-5.404-1.48l-.388-.23-3.896 1.022 1.04-3.798-.252-.402a10.575 10.575 0 0 1-1.622-5.636c0-5.858 4.766-10.624 10.628-10.624 2.838 0 5.506 1.106 7.512 3.114a10.556 10.556 0 0 1 3.11 7.516c0 5.86-4.768 10.618-10.624 10.618zm5.828-7.954c-.32-.16-1.89-.932-2.182-1.038-.294-.106-.508-.16-.72.16-.214.32-.826 1.038-1.012 1.252-.186.214-.374.24-.694.08-.32-.16-1.35-.498-2.572-1.588-.95-.848-1.592-1.894-1.778-2.214-.186-.32-.02-.492.14-.652.144-.144.32-.374.48-.56.16-.186.214-.32.32-.534.106-.214.054-.4-.026-.56-.08-.16-.72-1.734-.986-2.374-.26-.624-.524-.54-.72-.55l-.614-.01c-.214 0-.56.08-.854.4-.294.32-1.12 1.094-1.12 2.668s1.146 3.094 1.306 3.308c.16.214 2.256 3.444 5.466 4.83.764.33 1.36.526 1.824.674.766.244 1.464.21 2.016.126.614-.092 1.89-.772 2.156-1.518.266-.746.266-1.386.186-1.518-.08-.134-.294-.214-.614-.374z"/>
                </svg>
                Share on WhatsApp
            </a>
            <a class="share-btn btn-sms" href="sms:?&body={encoded}">💬 Share via Text / iMessage</a>
        </div>
        """, unsafe_allow_html=True)


        with st.expander("📋 Copy verse text to paste anywhere"):
            st.code(share_text, language=None)

# 8. Install Instructions Expander
st.divider()
expander_title = "📲 ¿Cómo poner este botón en tu teléfono?" if is_es else "📲 How to add this app button to your phone?"

with st.expander(expander_title):
    if is_es:
        st.write("""
        Para guardar el ícono oficial de **Bible Jar** en tu pantalla:
        1. Abre **https://github.io** en **Safari** (iPhone/iPad) o **Chrome** (Android).
        2. **Antes de tocar 'Abrir'**, toca el botón **Compartir** (Safari) o los **3 puntos** (Chrome) y elige **'Agregar a inicio' / 'Agregar a la pantalla principal'**.
        """)
    else:
        st.write("""
        To save the official **Bible Jar** icon to your Home Screen:
        1. Open **https://github.io** in **Safari** (iPhone/iPad) or **Chrome** (Android).
        2. **Before tapping 'Open'**, tap the **Share icon** (Safari) or **3 dots** (Chrome) and choose **'Add to Home Screen'**.
        """)
