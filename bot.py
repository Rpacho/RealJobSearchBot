# bot.py
import os
import random
import requests

import discord
from dotenv import load_dotenv
from bs4 import BeautifulSoup

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()

@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')

@client.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, welcome to my Discord server!'
    )

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    msgInput = message.content.split(' ')
    print(msgInput)

    if(msgInput[0] == "!link"):
        parsedData = parseTheLink(msgInput[1])
        if(parsedData == False):
            await message.channel.send('The website link you provided is not available')
        elif(parsedData == 'Error'):
            await message.channel.send('There is an error!')
        else:
            await message.channel.send('Data has been parsed.')

def parseTheLink(link):
    try:
        data = requests.get(link)
        if(data.status_code != 200):
            return False
        html_doc = data.text
        soup = BeautifulSoup(html_doc, 'html.parser')

        # write the data
        f = open(os.getenv("FILE_NAME"), "wt")
        f.write(soup.get_text())
        f.close()
        return True
    except:
        return 'Error'


client.run(TOKEN)