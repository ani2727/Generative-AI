from fastapi import FastAPI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq
from langserve import add_routes
import os
from dotenv import load_dotenv
load_dotenv()

groq_api_key = os.getenv("GROQ_API_KEY")

model = ChatGroq(model="Gemma2-9b-It",groq_api_key=groq_api_key)

system_template = "Translate the following into {language}:"
prompt_template = ChatPromptTemplate.from_messages(
    [("system",system_template),("user","{text}")]
)

output_parser = StrOutputParser()

#create chain
chain = prompt_template|model|output_parser

### app definition
# app = FastAPI(title="Langchain Server",
#                     version="1.0",
#                     description="A simple API server using langchain runnable interfaces"
# )

# ### Adding routes
# add_routes(
#     app,
#     chain,
#     path="/chain"
# )

# if __name__=="__main__":
#     import uvicorn
#     uvicorn.run(app,host="localhost",port="8000")

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class ChainRequest(BaseModel):
    token_or_url: str
    score: int
    value: int
    comment: str
    correction: dict
    metadata: dict
    input: dict

@app.post("/chain/invoke")
async def invoke_chain(request: ChainRequest):
    # Here you should handle the request data and implement your chain logic
    return {
        "message": "Chain invoked successfully",
        "data": request.dict()
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)
