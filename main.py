import discord
from discord import app_commands
from discord.ext import commands
import deepl
import dc_secrets as dcs  # This is so I don't have to delete the token before I commit anything.
import translations as t
import sys
import langcodes
import argparse
import json

from langdetect import detect, DetectorFactory, LangDetectException
# set seed to 0 to make langdetect deterministic
DetectorFactory.seed = 0

# TODO: use langcodes for plaintext language to code conversion (eg "english" -> "en")
# TODO: add translations for some pre-defined messages, like the slash command mention on line 40

intents = discord.Intents.default()
intents.message_content = True

activity = discord.Activity(name='and Translating...', type=discord.ActivityType.watching)

bot = commands.Bot(command_prefix="!", intents=intents, activity=activity)

url = "https://api-free.deepl.com/v2/translate"
translator = deepl.Translator(dcs.deepl_auth)  # dcs.deepl_auth is you DeepL API token
# TODO: Use translator.get_languages() to get a list of languages instead of hardcoding them
val_langs = ["BG", "CS", "DA", "DE", "EL", "EN-US", "EN-GB", "ES", "ET", "FI", "FR", "HU", "ID", "IT", "JA", "KO", "LT", "LV", "NB", "NL", "PL", "PT-BR", "PT-PT", "RO", "RU", "SL", "SV", "TR", "UK", "ZH"]


@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.startswith("!sync"):
        print("syncing")
        await bot.tree.sync(guild=discord.Object(id=889711909379641375))
        print("syncing...")
        await bot.tree.sync()
        print("done")
        return

    if message.content.startswith('!trans'):  # keeping this for backwards compat, might be phased out in the future
        req = message.content.split(" ", 2)
        lang = req[1].upper()
        text = req[2]
        await message.channel.send(t.use_translate(lang=lang, key="translation.warning"))
        # i hate the rest of this but it was 1 am when i coded this, it will be refactored later omg
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

# TODO: figure out how to use app_commands.translate and related functions to translate descriptions and add renames for the values


@bot.tree.command(name="translate", description="Translate some text")
@app_commands.describe(message="Message to translate")
@app_commands.describe(target_lang="Language to translate to (default is english)")
@app_commands.rename(target_lang="language")
@app_commands.describe(source_lang="Force DeepL to translate as this language")
@app_commands.rename(source_lang="source-language")
@app_commands.allowed_installs(guilds=True, users=True)
async def Translator(interaction: discord.Interaction, message: str, target_lang: str = None, source_lang: str = None):
    await interaction.response.defer()  # defer in case response takes a while

    if target_lang is None:  # default translate to english
        target_lang = "EN-US"

    target_lang = target_lang.upper()

    if target_lang == "EN":  # deepl needs en-us or en-gb
        target_lang == "EN-US"

    try:
        has_cjk = detect_cjk(message)  # maybe message has cjk?

        if has_cjk and len(message) < 4 and source_lang is None:  # only use on short messages, only if source lang is not forced
            await interaction.followup.send(content=t.use_translate(target_lang, "translation.cjk_ambiguous"))  # notify of cjk behavior
            # convert as if message is C, J, and K
            _cjk = ["zh", "ja", "ko"]

            _response = ""
            for cjk_source in _cjk:
                _response += t.use_translate("en", "translation.source") \
                    + langcodes.get(cjk_source) \
                    .describe(target_lang) \
                    .get("language") \
                    + "\n"

                _translated = translator.translate_text(
                    message,
                    source_lang=cjk_source,
                    target_lang=target_lang
                )

                _response += _translated.text
                _response += "\n"

            await interaction.followup.send(content=_response)
        else:
            if source_lang is not None:  # forcing source lang
                result = translator.translate_text(message, source_lang=source_lang, target_lang=target_lang)
            else:
                result = translator.translate_text(message, target_lang=target_lang)

            source_lang_obj = langcodes.get(result.detected_source_lang)
            source_lang_desc = source_lang_obj.describe(target_lang.lower())
            result_source_lang_name = source_lang_desc.get("language")

            final_response = t.use_translate(target_lang, "translation.source")
            final_response += result_source_lang_name
            final_response += "\n"
            final_response += result.text
            await interaction.followup.send(content=final_response)
    except deepl.exceptions.DeepLException as e:
        await interaction.followup.send(content=e)
    return


