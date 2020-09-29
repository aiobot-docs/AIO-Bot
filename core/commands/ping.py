description = "Shows Bot Ping"

import json
from discord import Embed
from datetime import datetime

with open('./config.json') as configuration: #Read JSON from config.json
    config = json.loads(configuration.read())

async def main(message, args, client, serverdata):
    del args, serverdata
    await message.delete()
    start_time = datetime.now()
    embed = Embed(title="AIO Bot Ping", color=0xf1f1f1, type="rich")
    embed.add_field(name="API Latency", value="`Calculating...`", inline="true")
    embed.add_field(name="Server Latency", value="`Calculating...`", inline="true")
    embed.add_field(name="Total Latency", value="`Calculating...`", inline="true")
    previous_embed = await message.channel.send(embed=embed)
    # Create Edited Embbed
    server_latency = round((datetime.now() - start_time).total_seconds()*1000)
    api_latency = round(client.latency*1000)
    edited_embed = Embed(title="AIO Bot Ping", color=0xf1f1f1, type="rich")
    edited_embed.add_field(name='API Latency:', value="`{}ms`".format(api_latency), inline="true")
    edited_embed.add_field(name="Server Latency", value="`{}ms`".format(server_latency - api_latency), inline="true")
    edited_embed.add_field(name="Total Latency", value="`{}ms`".format(server_latency), inline="true")
    edited_embed.set_footer(text="AIO Bot • This message automatically deletes in 30 seconds", icon_url=config["profileURL"])
    await previous_embed.edit(embed=edited_embed, delete_after=30)