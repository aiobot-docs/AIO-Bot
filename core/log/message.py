from datetime import datetime

async def main(message, serverdata):
    print("{} Message sent in {}({}). Sent from {} Content: \"{}\"".format(datetime.now(), message.guild.name, message.guild.id, message.author.name, message.content))