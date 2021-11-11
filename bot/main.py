import discord
import requests as req
import time as clock
import os
import math
from time import mktime
from discord.ext import commands as cmds
token = "" #put token here
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
def filter(message):
  letters='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()-=_+[]{};\':",./<>?`~\\|'
  retstr = ""
  for b in range(len(message)):
    if message[b] in letters:
      retstr += '#'
    else:
      retstr += message[b]
  return retstr
  
@bot.event
async def on_message(ctx):
  filterchannelid = 0 # paste your channel id here
  if ctx.channel.id == filterchannelid and ctx.author.bot == False:
    url = "" #put your filter webhook url here
    avatar = "https://cdn.discordapp.com/avatars/"+str(ctx.author.id)+"/"+str(ctx.author.avatar)+".webp?size=256"
    data = {"username":ctx.author.name,"avatar_url":avatar,"content":filter(ctx.content),"embeds":None}
    response = req.post(url, data=data)
    if str(response) == "<Response [204]>":
      await ctx.delete()
bot.run(token) 
