
import shutil
from modelscope import snapshot_download
model_dir = snapshot_download('Qwen/Qwen2.5-14B-Instruct')
print(model_dir)
shutil.move(model_dir,"ckpt/")
