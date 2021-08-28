from asyncio import events
import discord
import json

client = discord.Client()
# temporary stuff, i'll change later
minimum = {"value": 20000}  
listen_to_all = {"value": True}

try:
    with open("messages.json", "r") as a:
        msg_dic = json.loads(a.read())
except:
    msg_dic = {}


def update_json():
    msg_json = json.dumps(msg_dic, indent=1)
    with open("messages.json", "w") as b:
        b.write(msg_json)


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # adds a point to the author everytime a message is sent
    if message.content.startswith(""):
        if str(message.author.id) not in msg_dic and listen_to_all["value"] is True:
            name = str(message.author).split("#")
            msg_dic[str(message.author.id)] = {
                "messages": 1,
                "name": name[0],
                "alt": None,
                "is_alt": False,
            }
        elif str(message.author.id) in msg_dic:
            msg_dic[str(message.author.id)]["messages"] += 1

    if message.author.guild_permissions.manage_channels:
        # command to turn on/off automatic addition of new users to the leaderboard
        if message.content.startswith("-autoupdate"):
            if listen_to_all["value"] == True:
                listen_to_all["value"] = False
                await message.channel.send("New users will **not** get added to the leaderboard anymore")
            elif listen_to_all["value"] == False:
                listen_to_all["value"] = True
                await message.channel.send("New users **will** get added to the leaderboard")
        
        
        # command to add/update new entries to the leaderboard
        if message.content.startswith("-edit"):
            edit_content = message.content.split()
            try:
                user_name = await client.fetch_user(edit_content[1])
                user_name = str(user_name).split("#")
            except:
                user_name = ["Invalid User", ""]
            try:
                if not edit_content[1].isdigit() or not edit_content[2].isdigit():
                    await message.channel.send("Error: invalid id/number")
                else:
                    msg_dic[edit_content[1]] = {
                        "messages": int(edit_content[2]),
                        "name": user_name[0],
                        "alt": None,
                        "is_alt": False,
                    }
                    update_json()
                    await message.channel.send(
                        f"{user_name[0]} was saved with {edit_content[2]} messages"
                    )
            except:
                await message.channel.send(
                    "Error: you must input an valid id and a number of messages"
                )
        # command to save an user as someone else's alt
        if message.content.startswith("-alt"):
            main, alt = message.content.split()[1:]

            if main == alt:
                await message.channel.send(f"{main} can't be an alt of itself")
            elif main not in msg_dic:
                await message.channel.send(f"Error: {main} not found, try doing `-edit {main} [message_number]` first")
            elif alt not in msg_dic:
                await message.channel.send(f"Error: {alt} not found, try doing `-edit {alt} [message_number]` first")
            elif msg_dic[alt]["is_alt"]:
                await message.channel.send(
                    f"Error: {msg_dic[alt]['name']} ({alt}) is already an alt"
                )
            else:
                msg_dic[main]["alt"] = alt
                msg_dic[alt]["is_alt"] = True
                update_json()
                await message.channel.send(
                    f"{msg_dic[alt]['name']} was saved as an alt of {msg_dic[main]['name']}"
                )
                
        if message.content.startswith("-removealt"):
            main, alt = message.content.split()[1:]

            if main == alt:
                await message.channel.send(f"{main} can't be an alt of itself")
            elif main not in msg_dic:
                await message.channel.send(f"Error: {main} not found")
            elif alt not in msg_dic:
                await message.channel.send(f"Error: {alt} not found")
            elif msg_dic[main]["alt"] is None:
                await message.channel.send(f"Error: {main} has no alts")
            elif msg_dic[alt]["is_alt"] == False:
                await message.channel.send(f"Error: {alt} is not an alt")
            else:
                msg_dic[main]["alt"] = None
                msg_dic[alt]["is_alt"] = False
                update_json()
                await message.channel.send(
                    f"{msg_dic[alt]['name']} is no longer an alt of {msg_dic[main]['name']}"
                )

        # command to delete entries from the leaderboard
        if message.content.startswith("-delete"):
            del_content = message.content.split()
            
            try:
                await message.channel.send(
                    f"{msg_dic[del_content[1]]['name']} was deleted"
                )
                msg_dic.pop(del_content[1])
                update_json()
            except:
                await message.channel.send("Error: invalid id")

        # command to change the minimum amount of messages necessary to appear on the leaderboard
        if message.content.startswith("-minimum"):
            try:
                minimum["value"] = int(message.content.split()[1])
                await message.channel.send(
                    f"Every user with more than {message.content.split()[1]} message will now be displayed on the leadeboard"
                )
            except:
                await message.channel.send("Error: invalid value")

    # help command
    if message.content.startswith("-help"):
        await message.channel.send(
            "`-msglb`: prints the message leaderboard\n\n`-autoupdate`: turns on/off automatic addition of new users to the leaderboard\n\n`-edit [user_id] [message_number]`: update a user's message number\n\n`-delete [user_id]`: delete a user from the leaderboard\n\n`-alt [user_id] [alt_id]`: adds up the alt's messages to the user's messages (1 alt per user)\n\n`-removealt [user_id] [alt_id]`: removes alt from user\n\n`-minimum [value]`: change the minimum amount of messages necessary to appear on the leaderboard (defaults to 20000)\n\n`-minfo`: prints the current minimum value to appear on the leaderboard\n\n`-name`: updates author's name on the leadeboard\n\n`-source`: prints the source code link"
        )

    # command to print the source link
    if message.content.startswith("-source"):
        await message.channel.send("https://github.com/RafaeI11/Message_LeaderBot")

    # command to print the current value of minimum
    if message.content.startswith("-minfo"):
        await message.channel.send(
            f"The current minimum is {minimum['value']} messages"
        )

    # command to update a user's name
    if message.content.startswith("-name"):
        if str(message.author.id) not in msg_dic:
            pass
        else:
            name = str(message.author).split("#")
            if name[0] == msg_dic[str(message.author.id)]["name"]:
                await message.channel.send("Your name is already up to date")
            else:
                msg_dic[message.author.id]["name"] = name[0]
                await message.channel.send(f"Name updated to {name[0]}")

    # command to print the message leaderboard
    if message.content.startswith("-msglb"):
        update_json()
        simple_msg_dic = {}
        msg_lb = ""
        
        for id in msg_dic:
            if msg_dic[id]["alt"] is None and msg_dic[id]["is_alt"] == False:
                simple_msg_dic[id] = msg_dic[id]["messages"]

            if msg_dic[id]["alt"] is not None and msg_dic[id]["is_alt"] == False:
                simple_msg_dic[id] = (
                    msg_dic[id]["messages"] + msg_dic[msg_dic[id]["alt"]]["messages"]
                )

        # sorts the leaderboard by most messages in probably the ugliest way possible
        almost_sorted_msg_dic = sorted(
            simple_msg_dic.items(), key=lambda x: x[1], reverse=True
        )
        sorted_msg_dic = {}

        for item in almost_sorted_msg_dic:
            sorted_msg_dic[str(item[0])] = int(item[1])

        # restricts the leaderboard to only users with more than 20k messages
        for user in sorted_msg_dic:
            # prevents Steve from being on the top
            if user == "657571924527808512":
                pass
            elif int(sorted_msg_dic[user]) >= minimum["value"]:
                if msg_dic[user]["alt"] is not None:
                    msg_lb += f"{simple_msg_dic[user]}: {msg_dic[user]['name']} + alt\n"
                else:
                    msg_lb += f"{simple_msg_dic[user]}: {msg_dic[user]['name']}\n"
        
        # adds steve to the end
        if '657571924527808512' in simple_msg_dic:
            msg_lb += f"\n {simple_msg_dic['657571924527808512']}: Steve the bot"
        
        embed = discord.Embed(
            title="Message Leaderboard", color=7419530, description=msg_lb
        )
        await message.channel.send(embed=embed)


@client.event
async def on_message_delete(message):
    msg_dic[str(message.author.id)]["messages"] -= 1
