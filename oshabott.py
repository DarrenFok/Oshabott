import os
import discord
import asyncio

from dotenv import load_dotenv
from discord.ext import commands

intents = discord.Intents.all()
client = commands.Bot(command_prefix='!', intents=intents)

load_dotenv('token.env')
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')


@client.event
async def on_ready():
    print("Oshabott is now online!")


async def main():
    async with client:
        await client.load_extension('cogs.chat_commands')
        await client.load_extension('cogs.fishing')
        await client.start(DISCORD_TOKEN)

asyncio.run(main())
