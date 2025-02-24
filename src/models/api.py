# encoding : utf-8 -*-                            
# @author  : 冬瓜                              
# @mail    : dylan_han@126.com    
# @Time    : 2025/2/24 11:28
# encoding : utf-8 -*-
# @author  : 冬瓜
# @mail    : dylan_han@126.com
# @Time    : 2025/1/22 15:11
from openai import OpenAI
import sys
sys.path.append("/mnt/e/Github/ai-nlp-project-new/")
from conf.model_config import deep_zeek
from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI
from starlette.responses import StreamingResponse
import uvicorn

app = FastAPI()

class Query(BaseModel):
    question: str

async def event_generator(completion):
    for chunk in completion:
        if not chunk.choices:
            print("\nUsage:")
            print(chunk.usage)
        else:
            delta = chunk.choices[0].delta
            if hasattr(delta, 'reasoning_content') and delta.reasoning_content is not None:
                yield f"data: {delta.reasoning_content}\n\n"
            else:
                if delta.content != "":
                    yield f"data: {delta.content}\n\n"

@app.post("/ask")
async def ask(query: Query):
    client = OpenAI(
        api_key= deep_zeek["api_key"],
        base_url=deep_zeek["base_url"]
    )

    completion = client.chat.completions.create(
        model=deep_zeek["model_name"],
        messages=[{"role": "user", "content": query.question}],
        stream=True,
    )

    return StreamingResponse(event_generator(completion), media_type="text/event-stream")

# 运行应用时可以使用以下命令：
# uvicorn your_script_name:app --reload


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8801)


