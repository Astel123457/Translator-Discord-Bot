# Translator-Discord-Bot

Discord bot powered by Discord.py and DeepL.

## Requirements

- Python 3.8 or higher
- A DeepL API key (free or paid)

## Setup

1. Clone the repository.

```
git clone https://github.com/Astel123457/Translator-Discord-Bot
```

2. Install the required packages with pip.

```
python -m pip install -r requirements.txt
```

3. Replace the placeholder text in `dc_secrets_example.py` with your Discord bot token and DeepL API key. Rename the file to `dc_secrets.py`.  
**Do not share these keys or this file with anyone!**

```python
deepl_auth = "Put your DeepL API key here"
bot_token = "Put your Discord bot token here"
```

## Usage

### **/translate \<message> [language code]**

Translates a message. By default, the message will be translated to English. A language name or language code can be specified to choose a target language.

### Example

```
/translate message:初めまして。

Source language: Japanese
Nice to meet you.
```

```
/translate message:Es ist jetzt 6 Uhr. language:ES

Source language: German
Ahora son las 6 en punto.
```

### **/help [languages]**

Displays a help message for various topics. If a language code is specified, the help message will be displayed in that language.

### Example

```cls
/help help:languages language:EN

Here is a list of languages that I currently support:
Bulgarian (BG)
Czech (CS)
Danish (DA)
German (DE)
...
```

## Running the bot

The script is meant to be used primarily as a Discord bot. To start the bot, make sure you have properly set up the `dc_secrets.py` file, then run the following command:

```cls
python main.py
```

The script can also translate text in the console. To do so, run the following command:

```cls
python main.py --no-bot <language code> <message>
```

A target language code must be specified.

### Example

```cls
python main.py --no-bot DE "Hello, world!"
Lang: DE
Message: Hello, world!
Hallo Welt!
```
