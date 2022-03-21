#!/usr/bin/env python3.8
# coding:utf-8

# 前の音から1,2,3,4,5,8度で音を選ぶ
import random


note_list = ["C", "D", "E", "F", "G", "A",
             "B", "c", "d", "e", "f", "g"]
beat_dict = {0.5: "/2", 1: "", 1.5: "<", 2: "2"}
result_list = []


def select_note(before_note):
    # print("-----------------before:"+str(before_note))
    # 前の音から1,2,3,4,5,8度で音を選ぶ
    if before_note == "":
        return random.choice(note_list)
    before_index = note_list.index(before_note)
    # print("-----------------before_index:"+str(before_index))
    start_index = 0
    last_index = len(note_list)-1
    if before_index > 4:
        # Aだった場合Dからが対象
        start_index = before_index - 5
    if (before_index + 4) < len(note_list):
        last_index = before_index + 5
    # print("-----------------start:"+str(start_index)+" last:"+str(last_index))
    # print("-----------------list:"+str(note_list[start_index:last_index]))
    return random.choice(note_list[start_index:last_index])


def select_beat(before_beat_str):
    print("-------------------:before::"+before_beat_str)
    beat, beat_str = random.choice(list(beat_dict.items()))
    print("-------------------:randomで取れた音の長さ"+beat_str+";;;;"+str(beat))

    if beat_str == "<":
        # 今は四分音符に対してのみなのでこれを実行
        beat = 1
    base_length = beat
    # 計算の基準の長さを設定
    if beat_str == "<":
        base_length = beat/2

    if before_beat_str == "<":
        beat = base_length*(1.5)
    else:
        beat = base_length

    print("-------------------:最終的な音の長さ"+beat_str+";;;;"+str(beat))
    return beat, beat_str


def make_one_bar(note):
    # 合計した拍の長さ
    beat_len = 0
    score = ""
    beat_str = ""
    temp_beat_str = ""
    # note = ""
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
            if beat_str == "<":
                score = score[0:-1]+"/2"
                # base_length = beat/2
            score += random.choice(note_list) + "/4"
            return score+"|", note

        note = select_note(note)
        temp_beat_str = beat_str
        beat, beat_str = select_beat(beat_str)
        beat_len += beat
        print("--------------[beat]:"+str(beat)+"  [beat_str]:"+str(beat_str))

        if beat_len > 4:
            beat_len -= beat
            beat_str = temp_beat_str
            continue
        score += note
        score += beat_str
    return score, note


def make_bar():
    # 4小節作る
    score = "M:4/4 \nL:1/4\n"
    note = ""
    for i in range(4):
        print("------"+str(i + 1)+"小節目")
        get_score, note = make_one_bar(note)
        # score += make_one_bar(note)
        score += get_score
    return score+"z4|]"


def execute():
    # 4曲作る
    for i in range(1):
        print("--"+str(i + 1)+"曲目")
        # 4小節作る
        resutl = make_bar()
        result_list.append(resutl)
    # 出力
    for item in result_list:
        print(item)


if __name__ == "__main__":
    execute()
