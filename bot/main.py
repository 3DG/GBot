#GBot by 3DG
#You may use this code for any purpose, but make sure to credit me if you're using most of it.
import sqlite3
import discord
import requests as req
import time as clock
import os
import math
import random
import requests
import textwrap
import json
from statistics import mean
from io import BytesIO as toimg
from PIL import Image, ImageFont, ImageDraw, ImageOps, ImageSequence
from time import mktime
from discord.ext import commands
con = sqlite3.connect("gBotData.db")
cur = con.cursor()
file = open("./keys.json", "rb", buffering = 0)
jsonstr = str(file.readlines()[0])
jsonstr = json.loads(jsonstr[2:len(jsonstr)-1])
token = jsonstr["token"] # discord token
#cur.execute("CREATE TABLE settings (servid varchar(48), prefix varchar(20))")
#cur.execute("CREATE TABLE users (id varchar(48), server varchar(48))")
con.commit()
async def bprefix(bot, msg):
  server = msg.guild
  if server:
    cur.execute("SELECT * FROM settings WHERE `servid` = '"+str(server.id)+"'")
    try:
      return cur.fetchall()[0][1]
    except:
      return "g!"
  else:
    return "g!"
appid = 907439983579758632 # app id
activity = discord.Activity(type=discord.ActivityType.watching, name="you")
bot = commands.Bot(command_prefix=bprefix,activity=activity,help_command=None) # make a bot with no help command with prefix as the prefix for all commands
versionnum = 0.9 # version number
revision = 2 # revision number
def hex_format(color):
  try:
    return (int(color[0:2], 16),int(color[2:4], 16),int(color[4:6], 16), int(color[6:8], 16) if (len(color) > 7) else 255)
  except:
    return "error"
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

def get_avg_fps(PIL_Image_object):
    """ Returns the average framerate of a PIL Image object """
    PIL_Image_object.seek(0)
    frames = []
    while True:
        try:
            frames.append(PIL_Image_object.info['duration'])
            PIL_Image_object.seek(PIL_Image_object.tell() + 1)
        except EOFError:
            return frames
    return None
# stolen stackoverflow code but modified :scream:

#AFK COMMAND!!! first commandu tilizing a database!
@bot.command()
async def afk(ctx):
  cur.execute("SELECT `id` FROM `users` WHERE id = "+str(ctx.author.id)+" AND server = "+str(ctx.guild.id))
  if len(cur.fetchall()) == 0:
    cur.execute("INSERT INTO `users`(`servid`, `server`) VALUES (" + str(ctx.author.id) + ", "+ str(ctx.guild.id) +")")
    con.commit()
    await ctx.send(ctx.author.name + " is now AFK!")
    try:
      await ctx.author.edit(nick=ctx.author.name + " [AFK]")
    except:
      print("No permission")
  else:
    cur.execute("DELETE FROM `users` WHERE id="+str(ctx.author.id)+" AND server = "+ str(ctx.guild.id))
    con.commit()
    await ctx.send(ctx.author.name + " is no longer AFK!")
    try:
      if len(ctx.author.name.split(" [AFK]")) == 1:
        await ctx.author.edit(nick=ctx.author.name.split(" [AFK]")[0])
    except:
      print("No permission")

def escapestr(string):
  return string.replace("\\", "\\\\").replace('"', '\"').replace("'", "\'").replace("`", "\`")
#change prefix
@bot.command()
async def prefix(ctx, prefix):
  cur.execute("SELECT * FROM settings WHERE servid = '"+str(ctx.guild.id)+"'")
  if len(prefix) >= 1 and len(prefix) <= 20:
    if len(cur.fetchall()) == 0:
      cur.execute("INSERT INTO `settings`(`servid`, `prefix`) VALUES ('"+str(ctx.guild.id)+"', '"+escapestr(prefix)+"')")
      con.commit()
    else:
      cur.execute("UPDATE settings SET `servid`='"+str(ctx.guild.id)+"', `prefix`='"+escapestr(prefix)+"' WHERE servid = '"+str(ctx.guild.id)+"'")
      con.commit()
    await ctx.send("Prefix has changed to: "+prefix)
  else:
    await ctx.send("Your prefix must be in between 1 and 20 characters!")
#overlay command
@bot.command()
async def overlay(ctx, mode=0):
  if len(ctx.message.attachments) == 2: # if 2 images are attached
    url = ctx.message.attachments[0].url # blah blah blah im tired of making these comemnts i shouldve made them as i went instead of adding them after
    urltwo = ctx.message.attachments[1].url # blah blah blah im tired of making these comemnts i shouldve made them as i went instead of adding them after
    if (url.lower().endswith(".png") or url.lower().endswith(".jpg") or urltwo.lower().endswith(".png") or urltwo.lower().endswith(".jpg")) and not (url.lower().endswith(".gif") or urltwo.lower().endswith(".gif")):
      imgdata = requests.get(url)
      img = Image.open(toimg(imgdata.content))
      imgdatatwo = requests.get(urltwo)
      imgtwo = Image.open(toimg(imgdatatwo.content))
      fileName = randomStr(24)
      img = img.convert("RGBA")
      imgtwo = imgtwo.convert("RGBA")
      wid, hgt = img.size
      imgtwo = imgtwo.resize((wid, hgt), resample=Image.BILINEAR) #resize image with bilinear
      
      for y in range(hgt):
        for x in range(wid):
          pixel = imgtwo.getpixel((x,y))
          imgtwo.putpixel((x, y), (pixel[0], pixel[1], pixel[2], math.floor(pixel[3]/3)))
      img.paste(imgtwo, (0, 0), imgtwo)
      img.save("./temp/img/"+fileName+"overlay.png") # save to use
      file = open("./temp/img/"+fileName+"overlay.png", "rb", buffering = 0) #open file
      await ctx.send("Here is your image!", file=discord.File(file, filename="convertedimage.png")) #vague comment #274
      file.close() # close file to prevent memory leak
      os.remove("./temp/img/"+fileName+"overlay.png") # remove file
    elif url.lower().endswith(".gif") or urltwo.lower().endswith(".gif"):
      message = await ctx.send("Your image is being processed, this may take a few seconds...") #it takes a while to add a caption to an image, notify the user
      frames = []
      imgdata = requests.get(url)
      img = Image.open(toimg(imgdata.content))
      imgdatatwo = requests.get(urltwo)
      imgtwo = Image.open(toimg(imgdatatwo.content))
      whichImg = True if url.lower().endswith(".gif") else False
      if whichImg == True:
        for frame in ImageSequence.Iterator(img):
          imgtwo = Image.open(toimg(imgdatatwo.content))
          imgtwo = imgtwo.convert("RGBA")
          framedraw = frame.convert("RGBA")
          wid, hgt = framedraw.size
          imgtwo = imgtwo.resize((wid, hgt), resample=Image.BILINEAR) #resize image with bilinear
      
          for y in range(hgt):
            for x in range(wid):
              pixel = imgtwo.getpixel((x,y))
              imgtwo.putpixel((x, y), (pixel[0], pixel[1], pixel[2], math.floor(pixel[3]/3)))
          framedraw.paste(imgtwo, (0, 0), imgtwo)
          byteIO = toimg()
          frame.save(byteIO, format="GIF")
          frame = Image.open(byteIO)
          frames.append(framedraw)
      else:
        for frame in ImageSequence.Iterator(imgtwo):
          img = Image.open(toimg(imgdata.content))
          img = img.convert("RGBA")
          framedraw = frame.convert("RGBA")
          wid, hgt = img.size
          framedraw = framedraw.resize((wid, hgt), resample=Image.BILINEAR) #resize image with bilinear
          
          for y in range(hgt):
            for x in range(wid):
              pixel = framedraw.getpixel((x,y))
              framedraw.putpixel((x, y), (pixel[0], pixel[1], pixel[2], math.floor(pixel[3]/3)))
          img.paste(framedraw, (0, 0), framedraw)
          byteIO = toimg()
          frame.save(byteIO, format="GIF")
          frame = Image.open(byteIO)
          frames.append(img)
        
      fileName = randomStr(24) #zzzzzzzzzzzz
      byteIO = toimg()
      frames[0].save("./temp/img/"+fileName+"overlay.gif", duration = get_avg_fps(img if whichImg else imgtwo), loop = 0, save_all=True, append_images=frames[1:]) # save it to the temporary file blah blah blah
      file = open("./temp/img/"+fileName+"overlay.gif", "rb", buffering = 0)
      await message.edit(content="Sending image...") #edit the message to notify the user that the image is sending and not just my pc being bad
      await ctx.send("Here is your image!", file=discord.File(file, filename="convertedimage.gif")) # send the image
      await message.delete() # delete the edited message
      file.close() # stop using the caption file to prevent memory leak
      os.remove("./temp/img/"+fileName+"overlay.gif") # delete the caption file
    else:
      await ctx.send("Your image must be a PNG, JPG, or GIF image.")
  else:
    await ctx.send("This command requires 2 images!")
    
