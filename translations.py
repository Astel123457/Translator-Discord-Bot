# TODO: add more languages
en = {
    "translation.warning": "Please use /translate for better compatibility.",
    "translation.source": "Source: ",
    "translation.cjk_ambiguous": "This message may contain Chinese, Japanese, or Korean. Translating as all three for better accuracy.",
    "message.warning": "Please provide a message.",
    "message.somethingwrong": "Sorry, something went wrong. Please try again.",
    "help.warning": "Please specify a valid command for /help!",
    "help.supported": "Here is a list of languages that I currently support: "
}
ja = {
    "translation.warning": "より良い互換性のために /translate を使用してください。",
    "translation.source": "ソース: ",
    "translation.cjk_ambiguous": "このメッセージには、中国語、日本語、韓国語が含まれている可能性があります。より正確を期すため、3つとも翻訳しています。",
    "message.warning": "メッセージをご記入ください",
    "message.somethingwrong": "すみません、何か変でした。もう一度お試しください。",
    "help.warning": "/helpに有効なコマンドを指定してください!",
    "help.supported": "現在、私がサポートしている言語の一覧です: "
}
fr = {
    "translation.warning": "S'il vous plaît utilisez /translate pour une meilleure compatibilité",
    "translation.source": "Source: ",
    "translation.cjk_ambiguous": "Ce message peut contenir du chinois, du japonais ou du coréen. Traduction par les trois pour une meilleure précision.",
    "message.warning": "S'il vous plaît fournissez un message",
    "message.somethingwrong": "Désolé, quelque chose n'a pas marché, veuillez réessayer",
    "help.warning": "S'il vous plaît spécifiez une commande valide pour /help!",
    "help.supported": "Voici la liste des langues que je supporte pour le moment: "
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
# This is for testing purposed and is not to be used at all
# async def try_translate(*, message):
#    print(message)
#    return message


if __name__ == "__main__":
    print("why")
