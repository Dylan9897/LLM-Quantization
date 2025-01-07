import json

def read_jsonl(file):
    result = []
    with open(file,"r",encoding="utf-8") as fl:
        for line in fl.readlines():
            result.append(
                json.loads(line)
            )
    return result

def read_json(file):
    with open(file,"r",encoding="utf-8") as fl:
        return json.load(fl)

def read_txt(file):
    with open(file,"r",encoding="utf-8") as fl:
        return fl.read()
