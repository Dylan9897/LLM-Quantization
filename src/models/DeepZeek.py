# encoding : utf-8 -*-                            
# @author  : 冬瓜                              
# @mail    : dylan_han@126.com    
# @Time    : 2025/1/22 15:11
from openai import OpenAI
# import sys
# sys.path.append("/mnt/e/Github/ai-nlp-project-new/")
from conf.model_config import deep_zeek
from concurrent.futures import ThreadPoolExecutor, as_completed


class Model():
    def __init__(self):
        self.client = OpenAI(api_key=deep_zeek["api_key"], base_url=deep_zeek["base_url"])

    def infer(self,input_data):
        response = self.client.chat.completions.create(
            model=deep_zeek["model_name"],
            messages=[
                {"role": "system", "content": "You are a helpful assistant"},
                {"role": "user", "content": input_data},
            ],
            stream=False
        )
        try:
            return response.choices[0].message.content
        except:
            return None

    def infer_multi(self, data_list, max_workers=2):
        """
        :param data_list: list of questions to be inferred.
        :param max_workers: (optional) the maximum number of threads that can be used to execute the given calls.
        :return: list of inference results corresponding to the input data.
        """
        results = []

        # Use a context manager to properly manage resources.
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Map the infer function to the data_list using the executor.
            future_to_data = {executor.submit(self.infer, data): data for data in data_list}
            for future in as_completed(future_to_data):
                try:
                    result = future.result()  # Get the result of the infer method.
                    results.append(result)
                except Exception as exc:

                    print(f"Generated an exception: {exc}")

        return results

    def stream_infer(self,completion):
        for chunk in completion:
            if not chunk.choices:
                print("\nUsage:")
                print(chunk.usage)
            else:
                delta = chunk.choices[0].delta
                if hasattr(delta, 'reasoning_content') and delta.reasoning_content is not None:
                    # yield f"data: {delta.reasoning_content}\n\n"
                    print(f"data: {delta.reasoning_content}\n\n")
                else:
                    if delta.content != "":
                        # yield f"data: {delta.content}\n\n"
                        print(f"data: {delta.content}\n\n")



if __name__ == '__main__':

    model = Model()
    input_data = "窗前明月光"
    print(model.infer(input_data))
