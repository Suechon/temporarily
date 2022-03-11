#!/usr/bin/env python3.8
# coding:utf-8

# 前の音から1,2,3,4,5,8度で音を選ぶ
import random
import copy


note_list = ["C", "D", "E", "F", "G", "A",
             "B", "c", "d", "e", "f", "g"]
beat_dict = {0.5: "/2", 1: "", 1.5: "<", 2: "2"}
result_list = []


def select_note(before_note):
    print("-----------------before:"+str(before_note))
    # 前の音から1,2,3,4,5,8度で音を選ぶ
    if before_note == "":
        return random.choice(note_list)
    before_index = note_list.index(before_note)
    print("-----------------before_index:"+str(before_index))
    start_index = 0
    last_index = len(note_list)-1
    if before_index > 4:
        # Aだった場合Dからが対象
        start_index = before_index - 5
    if (before_index + 4) < len(note_list):
        last_index = before_index + 5
    print("-----------------start:"+str(start_index)+" last:"+str(last_index))
    print("-----------------list:"+str(note_list[start_index:last_index]))
    return random.choice(note_list[start_index:last_index])


def make_one_bar():
    # 合計した拍の長さ
    beat_len = 0
    score = ""
    note = ""
    # 1小節分作る
    while True:
        print("----------合計"+str(beat_len)+"です")
        if beat_len >= 4:
            # 4拍だったらおわり
            print("--------------拍超えた1:"+str(beat_len))
            score += "|"
            break

        note = select_note(note)
        # note = random.choice(note_list)
        beat, beat_str = random.choice(list(beat_dict.items()))
        beat_len += beat

        if beat_len > 4:
            beat_len -= beat
            # print("--------------拍超えた2:"+str(beat_len))
            # beat = beat_len-4
            # print("-----------------足す:"+str(beat))
            # score += beat_dict[beat]+"|"
            # break
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