# noise command
@bot.command()
async def noise(ctx, grayscale=False, wid=None, hgt=None):
  if wid == None:
    wid = 200
  try:
    wid = max(1, min(int(wid), 512))
  except:
    wid = 200
  finally:
    if hgt == None:
      hgt = 150
    try:
      hgt = max(1, min(int(hgt), 512))
    except:
      hgt = 150
  grayscale = bool(grayscale)
  canv = Image.new("RGB", (wid, hgt), (255, 255, 255))
  for y in range(hgt):
    for x in range(wid):
      if grayscale:
        pix = random.randint(0,255)
        canv.putpixel((x, y), (pix, pix, pix))
      else:
        canv.putpixel((x, y), (random.randint(0,255), random.randint(0,255), random.randint(0,255)))
  fileName = randomStr(24)
  canv.save("./temp/img/"+fileName+"noise.png")
  file = open("./temp/img/"+fileName+"noise.png", "rb", buffering = 0)
  await ctx.send(file=discord.File(file, filename="noise.png"))
#invert command
@bot.command()
async def invert(ctx):
  if len(ctx.message.attachments) >= 1: # if 1 image is attached
    url = ctx.message.attachments[0].url # blah blah blah im tired of making these comemnts i shouldve made them as i went instead of adding them after
    if url.lower().endswith(".png") or url.lower().endswith(".jpg"): # if image is png or jpg
      imgdata = requests.get(url) # get the image
      img = Image.open(toimg(imgdata.content)) # open it
      fileName = randomStr(24) 
      img = img.convert("RGBA")
      wid, hgt = img.size # get the image size
      imgmix = Image.new("RGBA", (wid,hgt), (255, 255, 255, 255)) # make a new image with the image size
      pixel = 0
      for y in range(hgt):
        for x in range(wid):
          pixel = img.getpixel((x,y)) # get pixel 
          imgmix.putpixel((x, y), (255-pixel[0], 255-pixel[1], 255-pixel[2], pixel[3])) # draw pixel with inverted color to imgmix
      imgmix.save("./temp/img/"+fileName+"invert.png") # save to use
      file = open("./temp/img/"+fileName+"invert.png", "rb", buffering = 0) #open file
      await ctx.send("Here is your image!", file=discord.File(file, filename="convertedimage.png")) #vague comment #274
      file.close() # close file to prevent memory leak
      os.remove("./temp/img/"+fileName+"invert.png") # remove file
    elif url.lower().endswith(".gif"):
      message = await ctx.send("Your image is being processed, this may take a few seconds...") #it takes a while to add a caption to an image, notify the user
      frames = []
      imgdata = requests.get(url) # get the image
      img = Image.open(toimg(imgdata.content))
      for frame in ImageSequence.Iterator(img):
        framedraw = frame.convert("RGBA")
        wid, hgt = img.size
        imgmix = Image.new("RGBA", (wid,hgt), (255, 255, 255, 255))
        pixel = 0
        for y in range(hgt):
          for x in range(wid):
            pixel = framedraw.getpixel((x,y))
            imgmix.putpixel((x, y), (255-pixel[0], 255-pixel[1], 255-pixel[2], pixel[3]))
        byteIO = toimg()
        frame.save(byteIO, format="GIF")
        frame = Image.open(byteIO)
        frames.append(imgmix)
      fileName = randomStr(24) #zzzzzzzzzzzz
      byteIO = toimg()
      frames[0].save("./temp/img/"+fileName+"invert.gif", duration = get_avg_fps(img), loop = 0, save_all=True, append_images=frames[1:]) # save it to the temporary file blah blah blah
      file = open("./temp/img/"+fileName+"invert.gif", "rb", buffering = 0)
      await message.edit(content="Sending image...") #edit the message to notify the user that the image is sending and not just my pc being bad
      await ctx.send("Here is your image!", file=discord.File(file, filename="convertedimage.gif")) # send the image
      await message.delete() # delete the edited message
      file.close() # stop using the caption file to prevent memory leak
      os.remove("./temp/img/"+fileName+"invert.gif") # delete the caption file
    else:
      await ctx.send("Your image must be a PNG, JPG, or GIF image.")
  else:
    await ctx.send("This command requires an image!")

