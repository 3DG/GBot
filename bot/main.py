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
from PIL import Image, ImageFont, ImageDraw, ImageOps
from time import mktime
from discord.ext import commands as cmds
token = "" # discord token
prefix = "g!" # bot prefix
appid = 907439983579758632 # app id
activity = discord.Activity(type=discord.ActivityType.watching, name="you (Prefix: "+prefix+")")
bot = cmds.Bot(command_prefix=prefix,activity=activity,help_command=None) # make a bot with no help command with prefix as the prefix for all commands
versionnum = 0.8 # version number
revision = 0 # revision number
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

#invert command
@bot.command()
async def invert(ctx):
  if len(ctx.message.attachments) >= 1: # if 1 image is attached
    url = ctx.message.attachments[0].url # blah blah blah im tired of making these comemnts i shouldve made them as i went instead of adding them after
    if url.endswith(".png") or url.endswith(".jpg") or url.endswith(".gif"):
      imgdata = requests.get(url)
      img = Image.open(toimg(imgdata.content))
      fileName = randomStr(24)
      img = img.convert("RGBA")
      wid, hgt = img.size
      imgmix = Image.new("RGBA", (wid,hgt), (255, 255, 255, 255))
      pixel = 0
      for y in range(hgt):
        for x in range(wid):
          pixel = img.getpixel((x,y))
          imgmix.putpixel((x, y), (255-pixel[0], 255-pixel[1], 255-pixel[2], pixel[3]))
      imgmix.save("./temp/img/"+fileName+"invert.png") # save to use
      file = open("./temp/img/"+fileName+"invert.png", "rb", buffering = 0) #open file
      await ctx.send("Here is your image!", file=discord.File(file, filename="convertedimage.png")) #vague comment #274
      file.close() # close file to prevent memory leak
      os.remove("./temp/img/"+fileName+"invert.png") # remove file
    else:
      await ctx.send("Your image must be a PNG, JPG, or GIF image.")
  else:
    await ctx.send("This command requires an image!")

#horiz flip command
@bot.command()
async def flip(ctx):
  if len(ctx.message.attachments) >= 1: # if 1 image is attached
    url = ctx.message.attachments[0].url # blah blah blah im tired of making these comemnts i shouldve made them as i went instead of adding them after
    if url.endswith(".png") or url.endswith(".jpg") or url.endswith(".gif"):
      imgdata = requests.get(url)
      img = Image.open(toimg(imgdata.content))
      fileName = randomStr(24)
      img = img.convert("RGBA")
      wid, hgt = img.size
      imgmix = Image.new("RGBA", (wid,hgt), (255, 255, 255, 255))
      pixel = 0
      for y in range(hgt):
        for x in range(wid):
          pixel = img.getpixel((x,y))
          imgmix.putpixel((wid-x-1, y), (pixel[0], pixel[1], pixel[2], pixel[3]))
      imgmix.save("./temp/img/"+fileName+"flipped.png") # save to use
      file = open("./temp/img/"+fileName+"flipped.png", "rb", buffering = 0) #open file
      await ctx.send("Here is your image!", file=discord.File(file, filename="convertedimage.png")) #vague comment #274
      file.close() # close file to prevent memory leak
      os.remove("./temp/img/"+fileName+"flipped.png") # remove file
    else:
      await ctx.send("Your image must be a PNG, JPG, or GIF image.")
  else:
    await ctx.send("This command requires an image!")
