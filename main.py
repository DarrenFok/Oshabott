import discord
from discord.ext import commands
from discord import FFmpegPCMAudio
import random
#import asyncio
client = commands.Bot(command_prefix="!", intents=discord.Intents.all()) #command prefix is !

announcement_channel = 1143402754086273026 #set where you want announcements
# music_queue = asyncio.Queue() #queue for music being played
# play_next_song = asyncio.Event()

@client.event
async def on_ready(): #when ready to recieve commands
    print("Oshabott is now online.\n")

@client.command()
async def hello(ctx): #ctx takes inputs from discord
    await ctx.send("Hello!")

@client.event
async def on_member_join(member): #upon user joining server
    channel = client.get_channel(announcement_channel) #id of channel that message is sent
    await channel.send(f"<@!{member.id}> has joined the server!  〵(^ o ^) / ")

@client.event
async def on_member_remove(member): #upon user leaving server
    channel = client.get_channel(announcement_channel)
    await channel.send(f"<@!{member.id}> has left :(")

@client.command()
async def rps(ctx, arg): #play rock, paper, scissors
    argCorrect = arg.upper() #corrects input to be uppercase
    mention = ctx.message.author.mention
    if(argCorrect != "R" and argCorrect != "P" and argCorrect != "S"): #check if input is correct
        await ctx.send("Invalid input! Please input R, P or S!")

    else:
        #make input lowercase
        roll = random.randint(1,3) #1 = R, 2 = P, 3 = S
        #9 possible cases
        if(argCorrect == "R" and roll == 1):
            await ctx.send("Oshabott chose rock. It's a tie! " + mention)
        elif(argCorrect == "R" and roll == 2):
            await ctx.send("Oshabott chose paper. You lose (◕︵◕) " + mention)
        elif(argCorrect == "R" and roll == 3):
            await ctx.send("Oshabott chose scissors. You win (づ｡◕‿‿◕｡)づ " + mention)

        elif(argCorrect == "P" and roll == 1):
            await ctx.send("Oshabott chose rock. You win (づ｡◕‿‿◕｡)づ " + mention)
        elif(argCorrect == "P" and roll ==2):
            await ctx.send("Oshabott chose paper. It's a tie! " + mention)
        elif(argCorrect == "P" and roll ==3):
            await ctx.send("Oshabott chose scissors. You lose (◕︵◕) " + mention)

        elif(argCorrect == "S" and roll == 1):
            await ctx.send("Oshabott chose rock. You lose (◕︵◕) " + mention)
        elif(argCorrect == "S" and roll == 2):
            await ctx.send("Oshabott chose paper. You win (づ｡◕‿‿◕｡)づ " + mention)
        elif(argCorrect == "S" and roll == 3):
            await ctx.send("Oshabott chose scissors. It's a tie! " + mention)

        else:
            print("ERROR: Impossible case") #this never happens

def isConnected(ctx):
    voice_client = discord.utils.get(ctx.bot.voice_clients, guild = ctx.guild)
    return voice_client and voice_client.isConnected()

@client.command(pass_context = True)
async def join(ctx):
    if(ctx.author.voice): #if user running command is in voice channel
        channel = ctx.message.author.voice.channel
        await channel.connect()
    else: #does not allow if user not in voice channel
        await ctx.send(f"Please join a voice channel first " + ctx.message.author.mention + "!")

@client.command(pass_context = True)
async def leave(ctx):
    if(ctx.author.voice):
        await ctx.guild.voice_client.disconnect() #guild = server, go to vc of server to disconnect
        await ctx.send("Oshabott disconnected!")
    else:
        await ctx.send(f"Please join a voice channel first " + ctx.message.author.mention + "!")

@client.command(pass_context = True)
async def play(ctx, arg):
    #check if user calling command is in the channel or not
    if(ctx.author.voice):
        # check if bot is already connected to a channel, if not, then connect it
        if (isConnected(ctx)):
            pass
        else:
            channel = ctx.message.author.voice.channel
            await channel.connect()

        vc = ctx.guild.voice_client
        source = FFmpegPCMAudio(arg)
        player = vc.play(source)
        await ctx.send(f"Now playing: " + arg + " " + ctx.message.author.mention)

    else:
        await ctx.send(f"Please join a voice channel first " + ctx.message.author.mention + "!")

@client.command(pass_context = True)
async def pause(ctx):
    if (ctx.author.voice):
        voice_client = discord.utils.get(ctx.bot.voice_clients, guild=ctx.guild)
        if (voice_client.is_playing()):
            voice_client.pause()
            await ctx.send(f"Song has been paused " + ctx.message.author.mention + "!")
        else:
            await ctx.send(f"There is no song being played at the moment " + ctx.message.author.mention + "!")
    else:
        await ctx.send(f"Please join a voice channel first " + ctx.message.author.mention + "!")

@client.command(pass_context = True)
async def resume(ctx):
    if (ctx.author.voice):
        voice_client = discord.utils.get(ctx.bot.voice_clients, guild=ctx.guild)
        if (voice_client.is_paused()):
            voice_client.resume()
            await ctx.send(f"Song has been resumed " + ctx.message.author.mention + "!")
        else:
            await ctx.send(f"There is no song being paused at the moment " + ctx.message.author.mention + "!")
    else:
        await ctx.send(f"Please join a voice channel first " + ctx.message.author.mention + "!")

@client.command(pass_context = True)
async def stop(ctx):
    if (ctx.author.voice):
        voice_client = discord.utils.get(ctx.bot.voice_clients, guild=ctx.guild)
        if (voice_client.is_playing()):
            voice_client.stop()
            await ctx.send(f"Song has been stopped " + ctx.message.author.mention + "!")
        else:
            await ctx.send(f"There is no song being played at the moment " + ctx.message.author.mention + "!")
    else:
        await ctx.send(f"Please join a voice channel first " + ctx.message.author.mention + "!")

if __name__ == '__main__':
    import config
    client.run(config.token)