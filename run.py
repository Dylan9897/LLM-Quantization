import argparse

parser = argparse.ArgumentParser(description="LLM reasoning and quantitative evaluation ...")
parser.add_argument("--dataset",default="AGIEval",type=str)
parser.add_argument("--quantize",default=None,type=str,help="choose an Quantization Algorithm")
parser.add_argument("--prompt_type",default=None,type=str,help="choose an instruction type")
parser.add_argument("--chat_mode",default=True,type=bool,help="")
parser.add_argument("--model",default="qwen",type=str,help="choose an LLM model")
parser.add_argument("--report",default=False,type=bool,help="Generate report or not")
parser.add_argument("--setting",default='few-shot-CoT',type=str,help="choose an reasoning mode ['few-shot','few-shot-CoT','zero-shot','zero-shot-CoT']")
args = parser.parse_args()

if __name__ == '__main__':
    from src.processor.AGIEvalProcessor import AGIEval
    func = AGIEval(args)
    func.combine_prompt()



