from tqdm import tqdm

from abc import ABC, abstractmethod
from vllm import LLM, SamplingParams


class Model(ABC):
    def __init__(self,model_path,config,args=None):
        """
        初始化模型推理类。

        :param model_path: 模型文件或目录路径
        :param config: 配置参数字典，默认为 None
        """
        self.model_path = model_path
        self.config = config or {}
        self.args = args
        self.load_model()

    def load_model(self):
        model_name = self.model_path.split("/")[-1]
        
        params = self.config[model_name]
        self.sample_params = SamplingParams(
            temperature=params["sample"]["temperature"],
            top_p=params["sample"]["top_p"],
            max_tokens = 1024
            )

        if not self.args.quantize:
            self.model = LLM(model=self.model_path)
        # elif self.args.quantize == "inf8":
        #     print("params is \n",params["inf8"])
        #     self.model=LLM(
        #         model=self.model_path,
        #         max_num_seqs=params["inf8"]["max_num_seqs"],
        #         max_model_len=params["inf8"]["max_model_len"],
        #         block_size=params["inf8"]["block_size"],
        #         device=params["inf8"]["device"],
        #         quantization=params["inf8"]["quantization"],
        #         override_neuron_config=params["inf8"]["override_neuron_config"],
        #         tensor_parallel_size=params["inf8"]["tensor_parallel_size"]
        #     )

    def operate_result(self,params):
        result = []
        for output in params:
            print(output)
            generated_text = output.outputs[0].text
            result.append(generated_text)
        return result

        
    def infer(self,input_data):
        result = []
        batch_size = self.args.batch_size
        total = len(input_data)
        data_iterator = iter(input_data)
        with tqdm(total=total, desc="Processing batches", unit="items") as pbar:
            while True:
                batch = list()
                try:
                    for _ in range(batch_size):
                        elem = next(data_iterator)
                        batch.append(elem)
            
                    cur_result = self.model.generate(
                        batch,
                        self.sample_params
                    )
                    response = self.operate_result(cur_result)
                    result.extend(response)
                    pbar.update(batch_size)  # 更新进度条
                except StopIteration:
                    # 如果数据不足一个批次，则只处理剩余的数据
                    if len(batch) == 0:
                        break
                    pass

                # 如果最后一批次小于设定的batch_size，则跳出循环
                if len(batch) < batch_size:
                    break
        return result

