import json
from time import sleep

while True:
    try:
        with open("messages.json", "r") as a:
            dic = json.loads(a.read())

        for key in dic:
            simple_dic = dic[key]

            with open(f"{key}.json", "w") as b:
                json.dump(simple_dic, b, indent=4)

        print("Backup done!")

    except FileNotFoundError:
        print("backup will be done on the next 24 hours if you run the bot")

    sleep(86400)  # 24 hours
