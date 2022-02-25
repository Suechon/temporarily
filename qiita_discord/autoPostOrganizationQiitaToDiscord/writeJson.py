
import json

FILE = "topic.md"
TITLE = "Discordにorganizationの記事を投稿する"


with open(FILE, 'r', encoding='UTF-8') as f:
    data = f.read()

dict_data = {}
dict_data["title"] = TITLE
dict_data["body"] = data
dict_data["tags"] = [{"name": "Python"}, {
    "name": "discord"}, {"name": "discord.py"}]


o_json = json.dumps(dict_data)
# print(o_json)

with open("20210927.json", 'w', encoding='UTF-8') as f:
    f.write(o_json)
