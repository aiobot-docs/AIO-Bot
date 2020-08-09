import json

with open('./servers.json') as serverjson:
    servers = json.loads(serverjson.read()) #Read JSON from ./servers.json

async def main(msg):
    words = msg.content.split()