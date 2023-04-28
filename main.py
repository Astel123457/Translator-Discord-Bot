import discord
from discord import app_commands
from discord.ext import commands
import deepl
import dc_secrets as dcs # This is so I don't have to delete the token before I commit anything.
import translations as t 
import sys
import langcodes

#TODO: further langcodes development, so you only have to type the langauge (in any language) instead of a code, when wanted
#TODO: add translations for some pre-defined messages, like the slash command mention on line 40

intents = discord.Intents.default()
intents.message_content = True

activity = discord.Activity(name='and Translating...', type=discord.ActivityType.watching)

client = discord.Client(intents=intents, activity=activity)

tree = app_commands.CommandTree(client)

url = "https://api-free.deepl.com/v2/translate"
translator = deepl.Translator(dcs.deepl_auth) # dcs.deepl_auth is you DeepL API token
#TODO: Use translator.get_languages() to get a list of languages instead of hardcoding them
val_langs = ["BG", "CS", "DA", "DE", "EL", "EN-US", "EN-GB", "ES", "ET", "FI", "FR", "HU", "ID", "IT", "JA", "KO", "LT", "LV", "NB", "NL", "PL", "PT-BR", "PT-PT", "RO", "RU", "SL", "SV", "TR", "UK", "ZH"]

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.content.startswith("!sync"):
        print("syncing")
        await tree.sync(guild=discord.Object(id=889711909379641375))
        print("syncing...")
        await tree.sync()
        print("done")
        return

    if message.content.startswith('!trans'): #keeping this for backwards compat, might be phased out in the future
        req = message.content.split(" ", 2)
        lang = req[1].upper()
        text = req[2]
        await message.channel.send(t.use_translate(lang=lang, key="translation.warning"))
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
    
#TODO: figure out how to use app_commands.translate and related functions to translate descriptions and add renames for the values
@tree.command(name="translate", description="Translate some text")
@app_commands.describe(message="Message to translate")
@app_commands.describe(language="Language to translate to (default is english)")
async def Translator(interaction: discord.Interaction, message: str, language: str = None):
    await interaction.response.defer() # fix 404 no webhook bc apperently it takes over 3 seconds to respond (it doesn't it only takes like 500 ms)
    if language == None:
        language = "EN-US"
    language = language.upper()
    if message == None:
        await interaction.followup.send(content=t.use_translate(lang=language.upper(), key="message.warning"))
        return
    if language == "EN":
        language == "EN-US"
    try: # This is mostly to fix limit/bad language errors, so we just show it to the user i'll figure out a way to make it better later
        result = translator.translate_text(message, target_lang=language)
        res_lang = langcodes.get(result.detected_source_lang)
        get = res_lang.describe(language.lower())
        result_lang = get.get("language")
    except deepl.exceptions.DeepLException as e:
        interaction.followup.send(content=e)
    await interaction.followup.send(content=t.use_translate(language, "translation.source") + result_lang + "\n" + result.text)
    return

@tree.command(name="help", description="Display a help message in your langauage")
@app_commands.describe(help="Which help message to display.")
@app_commands.describe(language="Displays the help message in this language (Default is \"English (United States)\")")
async def Help(interaction: discord.Interaction, help: str = "languages", language: str = "en-us"):
    await interaction.response.defer()
    if help == "languages":
        result = translator.get_target_languages()
        langs = "Here is a list of languages that I currently support: \n"
        for lang in result:
            res_lang = langcodes.get(lang.code)
            get = res_lang.describe(language.lower())
            result_lang = get.get("language")
            langs = langs + f"{result_lang} ({lang.code})\n"
        await interaction.followup.send(content=langs)
    else: 
        await interaction.followup.send(content=t.use_translate(language, "help.warning"))


if __name__ == "__main__":
    if len(sys.argv) < 1:
        if sys.argv[1] == "--no-bot":
            lang = sys.argv[2]
            print("Lang: " + lang)
            message = sys.argv[3:]
            text = ""
            for i in message:
                text = text + i + " "
            print("Message: " + text)
            result = translator.translate_text(text, target_lang=lang)
            print(result)
    else:
        client.run(dcs.bot_token)
