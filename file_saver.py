import json

def saver():
    with open("messages.json", "r") as a:
        dic = json.loads(a.read())
        for key in dic:
            simple_dic = dic[key]
            with open(f"{key}.json", "w") as b:
                json.dump(simple_dic, b, indent=4)
    print("Backup done!")
