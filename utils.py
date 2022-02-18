import json
import uuid
import os

FILENAME = "messages.json"
SETTINGS = "settings.json"


def saver():
    try:
        with open("messages.json", "r") as a:
            dic = json.loads(a.read())
            for key in dic:
                simple_dic = dic[key]
                with open(f"{key}.json", "w") as b:
                    json.dump(simple_dic, b, indent=4)
        print("Backup done!")
    except FileNotFoundError:
        print("file not found, will try again in 24 hours")


def update_settings(bot_settings):
    temp = f"{uuid.uuid4()}-{SETTINGS}.tmp"
    with open(temp, "w") as f:
        json.dump(bot_settings.copy(), f, indent=4)

    os.replace(temp, SETTINGS)


def update_json(bot_msg_dic):
    temp = f"{uuid.uuid4()}-{FILENAME}.tmp"
    with open(temp, "w") as f:
        json.dump(bot_msg_dic.copy(), f, indent=4)

    os.replace(temp, FILENAME)


def alt_handler(bot, ctx, user, alt, add=True):
    msg_dic = bot.msg_dic[str(ctx.message.guild.id)]

    if user == alt:
        return f"{user} can't be an alt of itself"

    elif str(user.id) not in msg_dic:
        if add:
            return f"Error: {user} not found, try doing `-edit {user.id} <message_number>` first"
        else:
            return f"Error: {user} not found"

    elif str(alt.id) not in msg_dic:
        if add:
            return f"Error: {alt} not found, try doing `-edit {alt.id} <message_number>` first"
        else:
            return f"Error: {alt} not found"

    elif add and msg_dic[str(alt.id)]["is_alt"]:
        return f"Error: {alt.name} ({alt.id}) is already an alt"

    elif not add and not msg_dic[str(user.id)]["alt"]:
        return f"Error: {user} has no alts"

    elif add and msg_dic[str(user.id)]["is_alt"]:
        return f"Error: {user.name} ({user.id}) is already an alt"

    elif not add and not msg_dic[str(alt.id)]["is_alt"]:
        return f"Error: {alt} is not an alt"

    else:
        if add:
            if msg_dic[str(user.id)]["alt"] is None:
                msg_dic[str(user.id)]["alt"] = [str(alt.id)]
            else:
                msg_dic[str(user.id)]["alt"].append(str(alt.id))

            msg_dic[str(alt.id)]["is_alt"] = True
            update_settings(bot.msg_dic)
            return f"{alt} was saved as an alt of {user}"
        else:
            if len(msg_dic[str(user.id)]["alt"]) == 1:
                msg_dic[str(user.id)]["alt"] = None
            else:
                msg_dic[str(user.id)]["alt"].remove(str(alt.id))

            msg_dic[str(alt.id)]["is_alt"] = False
            update_settings(bot.msg_dic)
            return f"{alt} is no longer an alt of {user}"
