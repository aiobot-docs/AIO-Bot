import json
import os
import discord
import requests
import json
from datetime import datetime
import core.log as log
import colors

async def main(message, client, config, serverdata):
    if message.content.startswith(config["prefix"]):
        command_handler = __import__("core.command_handler", fromlist=[None])
        await command_handler.main(message, client, serverdata)
    #Prevent possible recursion
    if client.user == message.author:
        return
    #Log Message
    await log.message.main(message, serverdata)
    #Anti Check
    if str(message.guild.id) not in serverdata:
        print(colors.OKGREEN + '{} {}({}) not in data. Skipping Module Proccessing.'.format(datetime.now(), message.guild.name, message.guild.id) + colors.ENDC)
        return
    request_data = {
            'comment': {'text': message.content},
            'languages': ['en'],
            'requestedAttributes': {'TOXICITY': {}, 'SEXUALLY_EXPLICIT': {}, 'PROFANITY': {}, "FLIRTATION": {}, "THREAT": {}, "INSULT": {}}
        }
    try:
        response = requests.post("https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={}".format(config["google-api-key"]), data=json.dumps(request_data)).json()
        attributescores = response['attributeScores']
    except:
        pass
    embed = discord.Embed(title="Message Score Report:", description="Message sent by <@!{}>.".format(message.author.id))
    embed.add_field(name="Message Content:", value=message.content, inline="false")
    attribute_search = ["TOXICITY", "PROFANITY", "THREAT", "INSULT", "SEXUALLY_EXPLICIT", "FLIRTATION"]
    
    for attribute in attribute_search:
        if float(attributescores[attribute]["summaryScore"]["value"]) > 0.7:
            sentence_string = "❌ {} Detected | Score: `{}%`".format(attribute.capitalize(), round(attributescores[attribute]["summaryScore"]["value"]*100))
            embed.add_field(name="{}".format(attribute.capitalize()), value=sentence_string, inline="true")
        else:
            sentence_string = "✅ No {} Detected | Score `{}%`".format(attribute.lower(), round(attributescores[attribute]["summaryScore"]["value"]*100))
            embed.add_field(name="{}".format(attribute.capitalize()), value=sentence_string, inline="true")
    await message.channel.send(embed=embed)
