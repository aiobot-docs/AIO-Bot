import asyncio
import discord

descrip = "About AIO Bot"


client = discord.Client()
#Custom Variables

async def main(msg, args):
    embed = discord.Embed(title="About AIO Bot", color=0x00000, type="rich")
    embed.add_field(name="About AIO Bot", value="AIO Bot is going to be the only bot you would need in a server. From Moderation to giveaway functions, AIO Bot can do them all.\n", inline="false")
    embed.add_field(name="How to Initialize Setup", value="Run `-setup`. Use `-help` to find advanced commands", inline="false")
    embed.add_field(name="Invite this bot to your server!", value="[Click Here](https://discord.com/api/oauth2/authorize?client_id=636359594301456394&permissions=0&scope=bot)", inline="true")
    embed.add_field(name="Patreon", value="[Click Here](https://www.patreon.com/AIOBot)", inline="true")
    await msg.channel.send(embed=embed)
