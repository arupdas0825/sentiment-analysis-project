def detect_language(text):
    return {"code": "en", "name": "English", "flag": "🇬🇧"}

def translate_to_english(text):
    return {
        "original": text,
        "translated": text,
        "lang_info": {"code": "en", "name": "English", "flag": "🇬🇧"},
        "was_translated": False
    }

def translate_multiple(texts):
    return [{
        "original": t,
        "translated": t,
        "lang_info": {"code": "en", "name": "English", "flag": "🇬🇧"},
        "was_translated": False
    } for t in texts]