#horiz flip command
@bot.command()
async def flip(ctx):
  if len(ctx.message.attachments) >= 1: # if 1 image is attached
    url = ctx.message.attachments[0].url # blah blah blah im tired of making these comemnts i shouldve made them as i went instead of adding them after
    if url.lower().endswith(".png") or url.lower().endswith(".jpg"):
      imgdata = requests.get(url)
      img = Image.open(toimg(imgdata.content))
      fileName = randomStr(24)
      img = img.convert("RGBA")
      img = ImageOps.mirror(img)
      img.save("./temp/img/"+fileName+"flipped.png") # save to use
      file = open("./temp/img/"+fileName+"flipped.png", "rb", buffering = 0) #open file
      await ctx.send("Here is your image!", file=discord.File(file, filename="convertedimage.png")) #vague comment #274
      file.close() # close file to prevent memory leak
      os.remove("./temp/img/"+fileName+"flipped.png") # remove file
    elif url.lower().endswith(".gif"):
      message = await ctx.send("Your image is being processed, this may take a few seconds...") #it takes a while to add a caption to an image, notify the user
      frames = []
      imgdata = requests.get(url) # get the image
      img = Image.open(toimg(imgdata.content))
      for frame in ImageSequence.Iterator(img):
        imgt = frame.convert("RGBA")
        imgt = ImageOps.mirror(imgt)
        byteIO = toimg()
        frame.save(byteIO, format="GIF")
        frame = Image.open(byteIO)
        frames.append(imgt)
      fileName = randomStr(24) #zzzzzzzzzzzz
      byteIO = toimg()
      frames[0].save("./temp/img/"+fileName+"flipped.gif", duration = get_avg_fps(img), loop = 0, save_all=True, append_images=frames[1:]) # save it to the temporary file blah blah blah
      file = open("./temp/img/"+fileName+"flipped.gif", "rb", buffering = 0)
      await message.edit(content="Sending image...") #edit the message to notify the user that the image is sending and not just my pc being bad
      await ctx.send("Here is your image!", file=discord.File(file, filename="convertedimage.gif")) # send the image
      await message.delete() # delete the edited message
      file.close() # stop using the caption file to prevent memory leak
      os.remove("./temp/img/"+fileName+"flipped.gif") # delete the caption file
    else:
      await ctx.send("Your image must be a PNG, JPG, or GIF image.")
  else:
    await ctx.send("This command requires an image!")

#wave command
@bot.command()
async def wave(ctx, wavesize=None):
  if wavesize == None:
    wavesize = 20
  try:
    wavesize = int(wavesize)
  except:
    wavesize = 20
  finally:
    if wavesize >= 300:
      wavesize = 300
    if len(ctx.message.attachments) >= 1: # if 1 image is attached
      url = ctx.message.attachments[0].url # blah blah blah im tired of making these comemnts i shouldve made them as i went instead of adding them after
      if url.lower().endswith(".png") or url.lower().endswith(".jpg"):
        imgdata = requests.get(url)
        img = Image.open(toimg(imgdata.content))
        fileName = randomStr(24)
        img = img.convert("RGBA")
        wid, hgt = img.size
        imgmix = Image.new("RGBA", (wid,hgt+(wavesize*2)), (255, 255, 255, 0))
        pixel = 0
        for y in range(hgt):
          for x in range(wid):
            pixel = img.getpixel((x,y))
            imgmix.putpixel((x, min(hgt+(wavesize*2)-1, max(0, int(wavesize+y+(math.sin(x/wavesize/2)*wavesize))))), (pixel[0], pixel[1], pixel[2], pixel[3]))
        imgmix.save("./temp/img/"+fileName+"wave.png") # save to use
        file = open("./temp/img/"+fileName+"wave.png", "rb", buffering = 0) #open file
        await ctx.send("Here is your image!", file=discord.File(file, filename="convertedimage.png")) #vague comment #274
        file.close() # close file to prevent memory leak
        os.remove("./temp/img/"+fileName+"wave.png") # remove file
      elif url.lower().endswith(".gif"):
        message = await ctx.send("Your image is being processed, this may take a few seconds...") #it takes a while to add a caption to an image, notify the user
        frames = []
        imgdata = requests.get(url) # get the image
        img = Image.open(toimg(imgdata.content))
        framenum = -1
        for frame in ImageSequence.Iterator(img):
          framenum += 1
          imgt = frame.convert("RGBA")
          wid, hgt = imgt.size
          imgmix = Image.new("RGBA", (wid,hgt+(wavesize*2)), (255, 255, 255, 0))
          for y in range(hgt):
            for x in range(wid):
              pixel = imgt.getpixel((x,y))
              imgmix.putpixel((x, min(hgt+(wavesize*2)-1, max(0, int(wavesize+y+(math.sin((x+(framenum*2))/wavesize/2)*wavesize))))), (pixel[0], pixel[1], pixel[2], pixel[3]))
          byteIO = toimg()
          frame.save(byteIO, format="GIF")
          frame = Image.open(byteIO)
          frames.append(imgmix)
        fileName = randomStr(24) #zzzzzzzzzzzz
        byteIO = toimg()
        frames[0].save("./temp/img/"+fileName+"wave.gif", duration = get_avg_fps(img), loop = 0, save_all=True, append_images=frames[1:]) # save it to the temporary file blah blah blah
        file = open("./temp/img/"+fileName+"wave.gif", "rb", buffering = 0)
        await message.edit(content="Sending image...") #edit the message to notify the user that the image is sending and not just my pc being bad
        await ctx.send("Here is your image!", file=discord.File(file, filename="convertedimage.gif")) # send the image
        await message.delete() # delete the edited message
        file.close() # stop using the caption file to prevent memory leak
        os.remove("./temp/img/"+fileName+"wave.gif") # delete the caption file
      else:
          await ctx.send("Your image must be a PNG, JPG, or GIF image.")
    else:
      await ctx.send("This command requires an image!")
#vert flip command
@bot.command()
async def flipvert(ctx):
  if len(ctx.message.attachments) >= 1: # if 1 image is attached
    url = ctx.message.attachments[0].url # blah blah blah im tired of making these comemnts i shouldve made them as i went instead of adding them after
    if url.lower().endswith(".png") or url.lower().endswith(".jpg"):
      imgdata = requests.get(url)
      img = Image.open(toimg(imgdata.content))
      fileName = randomStr(24)
      img = img.convert("RGBA")
      img = ImageOps.flip(img)
      img.save("./temp/img/"+fileName+"vflipped.png") # save to use
      file = open("./temp/img/"+fileName+"vflipped.png", "rb", buffering = 0) #open file
      await ctx.send("Here is your image!", file=discord.File(file, filename="convertedimage.png")) #vague comment #274
      file.close() # close file to prevent memory leak
      os.remove("./temp/img/"+fileName+"vflipped.png") # remove file
    elif url.lower().endswith(".gif"):
      message = await ctx.send("Your image is being processed, this may take a few seconds...") #it takes a while to add a caption to an image, notify the user
      frames = []
      imgdata = requests.get(url) # get the image
      img = Image.open(toimg(imgdata.content))
      for frame in ImageSequence.Iterator(img):
        imgt = frame.convert("RGBA")
        imgt = ImageOps.flip(imgt)
        byteIO = toimg()
        frame.save(byteIO, format="GIF")
        frame = Image.open(byteIO)
        frames.append(imgt)
      fileName = randomStr(24) #zzzzzzzzzzzz
      byteIO = toimg()
      frames[0].save("./temp/img/"+fileName+"vflipped.gif", duration = get_avg_fps(img), loop = 0, save_all=True, append_images=frames[1:]) # save it to the temporary file blah blah blah
      file = open("./temp/img/"+fileName+"vflipped.gif", "rb", buffering = 0)
      await message.edit(content="Sending image...") #edit the message to notify the user that the image is sending and not just my pc being bad
      await ctx.send("Here is your image!", file=discord.File(file, filename="convertedimage.gif")) # send the image
      await message.delete() # delete the edited message
      file.close() # stop using the caption file to prevent memory leak
      os.remove("./temp/img/"+fileName+"vflipped.gif") # delete the caption file
    else:
      await ctx.send("Your image must be a PNG, JPG, or GIF image.")
  else:
    await ctx.send("This command requires an image!")

