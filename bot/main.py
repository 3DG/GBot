import discord
import time as clock
import os
import math
from time import mktime
from discord.ext import commands as cmds
token = "TOKEN GOES HERE"
bot = cmds.Bot(command_prefix="!")
@bot.command()
async def ping(ctx):
  time = ctx.message.created_at
  timenow = mktime(clock.gmtime())
  msnow = math.floor(clock.time()*1000)/1000 - math.floor(clock.time())
  timenow += msnow
  print((timenow))
  print((time.timestamp()))
  timesend = math.floor(((timenow) - (time.timestamp()))*-1000)
  await ctx.send(':ping_pong: Pong! ('+str(timesend)+' ms)')
  
bot.run(token) 
