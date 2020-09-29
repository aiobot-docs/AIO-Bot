description = "The help command"

import discord
import json
from os import listdir

with open('./config.json') as configuration: #Read JSON from config.json
    config = json.loads(configuration.read())

commandlist = listdir('./core/commands')
#Create Dictionary for Words
command_dictionary = {}
for command in commandlist:
    if command.endswith('.py'):
        commandname = str(command.replace(".py",""))
        commanddescription = str(__import__("core.commands.{}".format(commandname), fromlist=[None]).description)
        command_dictionary[commandname] = commanddescription
help_description = "**Normal Commands:**\n" #Create String
for command in command_dictionary:
    help_description = help_description + "`{}{}` ⟶ {}\n".format(config["prefix"], command, command_dictionary[command])

help_description = help_description + "\n**After `-setup` Commands:**\n"

#Special Section
specialcommandlist = listdir("./core/commands/special")
#Create Dictionary for Words
command_dictionary = {}
for command in specialcommandlist:
    if command.endswith('.py'):
        commandname = str(command.replace(".py",""))
        commanddescription = str(__import__("core.commands.special.{}".format(commandname), fromlist=[None]).description)
        command_dictionary[commandname] = commanddescription
for command in command_dictionary:
    help_description = help_description + "`{}{}` ⟶ {}\n".format(config["prefix"], command, command_dictionary[command])

async def main(message, args, client, serverdata):
    del args, client, serverdata
    await message.delete()
    embed = discord.Embed(title="AIO Bot Help", description=help_description, color=0xf1f1f1, type="rich") #Create Embed
    embed.set_footer(text="AIO Bot • This message automatically deletes in 30 seconds", icon_url=config["profileURL"])
    await message.channel.send(embed=embed, delete_after=30)