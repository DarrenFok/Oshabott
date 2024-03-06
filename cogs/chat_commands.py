import discord
import random

from discord.ext import commands


class ChatCommands(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def ping(self, ctx):
        await ctx.send('pong')

    @commands.command(pass_context=True)
    async def clear(self, ctx, limit=120):
        await ctx.channel.purge(limit=limit)
        await ctx.send(f'Channel cleared by {ctx.author.mention}')
        await ctx.message.delete

    @commands.command()
    async def roll(self, ctx, sides=6):
        roll = random.randint(1, sides)
        await ctx.send(f'Rolled a {roll} on a {sides} sided die! {ctx.author.mention}')

    @commands.command(name='rps')
    async def rock_paper_scissors(self, ctx, input):
        choice = input.lower()
        roll = random.randint(1,3)  # 1 = rock, 2 = paper, 3 = scissors

        if choice in ('r', 'rock'):
            if roll == 1:
                await ctx.send(f'Oshabott chose rock! You tied! {ctx.author.mention}')
            elif roll == 2:
                await ctx.send(f'Oshabott chose paper! You lost! {ctx.author.mention}')
            elif roll == 3:
                await ctx.send(f'Oshabott chose scissors! You won! {ctx.author.mention}')

        elif choice in ('p', 'paper'):
            if roll == 1:
                await ctx.send(f'Oshabott chose rock! You won! {ctx.author.mention}')
            elif roll == 2:
                await ctx.send(f'Oshabott chose paper! You tied! {ctx.author.mention}')
            elif roll == 3:
                await ctx.send(f'Oshabott chose scissors! You lost! {ctx.author.mention}')

        elif choice in ('s', 'scissors'):
            if roll == 1:
                await ctx.send(f'Oshabott chose rock! You lost! {ctx.author.mention}')
            elif roll == 2:
                await ctx.send(f'Oshabott chose paper! You won! {ctx.author.mention}')
            elif roll == 3:
                await ctx.send(f'Oshabott chose scissors! You tied! {ctx.author.mention}')

        else:
            await ctx.send(f'Invalid input! Please try again! {ctx.author.mention}')


async def setup(client):
    await client.add_cog(ChatCommands(client))
