import discord
import requests as req
import time as clock
import os
import math
import random
import requests
from io import BytesIO as toimg
from PIL import Image
from time import mktime
from discord.ext import commands as cmds
token = ""
bot = cmds.Bot(command_prefix="g!",help_command=None)

def randomStr(length, letters="0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvexyz"):
  retstr = ""
  for i in range(length):
    retstr += letters[random.randint(0, len(letters)-1)]
  return retstr
#ping command
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


#jpeg image command
@bot.command()
async def jpegify(ctx, quality=5):
  if ctx.message.attachments != []:
    url = ctx.message.attachments[0].url
    imgdata = requests.get(url)
    img = Image.open(toimg(imgdata.content))
    fileName = randomStr(24)
    img = img.convert("RGB")
    img.save("./temp/img/"+fileName+"jpgified.jpg", mode="JPEG", quality=quality)
    file = open("./temp/img/"+fileName+"jpgified.jpg", "rb", buffering = 0)
    await ctx.send("Here is your image!", file=discord.File(file, filename="convertedimage.jpg"))
    file.close()
    os.remove("./temp/img/"+fileName+"jpgified.jpg")
  else:
    await ctx.send("This command requires an image!")

#jpeg image command
@bot.command()
async def pixel(ctx, scalewid=32, scalehgt=None):
  if ctx.message.attachments != []:
    if scalehgt == None:
      scalehgt = scalewid
    if scalewid < 1 or scalehgt < 1:
      await ctx.send("Scale factor must be more than 1")
    else:
      url = ctx.message.attachments[0].url
      imgdata = requests.get(url)
      img = Image.open(toimg(imgdata.content))
      fileName = randomStr(24)
      img = img.convert("RGBA")
      wid, hgt = img.size
      img = img.resize((math.floor(wid/scalewid)+1,math.floor(hgt/scalehgt)+1),resample=Image.BILINEAR)
      img = img.resize((wid,hgt), resample=Image.BILINEAR)
      img.save("./temp/img/"+fileName+"pixel.png")
      file = open("./temp/img/"+fileName+"pixel.png", "rb", buffering = 0)
      await ctx.send("Here is your image!", file=discord.File(file, filename="convertedimage.png"))
      file.close()
      os.remove("./temp/img/"+fileName+"pixel.png")
  else:
    await ctx.send("This command requires an image!")
    
#echo command
@bot.command()
async def echo(ctx):
  await ctx.send(str(ctx.message.content)[(4 + len(prefix)) : len(str(ctx.message.content))])
  await ctx.message.delete()

#help command
helpdef = {"pixel":"Requires an image. Lowers the resolution of an image and scales it back up (Arguments: [Scale X factor, Scale Y factor])",
           "jpegify":"Requires an image. Returns a low quality jpg of the image sent (Arguments: [Quality])",
           "help":"Shows a list of commands",
           "ping":"Gets your ping to the bot"}
@bot.command()
async def help(ctx, cmdorpage=0):
  send = ""
  cmds = len(bot.commands)
  for cmd in bot.commands:
    send += "`g!"+str(cmd)+"`" + " - " + helpdef.get(str(cmd))+'''\n'''
  await ctx.send(send)


#filter-chat in 3dg's discord
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
  filterchannelid = 907790324997443634 # paste your channel id here
  if ctx.channel.id == filterchannelid and ctx.author.bot == False:
    url = "" #put your filter webhook url here
    avatar = "https://cdn.discordapp.com/avatars/"+str(ctx.author.id)+"/"+str(ctx.author.avatar)+".webp?size=256"
    data = {"username":ctx.author.name,"avatar_url":avatar,"content":filter(ctx.content),"embeds":None}
    response = req.post(url, data=data)
    if str(response) == "<Response [204]>":
      await ctx.delete()
  await bot.process_commands(ctx)
bot.run(token) 
