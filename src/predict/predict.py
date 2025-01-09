import os
import json
from src.utils.utils import read_json
from src.models.QwenModelBase import QwenModel

def prepare(data):
    result = []
    for line in data:
        result.append(line["context"])
    return result


def inference(args):
    if "qwen" in args.model_path.lower():
        model_path = os.path.join("ckpt",args.model_path)

        target_path = "{}-chat".format(args.setting) if args.chat_mode else args.setting
        cache_root = os.path.join("experiments/result", target_path)
        if not os.path.exists(cache_root) or not os.path.isdir(cache_root):
            # 如果不存在，则创建目录
            os.makedirs(cache_root)
        else:
            # 如果目录已经存在，则跳过创建
            print(f"Directory '{cache_root}' already exists, skipping creation.")


        func = QwenModel(model_path=model_path)
        if args.chat_mode:
            target_file_root = os.path.join("experiments/cache/{}-{}".format(args.setting,"chat"))
        else:
            target_file_root = os.path.join("experiments/cache/{}".format(args.setting))
        file_list = os.listdir(target_file_root)
        for file in file_list:
            
            target_file_path = os.path.join(target_file_root,file)
            json_data = read_json(target_file_path)
            cur_data = prepare(json_data)
            cur_result = func.infer(cur_data)
            with open(os.path.join(cache_root,file),"w",encoding="utf-8") as ft:
                json_data = json.dumps(cur_result,ensure_ascii=False,indent=4)
                ft.write(json_data)


if __name__ == "__main__":
    func = QwenModel(
        model_path="ckpt/Qwen2___5-14B-Instruct"
    )