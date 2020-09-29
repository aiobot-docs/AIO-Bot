description = "View and configure logging settings"

import discord
import asyncio

async def main(message, args, client, serverdata):
    del args
    if str(message.channel.id) == serverdata[str(message.guild.id)]["channel_panel_ID"]:
        channel = message.channel
    else:
        channel = client.get_channel(int(serverdata[str(message.guild.id)]["channel_panel_ID"]))
    
    embed = discord.Embed(title="Logging Configuration", description="Current Configuration. React with 🛠️ to edit configuration. React with ❌ to close." ,color=0xf1f1f1, type="rich")
    logging = serverdata[str(message.guild.id)]["server_config"]["logging"]
    for key in logging:
        embed.add_field(name="{}:".format(key.replace("_"," ").capitalize()), value="{}\n[Learn More Here](https://aiobot-docs.github.io/AIO-Bot/logging#{})".format(logging[key].upper(), key), inline="true")
    embed.set_footer(text="This message autocloses")
    sent_message = await channel.send(embed=embed)
    await sent_message.add_reaction('🛠️')
    await sent_message.add_reaction('❌')
    def check(reaction, user):
        return user == message.author and str(reaction.emoji) in ['🛠️','❌']
    try:
        reaction, user = await client.wait_for('reaction_add', timeout=300.0, check=check)
    except asyncio.TimeoutError:
        await sent_message.delete()
    else:
        print(reaction)