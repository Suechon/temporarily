import requests
from bs4 import BeautifulSoup
import json
import datetime
from dataclasses import dataclass
import discord
import asyncio
import platform
import configparser


config = configparser.ConfigParser()
config.read('setting.ini')
section = 'postQiitaToDiscord'

URL = config.get(section, 'qiita_url')
API_URL = "https://qiita.com/api/v2/items?page="
QIITA_ACCESS_TOKEN = config.get(section, 'qiita_token')
DISCODE_ACCESS_TOKEN = config.get(section, 'discode_token')
# テスト用
CHANNEL_ID = config.get(section, 'channel_id')


def main():
    today = datetime.date.today()
    yesterday = today - datetime.timedelta(days=1)
    today_str = today.strftime('%Y-%m-%d')
    yesterday_str = yesterday.strftime('%Y-%m-%d')
    yesterday_str = "2021-4-1"
    query_dict = get_user(today_str, yesterday_str)
    if len(query_dict) == 0:
        return
    topic_list = get_topic(query_dict)
    if len(topic_list) == 0:
        return
    post_discord(topic_list)


def get_user(today_str, yesterday_str):
    count = 0
    user_dict = {}
    while True:
        count += 1
        response = requests.get(URL+str(count))
        soup = BeautifulSoup(response.text, 'html.parser')
        get_user_list = soup.find_all(
            'span', class_='od-MemberCardHeaderIdentities_userid')
        if get_user_list == None or len(get_user_list) == 0:
            return user_dict
        for item in get_user_list:
            user_id = item.get_text()[1:]
            user_dict[user_id] = QueryBean(
                user_id, yesterday_str, today_str)


def get_topic(query_dict):
    query = "query="
    count = 0
    list = []
    for bean in query_dict.values():
        count += 1
        query += "created:>="+bean.start_date+"+created:<" + \
            bean.end_date+"+user:"+bean.user+" OR "
        if count >= 5:
            list += request(query)
            count = 0
            query = "query="
    list += request(query)
    return list


def request(query):
    count = 0
    list = []
    while True:
        count += 1
        url = (
            API_URL + str(count)+"&per_page=100&" + query
        )
        headers = {"Authorization": 'Bearer {}'.format(QIITA_ACCESS_TOKEN)}
        response = requests.get(url, headers)

        if response.status_code > 200:
            print("うまくいかなかった")
            print(response)
            return list
        text = json.loads(response.text)

        if len(text) == 0:
            print("Nothing")
            return list

        for v2 in text:
            list.append(PostContents(v2["title"], v2["url"]))


def post_discord(topic_list):

    client = discord.Client()

    @client.event
    async def on_ready():
        print('ログインしました')
        # await greet()
        await client.close()

    async def greet():
        channel = client.get_channel(CHANNEL_ID)
        for topic in topic_list:
            await channel.send(topic.title+"\n"+topic.url)

    client.run(DISCODE_ACCESS_TOKEN)


@dataclass
class QueryBean:
    user: str = ""
    start_date: str = ""
    end_date: str = ""


@dataclass
class PostContents():
    title: str = ""
    url: str = ""


if __name__ == "__main__":
    main()
