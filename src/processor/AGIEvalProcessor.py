import os
import json

import pandas as pd

from src.processor import BaseDatasetProcessor,ChatGPTSchema
from src.utils.utils import read_jsonl
from src.utils.config import AGIEvalMappings

class AGIEval(BaseDatasetProcessor):
    def __init__(self,args):
        super().__init__(args=args)
        self._dataset = {}
        self._prompts = None
        self.load_dataset()
        self.load_prompts()

    def load_dataset(self):
        """
        从给定的路径加载数据集到内存。
        """
        dataset_path = self.config.get(self.dataset,"data_path")
        if os.path.isdir(dataset_path):
            dataset_list = os.listdir(dataset_path)
            for file in dataset_list:
                cur_file_path = os.path.join(dataset_path,file)
                cur_data = read_jsonl(cur_file_path)
                self._dataset[file[:-6]] = cur_data

        else:
            print(f"数据集文件不存在或未设置：{self.dataset_path}")

    def load_prompts(self):
        """
        从给定的路径加载提示词到内存。
        """
        prompt_path = self.config.get(self.dataset, "prompt_path")
        if os.path.exists(prompt_path):
            self._prompts = pd.read_csv(prompt_path)
        else:
            print(f"提示词文件不存在或未设置：{self.prompts_path}")


    def convert_zero_shot(self,line,dataset_name):
        try:
            passage = line["passage"] if line["passage"] is not None else ""
            if dataset_name in AGIEvalMappings["english_qa_datasets"]:
                option_string = "ABCDEFG"
                count = len(line["options"])
                if count == 1:
                    count = 5

                return passage + "Q: " + line["question"] + " " \
                    + "Answer Choices: " + " ".join(line["options"]) + "\n" + \
                    "A: Among A through {}, the answer is".format(option_string[count - 1])


            elif dataset_name in AGIEvalMappings["chinese_qa_datasets"]:
                option_string = "ABCDEFG"
                count = len(line["options"])
                if count == 1:
                    count = 4
                return passage + "问题：" + line["question"] + " " \
                    + "选项：" + " ".join(line["options"]) + "\n" + \
                    "答案：从A到{}, 我们应选择".format(option_string[count - 1])

            elif dataset_name in AGIEvalMappings["english_cloze_datasets"]:
                return passage + "Q: " + line["question"] + "\n" \
                                                            "A: The answer is"

            elif dataset_name in AGIEvalMappings["chinese_cloze_datasets"]:
                return passage + "问题：" + line["question"] + "\n" \
                                                              "答案："
        except NameError:
            print("Dataset not defined.")

    def convert_zero_shot_CoT_stage1(self,line, dataset_name):
        try:
            passage = line["passage"] if line["passage"] is not None else ""
            if dataset_name in AGIEvalMappings["english_qa_datasets"]:
                return passage + "Q: " + line["question"] + " " \
                    + "Answer Choices: " + " ".join(line["options"]) + "\n" + \
                    "Let's think step by step."

            elif dataset_name in AGIEvalMappings["chinese_qa_datasets"]:
                option_string = "ABCDEFG"
                count = len(line["options"])
                if count == 1:
                    count = 4
                return passage + "问题：" + line["question"] + " " \
                    + "选项：" + " ".join(line["options"]) + "\n" + \
                    "从A到{}, 我们应选择什么？让我们逐步思考：".format(option_string[count - 1])

            elif dataset_name in AGIEvalMappings["english_cloze_datasets"]:
                return passage + "Q: " + line["question"] + "\n" \
                                                            "A: Let's think step by step."

            elif dataset_name in AGIEvalMappings["chinese_cloze_datasets"]:
                return passage + "问题：" + line["question"] + "\n" \
                                                              "答案：让我们逐步思考："
        except NameError:
            print("Dataset not defined.")

    def combine_prompt(self):
        if self.setting == "zero-shot":
            for dataset_name,datas in self._dataset.items():
                processed = []
                for meta_idx,line in enumerate(datas):
                    ctxt = self.convert_zero_shot(line,dataset_name)
                    new_instance = ChatGPTSchema(context=ctxt,dataset_name=dataset_name,metadata = meta_idx)

                    processed.append(new_instance.to_dict())
                self._dataset[dataset_name]=processed

                cache_root = os.path.join("experiments/cache", self.setting)
                os.makedirs(cache_root, exist_ok=True)
                with open(os.path.join(cache_root,"{}.json".format(dataset_name)),"w",encoding="utf-8") as ft:
                    json_data = json.dumps(processed,ensure_ascii=False,indent=4)
                    ft.write(json_data)


        elif self.setting == "zero-shot-CoT":
            for dataset_name, datas in self._dataset.items():
                processed = []
                for meta_idx, line in enumerate(datas):
                    ctxt = self.convert_zero_shot_CoT_stage1(line, dataset_name)
                    new_instance = ChatGPTSchema(context=ctxt, dataset_name=dataset_name, metadata=meta_idx)

                    processed.append(new_instance.to_dict())
                self._dataset[dataset_name] = processed
                cache_root = os.path.join("experiments/cache", self.setting)
                os.makedirs(cache_root, exist_ok=True)
                with open(os.path.join(cache_root,"{}.json".format(dataset_name)),"w",encoding="utf-8") as ft:
                    json_data = json.dumps(processed,ensure_ascii=False,indent=4)
                    ft.write(json_data)

        else:
            pass


