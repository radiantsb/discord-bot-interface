import PIL.ImageGrab
import PIL.Image
import discord
import asyncio
import PIL
import io
import json
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
bot = discord.Bot(intents=intents)
config = json.load(open("config.json"))
token = config['token']
shortcuts = config['shortcuts']
images = {}
lastCommand = []
def dictOrInput(dict,input):
    if input in dict:
        return dict[input]
    return int(input)
async def processCommand(command):
    global lastCommand
    match command[0]:
        case "send":
            c = bot.get_channel(dictOrInput(shortcuts,command[1]))
            await c.send(" ".join(command[2:]))
            lastCommand = command[0:2]
        case "reply":
            c = bot.get_channel(dictOrInput(shortcuts,command[1]))
            m = await c.fetch_message(int(command[2]))
            await m.reply(" ".join(command[3:]))
            lastCommand = command[0:3]
        case "dm":
            user = await bot.get_or_fetch_user(dictOrInput(shortcuts,command[1]))
            await user.send(" ".join(command[2:]))
            lastCommand = command[0:2]
        case "read":
            user = await bot.get_or_fetch_user(dictOrInput(shortcuts,command[1]))
            channel = await user.create_dm()
            messages = [message async for message in channel.history(limit=100, oldest_first=False)]
            for x in messages[::-1]:
                print(f"[{x.created_at}] {x.author}: {x.content}")
            lastCommand = command[0:1]
        case "delete":
            channel = await bot.fetch_channel(dictOrInput(shortcuts, command[1]))
            message = await channel.fetch_message(int(command[2]))
            await message.delete()
            lastCommand = command[0:2]
        case "edit":
            channel = await bot.fetch_channel(dictOrInput(shortcuts, command[1]))
            message = await channel.fetch_message(int(command[2]))
            await message.edit(" ".join(command[3:]))
            lastCommand = command[0:3]
        case "image":
            result = PIL.ImageGrab.grabclipboard()
            if isinstance(result, PIL.Image.Image):
                img = result
            elif isinstance(result, list) and all(isinstance(path, str) for path in result):
                img = PIL.Image.open(result[0])
            else:
                print("image not found")
                return
            with io.BytesIO() as imgBytes:
                img.save(imgBytes, format="PNG")
                images[command[1]] = imgBytes.getvalue()
            lastCommand = command[0]
        case "send+":
            c = bot.get_channel(dictOrInput(shortcuts, command[1]))
            image_bytes = images[command[2]]
            await c.send(
                content=" ".join(command[3:]),
                file=discord.File(io.BytesIO(image_bytes), filename=f"{command[2]}.png"))
            lastCommand = command[0:3]
        case "reply+":
            c = bot.get_channel(dictOrInput(shortcuts, command[1]))
            m = await c.fetch_message(int(command[2]))
            image_bytes = images[command[3]]
            await m.reply(
                content=" ".join(command[4:]),
                file=discord.File(io.BytesIO(image_bytes), filename=f"{command[3]}.png")
            )
            lastCommand = command[0:4]
        case "dm+":
            user = await bot.get_or_fetch_user(dictOrInput(shortcuts, command[1]))
            image_bytes = images[command[2]]
            await user.send(
                content=" ".join(command[3:]),
                file=discord.File(io.BytesIO(image_bytes), filename=f"{command[2]}.png"))
            lastCommand = command[0:3]
        case "help":
            print("""commands:
            help - show this
            dm [userid] [message] - send a dm to a user
            read [userid] print dm history with a user
            send [channelid] [message] - send a message to a channel
            reply [channelid] [messageid] [message] reply to a message
            delete [channelid] [messageid] - delete a message
            edit [channelid] [messageid] [message] - edit a message
            image [name] save the image in your clipboard with a name
            dm+ [userid] [image] [message] - dm a user, including an image
            reply+ [channelid] [messageid] [image] [message] - reply to a message, including an image
            send+ [channelid] [image] [message] - send a message to a channel, including an image

            tips:
            config.json allows you to specify shortcuts for channel ids and user ids
            your most recent command is saved, typing an invalid command will reuse it with a new last argument
            eg.
            send [channel] message1
            message2
            """)
        case _:
            if command!=lastCommand:
                lastCommand.append(" ".join(command[0:]))
                await processCommand(lastCommand)


async def cmdLoop():
    while True:
        command = input(">> ").split(" ")
        await processCommand(command)
        
@bot.event
async def on_ready():
    print(f"logged in as {bot.user}\ntype help for a list of commands")
    await cmdLoop()
bot.run(token)
