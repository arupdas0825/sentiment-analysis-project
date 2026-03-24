from langdetect import detect, LangDetectException
from googletrans import Translator, LANGUAGES

translator = Translator()

# Language name + flag emoji map
LANG_FLAGS = {
    "en": ("English", "🇬🇧"),
    "bn": ("Bengali", "🇧🇩"),
    "hi": ("Hindi", "🇮🇳"),
    "fr": ("French", "🇫🇷"),
    "de": ("German", "🇩🇪"),
    "es": ("Spanish", "🇪🇸"),
    "zh-cn": ("Chinese", "🇨🇳"),
    "ar": ("Arabic", "🇸🇦"),
    "ja": ("Japanese", "🇯🇵"),
    "ru": ("Russian", "🇷🇺"),
    "pt": ("Portuguese", "🇵🇹"),
    "ko": ("Korean", "🇰🇷"),
}


def detect_language(text):
    try:
        lang_code = detect(text)
        if lang_code in LANG_FLAGS:
            name, flag = LANG_FLAGS[lang_code]
        else:
            name = LANGUAGES.get(lang_code, "Unknown").title()
            flag = "🌐"
        return {
            "code": lang_code,
            "name": name,
            "flag": flag
        }
    except LangDetectException:
        return {
            "code": "en",
            "name": "English",
            "flag": "🇬🇧"
        }


def translate_to_english(text):
    try:
        lang_info = detect_language(text)

        # Already English
        if lang_info["code"] == "en":
            return {
                "original": text,
                "translated": text,
                "lang_info": lang_info,
                "was_translated": False
            }

        result = translator.translate(text, dest="en")
        return {
            "original": text,
            "translated": result.text,
            "lang_info": lang_info,
            "was_translated": True
        }
    except Exception as e:
        return {
            "original": text,
            "translated": text,
            "lang_info": {"code": "en", "name": "English", "flag": "🇬🇧"},
            "was_translated": False,
            "error": str(e)
        }


def translate_multiple(texts):
    results = []
    for text in texts:
        result = translate_to_english(text)
        results.append(result)
    return results