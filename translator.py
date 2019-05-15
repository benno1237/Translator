import discord
from discord.ext import commands
from dataIO import js
import aiohttp
from googletrans import Translator

translator = Translator()
client = commands.Bot(command_prefix = '!')
codes = js.load("Configs/language-unicode.json")

with open("Configs/Token.txt", "r") as file:
    Token = file.read()

if Token == "":
    print("You don´t have a bottoken set yet!")
    Token = input("Enter your token here: ")

    with open("Configs/Token.txt", "w") as file:
        file.write(Token)

@client.event
async def on_ready():
    print("Translater Ready!")

@client.command(pass_context=True)
async def translate(ctx, lang_to, *, message):
    '''detect the language'''
    language_code = translator.detect(message)
    lang_from = language_code.lang

    '''translate the message'''
    trans = translator.translate(message, lang_to, lang_from)
    text = trans.text

    '''create an embed for the look'''
    embed = discord.Embed(
    color = discord.Color.blue(),
    description = "Arcis Translater")
    embed.add_field(name="Original", value=message, inline=False)
    embed.add_field(name="Translated", value=text, inline=False)
    await client.say(embed=embed)

async def on_reaction_add(reaction, user):
    '''defining shit'''
    message_object = reaction.message
    channel = message_object.channel
    message = message_object.content
    author = message_object.author
    emoji = reaction.emoji
    encoded_emoji = emoji.encode("utf-8", errors="ignore") #makes it readable for python
        
    '''detect the language'''
    language_code = translator.detect(message)
    lang_from = language_code.lang

    '''check if the emoji is valid for a language'''
    status = False
    for key in codes:
        if str(encoded_emoji) == str(key):
            status = True
            
    if status == False:
        await client.send_message(channel, "This reaction is not valid!")

    '''translate the message'''
    if status == True:
        lang_to = codes[str(encoded_emoji)]["lang_code"]
        trans = translator.translate(message, lang_to, lang_from)
        text = trans.text

        '''create an embed for the look'''
        embed = discord.Embed(
            color = discord.Color.blue(),
            description = "Translater")
        embed.add_field(name="Original", value=message, inline=False)
        embed.add_field(name="Translated", value=text, inline=False)

        await client.send_message(channel, embed=embed)

client.run(Token)
