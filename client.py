# -*- coding: utf-8 -*-
"""
Created on Tue Jun  1 14:51:06 2021

@author: Yucheng
"""

import discord
from discord.ext import commands, tasks
import datetime
import asyncio
import numpy as np
from MKLeaderboards import MKLeaderboard
import os

token = "ODQ5Mjc1Mzg0Mjc2MTg5MjA0.YLYzVg.X6-nIudRM4ku8RJYNycoeY07wWM"

client = commands.Bot(command_prefix = '!')

target_channel_id = 849278207966445628

categories = ["NO-SC", "UNRESTRICTED"]
track_names = np.load("track_names.npy")
track_names_alt = ["GRUMBLE VOLCANO", "N64 DK'S JUNGLE PARKWAY"]

@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online, activity=discord.Game('Mario Kart Wii'))
    print('Bot is ready.')

# @client.event
# async def on_message(message):
#     msg = str(message.content).split(" ")
#     print(msg)
#     if msg[0] == "hello":
#         await message.channel.send("hejsa :)")
#     await client.process_commands(message)

@client.command(name="wr",
                brief="Show WR time for a track",
                help="""
                !wr {category} {track name} 
                
                Example: !wr alt-sc grumble volcano
                """)
async def wr(ctx, *args):
    if len(args) > 0:
        msg = [arg for arg in args]

        category = msg[0].upper()
        track = " ".join(msg[1:]).upper()
        if category == "ALT-SC":
            if track not in track_names_alt:
                await ctx.channel.send("Sorry, that track doesn't exist!")
            else:
                wii = MKLeaderboard(category=category, track=track)
                await ctx.channel.send("```"+wii.wr()+"```")
        else:
            if category not in categories:
                await ctx.channel.send("Sorry, that category doesn't exist!")
            if track not in track_names:
                await ctx.channel.send("Sorry, that track doesn't exist!")
            elif category in categories and track in track_names:
                wii = MKLeaderboard(category=category, track=track)
                await ctx.channel.send("```"+wii.wr()+"```")

@client.command(name="playertop",
                brief="Shows number of WW tops by country",
                help="""
                !playertop {category} (default is unrestricted)
                
                Example: !playertop no-sc
                """)
async def playertop(ctx, cat="unrestricted"):
    category = cat.upper()
    if category == "ALT-SC" or category in categories:
        wii = MKLeaderboard(category=category, track="luigi circuit")
        wii.player_leaderboards()
        await ctx.channel.send(file=discord.File("playertop.png"))
        os.remove("playertop.png")
    else:
        await ctx.channel.send("Sorry, that category doesn't exist!")

@client.command(name="countrytop",
                brief="Shows number of WW tops by country",
                help="""
                !countrytop {category} (default is "unrestricted")
                
                Example: !countrytop alt-sc
                """)
async def countrytop(ctx, cat="unrestricted"):
    category = cat.upper()
    if category == "ALT-SC" or category in categories:
        wii = MKLeaderboard(category=category, track="luigi circuit")
        wii.country_leaderboards()
        await ctx.channel.send(file=discord.File("countrytop.png"))
        os.remove("countrytop.png")
    else:
        await ctx.channel.send("Sorry, that category doesn't exist!")

@client.command(name="tracks",
                help="List of tracks")
async def tracks(ctx):
    track_list = "\n".join(track_names)
    await ctx.channel.send("```" + track_list + "```")

@client.command(name="categories",
                help="List of categories")
async def ctgs(ctx):
    ctg = categories + ["ALT-SC"]
    category_list = " \n".join(ctg)
    await ctx.channel.send("```" + category_list + "```")

client.run(token)