@bot.command()
async def grayscale(ctx):
  if len(ctx.message.attachments) >= 1: # if 1 image is attached
    url = ctx.message.attachments[0].url # blah blah blah im tired of making these comemnts i shouldve made them as i went instead of adding them after
    if url.lower().endswith(".png") or url.lower().endswith(".jpg"):
      imgdata = requests.get(url)
      img = Image.open(toimg(imgdata.content))
      fileName = randomStr(24)
      img = img.convert("RGBA")
      img = ImageOps.grayscale(img)
      img = img.convert("RGBA")
      img.save("./temp/img/"+fileName+"grayscale.png") # save to use
      file = open("./temp/img/"+fileName+"grayscale.png", "rb", buffering = 0) #open file
      await ctx.send("Here is your image!", file=discord.File(file, filename="convertedimage.png")) #vague comment #274
      file.close() # close file to prevent memory leak
      os.remove("./temp/img/"+fileName+"grayscale.png") # remove file
    elif url.lower().endswith(".gif"):
      message = await ctx.send("Your image is being processed, this may take a few seconds...") #it takes a while to add a caption to an image, notify the user
      frames = []
      imgdata = requests.get(url) # get the image
      img = Image.open(toimg(imgdata.content))
      for frame in ImageSequence.Iterator(img):
        imgt = frame.convert("RGBA")
        imgt = ImageOps.grayscale(imgt)
        imgt = imgt.convert("RGBA")
        byteIO = toimg()
        frame.save(byteIO, format="GIF")
        frame = Image.open(byteIO)
        frames.append(imgt)
      fileName = randomStr(24) #zzzzzzzzzzzz
      byteIO = toimg()
      frames[0].save("./temp/img/"+fileName+"grayscale.gif", duration = get_avg_fps(img), loop = 0, save_all=True, append_images=frames[1:]) # save it to the temporary file blah blah blah
      file = open("./temp/img/"+fileName+"grayscale.gif", "rb", buffering = 0)
      await message.edit(content="Sending image...") #edit the message to notify the user that the image is sending and not just my pc being bad
      await ctx.send("Here is your image!", file=discord.File(file, filename="convertedimage.gif")) # send the image
      await message.delete() # delete the edited message
      file.close() # stop using the caption file to prevent memory leak
      os.remove("./temp/img/"+fileName+"grayscale.gif") # delete the caption file
    else:
      await ctx.send("Your image must be a PNG, JPG, or GIF image.")
  else:
    await ctx.send("This command requires an image!")
#jpeg image command
@bot.command()
async def jpegify(ctx, quality=None):
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
      if url.lower().endswith(".png") or url.lower().endswith(".jpg"): #if it is a png, jpg or gif
        imgdata = requests.get(url) # get the image data
        img = Image.open(toimg(imgdata.content)) # make a new PIL image
        fileName = randomStr(24) # make a random string 24 characters long
        img = img.convert("RGB") # convert the image to RGB
        img.save("./temp/img/"+fileName+"jpgified.jpg", mode="JPEG", quality=quality) # save it to a temporary folder to be deleted later as a JPG with quality set to the quality variable
        file = open("./temp/img/"+fileName+"jpgified.jpg", "rb", buffering = 0) # open the image that was just saved
        await ctx.send("Here is your image!", file=discord.File(file, filename="convertedimage.jpg")) # send the image
        file.close() # stop using the image to prevent memory leak
        os.remove("./temp/img/"+fileName+"jpgified.jpg") # delete it
      elif url.lower().endswith(".gif"):
        message = await ctx.send("Your image is being processed, this may take a few seconds...") #it takes a while to add a caption to an image, notify the user
        frames = []
        imgdata = requests.get(url) # get the image
        img = Image.open(toimg(imgdata.content))
        fileName = randomStr(24)
        framecount = 0
        for frame in ImageSequence.Iterator(img):
          framecount += 1
          imgt = frame.convert("RGB")
          imgt.save("./temp/img/"+fileName+"framejpegified"+str(framecount)+".jpg", mode="JPEG", quality=quality)
          imgt = Image.open("./temp/img/"+fileName+"framejpegified"+str(framecount)+".jpg")
          byteIO = toimg()
          frame.save(byteIO, format="GIF")
          frame = Image.open(byteIO)
          frames.append(imgt)
        byteIO = toimg()
        frames[0].save("./temp/img/"+fileName+"jpgified.gif", duration = get_avg_fps(img), loop = 0, save_all=True, append_images=frames[1:]) # save it to the temporary file blah blah blah
        file = open("./temp/img/"+fileName+"jpgified.gif", "rb", buffering = 0)
        await message.edit(content="Sending image...") #edit the message to notify the user that the image is sending and not just my pc being bad
        await ctx.send("Here is your image!", file=discord.File(file, filename="convertedimage.gif")) # send the image
        await message.delete() # delete the edited message
        file.close() # stop using the caption file to prevent memory leak
        os.remove("./temp/img/"+fileName+"jpgified.gif") # delete the caption file
        for i in range(framecount):
          os.remove("./temp/img/"+fileName+"framejpegified"+str(i+1)+".jpg")
      else: #if not
        await ctx.send("Your image must be a PNG, JPG, or GIF image.") # notify the user
    else: # if no attachment is attached
      await ctx.send("This command requires an image!") # notify the user

