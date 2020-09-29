from datetime import datetime

async def main(message, serverdata):
    messageContentList = message.content.split()
    command = messageContentList.pop(0).replace("-","").lower()
    print("{} [COMMAND USAGE] -{} was used.".format(datetime.now(), command))