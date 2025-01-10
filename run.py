import argparse

parser = argparse.ArgumentParser(description="LLM reasoning and quantitative evaluation ...")
parser.add_argument("--dataset",default="ceval",type=str)
parser.add_argument("--quantize",default=None,type=str,help="choose an Quantization Algorithm")
parser.add_argument("--prompt_type",default=None,type=str,help="choose an instruction type")
parser.add_argument("--chat_mode",default=False,type=bool,help="")
parser.add_argument("--model_path",default="Qwen2___5-7B-Instruct",type=str,help="choose an LLM model")
parser.add_argument("--report",default=False,type=bool,help="Generate report or not")
parser.add_argument("--setting",default='zero-shot',type=str,help="choose an reasoning mode ['few-shot','few-shot-CoT','zero-shot','zero-shot-CoT']")
args = parser.parse_args()

if __name__ == '__main__':
    if args.dataset == "AGIEval":
        from src.processor.AGIEvalProcessor import AGIEval
        from src.predict.predict import inference
        func = AGIEval(args)
        func.combine_prompt()
        inference(args)

    elif args.dataset == "ARC":
        from src.processor.ARCProcessor import ARC
        func = ARC(args)
        func.combine_prompt()

    elif args.dataset == "BBH":
        from src.processor.BBHProcessor import BBH
        func = BBH(args)
        func.combine_prompt()

    elif args.dataset == "ceval":
        from src.processor.CevalProcessor import CEVAL
        func = CEVAL(args)
        func.combine_prompt()
