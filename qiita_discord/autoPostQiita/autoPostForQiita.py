import jpbizday
import datetime
import json
import glob
import requests
import shutil
import configparser


config = configparser.ConfigParser()
config.read('setting.ini')
section = 'autoPostForQiita'
FILE_PATH = "./"
BK_FILE_PATH = FILE_PATH+"bk"
URL = "https://qiita.com/api/v2/items"
TOKEN = config.get(section, 'token')


def main():
    d_today = datetime.date.today()
    result = True

    print("result:"+str(result))
    if not result:
        print("resultだめ")
        return
    # 記事取得
    file_list = sorted(glob.glob(FILE_PATH+"*.json"))
    print("result:"+str(file_list))
    if len(file_list) == 0:
        print("ファイル取得できなかった")
        return
    file = file_list[0]
    contents = load_file(d_today, file)
    if len(contents[0]) < 1 or len(contents[1]) < 1 or len(contents[2]) < 1:
        print("ファイルの内容取得できなかった")
        return
    item = {"title": contents[0],
            "body": contents[1],
            "private": True,
            "tags": contents[2],
            "gist": False, "tweet": False
            }
    dumps = json.dumps(item)
    print(dumps)
    # 投げる
    res = post(item)
    http_status = res.status_code
    print("http_status:"+str(http_status))
    # 記事の移動
    if http_status == 201:
        shutil.move(file, BK_FILE_PATH)


# 週初めの営業日か判定する Trueの時週初めの営業日
# 月:0,火:1,水:2,木:3,金:4,土:5,日:6
def check_business_day_start_week(d_today):
    week = d_today.weekday()

    if week == 5 or week == 6:
        return False

    for num in range(week, -1, -1):
        check_date = d_today - datetime.timedelta(days=num)
        is_biz_day = jpbizday.is_bizday(check_date)
        if is_biz_day:
            if check_date == d_today:
                return True
            else:
                # 今日よりも前に営業日がある場合
                return False
    return False


def load_file(d_today, file):
    json_open = open(file, 'r',  encoding="utf-8")
    json_load = json.load(json_open)
    json_open.close()
    title = str(d_today.year)+"-"+str(d_today.month)+"-"+str(d_today.day)
    body = ""
    tags = []
    if "title" in json_load:
        if json_load["title"] != None:
            title = json_load["title"]
    if "body" in json_load:
        if json_load["body"] != None:
            body = json_load["body"]
    if "tags" in json_load:
        if json_load["tags"] != None:
            tags = json_load["tags"]

    return title, body, tags


def post(item):
    token = 'TOKEN'
    headers = {'Authorization': 'Bearer {}'.format(token)}
    res = requests.post(URL, headers=headers, json=item)

    return res


if __name__ == "__main__":
    main()
