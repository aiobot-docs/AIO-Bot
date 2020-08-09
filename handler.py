from os import listdir
import sys
import logger

async def commandhandler(command, msg, args):
    commandfiles = listdir("./commands")
    #Get List of Commands
    commandlist = []
    for commands in commandfiles:
        if commands.endswith('.py'):
            commandlist.append(commands.replace(".py",""))
    if command in commandlist:
        handle = __import__('commands.{}'.format(command), fromlist=[None])
        await handle.main(msg, args)