#vert flip command
@bot.command()
async def flipvert(ctx):
  if len(ctx.message.attachments) >= 1: # if 1 image is attached
    url = ctx.message.attachments[0].url # blah blah blah im tired of making these comemnts i shouldve made them as i went instead of adding them after
    if url.endswith(".png") or url.endswith(".jpg") or url.endswith(".gif"):
      imgdata = requests.get(url)
      img = Image.open(toimg(imgdata.content))
      fileName = randomStr(24)
      img = img.convert("RGBA")
      wid, hgt = img.size
      imgmix = Image.new("RGBA", (wid,hgt), (255, 255, 255, 255))
      pixel = 0
      for y in range(hgt):
        for x in range(wid):
          pixel = img.getpixel((x,y))
          imgmix.putpixel((x, hgt-y-1), (pixel[0], pixel[1], pixel[2], pixel[3]))
      imgmix.save("./temp/img/"+fileName+"vflipped.png") # save to use
      file = open("./temp/img/"+fileName+"vflipped.png", "rb", buffering = 0) #open file
      await ctx.send("Here is your image!", file=discord.File(file, filename="convertedimage.png")) #vague comment #274
      file.close() # close file to prevent memory leak
      os.remove("./temp/img/"+fileName+"vflipped.png") # remove file
    else:
      await ctx.send("Your image must be a PNG, JPG, or GIF image.")
  else:
    await ctx.send("This command requires an image!")

  
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
      print(cmd)
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
          await ctx.send("Error! (Mismatched parenthesis!)");
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
  code = msg[(len(prefix)+5):(len(msg)+1)]
  embed = discord.Embed(title="Lorem Ipsum", color=discord.Color(16777215))
  if ctx.author.id == 353911350545612801:
    try:
      output = await eval(code)
      embed.color = discord.Color(196607)
      embed.add_field(name="Input:", value="""```py\n"""+code+"```")
      embed.add_field(name="Output:", value="```"+output+"```")
      embed.title = "Code ran fine!"
      await ctx.send(embed=embed)
    except Exception as error:
      embed.title = "Error!"
      embed.color = discord.Color(8388608)
      embed.add_field(name="Error:", value="""```diff\n- """+str(error)+"```")
      await ctx.send(embed=embed)
  else:
    await ctx.send("Only the bot developer can run this command!")
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
    if url.endswith(".png") or url.endswith(".jpg") or url.endswith(".gif"):
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
    else:
      await ctx.send("Your image must be a PNG, JPG, or GIF image.")
  else:
    await ctx.send("This command requires 2 images!")
@bot.command()
async def avatar(ctx):
  try:
    idtoget = ctx.message.content.split("@")[1].split(">")[0].split("!")[1]
    user = await ctx.message.guild.fetch_member(idtoget)
    print(idtoget)
    print(user)
    avatar = "https://cdn.discordapp.com/avatars/"+idtoget+"/"+str(user.avatar)+".webp?size=256" # get user avatar url in 256p
    avatarpic = requests.get(avatar)
    Image.open(toimg(avatarpic.content)).convert("RGBA").save("./temp/img/"+idtoget+".png")
    file = open("./temp/img/"+idtoget+".png", "rb", buffering = 0)
    await ctx.send(user.name+"'s avatar!", file=discord.File(file, filename="avatar.png"))
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
commandnames = ["avatar","color","pixel","echo","caption","info","jpegify","help","lightdark","ping","eval","invert","flip","flipvert","duck","brainfrick"]
helpdef = {"avatar":"Gets a user's avatar. (Arguments: {User (mention)})",
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
  "invert":"Requires an image. Inverts an image.",
  "flip":"Requires an image. Flips an image horizontally.",
  "flipvert":"Requires an image. Flips an image vertically.",   
  "duck":"A Hello world Duck interpreter (Arguments: {Code})",
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
  for cmd in range((page-1)*10, min(cmds, (page*10))): # for each command
    send += "`g!"+str(commandnames[cmd])+"`" + " - " + str(helpdef.get(str(commandnames[cmd])))+'''\n''' # add it in send string
  embed.add_field(name="Page "+str(page), value=send) # add the send string to the embed
  embed.set_footer(text="Send g!help "+str(page+1)+" for the next page")
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
  filterchannelid = 0 # paste your filter channel id here
  if ctx.channel.id == filterchannelid and ctx.author.bot == False: # if message is in filter channel and author isnt a bot (to prevent webhook spam)
    url = "" #put your filter webhook url here
    avatar = "https://cdn.discordapp.com/avatars/"+str(ctx.author.id)+"/"+str(ctx.author.avatar)+".webp?size=256" # get user avatar url in 256p
    data = {"username":ctx.author.name,"avatar_url":avatar,"content":filter(ctx.content),"embeds":None} # data to send to the webhook
    response = req.post(url, data=data) # send it to the webhook
    await ctx.delete() # delete the message
  if ctx.channel.id == 0: # guilded discord chat
    url = "" #put your guilded webhook url here
    avatar = "https://cdn.discordapp.com/avatars/"+str(ctx.author.id)+"/"+str(ctx.author.avatar)+".webp?size=256" # get user avatar url in 256p
    data = {"username":ctx.author.name,"avatar_url":avatar,"content":ctx.author.name + ": " +ctx.content,"attachments":ctx.attachments,"embeds":None} # data to send to the webhook
    response = req.post(url, data=data) # send it to the webhook
  await bot.process_commands(ctx) # process commands again so bot doesnt break
bot.run(token)#run the bot
