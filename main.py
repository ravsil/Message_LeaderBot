import json

from discord.ext import commands

import discord


class HelpCmd(commands.HelpCommand):
    async def send_bot_help(self, mapping):
        ctx = self.context
        bot = ctx.bot
        commands = bot.commands

        result = []
        for cmd in commands:
            sign = self.get_command_signature(cmd)
            result.append(f"`{sign}`: {cmd.help}")

        await ctx.send("\n\n".join(result))

    send_cog_help = send_command_help = send_group_help = send_bot_help


bot = commands.Bot(
    command_prefix="-",
    help_command=HelpCmd(),
    allowed_mentions=discord.AllowedMentions.none(),
)

bot.minimum = 20000
bot.listen_to_all = True

try:
    with open("messages.json", "r") as a:
        bot.msg_dic = json.loads(a.read())
except BaseException:
    bot.msg_dic = {}
    with open("messages.json", "w+") as a:
        a.write(json.dumps({}, indent=4))


def update_json():
    with open("messages.json", "w") as b:
        b.write(json.dumps(bot.msg_dic, indent=4))


@bot.command()
@commands.has_guild_permissions(manage_channels=True)
async def autoupdate(ctx):
    """turns on/off automatic addition of new users to the leaderboard"""
    # command to turn on/off automatic addition of new users to the leaderboard
    if bot.listen_to_all:
        bot.listen_to_all = False
        return await ctx.send(
            "New users will **not** get added to the leaderboard anymore"
        )

    bot.listen_to_all = True
    return await ctx.send("New users **will** get added to the leaderboard")


@bot.command()
@commands.has_guild_permissions(manage_channels=True)
async def edit(ctx, user: discord.User, message_number: int):
    """update a user's message number"""
    name = user.name

    bot.msg_dic[user.id] = {
        "messages": message_number,
        "name": name,
        "alt": None,
        "is_alt": False,
    }
    update_json()
    await ctx.send(f"{name} was saved with {message_number} messages")


@edit.error
async def edit_err(ctx, error):
    # error handler for minimum command
    if isinstance(error, commands.BadArgument):
        return await ctx.send("Error: you must input a valid number of messages")
    await on_command_error(ctx, error, bypass_check=True)


@bot.command()
@commands.has_guild_permissions(manage_channels=True)
async def alt(ctx, user: discord.User, alt: discord.User):
    """adds up the alt's messages to the user's messages (1 alt per user)"""
    # command to save an user as someone else's alt
    if user == alt:
        return await ctx.send(f"{user} can't be an alt of itself")

    if str(user.id) not in bot.msg_dic:
        return await ctx.send(
            f"Error: {user} not found, try doing `-edit {user.id} [message_number]` first"
        )

    if str(alt.id) not in bot.msg_dic:
        return await ctx.send(
            f"Error: {alt} not found, try doing `-edit {alt.id} [message_number]` first"
        )

    if bot.msg_dic[str(alt.id)]["is_alt"]:
        return await ctx.send(
            f"Error: {bot.msg_dic[str(alt.id)]['name']} ({alt.name}) is already an alt"
        )

    bot.msg_dic[user.id]["alt"] = alt
    bot.msg_dic[alt.id]["is_alt"] = True

    update_json()

    await ctx.send(f"{alt.name} was saved as an alt of {user.name}")


@bot.command()
@commands.has_guild_permissions(manage_channels=True)
async def removealt(ctx, user: discord.User, alt: discord.User):
    """removes alt from user"""
    # command to remove an user's alt
    if user == alt:
        return await ctx.send(f"{user} can't be an alt of itself")

    if str(user.id) not in bot.msg_dic:
        return await ctx.send(f"Error: {user} not found")

    if str(alt.id) not in bot.msg_dic:
        return await ctx.send(f"Error: {alt} not found")

    if not bot.msg_dic[str(user.id)]["alt"]:
        return await ctx.send(f"Error: {user} has no alts")

    if not bot.msg_dic[str(alt.id)]["is_alt"]:
        return await ctx.send(f"Error: {alt} is not an alt")

    bot.msg_dic[str(user.id)]["alt"] = None
    bot.msg_dic[str(alt.id)]["is_alt"] = False

    update_json()

    await ctx.send(f"{alt.name} is no longer an alt of {user.name}")


@bot.command()
@commands.has_guild_permissions(manage_channels=True)
async def delete(ctx, user: discord.User):
    """delete a user from the leaderboard"""
    # command to delete entries from the leaderboard
    try:
        bot.msg_dic.pop(str(user.id))
        update_json()
        await ctx.send(f"{user} was deleted")
    except KeyError:
        await ctx.send(f"Error: user '{user.name}' is not listed in the leaderboard")