#uncaption
@bot.command()
async def uncaption(ctx):
  if len(ctx.message.attachments) >= 1: # if 1 image is attached
    url = ctx.message.attachments[0].url # blah blah blah im tired of making these comemnts i shouldve made them as i went instead of adding them after
    if url.lower().endswith(".png") or url.lower().endswith(".jpg"):
      imgdata = requests.get(url)
      img = Image.open(toimg(imgdata.content))
      fileName = randomStr(24)
      img = img.convert("RGBA")
      wid, hgt = img.size
      cutY = 0
      for y in range(hgt):
        if cutY == 0:
          pixel = img.getpixel((0, y))
          if pixel[0] != 255 and pixel[1] != 255 and pixel[2] != 255:
            cutY = y
      img = img.crop((0, cutY, wid, hgt))
      img = img.convert("RGBA")
      img.save("./temp/img/"+fileName+"uncaption.png") # save to use
      file = open("./temp/img/"+fileName+"uncaption.png", "rb", buffering = 0) #open file
      await ctx.send("Here is your image!", file=discord.File(file, filename="convertedimage.png")) #vague comment #274
      file.close() # close file to prevent memory leak
      os.remove("./temp/img/"+fileName+"uncaption.png") # remove file
    elif url.lower().endswith(".gif"):
      message = await ctx.send("Your image is being processed, this may take a few seconds...") #it takes a while to add a caption to an image, notify the user
      frames = []
      imgdata = requests.get(url) # get the image
      img = Image.open(toimg(imgdata.content))
      cutY = -1
      for frame in ImageSequence.Iterator(img):
        imgt = frame.convert("RGBA")
        wid, hgt = imgt.size
        if cutY == -1:
          for y in range(hgt):
            if cutY == -1:
              pixel = imgt.getpixel((0, y))
              if pixel[0] < 240 and pixel[1] < 240 and pixel[2] < 240:
                cutY = y
        imgt = imgt.crop((0, cutY, wid, hgt))
        imgt = imgt.convert("RGBA")
        byteIO = toimg()
        frame.save(byteIO, format="GIF")
        frame = Image.open(byteIO)
        frames.append(imgt)
      fileName = randomStr(24) #zzzzzzzzzzzz
      byteIO = toimg()
      frames[0].save("./temp/img/"+fileName+"uncaption.gif", duration = get_avg_fps(img), loop = 0, save_all=True, append_images=frames[1:]) # save it to the temporary file blah blah blah
      file = open("./temp/img/"+fileName+"uncaption.gif", "rb", buffering = 0)
      await message.edit(content="Sending image...") #edit the message to notify the user that the image is sending and not just my pc being bad
      await ctx.send("Here is your image!", file=discord.File(file, filename="convertedimage.gif")) # send the image
      await message.delete() # delete the edited message
      file.close() # stop using the caption file to prevent memory leak
      os.remove("./temp/img/"+fileName+"uncaption.gif") # delete the caption file
    else:
      await ctx.send("Your image must be a PNG, JPG, or GIF image.")
  else:
    await ctx.send("This command requires an image!")
#brainfuck
@bot.command()
async def brainfrick(ctx, code=">++++++++[<++++++++++>-]>+++++++++++[<++++++++++>-]>++++++[<+++++>-]>+++++++++++++++[<+++++++>-]<<<<--.>+.>++.>.<<-.++.+++++.-.>.>--.++.<<++.>>----.<<--------.>+."):
  buffer = []
  now = clock.time()+5
  output = ""
  inLoop = 0
  skip = False
  active = True
  pointer = 0
  for slot in range(128):
    buffer.append(0)
  ind = 0
  loopChars = []
  loopChars.append(0)
  while ind < len(code) and active == True:
    if pointer < 0 or pointer > 255:
      await ctx.send("Error! (Pointer out of range!)")
      active = False
    if now < clock.time():
      await ctx.send("Error! (Timeout)")
      active = False
      inLoop = 0
    if active == True:
      ind += 1
      cmd = code[ind-1]
      if cmd == ">":
        pointer += 1
      elif cmd == "<":
        pointer -= 1
      elif cmd == "+":
        buffer[pointer] += 1
        buffer[pointer] = buffer[pointer] % 256
      elif cmd == "-":
        buffer[pointer] -= 1
        buffer[pointer] = buffer[pointer] % 256
      elif cmd == "[":
        if buffer[pointer] != 0:
          inLoop = inLoop+1
          loopChars.append(ind)
        else:
          while (code[ind-1] != "]"):
            ind += 1
      elif cmd == "]":
        if inLoop >= 1:
          if buffer[pointer] != 0:
            ind = loopChars[inLoop]
          else:
            loopChars.pop(inLoop)
            inLoop = inLoop - 1
        else:
          await ctx.send("Error! (Mismatched parenthesis!)")
          active = False
      elif cmd == ".":
        output = output + str(chr(buffer[pointer]))
      elif cmd == ",":
        await ctx.send("Input is not supported yet.")
        active = False
  if inLoop != 0:
    active = False
    await ctx.send("Error! (End of loop not declared.)")
  if active == True:
    embed = discord.Embed(title="Brainfrick")
    string = ""
    for index in range(len(buffer)):
      string += ("0" + str(hex(buffer[index]))[2:4] if len(str(hex(buffer[index]))[2:4]) == 1 else str(hex(buffer[index]))[2:4]) + " "
      if index%16 == 15:
        string += """\n"""
    embed.add_field(name="Input:",value="""```bf\n"""+code+"```",inline=False)
    embed.add_field(name="Output:",value="```"+output+"```",inline=False)
    await ctx.send(embed = embed)
    embed = discord.Embed(title="Buffer:")
    embed.add_field(name="Buffer:",value="```"+string+"```")
    await ctx.send(embed = embed)
#fairly simple command
@bot.command()
async def info(ctx):
  embed = discord.Embed(title="Bot information", color=discord.Color(7312382))
  embed.add_field(name="Version:", value=str(versionnum)+"abcdefghijklmnopqrstuvwxyz"[revision], inline=True)
  embed.add_field(name="Servers:", value="I am in "+str(len(bot.guilds))+" servers", inline=True)
  await ctx.send(embed=embed)
#eval command
@bot.command()
async def eval(ctx):
  msg = ctx.message.content
  code = msg[(len(bprefix(bot, ctx))+5):(len(msg)+1)]
  embed = discord.Embed(title="Lorem Ipsum", color=discord.Color(16777215))
  if ctx.author.id == 353911350545612801:
    try:
      output = exec(code)
      embed.color = discord.Color(196607)
      embed.add_field(name="Input:", value="""```py\n"""+str(code)+"```")
      embed.add_field(name="Output:", value="```"+str(output)+"```")
      embed.title = "Code ran fine!"
      await ctx.reply(embed=embed)
    except Exception as error:
      embed.title = "Error!"
      embed.color = discord.Color(8388608)
      embed.add_field(name="Error:", value="""```diff\n- """+str(error)+"```")
      await ctx.reply(embed=embed)
  else:
    await ctx.send("Only the bot developer can run this command!")
#caption img command
    
