import discord
import time
from datetime import datetime
import json
import colors

with open('./config.json') as configuration: #Read JSON from config.json
    config = json.loads(configuration.read())

async def main(client, serverdata):
    embed = discord.Embed(title="Patch {}".format(config["version"]), description="AIO Bot has successfully been patched. Check [@AIOSmartBot](https://twitter.com/AIOSmartBot) for patchnotes.", color=0x00FF00, type="rich")
    time_est = len(serverdata)*0.5
    print(colors.OKBLUE +  "{} ETA for messages to send: ~{} seconds".format(datetime.now(), time_est) + colors.ENDC)
    for key in serverdata:
        channel = client.get_channel(int(serverdata[key]["channel_log_ID"])) #Get Channel
        await channel.send(embed=embed)
        time.sleep(0.5)