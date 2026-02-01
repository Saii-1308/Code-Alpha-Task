import streamlit as st
import requests

st.set_page_config(
    page_title="Language Translator",
    page_icon="🌍",
    layout="centered"
)

# ---------- CSS ----------
st.markdown("""
    <style>
        .main {
            background-color: #f7f9fc;
        }
        .stButton button {
            width: 100%;
            border-radius: 8px;
            height: 45px;
            font-size: 16px;
        }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if "output" not in st.session_state:
    st.session_state.output = ""

# ---------- UI ----------
st.markdown("<h1 style='text-align: center;'>🌍 Language Translator</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Translate text between languages instantly</p>", unsafe_allow_html=True)

st.markdown("### 🔤 Enter Your Text")
input_text = st.text_area("Type here...", height=120)

col1, col2 = st.columns(2)

with col1:
    source_lang = st.selectbox(
        "Source Language",
        ["Auto Detect", "English", "Spanish", "French", "German", "Japanese", "Hindi"]
    )

with col2:
    target_lang = st.selectbox(
        "Target Language",
        ["English", "Spanish", "French", "German", "Japanese", "Hindi"]
    )

# ---------- Translate Button ----------
if st.button("🔁 Translate"):
    if input_text.strip() == "":
        st.warning("⚠️ Please enter some text.")
    else:
        payload = {
            "text": input_text,
            "source_lang": source_lang,
            "target_lang": target_lang
        }

        try:
            res = requests.post("http://localhost:8000/translate", json=payload)

            if res.status_code == 200:
                translated_text = res.json().get("translated_text", "")
                st.session_state["output"] = translated_text
                st.success("✅ Translation Successful!")
            else:
                st.error("❌ Backend Error")

        except Exception as e:
            st.error("❌ Could not connect to backend")

# ---------- Output ----------
st.markdown("### 📘 Translated Text")
output_text = st.text_area(
    "Output",
    height=120,
    value=st.session_state.get("output", "")
)

# ---------- Buttons ----------
col3, col4 = st.columns(2)

with col3:
    if st.button("📋 Copy"):
        if output_text.strip() == "":
            st.warning("No text to copy!")
        else:
            st.toast("✅ Copied to clipboard!")

with col4:
    if st.button("🔊 Speak"):
        if output_text.strip() == "":
            st.warning("No text to speak!")
        else:
            try:
                tts_payload = {"text": output_text}
                tts_res = requests.post("http://localhost:8000/tts", json=tts_payload)

                if tts_res.status_code == 200:
                    audio_url = tts_res.json().get("audio_url")
                    st.audio(audio_url)
                    st.success("✅ Playing audio!")
                else:
                    st.error("❌ TTS failed!")

            except Exception as e:
                st.error("❌ Could not connect to TTS backend")

st.markdown("---")
st.markdown("<p style='text-align: center;'>Made with ❤️ using Streamlit</p>", unsafe_allow_html=True)
