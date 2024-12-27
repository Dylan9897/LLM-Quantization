
from tqdm import tqdm
from transformers import AutoModelForCausalLM, AutoTokenizer,TextStreamer
from src.models import BaseModelInference,InputTypeError

class QwenModel(BaseModelInference):
    def __init__(self,model_path,config=None):
        super().__init__(model_path=model_path,config=config)
        self.model_name = model_path        
        

    def __repr__(self):
        return (f"{self.__class__.__name__}, "
                f"model is {self.model_name!r}")
                

    def load_model(self):
        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_path,
            torch_dtype="auto",
            device_map="auto"
        )
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_path,padding_side='left')


    def return_message(self,input_data,chat_mode):
        if not chat_mode:
            message = [
                {"role": "system", "content": "You are Qwen, created by Alibaba Cloud. You are a helpful assistant."},
                {"role": "user", "content":input_data}
            ]
        else:
            message = [{"role": "system", "content": "You are Qwen, created by Alibaba Cloud. You are a helpful assistant."}]+input_data
  

        text = self.tokenizer.apply_chat_template(
            message,
            tokenize=False,
            add_generation_prompt=True
        )
        return text

    def preprocess(self,input_data,chat_mode):
        if isinstance(input_data,str):
            input_data = [self.return_message(input_data)]
        else:
            for i,cur_elem in enumerate(input_data):
                input_data[i] = self.return_message(cur_elem,chat_mode)

        model_inputs = self.tokenizer(input_data , return_tensors="pt",padding=True).to(self.model.device)
        return model_inputs

    def postprocess(self,raw_output):
        ...

    def infer(self, input_data,chat_mode=False):
        if isinstance(input_data,str):
            model_inputs = self.preprocess(input_data)
            generated_ids = self.model.generate(
                **model_inputs,
                max_new_tokens=self.config.get("max_tokens",512)
            )

            generated_ids = [
                output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
            ]

            response = self.tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
            return response
            

        elif isinstance(input_data,list):
            batch_size = self.config.get("batch_size",2)
            total = len(input_data)
            data_iterator = iter(input_data)
   
            result = []
            with tqdm(total=total, desc="Processing batches", unit="items") as pbar:
                while True:
                    batch = list()
                    try:
                        for _ in range(batch_size):
                            elem = next(data_iterator)
                            batch.append(elem)
                        cur_data = self.preprocess(batch,chat_mode)
                        generated_ids = self.model.generate(
                                **cur_data,
                                max_new_tokens=self.config.get("max_tokens",512)
                            )
                        generated_ids = [
                            output_ids[len(input_ids):] for input_ids, output_ids in zip(cur_data.input_ids, generated_ids)
                        ]
                        response = self.tokenizer.batch_decode(generated_ids, skip_special_tokens=True)
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

        else:
             raise InputTypeError(f"Unsupported input type: {type(input_data).__name__}. Expected 'str' or 'list'.")





