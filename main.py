from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI
import gradio as gr
import  lahjademo
import  wasmai
import  dashbord
import os
# إعداد Azure OpenAI Client
endpoint = "https://lahja-dev-resource.openai.azure.com/openai/v1/"
deployment_name = "gpt-4o"
api_key = os.getenv("keywasm")

client = OpenAI(
    base_url=endpoint,
    api_key=api_key
)

# تعريف FastAPI app
app = FastAPI()

# نموذج الإدخال
class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
async def chat(request: ChatRequest):
    completion = client.chat.completions.create(
        model=deployment_name,
        messages=[
            {"role": "user", "content": request.message}
        ],
    )
    
    reply = completion.choices[0].message.content
    return {"reply": reply}


app = gr.mount_gradio_app(app, lahjademo.demo, path='/lahja')
app = gr.mount_gradio_app(app, wasmai.demo, path='/wasm')

app = gr.mount_gradio_app(app, dashbord.demo, path='/')
