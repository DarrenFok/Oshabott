import discord
import random
import time
import json
import os
import io
import dataclasses

from discord.ext import commands


@dataclasses.dataclass
class User:
    user_id: str
    points: int

    def __init__(self, user_id: str, points: int):
        self.user_id = user_id
        self.points = points


async def write(user, server, points):
    file_location = f"{os.getcwd()}/storage/fishing.json"
    if not os.path.exists(file_location):
        with io.open(file_location, "w+") as outfile:  # if file doesn't exist start off json structure
            dictionary = {
                "{}".format(str(server.id)): {
                    "{}".format(str(user.id)): {
                        "points": points
                    }
                }
            }

            outfile.write(json.dumps(dictionary, indent=4))
        start = time.perf_counter()
        outfile.flush()
        stop = time.perf_counter()
        print(f"JSON file created in {stop - start} seconds")
        os.fsync(outfile.fileno())

    else:
        with io.open(file_location, "r") as infile:
            data = json.load(infile)
        if str(server.id) not in data:  # if server not yet entered
            data[str(server.id)] = {}
            if not str(user.id) in data[str(server.id)]:
                data[str(server.id)][str(user.id)] = {}
                data[str(server.id)][str(user.id)]["points"] = points

        elif not str(user.id) in data[str(server.id)]:  # if server exists, but user does not
            data[str(server.id)][str(user.id)] = {}
            data[str(server.id)][str(user.id)]["points"] = points

        elif str(user.id) in data[str(server.id)]:  # if user exists
            data[str(server.id)][str(user.id)]["points"] += points

        with io.open(file_location, "w") as outfile:
            outfile.write(json.dumps(data, indent=4))


class Fishing(commands.Cog):
    def __init__(self, client):
        self.client = client

    # @commands.command()
    # async def test(self, ctx):
    #     await write(ctx.message.author, ctx.message.guild, 24)

    @commands.command(name='fishboard')
    async def leaderboard(self, ctx):
        file_location = f"{os.getcwd()}/storage/fishing.json"
        size = 10
        if not os.path.exists(file_location):
            await ctx.send("No one has fished yet! Please fish first")
        else:
            user_list = []
            with io.open(file_location, "r") as infile:  # intake all users
                data = json.load(infile)

            for entry in list(data[str(ctx.message.guild.id)]):
                point_data = data[str(ctx.message.guild.id)][entry]["points"]
                instance = User(user_id=entry, points=point_data)
                user_list.append(instance)

            user_list.sort(key=lambda x: x.points, reverse=True)

            em = discord.Embed(
                title="Fishing Points Leaderboard",
                description=f"Top {size} fishing leaders in the server!"
            )

            index = 1
            for element in user_list:
                member = await self.client.fetch_user(int(element.user_id))
                em.add_field(name=f'{index}: {member.display_name}', value=f'{element.points} points', inline=False)

                if index == size:
                    break
                else:
                    index += 1

            await ctx.send(embed=em)

    @commands.command()
    async def fish(self, ctx):
        roll = random.randint(1, 100)
        await ctx.send("Fishing...")
        time.sleep(3)
        if roll in range(1, 41):
            regular_value = 1
            await ctx.send(":fish:")
            await ctx.send(f"You caught a regular fish {ctx.author.mention}! You gained {regular_value} point!")
            await write(ctx.message.author, ctx.message.guild, regular_value)
        elif roll in range(41, 56):
            tropical_value = 4
            await ctx.send(":tropical_fish:")
            await ctx.send(f"You caught a tropical fish {ctx.author.mention}! You gained {tropical_value} points!")
            await write(ctx.message.author, ctx.message.guild, tropical_value)
        elif roll in range(56, 66):
            blowfish_value = -1
            await ctx.send(":blowfish:")
            await ctx.send(f"You caught a blowfish {ctx.author.mention}! You lost {-blowfish_value} point...")
            await write(ctx.message.author, ctx.message.guild, blowfish_value)
        elif roll in range(66, 73):
            jellyfish_value = -5
            await ctx.send(":jellyfish:")
            await ctx.send(f"You caught a jellyfish {ctx.author.mention}! Yikes! You lost {-jellyfish_value} points...")
            await write(ctx.message.author, ctx.message.guild, jellyfish_value)
        elif roll in range(73, 76):
            shark_value = -7
            await ctx.send(":shark:")
            await ctx.send(f"You caught a shark {ctx.author.mention}! Run!! You lost {-shark_value} points...")
            await write(ctx.message.author, ctx.message.guild, shark_value)
        elif roll in range(76, 91):
            shrimp_value = 3
            await ctx.send(":shrimp:")
            await ctx.send(f"You caught a shrimp {ctx.author.mention}! You gained {shrimp_value} points!")
            await write(ctx.message.author, ctx.message.guild, shrimp_value)
        elif roll in range(91, 101):
            await ctx.send(":hiking_boot:")
            await ctx.send(f"You found a boot {ctx.author.mention}...? It's worthless...")


async def setup(client):
    await client.add_cog(Fishing(client))