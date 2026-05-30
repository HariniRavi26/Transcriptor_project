import streamlit as st
from streamlit_mic_recorder import mic_recorder
from transcriber import process_audio
import tempfile
import os

st.set_page_config(page_title="AI Voice Translator", page_icon="🌍")

st.title("🌍 AI Multilingual Voice Translator")
st.write("🎤 Speak in ANY language")

languages = {
    "English": "en",
    "Tamil": "ta",
    "Hindi": "hi",
    "French": "fr",
    "German": "de",
    "Spanish": "es",
    "Telugu": "te",
    "Kannada": "kn",
    "Malayalam": "ml",
    "Korean": "ko",
    "Japanese": "ja",
    "Chinese": "zh",
    "Arabic": "ar",
    "Russian": "ru",
    "Italian": "it",
    "Portuguese": "pt"
}

output_lang = st.selectbox("🌎 Choose Output Language", list(languages.keys()))

st.info("🎙️ Click Start Recording and speak clearly")

audio = mic_recorder(
    start_prompt="🎤 Start Recording",
    stop_prompt="⏹ Stop Recording",
    just_once=True
)

# ❌ NO DEBUG PRINTS ANYMORE

if audio and isinstance(audio, dict):

    audio_bytes = audio.get("bytes") or audio.get("audio") or audio.get("data")

    if audio_bytes:

        st.success("🎧 Audio captured successfully!")

        st.audio(audio_bytes)

        temp = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
        temp.write(audio_bytes)
        temp.flush()
        temp.close()

        st.info("🔍 Processing audio... please wait")

        try:
            detected, transcript, highlighted, translated = process_audio(
                temp.name,
                languages[output_lang]
            )

            # ❌ REMOVE DETECTED LANGUAGE DISPLAY (YOUR REQUEST)

            st.subheader("📝 Original Transcript")
            st.markdown(highlighted, unsafe_allow_html=True)

            st.subheader("🌎 Translated Output")
            st.write(translated)

        except Exception as e:
            st.error(f"Error during processing: {e}")

        finally:
            if os.path.exists(temp.name):
                os.remove(temp.name)

    else:
        st.error("❌ No valid audio detected. Try again.")

else:
    st.warning("🎙️ Please record audio to continue.")