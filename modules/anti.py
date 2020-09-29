import requests
import json
import discord

async def main(message, config, serverdata):
    if message.guild.id in serverdata:
        print('{} not in data. Skipping ANTI Check.'.format(message.guild.name))
        return
    request_data = {
            'comment': {'text': message.content},
            'languages': ['en'],
            'requestedAttributes': {'TOXICITY': {}, 'SEXUALLY_EXPLICIT': {}, 'PROFANITY': {}, "FLIRTATION": {}, "THREAT": {}}
        }
    try:
        response = requests.post("https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={}".format(config["google-api-key"]), data=json.dumps(request_data)).json()
        attributescores = response['attributeScores']
    except:
        pass
    embed = discord.Embed(title="Message Score Report:", description="Message sent by <@!{}>.".format(message.author.id))
    embed.add_field(name="Message Content:", value=message.content, inline="false")
    attribute_search = ["TOXICITY", "PROFANITY", "THREAT", "SEXUALLY_EXPLICIT", "FLIRTATION"]
    for attribute in attribute_search:
        if float(attributescores[attribute]["summaryScore"]["value"]) > 0.7:
            sentence_string = "❌ {} Detected | Score: `{}%`".format(attribute.capitalize(), round(attributescores[attribute]["summaryScore"]["value"]*100))
            embed.add_field(name="{}".format(attribute.capitalize()), value=sentence_string, inline="true")
        else:
            sentence_string = "✅ No {} Detected | Score `{}%`".format(attribute.lower(), round(attributescores[attribute]["summaryScore"]["value"]*100))
            embed.add_field(name="{}".format(attribute.capitalize()), value=sentence_string, inline="true")
    await message.channel.send(embed=embed)