from faster_whisper import WhisperModel
from deep_translator import GoogleTranslator

# 🔥 use stable model for CPU
model = WhisperModel(
    "base",
    device="cpu",
    compute_type="int8"
)

LANGUAGE_MAP = {
    "en": "en",
    "ta": "ta",
    "hi": "hi",
    "fr": "fr",
    "de": "de",
    "te": "te",
    "kn": "kn",
    "ml": "ml",
    "es": "es",
    "ko": "ko",
    "ja": "ja",
    "zh": "zh-cn",
    "ru": "ru",
    "ar": "ar",
    "it": "it",
    "pt": "pt"
}

def process_audio(audio_path, output_lang):

    # 1. detect language
    segments, info = model.transcribe(
        audio_path,
        beam_size=5,
        vad_filter=True
    )

    detected = info.language if info.language else "en"

    # 2. full transcription (IMPORTANT FIX HERE)
    segments, info = model.transcribe(
        audio_path,
        language=detected,
        beam_size=5,
        vad_filter=True
    )

    transcript = ""

    for seg in segments:
        transcript += seg.text + " "

    transcript = transcript.strip()

    # 3. translation
    try:
        translated = GoogleTranslator(
            source="auto",
            target=LANGUAGE_MAP.get(output_lang, "en")
        ).translate(transcript)

    except:
        translated = "Translation failed"

    highlighted = transcript

    return detected, transcript, highlighted, translated