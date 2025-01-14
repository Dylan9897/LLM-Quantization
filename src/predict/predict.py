import os
import json
from src.utils.utils import read_json
from src.models.ModelInfer import Model
from conf.model_config import config as configs

def prepare(data):
    result = []
    for line in data:
        result.append(line["context"])
    return result


def inference(args):
    if "qwen" in args.model_path.lower():
        model_path = os.path.join("ckpt",args.model_path)

        target_path = "{}-chat".format(args.setting) if args.chat_mode else args.setting
        if args.chat_mode:
            cache_root = "experiments/result/{dataset}/{settings}/{chat_mode}".format(
                dataset=args.dataset,
                settings = args.setting,
                chat_mode = args.chat_mode
            )
        else:
            cache_root = "experiments/result/{dataset}/{settings}".format(
                dataset=args.dataset,
                settings = args.setting
            )
        if not os.path.exists(cache_root) or not os.path.isdir(cache_root):
            # 如果不存在，则创建目录
            os.makedirs(cache_root)
        else:
            # 如果目录已经存在，则跳过创建
            print(f"Directory '{cache_root}' already exists, skipping creation.")

        # 加载参数并初始化模型
        func = Model(model_path=model_path,config=configs,args=args)

        
        if args.chat_mode:
            target_file_root = "experiments/cache/{dataset}/{settings}/{chat_mode}".format(
                dataset=args.dataset,
                settings = args.setting,
                chat_mode = args.chat_mode
            )
        else:
            target_file_root = "experiments/cache/{dataset}/{settings}".format(
                dataset=args.dataset,
                settings = args.setting
            )
        file_list = os.listdir(target_file_root)
        print(f"file_list is {file_list}")
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