@bot.command()
@commands.has_guild_permissions(manage_channels=True)
async def minimum(ctx, value: int):
    """change the minimum amount of messages necessary to appear on the leaderboard (defaults to 20000)"""
    bot.minimum = value
    await ctx.send(
        f"Every user with more than {value} message will now be displayed on the leadeboard"
    )


@minimum.error
async def minimum_err(ctx, error):
    # error handler for minimum command
    if isinstance(error, commands.BadArgument):
        return await ctx.send("Error: invalid value")
    await on_command_error(ctx, error, bypass_check=True)


@bot.command()
async def source(ctx):
    """prints the source code link"""
    # command to print the source link
    await ctx.send("https://github.com/RafaeI11/Message_LeaderBot")


@bot.command()
async def minfo(ctx):
    """prints the current minimum value to appear on the leaderboard"""
    # command to print the current value of minimum
    await ctx.send(f"The current minimum is {bot.minimum} messages")


@bot.command()
async def name(ctx):
    """updates author's name on the leadeboard"""
    # command to update a user's name
    author = ctx.author

    if str(author.id) not in bot.msg_dic:
        return

    name = author.name

    if name == bot.msg_dic[str(author.id)]["name"]:
        return await ctx.send("Your name is already up to date")

    bot.msg_dic[author.id]["name"] = name
    await ctx.send(f"Name updated to {name}")


@bot.command()
async def msglb(ctx):
    """prints the message leaderboard"""
    update_json()
    simple_msg_dic = {}
    msg_lb = ""
    msg_dic = bot.msg_dic

    for id in msg_dic:
        if not msg_dic[id]["alt"] and not msg_dic[id]["is_alt"]:
            simple_msg_dic[id] = msg_dic[id]["messages"]

        if msg_dic[id]["alt"] and not msg_dic[id]["is_alt"]:
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
        elif int(sorted_msg_dic[user]) >= bot.minimum:
            if msg_dic[user]["alt"] is not None:
                msg_lb += f"{simple_msg_dic[user]}: {msg_dic[user]['name']} + alt\n"
            else:
                msg_lb += f"{simple_msg_dic[user]}: {msg_dic[user]['name']}\n"

    # adds steve to the end
    if "657571924527808512" in simple_msg_dic:
        msg_lb += f"\n {simple_msg_dic['657571924527808512']}: Steve the bot"

    embed = discord.Embed(
        title="Message Leaderboard", color=7419530, description=msg_lb
    )
    await ctx.send(embed=embed)


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    # adds a point to the author everytime a message is sent
    if str(message.author.id) not in bot.msg_dic and bot.listen_to_all:
        bot.msg_dic[str(message.author.id)] = {
            "messages": 1,
            "name": message.author.name,
            "alt": None,
            "is_alt": False,
        }

    elif str(message.author.id) in bot.msg_dic:
        bot.msg_dic[str(message.author.id)]["messages"] += 1

    # process a command (if valid)
    await bot.process_commands(message)


@bot.event
async def on_message_delete(message):
    bot.msg_dic[str(message.author.id)]["messages"] -= 1


@bot.event
async def on_command_error(ctx, error: commands.CommandError, *, bypass_check: bool = False):
    # handles command error

    if ctx.command and ctx.command.has_error_handler() and not bypass_check:
        # already have error handler
        return

    # get the "real" error
    error = getattr(error, "original", error)

    if isinstance(error, commands.CommandNotFound):
        # command not found is annoying for most bot user, so just return nothing
        return

    if isinstance(error, commands.UserNotFound):
        return await ctx.send(f"Error: user '{error.argument}' not found")

    if isinstance(error, commands.MissingRequiredArgument):
        return await ctx.send(f"Error: you must input a valid `{error.param.name}`")

    if isinstance(error, commands.MissingPermissions):
        # probably i made it too over-complicated,
        # but its so that the message stays consistent with the other error messages
        error = str(error)
        return await ctx.send(f"Error: {error[0].lower()}{error[1:-1]}")

    raise error


@bot.event
async def on_ready():
    # launch everytime bot is online (not only first boot)
    # just a way to know if the bot is online
    print("Bot online!")


if __name__ == "__main__":
    # allows launching the bot using `python main.py [TOKEN]` command
    import sys

    try:
        bot.run(sys.argv[1], reconnect=True)
    except IndexError:
        print(f"Usage: python {sys.argv[0]} [TOKEN]")
