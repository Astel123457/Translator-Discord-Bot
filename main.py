import discord
from discord import app_commands
from discord.ext import commands
import deepl
import dc_secrets as dcs # This is so I don't have to delete the token before I commit anything.
from translations import Translations as t


#TODO: use langcodes for plaintext language to code conversion (eg "english" -> "en")
#TODO: add translations for some pre-defined messages, like the slash command mention on line 40

intents = discord.Intents.default()
intents.message_content = True

activity = discord.Activity(name='and Translating...', type=discord.ActivityType.watching)

client = discord.Client(intents=intents, activity=activity)

tree = app_commands.CommandTree(client)


url = "https://api-free.deepl.com/v2/translate"
translator = deepl.Translator(dcs.deepl_auth) # dcs.deepl_auth is you DeepL API token
#TODO: Use translator.get_languages() to get a list of languages instead of hardcoding them
val_langs = ["BG", "CS", "DA", "DE", "EL", "EN-US", "ES", "ET", "FI", "FR", "HU", "ID", "IT", "JA", "KO", "LT", "LV", "NB", "NL", "PL", "PT-BR", "PT-PT", "RO", "RU", "SL", "SV", "TR", "UK", "ZH"]

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.content.startswith("!sync"):
        await tree.sync(guild=discord.Object(id=889711909379641375))
        await tree.sync()
        return

    if message.content.startswith('!trans'): #keeping this for backwards compat, might be phased out in the future
        req = message.content.split(" ", 2)
        lang = req[1].upper()
        text = req[2]
        await message.channel.send(t.translate(lang=lang, key="translation.warning"))
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
    

@tree.command(name="translate", description="Translate some text")
@app_commands.describe(message="Message to translate")
@app_commands.describe(language="Language to translate to (default is english)")
async def Translator(interaction: discord.Interaction, message: str = None, language: str = None):
    await interaction.response.defer() # fix 404 no webhook bc apperently it takes over 3 seconds to respond (it doesn't it only takes like 500 ms)
    if language == None:
        language = "EN-US"
    language = language.upper()
    if message == None:
        await interaction.followup.send(content=t.translate(lang=language.upper(), key="message.warning"))
        return
    if language == "EN":
        language == "EN-US"
    try: # This is mostly to fix limit/bad language errors, so we just show it to the user i'll figure out a way to make it better later
        result = translator.translate_text(message, target_lang=language)
    except deepl.exceptions.DeepLException as e:
        interaction.followup.send(content=e)
    await interaction.followup.send(content=result)
    return
        
client.run(dcs.bot_token)
