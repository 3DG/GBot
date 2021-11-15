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
token = "" # discord token
prefix = "g!" # bot prefix
appid = 907439983579758632 # app id
activity = discord.Activity(type=discord.ActivityType.watching, name="you (Prefix: "+prefix+")")
bot = cmds.Bot(command_prefix=prefix,activity=activity,help_command=None) # make a bot with no help command with prefix as the prefix for all commands
versionnum = 0.5 # version number
revision = 3 # revision number
def randomStr(length, letters="0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"):
  retstr = "" # make a blank string to return later
  for i in range(length): #repeat length times
    retstr += letters[random.randint(0, len(letters)-1)] #add a random letter from 0 to the amount of letters -1 to the return string
  return retstr #return the return string
#ping command
@bot.command() # this is a command
async def ping(ctx): #ctx = context for message
  time = ctx.message.created_at # get time message was made
  timenow = mktime(clock.gmtime()) #get GMT time now
  msnow = math.floor(clock.time()*1000)/1000 - math.floor(clock.time()) #get milliseconds in current timezone (milliseconds arent affected by timezones)
  timenow += msnow # add milliseconds to time
  timesend = math.floor(((timenow) - (time.timestamp()))*-1000) # the amount of miliseconds to send with the message (the current time - the time the message was sent)
  await ctx.send(':ping_pong: Pong! ('+str(timesend)+' ms)') # await send function


#jpeg image command
@bot.command()
async def jpegify(ctx, quality):
  if quality == None: # if quality isnt set
    quality = 5 # set it to 5
  try: # see if the quality variable is an integer
    quality = int(quality)
  except: #if it isnt
    await ctx.send("Quality must be an integer!")
  finally: #if it is
    quality = int(quality) # convert the quality (idk if this is needed)
    if ctx.message.attachments != []: # if an attachment is attached
      url = ctx.message.attachments[0].url # only get the first one
      if url.endswith(".png") or url.endswith(".jpg") or url.endswith(".gif"): #if it is a png, jpg or gif
        imgdata = requests.get(url) # get the image data
        img = Image.open(toimg(imgdata.content)) # make a new PIL image
        fileName = randomStr(24) # make a random string 24 characters long
        img = img.convert("RGB") # convert the image to RGB
        img.save("./temp/img/"+fileName+"jpgified.jpg", mode="JPEG", quality=quality) # save it to a temporary folder to be deleted later as a JPG with quality set to the quality variable
        file = open("./temp/img/"+fileName+"jpgified.jpg", "rb", buffering = 0) # open the image that was just saved
        await ctx.send("Here is your image!", file=discord.File(file, filename="convertedimage.jpg")) # send the image
        file.close() # stop using the image to prevent memory leak
        os.remove("./temp/img/"+fileName+"jpgified.jpg") # delete it
      else: #if not
        await ctx.send("Your image must be a PNG, JPG, or GIF image.") # notify the user
    else: # if no attachment is attached
      await ctx.send("This command requires an image!") # notify the user

#fairly simple command
@bot.command()
async def version(ctx):
  await ctx.send("GBot is on version "+str(versionnum)+"abcdefghijklmnopqrstuvwxyz"[revision])
#caption img command
@bot.command()
async def caption(ctx, caption):
  if ctx.message.attachments != []: #if an attachment is attached
    url = ctx.message.attachments[0].url #only get the first one blah blah blah you know the drill
    if url.endswith(".png") or url.endswith(".jpg") or url.endswith(".gif"):
      message = await ctx.send("Your image is being processed, this may take a few seconds...") #it takes a while to add a caption to an image, notify the user
      imgdata = requests.get(url) # get the image
      fileName = randomStr(24) #zzzzzzzzzzzz
      img = Image.open(toimg(imgdata.content))
      img = img.convert("RGBA")
      wid, hgt = img.size # get the image width and height
      usefont = ImageFont.truetype("captfont.ttf", round((hgt/wid)/3*(wid/10)*3)) # get funny font
      stringtoputinimg = textwrap.wrap(caption, width=round(wid/((hgt/wid)/3*(wid/17)*3))) # caption breaks for each line it takes up
      caption = '''''' # replace caption with a string that supports line breaks for our caption
      for txt in range(len(stringtoputinimg)): # for each entry in the broken up caption
        caption += stringtoputinimg[txt] # add it to the caption
        if txt != len(stringtoputinimg)-1: #if it is not the last entry
          caption += '''\n''' # add a line break
      imgdraw = ImageDraw.Draw(img) # make a new image that can be pasted
      texwid, texhgt = imgdraw.textsize(caption, font=usefont) # get how much space text will take up
      captcanv = Image.new(img.mode, (wid, hgt+texhgt+6), (255, 255, 255)) # make a new canvas with the image height + the text height + a margin
      captcanv.paste(img, (0, texhgt+6)) # paste the image sent into the canvas
      capt = ImageDraw.Draw(captcanv) # make a new image that text can be drawn on
      capt.text(((wid/2), 0),str(caption),(0,0,0),font=usefont, align='center', anchor="ma") # draw the caption on the canvas image with central alignment
      captcanv.save("./temp/img/"+fileName+"caption.png") # save it to the temporary file blah blah blah
      file = open("./temp/img/"+fileName+"caption.png", "rb", buffering = 0)
      await message.edit(content="Sending image...") #edit the message to notify the user that the image is sending and not just my pc being bad
      await ctx.send("Here is your image!", file=discord.File(file, filename="convertedimage.jpg")) # send the image
      await message.delete() # delete the edited message
      file.close() # stop using the caption file to prevent memory leak
      os.remove("./temp/img/"+fileName+"caption.png") # delete the caption file
    else:
      await ctx.send("Your image must be a PNG, JPG, or GIF image.")
  else:
    await ctx.send("This command requires an image!")

