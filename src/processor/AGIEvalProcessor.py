import os
import json

import pandas as pd
import ast
import tiktoken
from src.processor import BaseDatasetProcessor,ChatGPTSchema
from src.utils.utils import read_jsonl
from src.utils.config import AGIEvalMappings

class AGIEval(BaseDatasetProcessor):
    def __init__(self,args):
        super().__init__(args=args)
        self._dataset = {}
        self._prompts = None
        self.enc = tiktoken.get_encoding("cl100k_base")
        self.enc = tiktoken.encoding_for_model("gpt-4")
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
            self._prompts = prompt_path
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


    def concat_prompt(self,dataset_name):
        load_explanation = self.setting == 'few-shot-CoT'
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
        for idx, (con, exp) in enumerate(zip(contexts, explanations)):
            passage = con["passage"] if con["passage"] is not None and not skip_passage else ""
            question = con["question"]
            options = con["options"] if con["options"] is not None else ""
            label = con["label"] if con["label"] is not None else ""
            answer = con["answer"] if "answer" in con and con["answer"] is not None else ""

            if dataset_name in AGIEvalMappings["english_qa_datasets"]:
                question_input = "Problem {}.   ".format(idx + 1) + passage + " " + question + "\n" \
                                 + "Choose from the following options:    " + " ".join(options) + "\n"
                question_output = (("Explanation for Problem {}:   ".format(
                    idx + 1) + exp + "\n") if load_explanation else "") \
                                  + "The answer is therefore {}".format(label)

            elif dataset_name in AGIEvalMappings["chinese_qa_datasets"]:
                question_input = "问题 {}.   ".format(idx + 1) + passage + " " + question + "\n" \
                                 + "从以下选项中选择:    " + " ".join(options) + "\n"
                question_output = (("问题 {}的解析:   ".format(idx + 1) + exp + "\n") if load_explanation else "") \
                                  + "答案是 {}".format(label)

            elif dataset_name in AGIEvalMappings["english_cloze_datasets"]:
                question_input = "Problem {}.   ".format(idx + 1) + question + "\n"
                question_output = (("Explanation for Problem {}:   ".format(
                    idx + 1) + exp + "\n") if load_explanation else "") \
                                  + "The answer is therefore {}".format(answer)

            elif dataset_name in AGIEvalMappings["chinese_cloze_datasets"]:
                question_input = "问题 {}.   ".format(idx + 1) + question + "\n"
                question_output = (("问题 {}的解析:   ".format(idx + 1) + exp + "\n") if load_explanation else "") \
                                  + "答案是 {}".format(answer)
            else:
                raise ValueError(f"During loading few-sot examples, found unknown dataset: {dataset_name}")
            if chat_mode:
                demostrations.append((question_input, question_output))
            else:
                demostrations.append(question_input + question_output + '\n')

        return demostrations

    def concat_prompt_chat_mode(self,demos, dataset_name, max_tokens, end_of_example="\n", verbose=False):
        answers = []
        sentences = ""
        for i in range(len(demos)):
            answers += [
                {"role": "user", "content": demos[i][0]},
                {"role": "assistant", "content": demos[i][1]},
            ]
            sentences += json.dumps(answers[-1])
            # break if reach max token limit
            if len(self.enc.encode(sentences)) > max_tokens:
                answers.pop()
                answers.pop()
                break
        if verbose:
            print("max_tokens set as ", max_tokens, "actual_tokens is", len(self.enc.encode(sentences)), "num_shot is",
                  len(answers) // 2)
        return answers, len(answers) // 2

    def concat_data_prompt(self,demos, dataset_name, max_tokens, end_of_example="\n", verbose=False):
        demostration_en = "Here are the answers for the problems in the exam.\n"
        demostration_zh = "以下是考试中各个问题的答案。\n"

        for i in range(len(demos)):
            # print(len(enc.encode(demostration_en)), len(enc.encode(demostration_zh)))
            if dataset_name in AGIEvalMappings["english_qa_datasets"]:
                demostration_en = demostration_en + demos[i] + end_of_example
            elif dataset_name in AGIEvalMappings["chinese_qa_datasets"]:
                demostration_zh = demostration_zh + demos[i] + end_of_example
            elif dataset_name in AGIEvalMappings["english_cloze_datasets"]:
                demostration_en = demostration_en + demos[i] + end_of_example
            elif dataset_name in AGIEvalMappings["chinese_cloze_datasets"]:
                demostration_zh = demostration_zh + demos[i] + end_of_example
            # break if reach max token limit
            if len(self.enc.encode(demostration_en)) < max_tokens and len(self.enc.encode(demostration_zh)) < max_tokens:
                output = demostration_en if len(demostration_en) > len(demostration_zh) else demostration_zh
                prompt_num = i + 1
            else:
                break
        if verbose:
            print("max_tokens set as ", max_tokens, "actual_tokens is", len(self.enc.encode(output)), "num_shot is",
                  prompt_num)
        return output, prompt_num

    def convert_few_shot(self,line, dataset_name, demo, n_shot, chat_mode=False):
        passage = line["passage"] if line["passage"] is not None else ""
        question = line["question"]
        options = line["options"] if line["options"] is not None else ""

        if dataset_name in AGIEvalMappings["english_qa_datasets"]:
            question_input = "Problem {}.   ".format(n_shot + 1) + passage + " " + question + "\n" \
                             + "Choose from the following options:    " + " ".join(options) + "\n"
            # + "Explanation for Problem {}:   ".format(n_shot + 1)

        if dataset_name in AGIEvalMappings["chinese_qa_datasets"]:
            question_input = "问题 {}.   ".format(n_shot + 1) + passage + " " + question + "\n" \
                             + "从以下选项中选择:    " + " ".join(options) + "\n"
            # + "问题 {}的解析:   ".format(n_shot + 1)

        if dataset_name in AGIEvalMappings["english_cloze_datasets"]:
            question_input = "Problem {}.   ".format(n_shot + 1) + question + "\n"
            # + "Explanation for Problem {}:   ".format(n_shot + 1)

        if dataset_name in AGIEvalMappings["chinese_cloze_datasets"]:
            question_input = "问题 {}.   ".format(n_shot + 1) + question + "\n"
            # + "问题 {}的解析:   ".format(n_shot + 1)
        if chat_mode:
            return demo + [
                {"role": "user", "content": question_input},
            ]
        else:
            return demo + question_input


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
            for dataset_name, datas in self._dataset.items():
                processed_demos = self.concat_prompt(dataset_name)
                if self.chat_mode:
                    chosen_prompt, n_shot = self.concat_prompt_chat_mode(
                        processed_demos, dataset_name, max_tokens=2048, end_of_example="<END>\n", verbose=False)


                else:
                    chosen_prompt, n_shot = self.concat_data_prompt(
                        processed_demos, dataset_name, max_tokens=2048, end_of_example="<END>\n", verbose=False)
                processed = []
                for meta_idx, line in enumerate(datas):
                    ctxt = self.convert_few_shot(line, dataset_name, chosen_prompt, n_shot, self.chat_mode)
                    new_instance = ChatGPTSchema(context=ctxt, dataset_name=dataset_name, metadata=meta_idx)

                    processed.append(new_instance.to_dict())

                self._dataset[dataset_name] = processed
                cache_root = os.path.join("experiments/cache", self.setting)
                os.makedirs(cache_root, exist_ok=True)
                with open(os.path.join(cache_root, "{}.json".format(dataset_name)), "w", encoding="utf-8") as ft:
                    json_data = json.dumps(processed, ensure_ascii=False, indent=4)
                    ft.write(json_data)

