# -*- coding: utf-8 -*-
import re


def parser(content):
    pass

def extract_answer(data):
    for unit in data:
        cur_elem_result = parser(unit)
        s = input()



if __name__ == '__main__':
    import json
    with open("experiments/arc-c.json","r") as fl:
        data = json.load(fl)
        extract_answer(data)


