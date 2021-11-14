#GBot by 3DG
#You may use this code for any purpose, but make sure to credit me if you're using most of it.
import discord
import requests as req
import time as clock
import os
import math
import random
import requests
import textwrap
from io import BytesIO as toimg
from PIL import Image, ImageFont, ImageDraw
from time import mktime
from discord.ext import commands as cmds
token = ""
prefix = "g!"
bot = cmds.Bot(command_prefix=prefix,help_command=None)
versionnum = 0.5
revision = 0
def randomStr(length, letters="0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"):
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
    if url.endswith(".png") or url.endswith(".jpg") or url.endswith(".gif"):
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
      await ctx.send("Your image must be a PNG, JPG, or GIF image.")
  else:
    await ctx.send("This command requires an image!")

@bot.command()
async def version(ctx):
  await ctx.send("GBot is on version "+str(versionnum)+"abcdefghijklmnopqrstuvwxyz"[revision])
#caption img command
@bot.command()
async def caption(ctx, caption):
  if ctx.message.attachments != []:
    url = ctx.message.attachments[0].url
    if url.endswith(".png") or url.endswith(".jpg") or url.endswith(".gif"):
      message = await ctx.send("Your image is being processed, this may take a few seconds...")
      imgdata = requests.get(url)
      fileName = randomStr(24)
      img = Image.open(toimg(imgdata.content))
      img = img.convert("RGBA")
      wid, hgt = img.size
      usefont = ImageFont.truetype("Roboto-Black.ttf", round((hgt/wid)/3*(wid/10)*3))
      stringtoputinimg = textwrap.wrap(caption, width=round(wid/((hgt/wid)/3*(wid/20)*3)))
      caption = ''''''
      for txt in range(len(stringtoputinimg)):
        caption += stringtoputinimg[txt]
        if txt != len(stringtoputinimg)-1:
          caption += '''\n'''
      print(stringtoputinimg)
      imgdraw = ImageDraw.Draw(img)
      texwid, texhgt = imgdraw.textsize(caption, font=usefont)
      captcanv = Image.new(img.mode, (wid, hgt+texhgt+6), (255, 255, 255))
      captcanv.paste(img, (0, texhgt+6))
      capt = ImageDraw.Draw(captcanv)
      capt.text(((wid/2), 0),str(caption),(0,0,0),font=usefont, align='center', anchor="ma")
      captcanv.save("./temp/img/"+fileName+"caption.png")
      file = open("./temp/img/"+fileName+"caption.png", "rb", buffering = 0)
      await message.edit(content="Sending image...")
      await ctx.send("Here is your image!", file=discord.File(file, filename="convertedimage.jpg"))
      await message.delete()
      file.close()
      os.remove("./temp/img/"+fileName+"caption.png")
    else:
      await ctx.send("Your image must be a PNG, JPG, or GIF image.")
  else:
    await ctx.send("This command requires an image!")

#pixel image command
@bot.command()
async def pixel(ctx, scalewid=24.0, scalehgt=None):
  if ctx.message.attachments != []:
    if scalehgt == None:
      scalehgt = scalewid
    if scalewid < 1.0 or scalehgt < 1.0:
      await ctx.send("Scale factor must be more than 1")
    else:
      url = ctx.message.attachments[0].url
      if url.endswith(".png") or url.endswith(".jpg") or url.endswith(".gif"):
        imgdata = requests.get(url)
        img = Image.open(toimg(imgdata.content))
        fileName = randomStr(24)
        img = img.convert("RGBA")
        wid, hgt = img.size
        img = img.resize((round(wid/scalewid)+1,round(hgt/scalehgt)+1),resample=Image.BILINEAR)
        img = img.resize((wid,hgt), resample=Image.NEAREST)
        img.save("./temp/img/"+fileName+"pixel.png")
        file = open("./temp/img/"+fileName+"pixel.png", "rb", buffering = 0)
        await ctx.send("Here is your image!", file=discord.File(file, filename="convertedimage.png"))
        file.close()
        os.remove("./temp/img/"+fileName+"pixel.png")
      else:
        await ctx.send("Your image must be a PNG, JPG, or GIF image.")
  else:
    await ctx.send("This command requires an image!")
#help command
helpdef = {"pixel":"Requires an image. Lowers the resolution of an image and scales it back up (Arguments: [Scale X factor, Scale Y factor])",
           "echo":"Make the bot say anything! (Arguments: {Message})",
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

#echo command
@bot.command()
async def echo(ctx):
  await ctx.send(str(ctx.message.content)[(4 + len(prefix)) : len(str(ctx.message.content))])
  await ctx.message.delete()

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
  filterchannelid = # paste your channel id here
  if ctx.channel.id == filterchannelid and ctx.author.bot == False:
    url = "" #put your filter webhook url here
    avatar = "https://cdn.discordapp.com/avatars/"+str(ctx.author.id)+"/"+str(ctx.author.avatar)+".webp?size=256"
    data = {"username":ctx.author.name,"avatar_url":avatar,"content":filter(ctx.content),"embeds":None}
    response = req.post(url, data=data)
    if str(response) == "<Response [204]>":
      await ctx.delete()
  await bot.process_commands(ctx)
bot.run(token) 
