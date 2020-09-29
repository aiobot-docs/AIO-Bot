from os import listdir
import core.log as log

async def main(message, client, serverdata):
    #Part 1
    commandfiles = listdir("./core/commands")
    commandList = []
    #Check if Command is a file
    for commands in commandfiles:
        if commands.endswith('.py'):
            commandList.append(commands.replace(".py", ""))
    #Get Variables
    messageContentList = message.content.split()
    command = messageContentList.pop(0).replace("-","").lower()
    args = messageContentList
    #Execute Command
    if command in commandList:
        commandexecute = __import__('core.commands.{}'.format(command), fromlist=[None])
        await commandexecute.main(message, args, client, serverdata)
        await log.command.main(message, serverdata)
    else:
        if str(message.guild.id) in serverdata:
            commandfiles = listdir("./core/commands/special")
            commandList = []
            #Check if Command is a file
            for commands in commandfiles:
                if commands.endswith('.py'):
                    commandList.append(commands.replace(".py", ""))
            #Get Variables
            messageContentList = message.content.split()
            command = messageContentList.pop(0).replace("-","").lower()
            args = messageContentList
            #Execute Command
            if command not in commandList:
                return
            commandexecute = __import__('core.commands.special.{}'.format(command), fromlist=[None])
            await commandexecute.main(message, args, client, serverdata)
            await log.command.main(message, serverdata)