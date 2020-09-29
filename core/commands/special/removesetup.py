description = "Removes setup for the server. Basically a termination command. Only gives you access to Normal Commands"

import json
import discord

async def main(message, args, client, serverdata):
    del args
    if message.author != message.guild.owner:
        embed = discord.Embed(title="Could not setup server.", description="Ask the server owner <@!{}> to run `-removesetup`.\nOnly server owners can use `-removesetup`".format(message.guild.owner_id), color=0xff0000, type="rich")
        embed.set_footer(text="This message deletes in 10 seconds")
        await message.channel.send(embed=embed, delete_after=10)
        await message.delete()
        return
    if str(message.guild.id) not in serverdata:
        embed = discord.Embed(title="Could not remove setup for server.", description="In order to use this command, you must first run `-setup`", color=0xff0000, type="rich")
    #Get Channels
    channel_panel = client.get_channel(int(serverdata[str(message.guild.id)]["channel_panel_ID"]))
    channel_log = client.get_channel(int(serverdata[str(message.guild.id)]["channel_log_ID"]))
    category = client.get_channel(int(serverdata[str(message.guild.id)]["category_ID"]))
    #Delete Channels
    try:
        await channel_panel.delete()
        await channel_log.delete()
        await category.delete()
    except:
        embed = discord.Embed(title="There was an error while removing the channels/categories", description="You can attempt to remove the channels manually.", color=0xff0000, type="rich")
        message.guild.owner.send(embed)
    #Delete From File
    del serverdata[str(message.guild.id)]
    with open('./data.json', 'w') as data:
        serverdata = json.dump(serverdata, data)