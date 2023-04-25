class Translations:
    #TODO: add more languages
    en = {
        "translation.warning" : "Please use /translate for better compatibiliy.",
        "message.warning" : "Please provide a message."
    }
    

    def translate(self, lang, key):
        lang = lang.upper()
        if lang == "EN":
            trans = self.en.get(key, key)
        # If it's not a language that's supported, default to EN translations
        else: 
            self.en.get(key, key)
        return trans