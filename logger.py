import discord
import json
import datetime

with open('config.json') as configuration:
    config = json.loads(configuration.read()) #Read JSON from config.json

async def on_message(msg, client):
    #Do not Log Own Messages
    with open('./servers.json') as serverjson:
        servers = json.loads(serverjson.read()) #Read JSON from ./servers.json
    if str(msg.channel.type) == 'private': #Do not Log DMs
        return
    if str(msg.guild.id) not in servers: #Do not Log servers who haven't been setup
        return
    if msg.author == client.user:
        return
    #Get Log Channel
    try:
        channel_ID = servers["{}".format(msg.guild.id)]["log_channel_ID"]
    except KeyError as error:
        print("KeyError for Guild {} | {}".format(msg.guild.id, error))
    try:
        channel = client.get_channel(channel_ID)
    except:
        print("Couldn't get Channel for Guild {}".format(msg.guild.id))
    #Create Embed
    embed = discord.Embed(title="{} sent:".format(msg.author.name), description=msg.content, color=0x00000, type="rich")
    embed.add_field(name="Message sent in:", value="<#{}>".format(msg.channel.id), inline="true")
    embed.add_field(name="Jump to Message:", value="[Click Here]({})".format(msg.jump_url), inline="true")
    embed.set_footer(text=config["footer_msg"], icon_url=client.user.avatar_url)
    await channel.send(embed=embed)

#On Command Use
async def on_command(msg, command, client):
    with open('./servers.json') as serverjson:
        servers = json.loads(serverjson.read()) #Read JSON from ./servers.json
    #Get Log Channel
    try:
        channel_ID = servers["{}".format(msg.guild.id)]["log_channel_ID"]
    except KeyError as error:
        print("KeyError for Guild {} | {}".format(msg.guild.id, error))
    try:
        channel = client.get_channel(channel_ID)
    except:
        print("Couldn't get Channel for Guild {}".format(msg.guild.id))
    embed = discord.Embed(title="`{}{}` was used by {}".format(config["prefix"], command, msg.author.name), color=0x00000, type="rich")
    embed.add_field(name="Command sent in:", value="<#{}>".format(msg.channel.id))
    embed.set_footer(text=config["footer_msg"], icon_url=client.user.avatar_url)
    await channel.send(embed=embed)

#On Member Join
async def on_join(member, client):
    with open('./servers.json') as serverjson:
        servers = json.loads(serverjson.read()) #Read JSON from ./servers.json
    #Get Log Channel
    try:
        channel_ID = servers["{}".format(member.guild.id)]["log_channel_ID"]
    except KeyError as error:
        print("KeyError for Guild {} | {}".format(member.guild.id, error))
    try:
        channel = client.get_channel(channel_ID)
    except:
        print("Couldn't get Channel for Guild {}".format(member.guild.id))
    embed = discord.Embed(title="{} joined the server".format(member.name), color=0x0080ff, type="rich")
    embed.add_field(name="Account Creation:", value=member.created_at.strftime("%m/%d/%Y"), inline="true")
    embed.set_thumbnail(url=member.avatar_url)
    embed.set_footer(text=config["footer_msg"], icon_url=client.user.avatar_url)
    await channel.send(embed=embed)

#On Member Leave
async def on_leave(member, client):
    with open('./servers.json') as serverjson:
        servers = json.loads(serverjson.read()) #Read JSON from ./servers.json
    #Get Log Channel
    try:
        channel_ID = servers["{}".format(member.guild.id)]["log_channel_ID"]
    except KeyError as error:
        print("KeyError for Guild {} | {}".format(member.guild.id, error))
    try:
        channel = client.get_channel(channel_ID)
    except:
        print("Couldn't get Channel for Guild {}".format(member.guild.id))
    embed = discord.Embed(title="{} left the server".format(member.name), color=0x8000ff, type="rich")
    embed.add_field(name="Mention:", value=member.mention, inline="true")
    embed.add_field(name="Joined on:", value=member.joined_at.strftime("%m/%d/%Y"), inline="true")
    tis_str = (member.joined_at - datetime.datetime.now()).days #Time In Server String
    embed.add_field(name="Time in the server:", value="`{}` days".format(tis_str), inline="true")
    embed.set_thumbnail(url=member.avatar_url)
    embed.set_footer(text=config["footer_msg"], icon_url=client.user.avatar_url)
    await channel.send(embed=embed)

#On Message Edit
async def on_msg_edit(before, after, client):
    with open('./servers.json') as serverjson:
        servers = json.loads(serverjson.read()) #Read JSON from ./servers.json
    try:
        channel_ID = servers["{}".format(after.guild.id)]["log_channel_ID"]
    except KeyError as error:
        print("KeyError for Guild {} | {}".format(after.guild.id, error))
    try:
        channel = client.get_channel(channel_ID)
    except:
        print("Couldn't get Channel for Guild {}".format(after.guild.id))
    embed = discord.Embed(title="{} edited a message".format(after.author.name), description="**Original Message:** {}\n**New Message:** {}".format(before.content, after.content), color=0x00000, type="rich")
    embed.set_footer(text=config["footer_msg"], icon_url=client.user.avatar_url)
    await channel.send(embed=embed)

#On Message Delete
async def on_delete(msg, client):
    with open('./servers.json') as serverjson:
        servers = json.loads(serverjson.read()) #Read JSON from ./servers.json
    try:
        channel_ID = servers["{}".format(msg.guild.id)]["log_channel_ID"]
    except KeyError as error:
        print("KeyError for Guild {} | {}".format(msg.guild.id, error))
    try:
        channel = client.get_channel(channel_ID)
    except:
        print("Couldn't get Channel for Guild {}".format(after.guild.id))
    embed = discord.Embed(title="Message sent by {} was deleted".format(msg.author.name), color=0x00000, type="rich")
    embed.add_field(name="Message Content:", value=msg.content, inline="false")
    embed.add_field(name="Message Deleted in:", value="<#{}>".format(msg.channel.id), inline="false")
    embed.set_footer(text=config["footer_msg"], icon_url=client.user.avatar_url)
    await channel.send(embed=embed)
