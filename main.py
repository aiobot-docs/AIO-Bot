import discord
import json
import handler
import commands
import logger
#Events

client = discord.Client()

with open('config.json') as configuration:
    config = json.loads(configuration.read()) #Read JSON from config.json

@client.event
async def on_ready():
    print(f"{client.user} logged into Discord")
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=config["presence"]))
@client.event #On Message | Includes Commands
async def on_message(message):
    #Commands
    if message.content.startswith(config["prefix"]): #Command Detection
        messageContent = message.content.split() #Make Content into Array
        command = messageContent.pop(0).replace("-","").lower() #Seperate Command from Message Content
        args = messageContent #Get Command Arguments (If Any)
        await handler.commandhandler(command, message, args) #Send Command + Args to Handler
        await logger.on_command(message, command, client) #Log Command
        return
    #Log Messages (Not Commands)
    await logger.on_message(message, client)

#Events
@client.event #On Join
async def on_member_join(member):
    with open('./servers.json') as serverjson:
        servers = json.loads(serverjson.read()) #Read JSON from ./servers.json
    if str(member.guild.id) not in servers: #Do not Log servers who haven't been setup
        return
    #Logging
    if servers["{}".format(member.guild.id)]["configuration"]["logging"]["on_join"] == "false": #If Server Doesn't want to be logged
        return
    await logger.on_join(member, client) #Send to Logger
@client.event #On Leave
async def on_member_remove(member):
    with open('./servers.json') as serverjson:
        servers = json.loads(serverjson.read()) #Read JSON from ./servers.json
    if str(member.guild.id) not in servers: #Do not Log servers who haven't been setup
        return
    if servers["{}".format(member.guild.id)]["configuration"]["logging"]["on_leave"] == "false": #If Server Doesn't want to be logged
        return
    await logger.on_leave(member, client) #Send to Logger
@client.event #On Message Edit
async def on_message_edit(before, after):
    if after.author == client.user:
        return
    with open('./servers.json') as serverjson:
        servers = json.loads(serverjson.read()) #Read JSON from ./servers.json
    if str(after.guild.id) not in servers: #Do not Log servers who haven't been setup
        return
    if servers["{}".format(after.guild.id)]["configuration"]["logging"]["on_message_edit"] == "false": #If Server Doesn't want to be logged
        return
    await logger.on_msg_edit(before, after, client) #Send to Logger
@client.event #On Message Delete
async def on_message_delete(message):
    if message.author == client.user:
        return
    with open('./servers.json') as serverjson:
        servers = json.loads(serverjson.read()) #Read JSON from ./servers.json
    if str(message.guild.id) not in servers: #Do not Log servers who haven't been setup
        return
    if servers["{}".format(message.guild.id)]["configuration"]["logging"]["on_message_delete"] == "false": #If Server Doesn't want to be logged
        return
    await logger.on_delete(message, client)
@client.event #On Channel Create
async def on_guild_channel_create(channel):

@client.event #On Channel Update
async def on_guild_channel_update(before, after):

@client.event #On Channel Delete
async def on_guild_channel_delete(channel):

client.run(config["token"])