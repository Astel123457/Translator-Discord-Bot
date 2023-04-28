#TODO: add more languages
en = {
    "translation.warning" : "Please use /translate for better compatibility.",
    "translation.source": "Source: ",
    "message.warning" : "Please provide a message.",
    "message.somethingwrong" : "Sorry, something went wrong. Please try again.",
    "help.warning" : "Please specify a valid command for /help!", 
    "help.supported" : "Here is a list of languages that I currently support: "
}
ja = {
    "translation.warning" : "より良い互換性のために /translate を使用してください。",
    "translation.source": "ソース: ",
    "message.warning" : "メッセージをご記入ください",
    "message.somethingwrong" : "すみません、何か変でした。もう一度お試しください。",
    "help.warning" : "/helpに有効なコマンドを指定してください!", 
    "help.supported" : "Here is a list of languages that I currently support: "
}
fr {
    "translation.warning" : "Please use /translate for better compatibility.",
    "translation.source": "Source: ",
    "message.warning" : "Please provide a message.",
    "message.somethingwrong" : "Sorry, something went wrong. Please try again.",
    "help.warning" : "Please specify a valid command for /help!",
    "help.supported" : "Here is a list of languages that I currently support: "
}

def use_translate(lang, key):
    lang = lang.upper()
    trans = ""
    if lang == "EN":
        trans = en.get(key, key)
    
    elif lang == "JA":
        trans = ja.get(key, key)
    elif lang == "FR":
        trans = fr.get(key, key)
    # If it's not a language that's supported, default to EN translations
    else: 
        trans = en.get(key, key)
    return trans

async def try_translate(*, message):
    print(message)
    return message

if __name__ == "__main__":
    print("why")
