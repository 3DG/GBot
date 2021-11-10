import discord
from discord.ext import commands as cmds
token = "TOKEN GOES HERE"
bot = cmds.Bot(command_prefix="!")
@Bot.commands()
async def ping(ctx):
  await ctx.send("Pong!")
  
bot.run(token)
