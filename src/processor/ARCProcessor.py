# encoding : utf-8 -*-                            
# @author  : 冬瓜                              
# @mail    : dylan_han@126.com    
# @Time    : 2025/2/26 13:26
import json
import os
from src.processor import BaseDatasetProcessor,ChatGPTSchema
from src.utils.utils import read_jsonl,read_txt
from src.models.DeepZeek import Model
from tqdm import tqdm

class ARC(BaseDatasetProcessor):
    def __init__(self,args):
        super().__init__(args=args)
        self.args = args
        self._dataset = {}
        self._prompts = None
        self.load_dataset()
        self.load_prompts()
        self.model = Model()

    def load_dataset(self):
        """
        从给定的路径加载数据集到内存。
        """
        dataset_path = self.config.get(self.dataset, "data_path")
        if os.path.isdir(dataset_path):
            for file in ["ARC-c/ARC-Challenge-Test.jsonl", "ARC-e/ARC-Easy-Test.jsonl"]:
                cur_file_path = os.path.join(dataset_path, file)
                cur_data = read_jsonl(cur_file_path)
                self._dataset[file[:-6]] = cur_data

        else:
            print(f"数据集文件不存在或未设置：{self.dataset_path}")

    def load_prompts(self):
        prompt_path = self.config.get(self.dataset, "prompt_path")
        arc_c_prompt_path = os.path.join(prompt_path, "arc-c-GseRo.txt")
        arc_e_prompt_path = os.path.join(prompt_path, "arc-e-GseRo.txt")
        arc_c_prompt = read_txt(arc_c_prompt_path)
        arc_e_prompt = read_txt(arc_e_prompt_path)
        self._prompts = {
            "arc-c": arc_c_prompt,
            "arc-e": arc_e_prompt
        }

    def merge_question(self,params):
        """
        question：
            A substance in the solid phase (state) of matter has
        choices:
            1:a definite shape and a definite volume
            2:a definite shape, but no definite volume
            3:no definite shape, but a definite volume
            4:no definite shape and no definite volume
        :param params:
        :return:
        """
        target = "question:" + params["stem"] + "\n"
        choices = "\n".join([unit["label"]+":"+unit["text"] for unit in params["choices"]])
        return target + choices

    def combine_CseRo_prompt(self):
        cache_root = "experiments/cache/{dataset}/{settings}".format(
            dataset=self.args.dataset,
            settings=self.args.setting
        )
        if not os.path.exists(cache_root) or not os.path.isdir(cache_root):
            # 如果不存在，则创建目录
            os.makedirs(cache_root)
        for k, v in self._dataset.items():
            if k.startswith("ARC-c"):
                prompt = self._prompts["arc-c"]
                file_name = "ARC-c"
            else:
                prompt = self._prompts["arc-e"]
                file_name = "ARC-e"
            result = []
            for unit in tqdm(v,desc=file_name):
                answer = unit["answerKey"]
                cur_id = unit["id"]
                question = self.merge_question(unit["question"])
                instruction =prompt.format(questions=question)
                i = 0
                while i < 3:
                    # api 不稳定，最多可重复三次
                    model_output = self.model.infer(instruction)
                    if model_output != None:
                        break
                    i += 1
                data = {
                    "context": instruction,
                    "dataset": file_name,
                    "metadata": cur_id,
                    "label":answer,
                    "model_output":model_output if model_output != None else "error"
                }
                result.append(data)
            with open(os.path.join(cache_root, "{}.json".format(file_name)), "w", encoding="utf-8") as ft:
                json_data = json.dumps(result, ensure_ascii=False, indent=4)
                ft.write(json_data)