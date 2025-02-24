# encoding : utf-8 -*-                            
# @author  : 冬瓜                              
# @mail    : dylan_han@126.com    
# @Time    : 2025/2/17 11:01
import os
import json
import random

import pandas as pd
import ast
import tiktoken
from src.processor import BaseDatasetProcessor,ChatGPTSchema
from src.utils.utils import read_jsonl
from src.utils.config import AGIEvalMappings
from src.prompts import AGIEval as prompts_mapping
from src.models.DeepZeek import Model
from tqdm import tqdm
class AGIEval(BaseDatasetProcessor):
    def __init__(self,args):
        super().__init__(args=args)
        self._dataset = {}
        self._prompts = None
        self.enc = tiktoken.get_encoding("cl100k_base")
        self.enc = tiktoken.encoding_for_model("gpt-4")
        self.load_dataset()
        self.load_prompts()
        self.args = args
        self.model = Model()

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
            self._prompts = prompt_path
        else:
            print(f"提示词文件不存在或未设置：{self.prompts_path}")

    def concat_CseRo_prompt(self,dataset_name):
        load_explanation = self.setting == 'GseRo'
        chat_mode = self.chat_mode
        skip_passage = False
        if dataset_name == 'sat-en-without-passage':
            skip_passage = True
            dataset_name = "sat-en"
        demostrations = []
        # read the prompts by context and explanation
        context_row = [0, 1, 3, 5, 7, 9]
        # 解释
        explanation_row = [0, 2, 4, 6, 8, 10]

        # saamples 行
        raw_prompts_context = pd.read_csv(self._prompts, header=0, skiprows=lambda x: x not in context_row,
                                          keep_default_na=False)

        # explan 行
        raw_prompts_explanation = pd.read_csv(self._prompts, header=0, skiprows=lambda x: x not in explanation_row,
                                              keep_default_na=False).replace(r'\n\n', '\n', regex=True)

        contexts = []
        for line in list(raw_prompts_context[dataset_name]):
            if line:
                contexts.append(ast.literal_eval(line))

        ##################################################

        explanations = [exp for exp in raw_prompts_explanation[dataset_name] if exp]
        contexts = random.sample(contexts,2)
        explanations = random.sample(explanations,2)
        instruction = ""
        for idx, (con, exp) in enumerate(zip(contexts, explanations)):

            passage = con["passage"] if con["passage"] is not None and not skip_passage else ""
            question = con["question"]
            options = con["options"] if con["options"] is not None else ""
            label = con["label"] if con["label"] is not None else ""
            answer = con["answer"] if "answer" in con and con["answer"] is not None else ""

            if dataset_name in AGIEvalMappings["english_qa_datasets"]:
                if idx == 0:
                    instruction += "--Goal--"+"\n\n"
                    description = prompts_mapping.descrips[dataset_name]

                    instruction += prompts_mapping.en_prefix.format(description=description)+"\n"

                    instruction += prompts_mapping.en_steps+"\n"

                    instruction += "--Examples--"+"\n"

                question_input = "Problem {}   ".format(idx + 1) + "\n" + passage + " " + question + "\n" \
                                 + "Choose from the following options:    " + " ".join(options) + "\n"
                question_output = "answer|{}".format(label)+ "\n"+(("Explanation for Problem {}:   ".format(
                    idx + 1) + exp + "\n") if load_explanation else "")

                instruction+=question_input + "\n" + question_output

            elif dataset_name in AGIEvalMappings["chinese_qa_datasets"]:
                if idx == 0:
                    instruction += "--Goal--"+"\n\n"
                    description = prompts_mapping.descrips[dataset_name]

                    instruction += prompts_mapping.zh_prefix.format(description=description)+"\n"

                    instruction += prompts_mapping.zh_steps+"\n"

                    instruction += "--Examples--"+"\n"

                question_input = "问题 {}.   ".format(idx + 1) + "\n" + passage + " " + question + "\n" \
                                 + "从以下选项中选择:    " + " ".join(options) + "\n"
                question_output = "answer|{}".format(label)+ "\n"+(("问题 {}的解析:   ".format(idx + 1) + exp + "\n") if load_explanation else "")
                instruction += question_input + "\n" + question_output


            elif dataset_name in AGIEvalMappings["english_cloze_datasets"]:
                if idx == 0:
                    instruction += "--Goal--"+"\n\n"
                    description = prompts_mapping.descrips[dataset_name]

                    instruction += prompts_mapping.en_prefix.format(description=description)+"\n"

                    instruction += prompts_mapping.en_steps+"\n"

                    instruction += "--Examples--"+"\n"

                question_input = "Problem {}.   ".format(idx + 1) + question + "\n"
                question_output = "answer|{}".format(answer)+"\n"+(("Explanation for Problem {}:   ".format(
                    idx + 1) + exp + "\n") if load_explanation else "")
                instruction += question_input + "\n" + question_output

            elif dataset_name in AGIEvalMappings["chinese_cloze_datasets"]:
                if idx == 0:
                    instruction += "--Goal--"+"\n\n"
                    description = prompts_mapping.descrips[dataset_name]

                    instruction += prompts_mapping.zh_prefix.format(description=description)+"\n"

                    instruction += prompts_mapping.zh_steps+"\n"

                    instruction += "--Examples--"+"\n"

                question_input = "问题 {}.   ".format(idx + 1) + question + "\n"
                question_output = "answer|{}".format(answer)+"\n"+(("问题 {}的解析:   ".format(idx + 1) + exp + "\n") if load_explanation else "")
                instruction += question_input + "\n" + question_output
            else:
                raise ValueError(f"During loading few-sot examples, found unknown dataset: {dataset_name}")

        return instruction

    def convert_CseRo_few_shot(self,prefix,line, dataset_name):
        prefix += """
        #########################
        --Real data--
        #########################
        """
        passage = line["passage"] if line["passage"] is not None else ""
        question = line["question"]
        options = line["options"] if line["options"] is not None else ""

        if dataset_name in AGIEvalMappings["english_qa_datasets"]:
            question_input = "Problem: "+"\n" + passage + " " + question + "\n" \
                             + "Choose from the following options:    " + " ".join(options) + "\n"
            # + "Explanation for Problem {}:   ".format(n_shot + 1)

        if dataset_name in AGIEvalMappings["chinese_qa_datasets"]:
            question_input = "问题：  "+"\n" + passage + " " + question + "\n" \
                             + "从以下选项中选择:    " + " ".join(options) + "\n"
            # + "问题 {}的解析:   ".format(n_shot + 1)

        if dataset_name in AGIEvalMappings["english_cloze_datasets"]:
            question_input = "Problem:   "+"\n" + question + "\n"
            # + "Explanation for Problem {}:   ".format(n_shot + 1)

        if dataset_name in AGIEvalMappings["chinese_cloze_datasets"]:
            question_input = "问题:   "+"\n" + question + "\n"
            # + "问题 {}的解析:   ".format(n_shot + 1)

        return prefix + question_input

    def combine_CseRo_prompt(self):
        cache_root = "experiments/cache/AGIEval/GseRo"

        if not os.path.exists(cache_root) or not os.path.isdir(cache_root):
            # 如果不存在，则创建目录
            os.makedirs(cache_root)
        else:
            # 如果目录已经存在，则跳过创建
            print(f"Directory '{cache_root}' already exists, skipping creation.")

        for dataset_name, datas in self._dataset.items():
            processed = []
            processed_demos = self.concat_CseRo_prompt(dataset_name)
            for meta_idx, line in enumerate(tqdm(datas,desc=dataset_name)):
                ctxt = self.convert_CseRo_few_shot(processed_demos,line, dataset_name)
                new_instance = ChatGPTSchema(context=ctxt, dataset_name=dataset_name, metadata=meta_idx)
                new_instance=new_instance.to_dict()
                new_instance["answer"] = line.get("answer","")
                new_instance["label"] = line["label"]

                i = 0
                while i < 3:
                    # api 不稳定，最多可重复三次
                    model_output = self.model.infer(new_instance["context"])
                    if model_output != None:
                        break
                    i+=1

                new_instance["model_output"] = model_output if model_output != None else "error"
                processed.append(new_instance)

            self._dataset[dataset_name] = processed
            with open(os.path.join(cache_root, "{}.json".format(dataset_name)), "w", encoding="utf-8") as ft:
                json_data = json.dumps(processed, ensure_ascii=False, indent=4)
                ft.write(json_data)