@bot.command()
async def caption(ctx, caption):
  if ctx.message.attachments != []: #if an attachment is attached
    url = ctx.message.attachments[0].url #only get the first one blah blah blah you know the drill
    if url.lower().endswith(".png") or url.lower().endswith(".jpg"):
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
    elif url.lower().endswith(".gif"):
      message = await ctx.send("Your image is being processed, this may take a few seconds...") #it takes a while to add a caption to an image, notify the user
      frames = []
      imgdata = requests.get(url) # get the image
      img = Image.open(toimg(imgdata.content))
      for frame in ImageSequence.Iterator(img):
        framedraw = frame.convert("RGBA")
        wid, hgt = framedraw.size # get the image width and height
        usefont = ImageFont.truetype("captfont.ttf", round((hgt/wid)/3*(wid/10)*3)) # get funny font
        stringtoputinimg = textwrap.wrap(caption, width=round(wid/((hgt/wid)/3*(wid/17)*3))) # caption breaks for each line it takes up
        caption = '''''' # replace caption with a string that supports line breaks for our caption
        for txt in range(len(stringtoputinimg)): # for each entry in the broken up caption
          caption += stringtoputinimg[txt] # add it to the caption
          if txt != len(stringtoputinimg)-1: #if it is not the last entry
            caption += '''\n''' # add a line break
        imgdraw = ImageDraw.Draw(framedraw) # make a new image that can be pasted
        texwid, texhgt = imgdraw.textsize(caption, font=usefont) # get how much space text will take up
        captcanv = Image.new(framedraw.mode, (wid, hgt+texhgt+6), (255, 255, 255)) # make a new canvas with the image height + the text height + a margin
        captcanv.paste(framedraw, (0, texhgt+6)) # paste the image sent into the canvas
        capt = ImageDraw.Draw(captcanv) # make a new image that text can be drawn on
        capt.text(((wid/2), 0),str(caption),(0,0,0),font=usefont, align='center', anchor="ma") # draw the caption on the canvas image with central alignment
        byteIO = toimg()
        frame.save(byteIO, format="GIF")
        frame = Image.open(byteIO)
        frames.append(captcanv)
      fileName = randomStr(24) #zzzzzzzzzzzz
      byteIO = toimg()
      frames[0].save("./temp/img/"+fileName+"caption.gif", duration = get_avg_fps(img), loop = 0, save_all=True, append_images=frames[1:]) # save it to the temporary file blah blah blah
      file = open("./temp/img/"+fileName+"caption.gif", "rb", buffering = 0)
      await message.edit(content="Sending image...") #edit the message to notify the user that the image is sending and not just my pc being bad
      await ctx.send("Here is your image!", file=discord.File(file, filename="convertedimage.gif")) # send the image
      await message.delete() # delete the edited message
      file.close() # stop using the caption file to prevent memory leak
      os.remove("./temp/img/"+fileName+"caption.gif") # delete the caption file
      
    else:
      await ctx.send("Your image must be a PNG, JPG, or GIF image.")
  else:
    await ctx.send("This command requires an image!")

@bot.command()
async def duck(ctx, code=None):
  if code == None:
    await ctx.send("No input given.")
  else:
    await ctx.send("Hello world")

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
          if url.lower().endswith(".png") or url.lower().endswith(".jpg"):
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
          elif url.lower().endswith(".gif"):
            message = await ctx.send("Your image is being processed, this may take a few seconds...") #it takes a while to add a caption to an image, notify the user
            frames = []
            imgdata = requests.get(url) # get the image
            img = Image.open(toimg(imgdata.content))
            for frame in ImageSequence.Iterator(img):
              framedraw = frame.convert("RGBA")
              wid, hgt = framedraw.size # get the image width and height
              framedraw = framedraw.resize((round(wid/scalewid)+1,round(hgt/scalehgt)+1),resample=Image.BILINEAR) #resize image with bilinear
              if scalemode == 0: # nearest neighbor scaling
                framedraw = framedraw.resize((wid,hgt), resample=Image.NEAREST)
              else: # bilinear scaling
                framedraw = framedraw.resize((wid,hgt), resample=Image.BILINEAR)
              byteIO = toimg()
              frame.save(byteIO, format="GIF")
              frame = Image.open(byteIO)
              frames.append(framedraw)
            fileName = randomStr(24) #zzzzzzzzzzzz
            byteIO = toimg()
            frames[0].save("./temp/img/"+fileName+"caption.gif", duration = get_avg_fps(img), loop = 0, save_all=True, append_images=frames[1:]) # save it to the temporary file blah blah blah
            file = open("./temp/img/"+fileName+"caption.gif", "rb", buffering = 0)
            await message.edit(content="Sending image...") #edit the message to notify the user that the image is sending and not just my pc being bad
            await ctx.send("Here is your image!", file=discord.File(file, filename="convertedimage.gif")) # send the image
            await message.delete() # delete the edited message
            file.close() # stop using the caption file to prevent memory leak
            os.remove("./temp/img/"+fileName+"caption.gif") # delete the caption file
          else:
            await ctx.send("Your image must be a PNG, JPG, or GIF image.")
      else:
        await ctx.send("This command requires an image!")

#finally thank god i dont have to repeat the same comments over and over

#future 3dg to past 3dg: you got pranked :troll:
@bot.command()
async def lightdark(ctx, scalemode=None):
  if scalemode == None: # if scale mode isnt set
    scalemode = 0 #set to nearest
  try: #see if scalemode is an integer
    scalemode = int(scalemode)
  except: #if it isnt
    scalemode = 0 #set it to nearest
  if len(ctx.message.attachments) == 2: # if 2 images are attached
    url = ctx.message.attachments[0].url # blah blah blah im tired of making these comemnts i shouldve made them as i went instead of adding them after
    urltwo = ctx.message.attachments[1].url # blah blah blah im tired of making these comemnts i shouldve made them as i went instead of adding them after
    if url.lower().endswith(".png") or url.lower().endswith(".jpg") or urltwo.lower().endswith(".png") or urltwo.lower().endswith(".jpg") or url.lower().endswith(".gif") or urltwo.lower().endswith(".gif"):
      imgdata = requests.get(url)
      img = Image.open(toimg(imgdata.content))
      imgdatatwo = requests.get(urltwo)
      imgtwo = Image.open(toimg(imgdatatwo.content))
      fileName = randomStr(24)
      img = img.convert("RGBA")
      imgtwo = imgtwo.convert("RGBA")
      img = img.resize((320, 240), resample=Image.BILINEAR) #resize image with bilinear
      imgtwo = imgtwo.resize((320, 240), resample=Image.BILINEAR) #resize image with bilinear
      img = ImageOps.grayscale(img)
      imgtwo = ImageOps.grayscale(imgtwo)
      img = img.convert("RGBA")
      imgtwo = imgtwo.convert("RGBA")
      imgmix = Image.new("RGBA", (320,240), (255, 255, 255, 255))
      pixel = 0
      for y in range(240):
        for x in range(320):
          if (x+y)%2 == 1:
            pixel = imgtwo.getpixel((x,y))
            imgmix.putpixel((x, y), (54, 57, 63, 255-pixel[0]))
          else:
            pixel = img.getpixel((x,y))
            imgmix.putpixel((x, y), (255, 255, 255, pixel[0]))
      imgmix.save("./temp/img/"+fileName+"bwchange.png") # save to use
      file = open("./temp/img/"+fileName+"bwchange.png", "rb", buffering = 0) #open file
      await ctx.send("Here is your image!", file=discord.File(file, filename="convertedimage.png")) #vague comment #274
      file.close() # close file to prevent memory leak
      os.remove("./temp/img/"+fileName+"bwchange.png") # remove file

