#!/usr/bin/env python3.8
# coding:utf-8

# ABC記譜法で適当に曲つくる
import random


note_list = ["C", "D", "E", "F", "G", "A",
             "B", "c", "d", "e", "f", "g"]
beat_dict = {0.5: "/2", 0.75: "3/4", 1: "", 1.5: "3/2", 2: "2"}
# beat_dict = {1: "",  2: "2"}
result_list = []


def make_one_bar():
    # 合計した拍の長さ
    beat_len = 0
    score = ""
    temp_beat_str = ""
    # 1小節分作る
    while True:
        print("----------合計"+str(beat_len)+"です")
        if beat_len >= 4:
            # 4拍だったらおわり
            print("--------------拍超えた1:"+str(beat_len))
            score += "|"
            break
        if beat_len > 3.5:
            print("--------------拍足りない:"+str(4-beat_len))
            score += random.choice(note_list) + "/4"
            return score+"|"

        note = random.choice(note_list)
        beat, beat_str = random.choice(list(beat_dict.items()))
        temp_beat_str = beat_str
        beat_len += beat

        if beat_len > 4:
            beat_len -= beat
            beat_str = temp_beat_str
            continue
        score += note
        score += beat_str
    return score


def make_bar():
    # 4小節作る
    score = "M:4/4 \nL:1/4\n"
    for i in range(4):
        print("------"+str(i)+"小節目")
        score += make_one_bar()
    return score+"z4|]"


def execute():
    # 4曲作る
    for i in range(4):
        print("--"+str(i)+"曲目")
        # 4小節作る
        resutl = make_bar()
        result_list.append(resutl)
    # 出力
    for item in result_list:
        print(item)


if __name__ == "__main__":
    execute()
