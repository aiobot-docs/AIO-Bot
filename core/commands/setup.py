description = "Setup Server"

import json
import discord
import asyncio

async def main(message, args, client, serverdata):
    del args
    guild =  message.guild
    if message.author != message.guild.owner: #Check that user of command was server owner (security reasons)
        embed = discord.Embed(title="Could not setup server.", description="Ask the server owner <@!{}> to run `-setup`.\nOnly server owners can use `-setup`".format(message.guild.owner_id), color=0xff0000, type="rich")
        embed.set_footer(text="This message deletes in 10 seconds.")
        await message.channel.send(embed=embed, delete_after=10)
        await message.delete()
        return
    if str(message.guild.id) in serverdata:
        embed = discord.Embed(title="There was an error setting up the server", description="This server has already been setup", color=0xff0000, type="rich")
        await message.channel.send(embed=embed)
        return
    
    #TOS GATE
    embed = discord.Embed(title="Terms of Service:", description="Setting up AIO Bot requires you to agree to the Terms of Service (provided by Google). By using AIO Bot, you agree to [GOOGLE'S API TERMS OF SERVICE](https://developers.google.com/terms) and [GOOGLE'S TERMS OF SERVICE](https://policies.google.com/privacy)\n\nOnce you react with ✅, you agree that you have fully read and understood [GOOGLE'S API TERMS OF SERVICE](https://developers.google.com/terms) and [GOOGLE'S TERMS OF SERVICE](https://policies.google.com/privacy)")
    embed.set_footer(text="This message automaticly deletes in 5 minutes")
    sent_embed = await message.channel.send(embed=embed)
    await sent_embed.add_reaction('✅')
    #Await Reaction For TOS Acception
    def check(reaction, user):
        return user == message.author and str(reaction.emoji) == '✅'
    try:
        reaction, user = await client.wait_for('reaction_add', timeout=300.0, check=check)
    except asyncio.TimeoutError:
        await sent_embed.delete()
    else: #Once ToS is accepted
        overwrites = { #Create Private Variable (for permissions)
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            guild.me: discord.PermissionOverwrite(read_messages=True)
        }
        #Create Channels
        try:
            category = await guild.create_category("AIO Bot", overwrites=overwrites, reason="AIO Bot setup was used by {}".format(message.author.name))
            panel = await guild.create_text_channel("main-panel", overwrites=overwrites, reason="AIO Bot setup was used by {}".format(message.author.name), topic="Do not DELETE. To grant permissions to staff, give permission to the staff to read/send messages in this channel", category=category)
            log_channel = await guild.create_text_channel("log-channel", overwrites=overwrites, reason="AIO Bot setup was used by {}".format(message.author.name), category=category)
            #Send Messages
            embed = discord.Embed(title="AIO Bot Panel", color=0xf1f1f1, type="rich")
            embed.add_field(name="Logging:", value="Status: `ENABLED`\nReact with 🇱 to view/config.", inline="false")
            embed.add_field(name="Anti Modules:", value="Status: `DISABLED`\nReact with 🅰️ to view/config.", inline="false")
            embed.add_field(name="Authorized Roles", value="Currently `0` roles are authorized.\nReact with 🇷 to view/config.", inline="false")
            embed.add_field(name="Miscellaneous", value="React with 🇲 to view/config.", inline="false")
            message_panel = await panel.send(embed=embed)
            #React to Message
        except discord.Forbidden: #If insuffecient permissions
            embed = discord.Embed(title="Permissions Insufficient", description="Error Code: `Forbidden`\nMake sure AIO Bot has the proper permissions to create channels.", color=0xf1f1f1, type="rich")
            await message.channel.send(embed=embed)
            return
        #Put in JSON Data
        with open("./data.json", "r+") as file:
            append = {
                "{}".format(guild.id): {
                    "message_panel_ID": "{}".format(message_panel.id),
                    "channel_log_ID": "{}".format(log_channel.id),
                    "channel_panel_ID": "{}".format(panel.id),
                    "category_ID": "{}".format(category.id),
                    "server_config": {
                        "logging": {
                            "enabled": "true",
                            "on_message": "true",
                            "message_score_reports": "true",
                            "on_command": "true",
                            "on_edit": "true",
                            "on_moderation": "true",
                            "on_server_config": "true",
                            "on_server_join": "true",
                            "on_server_leave": "true"
                        },
                        "modules": {
                            "anti_toxicity": ["false", 0.8],
                            "anti_sexual": ["false", 0.8],
                            "anti_profanity": ["false", 0.8],
                            "anti_flirt": ["false", 0.8],
                            "anti_threats": ["false", 0.8],
                            "anti_nuke": "false"
                        }
                    }
                }
            }
            data = json.load(file)
            data.update(append)
            file.seek(0)
            json.dump(data, file, indent=4)
        embed = discord.Embed(title="Setup Success.", color=0xf1f1f1, type="rich")
        await sent_embed.edit(embed=embed)
    
    