#there used to be a gif part here but gif literally does not support transparent images :pensive:
#wasted like 2 hours of my time :)
      
    else:
      await ctx.send("Your image must be a PNG, JPG, or GIF image.")
  else:
    await ctx.send("This command requires 2 images!")
@bot.command()
async def avatar(ctx):
  try:
    idtoget = str(ctx.message.mentions[0].id)
    user = await ctx.message.guild.fetch_member(idtoget)
    print(user)
    avatar = "https://cdn.discordapp.com/avatars/"+idtoget+"/"+str(user.avatar)+".webp?size=4096" # get user avatar url in 256p
    await ctx.send(user.name+"'s avatar!")
    await ctx.send(avatar)
  except Exception as err:
    print(err)
    await ctx.send("You must mention a user!")
@bot.command()
async def color(ctx, hexcode=None):
  if hexcode == None:
    await ctx.send("No hex code given!")
  elif len(hexcode) >= 6 and len(hexcode) <= 8 and hex_format(hexcode) != "error":
    name = randomStr(24)
    Image.new("RGBA", (72, 72), hex_format(hexcode)).save("./temp/img/"+name+"Color.png")
    file = open("./temp/img/"+name+"Color.png", "rb", buffering = 0)
    await ctx.send("Color #"+str(hexcode), file=discord.File(file, filename="color.png"))
    file.close()
    os.remove("./temp/img/"+name+"Color.png")
  else:
    await ctx.send("Not a valid hex code!")
#help command
helpdef = {"avatar":"Gets a user's avatar. (Arguments: {User (mention)})",
  "noise":"Gives random noise. Defaults to 200x150 colored image. (Arguments: (Grayscale), (Width), (Height))",
  "color":"Gives an image representing the color inputted. (Arguments: {Hex code})",
  "pixel":"Requires an image. Lowers the resolution of an image and scales it back up (Arguments: [Scale X factor, Scale Y factor, Scaling algorithm (0 - Nearest, 1 - Bilinear)])",
  "echo":"Make the bot say anything! (Arguments: {Message})",
  "caption":"Requires an image. Adds a caption to any image (Arguments: {Caption})",
  "info":"Sends information about the bot",
  "jpegify":"Requires an image. Returns a low quality jpg of the image sent (Arguments: [Quality])",
  "help":"Shows a list of commands",
  "lightdark":"Requires two images. Mixes two images together to make one that changes with your theme! The first image will appear in the dark theme, and the second one will appear in the light theme!(Arguments: [Scaling algorithm])",
  "ping":"Gets your ping to the bot",
  "eval":"This command can only be ran by the bot developer.",
  "afk":"Makes you AFK.",
  "invert":"Requires an image. Inverts an image.",
  "prefix":"Changes the prefix of the bot. (Arguments: {Prefix})",
  "flip":"Requires an image. Flips an image horizontally.",
  "flipvert":"Requires an image. Flips an image vertically.",   
  "duck":"A Hello world Duck interpreter (Arguments: {Code})",
  "wave":"Requires an image. Makes an image wavy!",
  "uncaption":"Requires an image. Removes the caption from an image if it finds one.",
  "tictactoe":"Tic tac toe! (Arguments: {User (mention)})",
  "grayscale":"Requires an image. Grayscales an image.",
  "endmatch":"Ends a tic tac toe match",
  "brainfrick":"Runs brainf█:k code. (Arguments: {Code})"
} # dictionary containing all of the descriptions for the commands
@bot.command()
async def help(ctx, page=1):
  try:
    page = int(page)
  except:
    page = 1
  send = """Commands:\n"""
  embed = discord.Embed(title="Commands", color=discord.Color(1977406)) # make a new embed with title "Commands" with color #1e2c3e
  cmds = len(bot.commands)
  cmdstable = []
  cmdValue = 0
  cmdssort = [str(p) for p in bot.commands]
  cmdssort = sorted(cmdssort)
  for cmd in cmdssort:
    cmdstable.append(cmd)
    cmdValue += 1
  for cmd in range((page-1)*10, min(cmds, (page*10))): # for each command
    send += "`g!"+str(cmdstable[cmd])+"`" + " - " + str(helpdef.get(str(cmdstable[cmd])))+'''\n''' # add it in send string
  embed.add_field(name="Page "+str(page), value=send) # add the send string to the embed
  embed.add_field(name="Vote for GBot!",
                  value="""[Top.gg](https://top.gg/bot/907439983579758632/vote)\n[Vibeslist.cf](https://vibeslist.cf/bot/907439983579758632/vote)"""
                  , inline=False)
  embed.set_footer(text="Send g!help "+str(page+1)+" for the next page")
  #buttonprevpage = discord.ui.Button(label="prev page", custom_id="prev")
  
  #buttonprevpage.coroutine = discord.Interaction(id=random.randint(0, 1000000000), type=discord.InteractionType("component"), application_id=appid)
  await ctx.send(embed = embed) # send commands

#echo command
@bot.command()
async def echo(ctx): # echo command ok this should be simple
  await ctx.send("``"+str(ctx.message.content)[(5 + len(await bprefix(bot, ctx.message))) : len(str(ctx.message.content))].replace("`", "'")+"``") # slice the first 5 + prefix length characters off the message and send it
  await ctx.message.delete() # delete the message

################################
### /!\ epic gaming time /!\ ###
################################
boards = {}
@bot.command()
async def endmatch(ctx):
  if ctx.author.id in boards:
    boards.pop(ctx.author.id)
    await ctx.send("Left match!")
  else:
    await ctx.send("You are not in a match! To join one, use g!tictactoe and mention an opponent!")
def makeEmbed(board, win=False):
  boardEmojis = [":black_large_square:", "<:tictactoe_x:918581530551533638>", "<:tictactoe_o:918581530543145040>"]
  boardTxt = ""
  for y in range(0, 3):
    for x in range(0, 3):
      boardTxt += boardEmojis[int(board["board"][y][x])]
    if y != 2:
      boardTxt += """\n"""
  embed = discord.Embed(title="Tic tac toe", color=discord.Color(1977406 if win == False else 65280 if win == "o" or win == "x" else 65535))
  embed.add_field(name = "To play, say a number for the horizontal position, next to a number for your vertical position." if win == False else "O wins!" if win == "o" else "X wins!" if win == "x" else "Tie!", value=boardTxt)
  embed.set_footer(text = "To start your own game, type g!tictactoe and mention someone!")
  return embed
