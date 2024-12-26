
import argparse
import configparser

class ChatGPTSchema(object):
    def __init__(self, context=None,dataset_name="", metadata=""):
        self.context = context
        self.dataset = dataset_name
        self.metadata = metadata

    def to_dict(self):
        return {
            "context": self.context,
            "dataset": self.dataset,
            "metadata": self.metadata
        }


class BaseDatasetProcessor:
    def __init__(self,args: argparse.Namespace):
        self.dataset = args.dataset
        self.prompt_type = args.prompt_type
        self.chat_mode = args.chat_mode
        self.setting = args.setting
        self._dataset_path = None
        self._prompts_path = None
        self.dataset_config()

    def dataset_config(self):
        self.config = configparser.ConfigParser()
        self.config.read("src/dataset.ini", encoding="utf-8")

    def __repr__(self):
        return (f"{self.__class__.__name__}(dataset={self.dataset!r}, "
                f"prompt_type={self.prompt_type!r}, "
                f"chat_mode={self.chat_mode!r}, "
                f"setting={self.setting!r})")

    @property
    def dataset_path(self):
        """获取数据集路径"""
        return self._dataset_path

    def load_dataset(self):
        """加载数据集的方法，由子类实现"""
        raise NotImplementedError("子类必须实现load_dataset方法")

    @dataset_path.setter
    def dataset_path(self, value):
        """设置数据集路径并尝试加载数据集"""
        self._dataset_path = value
        self.load_dataset()

    @property
    def prompts_path(self):
        """获取提示词路径"""
        return self._prompts_path

    def load_prompts(self):
        """加载提示词的方法，由子类实现"""
        raise NotImplementedError("子类必须实现load_prompts方法")

    @prompts_path.setter
    def prompts_path(self, value):
        """设置提示词路径并尝试加载提示词"""
        self._prompts_path = value
        self.load_prompts()

    @property
    def combine_prompt(self):
        ...