import json
import discord

descrip = "Initialize the setup proccess for the bot."

async def main(msg, args):
    with open('./servers.json') as serverjson:
        servers = json.loads(serverjson.read()) #Read JSON from ./servers.json
    if str(msg.guild.id) in servers:
        embed = discord.Embed(title="⚠️ Command Failed to Execute", description="Reason: `This command has been used already in the server`", color=0xff0000)
        await msg.channel.send(embed=embed)
        return
    #Permissions for Channels
    permissions = {msg.guild.default_role: discord.PermissionOverwrite(read_messages=False), msg.guild.me: discord.PermissionOverwrite(read_messages=True)}
    #Create Channels
    try:
        setup_category = await msg.guild.create_category_channel("AIO Bot", reason="AIO Bot Setup", overwrites=permissions)
        mainpanel = await msg.guild.create_text_channel("main-panel", category=setup_category, topic="AIO Main Panel | DO NOT DELETE", reason="AIO Bot Setup")
        log_channel = await msg.guild.create_text_channel("log-channel", category=setup_category, topic="Logs Actions in this server | DO NOT DELETE", reason="AIO Bot Setup")
        warning_channel = await msg.guild.create_text_channel("moderation-log", category=setup_category, topic="Logs Actions in this server | DO NOT DELETE", reason="AIO Bot Setup")
    except discord.Forbidden: #Failed because denied Permissions
        await msg.channel.send("I don't have the proper permissions to create Categorys/Channels.")
    #Send Panel
    try:
        mainpanel_embed = discord.Embed(title="Staff Panel", description="Configure this bot to your server needs", color=0xf9f9f9, type="rich")
        mainpanel_embed.add_field(name="Moderation Word Filter:", value="❌ `Disabled`.\nReact with 1️⃣ to open Configuration", inline="true")
        mainpanel_embed.add_field(name="Welcome Messages:", value="❌ `Disabled`.\nReact with 2️⃣ to open Configuration", inline="true")
        mainpanel_embed.add_field(name="Leave Messages:", value="❌ `Disabled`.\nReact with 3️⃣ to open Configuration", inline="true")
        mainpanel_embed.add_field(name="Member Counter:", value="❌ `Disabled`.\nReact with 4️⃣ to open Configuration", inline="true")
        mainpanel_embed.add_field(name="Anti-Spam:", value="❌ `Disabled`.\nReact with 5️⃣ to open Configuration", inline="true")
        mainpanel_embed.add_field(name="Warns, Mutes, Bans", value="❌ `Disabled`.\nReact with 6️⃣ to open Configuration", inline="true")
        mainpanel_embed.add_field(name="Automatic Roles:", value="Reaction Roles: ❌ `Disabled`.\nOn-Join Roles: ❌ `Disabled`.\nReact with 7️⃣ to open Configuration", inline="true")
        mainpanel_embed.add_field(name="Logging: ", value="✅ `Enabled` (By Default).\nReact with 8️⃣ to open Configuration", inline="true")
        main_panel_msg = await mainpanel.send(embed=mainpanel_embed)
    except:
        msg.channel.send("There was an error sending the configuration panel in <#{}>".format(mainpanel.id))
    try:
        await main_panel_msg.add_reaction('1️⃣')
        await main_panel_msg.add_reaction('2️⃣')
        await main_panel_msg.add_reaction('3️⃣')
        await main_panel_msg.add_reaction('4️⃣')
        await main_panel_msg.add_reaction('5️⃣')
        await main_panel_msg.add_reaction('6️⃣')
        await main_panel_msg.add_reaction('7️⃣')
        await main_panel_msg.add_reaction('8️⃣')
    except discord.Forbidden:
        msg.channel.send("There was an error reacting to (this message)[{}]. I don't have the `Add Reactions` Permission.".format(main_panel_msg.jump_url))
    with open("./servers.json", "r+") as file:
        data_to_add = {
            "{}".format(msg.guild.id) : {
                "setup_category_ID" : setup_category.id,
                "main_panel_ID": mainpanel.id,
                "main_panel_msg_ID": main_panel_msg.id,
                "log_channel_ID": log_channel.id,
                "warning_channel": warning_channel.id,
                "configuration": {
                    "word_filter": {
                        "enabled": "false",
                        "badwords": [],
                        "staffpass": "false"
                    },
                    "welcomemsg": {
                        "enabled": "false",
                        "message": "Welcome to <server.name>, <user.mention>",
                        "dm_message": {
                            "enabled": "false",
                            "message": ""
                        }
                    },
                    "leavemsg": {
                        "enabled": "false",
                        "message": "<user.mention> left <server.name>"
                    },
                    "member_counter": {
                        "enabled": "false",
                        "channel_ID": "none"
                    },
                    "anti_spam": "disabled",
                    "warns_mutes_bans": {
                        "enabled": "false",
                        "qualified_roles": []
                    },
                    "autoroles": {
                        "reaction_roles": {
                            "enabled": "false",
                            "reaction_dictionary": {}
                        },
                        "on_join": {
                            "enabled": "false",
                            "roles_to_give": []
                        }
                    },
                    "logging": {
                        "on_patch_complete": "true",
                        "on_join": "true",
                        "on_leave": "true",
                        "on_message": "true",
                        "on_message_delete": "true",
                        "on_message_edit": "true",
                        "on_channel_create": "true",
                        "on_channel_edit": "true",
                        "on_channel_delete": "true",
                        "on_guild_update": "true",
                        "on_user_update": "true",
                        "on_ban": "true",
                        "on_unban": "true"
                    }
                }
            }
        }
        data = json.load(file) #Load File
        data.update(data_to_add) #Basically Append Data
        file.seek(0) #Seek
        json.dump(data, file) #Execute/Add data
    #Create New Message
    