def checkWin(board):
  winpatterns = [
      [
        "oxx",
        "xox",
        "xxo"
      ],
      [
        "xxo",
        "xox",
        "oxx"
      ],
      [
        "oxx",
        "oxx",
        "oxx"
      ],
      [
        "xox",
        "xox",
        "xox"
      ],
      [
        "xxo",
        "xxo",
        "xxo"
      ],
      [
        "ooo",
        "xxx",
        "xxx"
      ],
      [
        "xxx",
        "ooo",
        "xxx"
      ],
      [
        "xxx",
        "xxx",
        "ooo"
      ]
    ]
  for pattern in winpatterns:
    cross = 0
    for y in range(0, 3):
      for x in range(0,3):
        if pattern[y][x] != "x":
          if board[y][x].replace("1","o").replace("2","x") == pattern[y][x]:
            cross += 1
    if cross == 3:
      return "x"
    cross = 0
    for y in range(0, 3):
      for x in range(0,3):
        if pattern[y][x] != "x":
          if board[y][x].replace("2","o").replace("1","x") == pattern[y][x]:
            cross += 1
    if cross == 3:
      return "o"
    tie = 0
    for y in range(0, 3):
      if board[y].replace("1","x").replace("2","x") == "xxx":
        tie += 3
    if tie == 9:
      return "tie"
  return False # function ends on return, if it didnt end we know none of this stuff is true
  
@bot.command()
async def tictactoe(ctx):
  opponent = ctx.message.mentions[0]
  if opponent == None:
    await ctx.send("You must mention an opponent!")
  elif ctx.author.id in boards:
    await ctx.send("You're already in a game! Use g!endmatch to leave your game!")
  elif str(opponent.id) in boards:
    await ctx.send(opponent.name + " is already in a game! Wait for them to finish before you play with them!")
  else:
    opponentid = str(opponent.id)
    boards[int(ctx.author.id)] = {"opponent":opponentid,"board":["000","000","000"],"secondaryPlr":False,"turn":0}
    boards[int(opponentid)] = {"opponent":ctx.author.id,"secondaryPlr":True,"turn":0}
    
    msg = await ctx.send(embed=makeEmbed(boards[ctx.author.id]))
    boards[int(ctx.author.id)]["message"] = msg

@bot.event
async def on_message(ctx):
  for mention in ctx.mentions:
    cur.execute("SELECT `id` FROM `users` WHERE id = "+str(mention.id)+" AND server = "+str(ctx.guild.id))
    if len(cur.fetchall()) != 0:
      await ctx.reply(mention.name + " is currently AFK!")
  if ctx.content[0:5] != "g!afk":
    cur.execute("SELECT `id` FROM `users` WHERE id = "+str(ctx.author.id)+" AND server = "+str(ctx.guild.id))
    if len(cur.fetchall()) != 0:
      cur.execute("DELETE FROM `users` WHERE id="+str(ctx.author.id)+" AND server = "+ str(ctx.guild.id))
      con.commit()
      await ctx.reply(ctx.author.name + " is no longer AFK!")
      try:
        if len(ctx.author.name.split(" [AFK]")) == 1:
          await ctx.author.edit(nick=ctx.author.name.split(" [AFK]")[0])
      except:
        print("No permission")
  
  if int(ctx.author.id) in boards: # dogwater tictactoe code
    if len(ctx.content) == 2:
      if ctx.content[0] in "123" and ctx.content[1] in "123":
        if boards[int(ctx.author.id)]["turn"] == 0 and boards[int(ctx.author.id)]["secondaryPlr"] == False:
          board = boards[int(ctx.author.id)]["board"]
          oldStr = board[int(ctx.content[1])-1]
          string = ("1" if (ctx.content[0] == "1" and oldStr[0] == "0") else oldStr[0]) + ("1" if (ctx.content[0] == "2" and oldStr[1] == "0") else oldStr[1]) + ("1" if (ctx.content[0] == "3" and oldStr[2] == "0") else oldStr[2])
          if string != oldStr:
            boards[int(ctx.author.id)]["board"][int(ctx.content[1])-1] = string
            embed = makeEmbed(boards[int(ctx.author.id)], checkWin(board))
            await ctx.reply(embed = embed)
            if checkWin(board) == False:
              boards[int(boards[int(ctx.author.id)]["opponent"])]["turn"] = 1
              boards[int(ctx.author.id)]["turn"] = 1
            else:
              boards.pop(int(boards[int(ctx.author.id)]["opponent"]))
              boards.pop(int(ctx.author.id))
          else:
            await ctx.reply("That spot is already taken!")
        elif boards[int(ctx.author.id)]["turn"] == 1 and boards[int(ctx.author.id)]["secondaryPlr"] == True:
          board = boards[boards[int(ctx.author.id)]["opponent"]]["board"]
          oldStr = board[int(ctx.content[1])-1]
          string = ("2" if (ctx.content[0] == "1" and oldStr[0] == "0") else oldStr[0]) + ("2" if (ctx.content[0] == "2" and oldStr[1] == "0") else oldStr[1]) + ("2" if (ctx.content[0] == "3" and oldStr[2] == "0") else oldStr[2])
          if string != oldStr:
            boards[boards[int(ctx.author.id)]["opponent"]]["board"][int(ctx.content[1])-1] = string
            embed = makeEmbed(boards[boards[int(ctx.author.id)]["opponent"]], checkWin(board))
            await ctx.reply(embed = embed)
            if checkWin(board) == False:
              boards[int(boards[int(ctx.author.id)]["opponent"])]["turn"] = 0
              boards[int(ctx.author.id)]["turn"] = 0
            else:
              boards.pop(int(boards[int(ctx.author.id)]["opponent"]))
              boards.pop(int(ctx.author.id))
          else:
            await ctx.reply("That spot is already taken!")
  await bot.process_commands(ctx) # process commands again so bot doesnt break

@bot.event
async def on_command_error(ctx, error):
    try:
        if type(error) == discord.ext.commands.errors.CommandNotFound:
            await ctx.send("This command does not exist! Please use `g!help` for a list of avaliable commands.")
        else:
            await ctx.send(error)
    except Exception as err:
        print(err)
        print(str(ctx.guild.name) + """\n""" + str(ctx.guild.id))
        await ctx.author.send("I seem to be missing permissions for this server: `"+ctx.guild.name+"`. Have you enabled \"Administrator\" under GBot's role in Permissions?")
bot.run(token)#run the bot
