from datetime import datetime
import discord
import time
import json
import requests

descrip = "Displays the latency"

with open('config.json') as configuration:
    config = json.loads(configuration.read()) #Read JSON from config.json

async def main(msg, args):
    del args #No need for args
    startlatency = datetime.now() #Get Latency Field 1
    embed = discord.Embed(title="Calculating Latency...", color=0x00000, type="rich")
    sent_message = await msg.channel.send(embed=embed)
    total_latency = (datetime.now() - startlatency).total_seconds()*1000
    one_way = total_latency/2
    time.sleep(1)
    #Server Status Determinator
    emoji_str = ""
    if total_latency < 230:
        emoji_str = "✅ Good"
    elif total_latency >= 230 and total_latency < 300:
        emoji_str = "⚠️ Latency is High"
        embed.set_footer
    elif total_latency <= 300:
        emoji_str = "⛔ Latency is Extremely High"
    display_api_status = requests.get("https://srhpyqt94yxb.statuspage.io/api/v2/status.json").json()["status"]["description"]
    discord_api_url = requests.get("https://srhpyqt94yxb.statuspage.io/api/v2/status.json").json()["page"]["url"]
    #Add Fields
    embed = discord.Embed(title="Latency", color=0x00000, type="rich")
    embed.add_field(name="Total Latency:", value="`{}ms`".format(total_latency), inline="true")
    embed.add_field(name="One Way Latency:", value="`{}ms`".format(one_way), inline="true")
    embed.add_field(name="Latency Status", value=emoji_str, inline="true")
    embed.add_field(name="Discord Status", value=f"{display_api_status}, [Click Here to View]({discord_api_url})", inline="true")
    await sent_message.edit(embed=embed)
