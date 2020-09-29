import discord

#Python Libraries
import json
import datetime

#Local Files
import core
import colors

client = discord.Client()

with open('config.json') as configuration: #Read JSON from config.json
    config = json.loads(configuration.read())

#Discord

@client.event #On Ready Event
async def on_ready():
    print(colors.HEADER + "{} {} has successfully logged into Discord".format(datetime.datetime.now(), client.user) + colors.ENDC) #Conformation
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=config["presence"])) #Set Presence
    #Announce Patch
    with open('./data.json', 'r') as data: #Get Serverdata
        serverdata = json.loads(data.read()) 
    await core.patch.main(client, serverdata)

@client.event
async def on_message(message): #On Message
    with open('./data.json', 'r') as data: #Get Serverdata
        serverdata = json.loads(data.read()) 
    await core.message_handler.main(message, client, config, serverdata)

client.run(config["token"])