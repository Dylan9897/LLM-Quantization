# encoding : utf-8 -*-                            
# @author  : 冬瓜                              
# @mail    : dylan_han@126.com    
# @Time    : 2025/3/3 17:59
import json
import os
import pandas as pd
from src.processor import BaseDatasetProcessor,ChatGPTSchema
from src.prompts import AGIEval as prompts_mapping
from src.models.Model import Model
from tqdm import tqdm

class CEVAL(BaseDatasetProcessor):
    def __init__(self,args):
        super().__init__(args=args)
        self.args = args
        self._dataset = {}
        self._prompts = {}
        self.load_dataset()
        self.load_prompts()
        self.model = Model()
        self.config = {
            "accountant": "注册会计师",
            "advanced_mathematics": "高等数学",
            "art_studies": "艺术学",
            "basic_medicine": "基础医学",
            "business_administration": "工商管理",
            "chinese_language_and_literature": "中国语言文学",
            "civil_servant": "公务员",
            "clinical_medicine": "临床医学",
            "college_chemistry": "大学化学",
            "college_economics": "大学经济学",
            "college_physics": "大学物理",
            "college_programming": "大学编程",
            "computer_architecture": "计算机组成原理",
            "computer_network": "计算机网络",
            "discrete_mathematics": "离散数学",
            "education_science": "教育学",
            "electrical_engineer": "注册电气工程师",
            "environmental_impact_assessment_engineer": "环境影响评价工程师",
            "fire_engineer": "注册消防工程师",
            "high_school_biology": "高中生物",
            "high_school_chemistry": "高中化学",
            "high_school_chinese": "高中语文",
            "high_school_geography": "高中地理",
            "high_school_history": "高中历史",
            "high_school_mathematics": "高中数学",
            "high_school_physics": "高中地理",
            "high_school_politics": "高中政治",
            "ideological_and_moral_cultivation": "思想道德修养与法律基础",
            "law": "法学",
            "legal_professional": "法律职业资格",
            "logic": "逻辑学",
            "mao_zedong_thought": "毛泽东思想和中国特色社会主义理论体系概论",
            "marxism": "马克思主义基本原理",
            "metrology_engineer": "注册计量师",
            "middle_school_biology": "初中生物",
            "middle_school_chemistry": "初中化学",
            "middle_school_geography": "初中地理",
            "middle_school_history": "初中历史",
            "middle_school_mathematics": "初中数学",
            "middle_school_physics": "初中物理",
            "middle_school_politics": "初中政治",
            "modern_chinese_history": "近代史纲要",
            "operating_system": "操作系统",
            "physician": "医师资格",
            "plant_protection": "植物保护",
            "probability_and_statistics": "概率统计",
            "professional_tour_guide": "导游资格",
            "sports_science": "体育学",
            "tax_accountant": "税务师",
            "teacher_qualification": "教师资格",
            "urban_and_rural_planner": "注册城乡规划师",
            "veterinary_medicine": "兽医学"
        }

    def load_dataset(self):
        dataset_path = self.config.get(self.dataset, "data_path")
        if os.path.isdir(dataset_path):
            file_list = os.listdir(dataset_path)
            # cache = {}
            for file in file_list:
                if not file.endswith("csv"):
                    continue
                # cache[file[:-8]]= ""
                file_path = os.path.join(dataset_path,file)
                df = pd.read_csv(file_path)
                cur_data = []
                for i in df.index:
                    line = df.loc[i]
                    question = line["question"]
                    options = [
                        "(A) " + line["A"],
                        "(B) " + line["B"],
                        "(C) " + line["C"],
                        "(D) " + line["D"],
                    ]
                    index = line["id"]
                    cur_data.append(
                        {
                            "index":index,
                            "question":question,
                            "options":options,
                            "answer":line["answer"]
                        }
                    )

                self._dataset[file[:-4]] = cur_data
            # print(json.dumps(cache,ensure_ascii=False,indent=4))
        else:
            print(f"数据集文件不存在或未设置：{self.dataset_path}")

    def load_prompts(self):
        dataset_path = self.config.get(self.dataset, "prompt_path")
        if os.path.isdir(dataset_path):
            file_list = os.listdir(dataset_path)
            for file in file_list:
                file_path = os.path.join(dataset_path, file)
                df = pd.read_csv(file_path)
                self._prompts[file[:-8]] = df
        else:
            print(f"提示词文件不存在或未设置：{self.dataset_path}")

    def prepare_prompt(self,data):
        examples = []
        for i in data.index:
            line = data.loc[i]
            example = "question{}: ".format(i+1)+line["question"] + "\n"
            example+= "options:"+"\n"
            for tag in ["A","B","C","D"]:
                example+="  ({}) ".format(tag) + line[tag]

            example += "output:" + "\n" + "answer|{}".format(line["answer"])
            examples.append(example)

        return examples[:2]

    def combine_CseRo_prompt(self):

        cache_root = "experiments/cache/{dataset}/{settings}".format(
            dataset=self.args.dataset,
            settings = self.args.setting
        )

        if not os.path.exists(cache_root) or not os.path.isdir(cache_root):
            # 如果不存在，则创建目录
            os.makedirs(cache_root)

        # print(self._prompts.keys())
        for dataset_name,data in self._dataset.items():
            description = self.config[dataset_name[:-4]]
            # print(f"dataset is {dataset_name}, description is {description}")

            prompt_df = self._prompts[dataset_name[:-4]]
            prompts = self.prepare_prompt(prompt_df)

            cur_result = []
            for idx,line in enumerate(tqdm(data,desc=dataset_name)):
                instruction = "--Goal--"+"\n" + prompts_mapping.zh_prefix.format(description=description)+"\n"
                instruction += "--steps--" + "\n" + prompts_mapping.zh_steps + "\n"

                instruction += """
                ######################
                --Examples--
                ######################
                """

                instruction += "\n".join(prompts)

                instruction+="""
                ######################
                --Real Data--
                ######################
                """

                instruction += "question: "+line["question"]

                instruction += "options:"+"\n"

                instruction += "  \n".join(line["options"])

                instruction += "\noutput:"

                i = 0
                while i < 3:
                    # api 不稳定，最多可重复三次
                    model_output = self.model.infer(instruction)
                    if model_output != None:
                        break
                    i += 1


                cur_result.append(
                    {
                        "metadata":idx+1,
                        "context":instruction,
                        "dataset":dataset_name[:-4],
                        "label": line["answer"],
                        "model_output":model_output if model_output != None else "error"
                    }
                )
            with open(os.path.join(cache_root,"{}.json".format(dataset_name[:-4])),"w",encoding="utf-8") as ft:
                json_data = json.dumps(cur_result,ensure_ascii=False,indent=4)
                ft.write(json_data)








