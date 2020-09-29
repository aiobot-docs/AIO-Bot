description = "Restart's setup. Will require you to agree to ToS again."

import discord
import core.commands.setup as setup
import core.commands.special.removesetup as removesetup
import time

async def main(message, args, client, serverdata):
    if message.author != message.guild.owner:
        embed = discord.Embed(title="Could not reset server.", description="Ask the server owner <@!{}> to run `-removesetup`.\nOnly server owners can use `-removesetup`".format(message.guild.owner_id), color=0xff0000, type="rich")
        embed.set_footer(text="This message deletes in 10 seconds")
        await message.channel.send(embed=embed, delete_after=10)
        await message.delete()
        return
    embed = discord.Embed(title="Resetting Server", description="This will take some time if the bot is under heavy load.", color=0xf1f1f1, type="rich")
    setup_confirm_message = await message.author.send(embed=embed)
    if str(message.guild.id) in serverdata:
        await removesetup.main(message, args, client, serverdata)
        time.sleep(1)
    await setup.main(message, args, client, serverdata)
    embed = discord.Embed(title="Reset Success", color=0xf1f1f1, type="rich")
    await setup_confirm_message.edit(embed=embed)