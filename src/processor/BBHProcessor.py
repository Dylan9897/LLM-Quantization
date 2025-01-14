import json
import os
from src.processor import BaseDatasetProcessor,ChatGPTSchema
from src.utils.utils import read_jsonl,read_txt

class BBH(BaseDatasetProcessor):
    def __init__(self,args):
        super().__init__(args=args)
        self._dataset = {}
        self._prompts = {}
        self.load_dataset()
        self.load_prompts()

    def load_dataset(self):
        """
        从给定的路径加载数据集到内存。
        """
        dataset_path = self.config.get(self.dataset, "data_path")

        if os.path.isdir(dataset_path):
            file_root = os.path.join(dataset_path,"data")
            file_list = os.listdir(file_root)
            for file in file_list:
                if file.endswith("json"):
                    file_path = os.path.join(file_root,file)
                    with open(file_path,"r",encoding="utf-8") as fl:
                        data = json.load(fl)
                        self._dataset[file[:-5]] = data["examples"]

        else:
            print(f"数据集文件不存在或未设置：{self.dataset_path}")

    def split_description_example(self,data):
        description = []
        example = []
        tag = False
        data = data.split("\n")
        for line in data:
            if line.startswith("Q"):
                tag = True

            if tag:
                example.append(line)
            else:
                description.append(line)
        instruction = "--Goal--"+"\n"
        instruction += "\n".join(description)
        instruction += "\n" + "--Example--" + "\n"
        count = 1
        instruction += "\n" + "Example{}:".format(count) + '\n'*2
        for unit in example:

            if unit != "":
                instruction+=unit+'\n'
            else:
                count+=1
                instruction += '\n'+"Example{}:".format(count) + '\n'
                instruction += ""+"\n"
        instruction+="""#######
--Real Data--
{questions}
#######
Output:
"""
        return instruction

    def load_prompts(self):
        prompt_path = self.config.get(self.dataset, "prompt_path")
        file_list = os.listdir(prompt_path)
        for file in file_list:

            prompt_file = os.path.join(prompt_path,file)
            with open(prompt_file,"r",encoding="utf-8") as fl:
                fl = fl.read()
                instruction = self.split_description_example(fl)
                self._prompts[
                    file[:-4]
                ] = instruction

    def combine_prompt(self):
        for k, v in self._dataset.items():
            instruction = self._prompts[k]
            result = []
            for i,unit in enumerate(v):
                if k != "dyck_languages":

                    data = {
                        "context": instruction.format(questions=unit["input"]),
                        "dataset": k,
                        "metadata": i
                    }
                else:
                    instructions = instruction.split("{questions}\n")
                    data = {
                        "context": instructions[0] + "\n"+unit["input"] + "\n"+instructions[1],
                        "dataset": k,
                        "metadata": i
                    }
                result.append(data)
            with open("experiments/cache/{}/{}.json".format(self.dataset,k), "w", encoding="utf-8") as ft:
                json_data = json.dumps(result, ensure_ascii=False, indent=4)
                ft.write(json_data)