#pixel image command
@bot.command()
async def pixel(ctx, scalewid=None, scalehgt=None, scalemode=None):
  if scalemode == None: # if scale mode isnt set
    scalemode = 0 #set to nearest
  try: #see if scalemode is an integer
    scalemode = int(scalemode)
  except: #if it isnt
    scalemode = 0 #set it to nearest
  if scalewid == None: # if scalewid isnt set
    scalewid = 24.0 # set it to 24
  try: # see if scalewid is a number
    scalewid = float(scalewid)
  except: # if it isnt
    await ctx.send("Scale factors must be a number") # notify user
  finally: #if it is
    scalewid = float(scalewid) #convert number
    if scalehgt == None: # same stuff that scalewid just went through
        scalehgt = scalewid
    try:
      scalehgt = float(scalehgt)
    except:
      await ctx.send("Scale factors must be a number")
    finally:
      if ctx.message.attachments != []: # if  images are attached or smth idfk anymore
        if int(scalewid) < 1.0 or int(scalehgt) < 1.0: # if scale width or height are less than one
          await ctx.send("Scale factor must be more than 1") #notify user
        else: # if they are proper
          url = ctx.message.attachments[0].url # blah blah blah im tired of making these comemnts i shouldve made them as i went instead of adding them after
          if url.endswith(".png") or url.endswith(".jpg") or url.endswith(".gif"):
            imgdata = requests.get(url)
            img = Image.open(toimg(imgdata.content))
            fileName = randomStr(24)
            img = img.convert("RGBA")
            wid, hgt = img.size # get image size
            img = img.resize((round(wid/scalewid)+1,round(hgt/scalehgt)+1),resample=Image.BILINEAR) #resize image with bilinear
            if scalemode == 0: # nearest neighbor scaling
              img = img.resize((wid,hgt), resample=Image.NEAREST)
            else: # bilinear scaling
              img = img.resize((wid,hgt), resample=Image.BILINEAR)
            img.save("./temp/img/"+fileName+"pixel.png") # save to use
            file = open("./temp/img/"+fileName+"pixel.png", "rb", buffering = 0) #open file
            await ctx.send("Here is your image!", file=discord.File(file, filename="convertedimage.png")) #vague comment #274
            file.close() # close file to prevent memory leak
            os.remove("./temp/img/"+fileName+"pixel.png") # remove file
          else:
            await ctx.send("Your image must be a PNG, JPG, or GIF image.")
      else:
        await ctx.send("This command requires an image!")

#finally thank god i dont have to repeat the same comments over and over
        
#help command
helpdef = {"pixel":"Requires an image. Lowers the resolution of an image and scales it back up (Arguments: [Scale X factor, Scale Y factor, Scaling algorithm (0 - Nearest, 1 - Bilinear)])",
  "echo":"Make the bot say anything! (Arguments: {Message})",
  "caption":"Requires an image. Adds a caption to any image (Arguments: {Caption})",
  "version":"Sends the version number",
  "jpegify":"Requires an image. Returns a low quality jpg of the image sent (Arguments: [Quality])",
  "help":"Shows a list of commands",
  "ping":"Gets your ping to the bot"
} # dictionary containing all of the descriptions for the commands
@bot.command()
async def help(ctx, cmdorpage=None):
  send = ""
  embed = discord.Embed(title="Commands", color=discord.Color(1977406)) # make a new embed with title "Commands" with color #1e2c3e
  #cmds = len(bot.commands)
  for cmd in bot.commands: # for each command
    send += "`g!"+str(cmd)+"`" + " - " + str(helpdef.get(str(cmd)))+'''\n''' # add it in send string
  embed.add_field(name="All commands", value=send) # add the send string to the embed
  #buttonprevpage = discord.ui.Button(label="prev page", custom_id="prev")
  
  #buttonprevpage.coroutine = discord.Interaction(id=random.randint(0, 1000000000), type=discord.InteractionType("component"), application_id=appid)
  await ctx.send(embed = embed) # send commands

#echo command
@bot.command()
async def echo(ctx): # echo command ok this should be simple
  await ctx.send("``"+str(ctx.message.content)[(5 + len(prefix)) : len(str(ctx.message.content))].replace("`", "'")+"``") # slice the first 5 + prefix length characters off the message and send it
  await ctx.message.delete() # delete the message

#filter-chat in 3dg's discord
def filter(message): #filter
  retstr = "" #return string
  for b in range(len(message)): # for message length
    if message[b] != " ": # if letter is not a space
      retstr += '#' # replace it with a hashtag and add it to string
    else: # if not
      retstr += message[b] # add it to string
  return retstr #return the string
@bot.event
async def on_message(ctx):
  filterchannelid = 907790324997443634 # paste your channel id here
  if ctx.channel.id == filterchannelid and ctx.author.bot == False: # if message is in filter channel and author isnt a bot (to prevent webhook spam)
    url = "" #put your filter webhook url here
    avatar = "https://cdn.discordapp.com/avatars/"+str(ctx.author.id)+"/"+str(ctx.author.avatar)+".webp?size=256" # get user avatar url in 256p
    data = {"username":ctx.author.name,"avatar_url":avatar,"content":filter(ctx.content),"embeds":None} # data to send to the webhook
    response = req.post(url, data=data) # send it to the webhook
    await ctx.delete() # delete the message
  await bot.process_commands(ctx) # process commands again so bot doesnt break
bot.run(token)#run the bot
