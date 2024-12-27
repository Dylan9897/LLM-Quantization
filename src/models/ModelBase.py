from abc import ABC, abstractmethod
import logging

class InputTypeError(TypeError):
    """Custom exception for unsupported input types."""
    ...

class BaseModelInference(ABC):
    def __init__(self, model_path, config=None):
        """
        初始化模型推理类。

        :param model_path: 模型文件或目录路径
        :param config: 配置参数字典，默认为 None
        """
        self.model_path = model_path
        self.config = config or {}
        self._model = None
        self._tokenizer = None
        self.logger = logging.getLogger(self.__class__.__name__)
        self.load_model()

    @abstractmethod
    def load_model(self):
        """加载模型的具体实现由子类完成"""
        ...

    @abstractmethod
    def preprocess(self, input_data):
        """
        对输入数据进行预处理。

        :param input_data: 输入的数据，类型取决于具体应用
        :return: 预处理后的数据，准备传递给模型
        """
        ...

    @abstractmethod
    def postprocess(self, raw_output):
        """
        对模型的原始输出进行后处理。

        :param raw_output: 模型生成的原始输出
        :return: 处理后的最终输出结果
        """
        ...

    def infer_non_streaming(self, input_data):
        """
        执行非流式推理。

        :param input_data: 输入的数据
        :return: 推理结果
        """
        processed_input = self.preprocess(input_data)
        raw_output = self._model.infer(processed_input)  # 假设模型有一个 infer 方法
        result = self.postprocess(raw_output)
        return result

    def infer_streaming(self, input_data, chunk_size=1024):
        """
        执行流式推理。

        :param input_data: 输入的数据
        :param chunk_size: 流式推理时每个块的大小
        :yield: 每次迭代返回一部分推理结果
        """
        processed_input = self.preprocess(input_data)
        for chunk in self._model.stream_infer(processed_input, chunk_size):  # 假设模型有 stream_infer 方法
            processed_chunk = self.postprocess(chunk)
            yield processed_chunk