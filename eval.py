# -*- coding: utf-8 -*-
import re
import os
import json
import pandas as pd
from tqdm import tqdm
from src.models.Model import Model
from src.utils.logger import logger

class Evaluate():
    def __init__(self,args):
        self.load_dataset_remark()
        self.args = args
        self.model = Model()

    def load_dataset_remark(self):
        self.df = pd.read_excel("conf/dataset.xlsx")

    def extract_single_choice(self,text):
        """
        使用正则表达式从文本中提取选项答案
        参数:
            text: str, 格式为 "answer|A" 的文本
        返回:
            str: 提取出的选项字母，如果格式错误则返回错误信息
        示例:
            >>> extract_single_choice("这是正确答案|A")
            'A'
        """
        text = text.replace("\n","")
        try:
            # 正则表达式模式
            # .+表示任意字符(除换行符外)出现一次或多次
            # \| 转义竖线字符
            # [A-Za-z] 匹配一个字母
            # $ 确保答案后没有其他内容
            pattern = r'.+\|([A-Za-z])'

            # 查找匹配
            match = re.match(pattern, text.strip())

            if not match:
                raise ValueError("格式错误，应为'答案|字母选项'格式")

            # 返回大写的选项字母
            return match.group(1).upper()

        except Exception as e:
            return None

    def extract_multi_choice(self,text):
        text = text.replace("\n","")
        pattern = r"answer\|(\[.*?\])"
        match = re.search(pattern, text)
        if match:
            answers = match.group(1)  # 提取出的答案列表内容，不包括方括号
            return answers
        else:
            return None

    def extract_calculation(self,text):
        text = text.replace("\n","")
        pattern = r"answer\|(.*?)$"
        match = re.search(pattern, text)
        if match:
            answer = match.group(1)  # 提取出的答案，不包括 'answer|' 和 '\n'
            return answer
        else:
            return None

    def extract_judgement(self,text):
        text = text.replace("\n", "")
        pattern = r"answer\|(False|True|Yes|No)"
        match = re.search(pattern, text)
        if match:
            answer = match.group(1)  # 提取出的答案，不包括 'answer|' 和 '\n'
            return answer
        else:
            return None


    def evaluate(self,report=True):
        ## 获取预测的指标信息
        predict_data_root = "experiments/cache/{}/{}".format(self.args.dataset,self.args.setting)
        file_list = os.listdir(predict_data_root)
        target_df = self.df[self.df["dataset"]==self.args.dataset]
        for file in file_list:

            file_name = file[:-5]
            file_path = os.path.join(predict_data_root,file)
            
            file_name = file[:-5]
            cur_df = target_df[target_df["data_file_name"]==file_name]
            types = list(cur_df["question_type"])[0]
            logger.info(f"当前模型的文件为：{file_path}, 类型为：{types}")
            accuracy = 0
            compliance = 0
            with open(file_path,'r',encoding="utf-8") as fl:
                data = json.load(fl)
                for i,elem in enumerate(data):
                    if types == "single_choice":
                        cur_answer = self.extract_single_choice(elem['model_output'])
                        if cur_answer != None:
                            compliance += 1
                        if cur_answer == elem["label"]:
                            accuracy += 1

                    elif types == "multi_choice":
                        cur_answer = self.extract_multi_choice(elem['model_output'])
                        if isinstance("cur_answer",str):
                            try:
                                cur_answer = eval(cur_answer)
                            except:
                                cur_answer = cur_answer
                        if cur_answer != None:
                            compliance += 1
                        if cur_answer == elem["label"]:
                            accuracy += 1

                    elif types == "calculation":
                        prompt = "请判断当前的回答的内容是否正确：预测：{predict}，正确答案：{answer}，如果正确，请输出'yes'，否则输出'no'，不要输出其他信息"
                        
                        cur_answer = self.extract_calculation(elem['model_output'])
                        if cur_answer != None:
                            compliance += 1

                        else:
                            cur_answer = "Unknown"
                        instruction = prompt.format(predict=cur_answer, answer=elem["answer"])
                        response = self.model.infer(instruction)
                        if response == "yes":
                            accuracy += 1
                        
                    elif types == "judgement":
                        cur_answer = self.extract_judgement(elem['model_output'])
                        if cur_answer != None:
                            compliance += 1
                        if cur_answer == elem["label"]:
                            accuracy += 1
                    elif types == "explanation":
                        ...

                    else:
                        raise Exception("error")

            logger.info(f"file name is {file_name}, accuracy is {accuracy/len(data)}, compliance is {compliance/len(data)}")
            s = input("push ...")

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description="LLM reasoning and quantitative evaluation ...")
    parser.add_argument("--dataset", default="BBH", type=str)
    parser.add_argument("--setting", default='GseRo', type=str,
                        help="choose an reasoning mode ['GseRo']")
    args = parser.parse_args()
    func = Evaluate(args)
    func.evaluate()






