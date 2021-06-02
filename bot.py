import os
import discord
import urllib.request
import json
import base64
import re
from discord.ext import commands
import requests
import json

client = commands.Bot(command_prefix='m/ ')

token = "BOT DISCORD TOKEN HERE"
my_guild = os.getenv("DISCORD_GUILD")

intents = discord.Intents.default()

ipserver = "hypixel.net"
url = "https://api.mcsrvstat.us/2/" + ipserver

channelKey = 123123123123 #change to your discord ID channel


@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == my_guild:
            break

    print(
        f"{client.user} is connected to the following guild:\n"
        f"{guild.name}(id: {guild.id})"
    )
    await messageOnOff()


async def messageOnOff():
    data = await checkIfIsOnline()
    channel = client.get_channel(channelKey)
    if data[1]:
        await embedOnline(channel, data[0])
    else:
        await embedOffline(channel, data[0])


async def checkIfIsOnline():
    content = requests.get(url)
    data = json.loads(content.content)
    return [data, data['online']]


@client.event
async def on_message(message):
    if message.content == "hello":
        await message.channel.send("from the other side.")
    await client.process_commands(message)


@client.command()
async def status(ctx):
    await messageOnOff()


async def embedOnline(ctx, data):
    embed = discord.Embed(title=data["hostname"],
                          description=":green_circle: O servidor está ligado",
                          color=discord.Color.green())

    filename = decode_image(data["icon"], (data["hostname"].split("."))[0])
    f = discord.File(filename)

    embed.set_thumbnail(url="attachment://"+data["hostname"]+".png")

    string = (data["motd"]["clean"])[0]
    embed.add_field(name="**MOTD**", value=string, inline=False)
    mods = data["mods"]["names"]
    lengthmods = len(mods)
    stringOfMods = str( lengthmods) + " ("+mods[0]+","+mods[1]+","+mods[2]+","+mods[3]+","+mods[4]+","+mods[5]+",...)"
    embed.add_field(name="**MODS: **", value=stringOfMods, inline=True)
    await ctx.send(file=f, embed=embed)


async def embedOffline(ctx, data):
    embed = discord.Embed(title=data["hostname"],
                          description=":red_circle: O servidor está desligado",
                          color=discord.Color.red())

    await ctx.send(embed=embed)


def decode_image(src, hostname):
    # 1, information extraction
    result = re.search(
        "data:image/(?P<ext>.*?);base64,(?P<data>.*)", src, re.DOTALL)
    if result:
        ext = result.groupdict().get("ext")
        data = result.groupdict().get("data")

    else:
        raise Exception("Do not parse!")

    # # 2, base64 decoding
    img = base64.urlsafe_b64decode(data)

    # 3, the binary file is saved
    filename = hostname+".png"
    with open(filename, "wb") as f:
        f.write(img)

    return filename


client.run(token)
