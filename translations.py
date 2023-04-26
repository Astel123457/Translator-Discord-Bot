#TODO: add more languages
en = {
    "translation.warning" : "Please use /translate for better compatibiliy.",
    "message.warning" : "Please provide a message."
}
    

def translate(lang, key):
    lang = lang.upper()
    trans = ""
    if lang == "EN":
        trans = en.get(key, key)
    # If it's not a language that's supported, default to EN translations
    else: 
        trans = en.get(key, key)
    return trans

if __name__ == "__main__":
    print("why")
