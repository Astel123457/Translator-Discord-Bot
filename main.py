import discord
import deepl
import dc_secrets as dcs # This is so I don't have to delete the token before I commit anything.

#TODO: use langcodes for plaintext language to code conversion (eg "english" -> "en")

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

url = "https://api-free.deepl.com/v2/translate"
translator = deepl.Translator(dcs.deepl_auth) # dcs.deepl_auth is your DeepL API token
#TODO: Use translator.get_languages() to get a list of languages instead of hardcoding them
val_langs = ["BG", "CS", "DA", "DE", "EL", "EN-US", "ES", "ET", "FI", "FR", "HU", "ID", "IT", "JA", "KO", "LT", "LV", "NB", "NL", "PL", "PT-BR", "PT-PT", "RO", "RU", "SL", "SV", "TR", "UK", "ZH"]

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!trans'):
        req = message.content.split(" ", 2)
        lang = req[1].upper()
        text = req[2]
        #i hate the rest of this but it was 1 am when i coded this, it will be refactored later omg
        if lang == "EN":
            lang = "EN-US"
        if lang == "PT":
            message.channel.send("Especificar PT-BR ou PT-PT.")
            return
        if lang == "HELP":
            if text == "langs":
                langs = "Here is a list of languages that I currently support: \n"
                for i in val_langs:
                    if i == "EN-US":
                        langs = langs + "EN-US/EN\n"
                    else:
                        langs = langs + i + "\n"
                await message.channel.send(langs)
                return
        if lang not in val_langs:
            await message.channel.send("Sorry, but that is not a valid language, please type `!trans help langs` to get a list of languages.")
        else:
            result = translator.translate_text(text, target_lang=lang)
            await message.channel.send(result.text)
    if message.content.startswith('!usage'):
        usage = translator.get_usage()
        await message.channel.send(f"Character usage: {usage.character.count} of {usage.character.limit}")
        
client.run(dcs.bot_token)