@bot.tree.command(name="help", description="Display a help message in your langauage")
@app_commands.describe(help="Which help message to display.")
@app_commands.describe(language="Displays the help message in this language (Default is \"English (United States)\")")
@app_commands.allowed_installs(guilds=True, users=True)
async def Help(interaction: discord.Interaction, help: str = "languages", language: str = "en-us"):
    await interaction.response.defer()
    if help == "languages":
        result = translator.get_target_languages()
        langs = t.use_translate(language, "help.supported") + "\n"
        for lang in result:
            res_lang = langcodes.get(lang.code)
            get = res_lang.describe(language.lower())
            result_lang = get.get("language")
            langs = langs + f"{result_lang} ({lang.code})\n"
        await interaction.followup.send(content=langs)
    else:
        await interaction.followup.send(content=t.use_translate(language, "help.warning"))


def detect_cjk(_text: str):
    """
    Use the langdetect library to possibly detect CJK in a string.
    Meant to fix the ambiguous issue where DeepL detects single
    kanji/hanzi as English.

    langdetect is not error-free either; some characters are
    detected as Korean.

    Parameters:
        _text: The text to detect CJK in.

    Returns:
        A boolean value indicating whether CJK may be detected.
    """
    _cjk = ["ko", "zh-cn", "zh-tw", "ja", "zh"]
    try:
        lang = detect(_text)
        if lang in _cjk:
            return True
        return False
    except LangDetectException:
        return False


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--no-bot",
        help="Don't run the Discord bot; translate in the console",
        action="store_true"
    )

    # Add optional arguments that are required if --no-bot is included
    if "--no-bot" in sys.argv:
        # required lang; 1 argument only
        parser.add_argument(
            "lang",
            nargs=1,
            help="Language to translate to"
        )

        # required message;
        # can return list if typed directly into console, or string if typed in quotes
        # value must be sanitized later
        parser.add_argument(
            "message",
            nargs="+",
            help="Message to translate"
        )

    parser.add_argument(
        "--usage",
        help="Retrieve DeepL character usage quota",
        action="store_true"
    )

    # add json output bc why not
    parser.add_argument(
        "--json",
        help="Return result as JSON",
        action="store_true"
    )

    args = parser.parse_args()

    if args.usage:
        usage = translator.get_usage()
        print(f"Character usage: {usage.character.count} of {usage.character.limit}")
    # continue

    if args.no_bot:
        returnjson = args.json
        lang = args.lang[0]

        # consider that user may have typed a name of a language instead of a code
        # parse to a code by langcodes.find()
        try:
            code = langcodes.find(lang).language  # find language by english name, get code from .language
        except langcodes.LanguageTagError:  # invalid tag
            if not returnjson:
                print("Could not parse language tag.")
            code = "en-us"
        except LookupError:  # language not found
            if not returnjson:
                print(f"Could not find language \"{lang}\".")
            code = "en-us"

        if code == "en":  # dumb fix
            code = "en-us"

        if code.upper() not in val_langs:  # not supported by deepL
            if not returnjson:
                print("Sorry, DeepL doesn't support that language.")
            code = "en-us"

        if not returnjson:
            print("Target: " + code)

        # here is the message sanitization; check if list, join by space if so
        # continues with message if string
        message = args.message
        if isinstance(args.message, list):
            message = " ".join(args.message)
        if not returnjson:
            print("Message: " + message)

        result = translator.translate_text(message, target_lang=code)

        if returnjson:
            resultdict = {
                "input": message,
                "target": code,
                "output": result.text
            }
            print(json.dumps(resultdict, indent=None))
        else:
            print(result)

    else:  # if not no_bot
        bot.run(dcs.bot_token)
