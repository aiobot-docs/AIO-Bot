import os
import discord
import json

descrip = "Displays all the commands you can use"

client = discord.Client()

#Read Config
with open('config.json') as configuration:
    config = json.loads(configuration.read()) #Read JSON from config.json

commands_ext = os.listdir('commands') #Gets all the commands (With.py)
help_dictionary = {}
commands_list = [] #Create Empty Array for those without .py
for commands in commands_ext:
    if commands.endswith('.py'):
        command_no_ext = commands.replace(".py","")
        commands_list.append(command_no_ext) #Add command to list

        help_dictionary[command_no_ext] = __import__('commands.{}'.format(command_no_ext), fromlist=[None]).descrip #Add Command + Descrip to dictionary

number_of_commands = len(commands_list)

#Formatting help_dictionary
help_str = ""
for commands in commands_list:
    descrip = help_dictionary.get(commands)
    help_str = "{}\n `{}{}` - {}".format(help_str, config["prefix"], commands, descrip)

async def main(msg, args):
    embed = discord.Embed(title="Help", color=0x00000, type="rich")
    embed.add_field(name="Number of Commands", value="{} Commands".format(number_of_commands), inline="true")
    embed.add_field(name="Invite", value="[Click Here](https://discord.com/api/oauth2/authorize?client_id=636359594301456394&permissions=0&scope=bot)", inline="true")
    embed.add_field(name="Commands", value=help_str, inline="false")
    await msg.channel.send(embed=embed)
