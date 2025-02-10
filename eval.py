# -*- coding: utf-8 -*-
import re
import os
import json
import pandas as pd
from tqdm import tqdm

class Evaluate():
    def __init__(self,args):
        self.load_dataset_remark()
        self.args = args

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
        pattern = r"answer\|(\[.*?\])"
        match = re.search(pattern, text)
        if match:
            answers = match.group(1)  # 提取出的答案列表内容，不包括方括号
            return answers
        else:
            return None

    def extract_calculation(self,text):

        pattern = r"answer\|(.*?)\n"
        match = re.search(pattern, text)
        if match:
            answer = match.group(1)  # 提取出的答案，不包括 'answer|' 和 '\n'
            return answer
        else:
            return None

    def main(self):
        src_data_root = "experiments/cache/{}/{}".format(self.args.dataset,self.args.setting)
        predict_data_root = "experiments/result/{}/{}".format(self.args.dataset,self.args.setting)
        if not os.path.exists(predict_data_root) or not os.path.isdir(predict_data_root):
            # 如果不存在，则创建目录
            os.makedirs(predict_data_root)
        target_df = self.df[self.df["dataset"]==self.args.dataset]

        src_data_list = os.listdir(src_data_root)
        for file in src_data_list:
            file_name = file[:-5]
            cur_df = target_df[target_df["data_file_name"]==file_name]
            types = list(cur_df["question_type"])[0]

            with open(os.path.join(predict_data_root, file), "r", encoding="utf-8") as fl:
                with open(os.path.join(src_data_root, file), "r", encoding="utf-8") as fl2:
                    eval_data = json.load(fl)
                    src_data = json.load(fl2)


                    if types == "single_choice":
                        for i,elem in enumerate(eval_data):
                            cur_answer = self.extract_single_choice(elem)
                            src_data[i]["predict"] = elem
                            src_data[i]["predict_answer"] = cur_answer

                    elif types == "multi_choice":
                        for i, elem in enumerate(eval_data):
                            cur_answer = self.extract_multi_choice(elem)
                            src_data[i]["predict"] = elem
                            src_data[i]["predict_answer"] = cur_answer

                    elif types == "calculation":
                        for i, elem in enumerate(eval_data):
                            cur_answer = self.extract_calculation(elem)
                            src_data[i]["predict"] = elem
                            src_data[i]["predict_answer"] = cur_answer

                    elif types == "judgement":
                        for i, elem in enumerate(eval_data):
                            cur_answer = self.extract_judgement(elem)
                            src_data[i]["predict"] = elem
                            src_data[i]["predict_answer"] = cur_answer

                    elif types == "explanation":
                        ...



                    else:
                        raise Exception("error")
            # with open(os.path.join(predict_data_root, file), "w", encoding="utf-8") as ft:
            #     json_data = json.dumps(src_data,ensure_ascii=False,indent=4)
            #     ft.write(json_data)

    def cal_Compliance(self,data):
        """
        统计模型对指令的服从性
        :return:
        """
        k = 0
        for unit in tqdm(data):
            if unit.get("predict_answer",None):
                k+=1
        return k/len(data)

    def cal_Accuracy(self,data,file_name):
        """
        计算模型的准确率
        :return:
        """
        k = 0
        line = self.df[self.df["data_file_name"]==file_name]
        question_type = list(line["question_type"])[0]

        for unit in tqdm(data):
            predict_answer = unit.get("predict_answer",None)
            answer = unit["answer"] if unit["answer"] else unit["label"]
            if question_type == "multi_choice" and predict_answer:
                predict_answer=eval(predict_answer)
            if predict_answer == answer:
                k+=1
        return k/len(data)

    def evaluate(self,report=True):
        ## 获取预测的指标信息
        predict_data_root = "experiments/result/{}/{}".format(self.args.dataset,self.args.setting)
        file_list = os.listdir(predict_data_root)
        for file in file_list:

            file_name = file[:-5]
            file_path = os.path.join(predict_data_root,file)
            print(f"当前模型的文件为：{file_path}")
            with open(file_path,'r',encoding="utf-8") as fl:
                data = json.load(fl)
                compliance_result = self.cal_Compliance(data)
                accuracy_result = self.cal_Accuracy(data,file_name)
                print(compliance_result)
                print(accuracy_result)
                s = input()



if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description="LLM reasoning and quantitative evaluation ...")
    parser.add_argument("--dataset", default="AGIEval", type=str)
    parser.add_argument("--setting", default='GseRo', type=str,
                        help="choose an reasoning mode ['GseRo']")
    args = parser.parse_args()
    func = Evaluate(args)
    func.main()
    func.evaluate()







