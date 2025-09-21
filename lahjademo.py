import gradio as gr
import modelscope_studio.components.antd as antd
import modelscope_studio.components.antdx as antdx
import modelscope_studio.components.base as ms
import modelscope_studio.components.pro as pro
import azure.cognitiveservices.speech as speechsdk
import base64
import os
from gradio_client import Client

import uuid
from openai import OpenAI

bodyicon = """
    <style>
      :root {
    --name: default;

    --primary-500: rgba(11, 186, 131, 1);
    }
      .shadow-primary {
        box-shadow: 0 4px 8px rgba(0, 123, 255, 0.25);
      }
      .icon-xxl {
        width: 170px;
        height: 170px;
        line-height: 6.8rem;
        align-items: center;
      }
      .icon-md, .icon-lg, .icon-xl, .icon-xxl {
        display: flex;
        justify-content: center;
        align-items: center;
        border-radius: 50%;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        background-color: #ffffff;
      }
      .flex-shrink-0 {
        flex-shrink: 0 !important;
      }
      .rounded-circle {
        border-radius: 50% !important;
      }
      .text-center {
        text-align: center;
      }
      .mud-icon-root.mud-svg-icon {
        fill: rgba(11,186,131,1);
      }
      .mud-icon-size-large {
        font-size: 4.25rem !important;
        width: 7.25rem !important;
        height: 7.25rem !important;
      }
      .mud-success-text {
        color: rgba(11,186,131,1);
      }
      .icon-cont-center {
        display: flex;
        justify-content: center;
        align-items: center;
        width: 100%;

      }
      .built-with.svelte-sar7eh.svelte-sar7eh.svelte-sar7eh {
        display:none !important;
      }
     footer.svelte-sar7eh.svelte-sar7eh.svelte-sar7eh {
    position: fixed;
    right: 20px;
    top: 0;
}
       .gap.svelte-vt1mxs {
    gap: 8px !important;
}
    </style>
    <div class="icon-cont-center  ">
    <div id="logo-icon-static-id" class="icon-xxl text-center shadow-primary rounded-circle flex-shrink-0">
        <svg class="mud-icon-root mud-svg-icon mud-success-text mud-icon-size-large" style="direction:ltr !important;margin:8px !important" focusable="false" viewBox="0 0 24 24" aria-hidden="true" role="img">
            <title>API</title>
            <path d="M0 0h24v24H0z" fill="none"></path>
            <path d="M6 13c-.55 0-1 .45-1 1s.45 1 1 1 1-.45 1-1-.45-1-1-1zm0 4c-.55 0-1 .45-1 1s.45 1 1 1 1-.45 1-1-.45-1-1-1zm0-8c-.55 0-1 .45-1 1s.45 1 1 1 1-.45 1-1-.45-1-1-1zm-3 .5c-.28 0-.5.22-.5.5s.22.5.5.5.5-.22.5-.5-.22-.5-.5-.5zM6 5c-.55 0-1 .45-1 1s.45 1 1 1 1-.45 1-1-.45-1-1-1zm15 5.5c.28 0 .5-.22.5-.5s-.22-.5-.5-.5-.5.22-.5.5.22.5.5.5zM14 7c.55 0 1-.45 1-1s-.45-1-1-1-1 .45-1 1 .45 1 1 1zm0-3.5c.28 0 .5-.22.5-.5s-.22-.5-.5-.5-.5.22-.5.5.22.5.5.5zm-11 10c-.28 0-.5.22-.5.5s.22.5.5.5.5-.22.5-.5-.22-.5-.5-.5zm7 7c-.28 0-.5.22-.5.5s.22.5.5.5.5-.22.5-.5-.22-.5-.5-.5zm0-17c.28 0 .5-.22.5-.5s-.22-.5-.5-.5-.5.22-.5.5.22.5.5.5zM10 7c.55 0 1-.45 1-1s-.45-1-1-1-1 .45-1 1 .45 1 1 1zm0 5.5c-.83 0-1.5.67-1.5 1.5s.67 1.5 1.5 1.5 1.5-.67 1.5-1.5-.67-1.5-1.5-1.5zm8 .5c-.55 0-1 .45-1 1s.45 1 1 1 1-.45 1-1-.45-1-1-1zm0 4c-.55 0-1 .45-1 1s.45 1 1 1 1-.45 1-1-.45-1-1-1zm0-8c-.55 0-1 .45-1 1s.45 1 1 1 1-.45 1-1-.45-1-1-1zm0-4c-.55 0-1 .45-1 1s.45 1 1 1 1-.45 1-1-.45-1-1-1zm3 8.5c-.28 0-.5.22-.5.5s.22.5.5.5.5-.22.5-.5-.22-.5-.5-.5zM14 17c-.55 0-1 .45-1 1s.45 1 1 1 1-.45 1-1-.45-1-1-1zm0 3.5c-.28 0-.5.22-.5.5s.22.5.5.5.5-.22.5-.5-.22-.5-.5-.5zm-4-12c-.83 0-1.5.67-1.5 1.5s.67 1.5 1.5 1.5 1.5-.67 1.5-1.5-.67-1.5-1.5-1.5zm0 8.5c-.55 0-1 .45-1 1s.45 1 1 1 1-.45 1-1-.45-1-1-1zm4-4.5c-.83 0-1.5.67-1.5 1.5s.67 1.5 1.5 1.5 1.5-.67 1.5-1.5-.67-1.5-1.5-1.5zm0-4c-.83 0-1.5.67-1.5 1.5s.67 1.5 1.5 1.5 1.5-.67 1.5-1.5-.67-1.5-1.5-1.5z"></path>
        </svg>
    </div>
    </div>
"""
users = [("admin", "password123"), ("user", "userpass")]



LANGUAGES = {
    "en": "English",
    "ar": "Arabic",
    "fr": "French",
}

# اللهجات / الأصوات
LANGUAGESPEECH = {
    "en": ["US", "UK"],
    "ar": ["Saudi", "Egyptian"],
    "fr": ["France"],
}

# دالة تجيب التصنيفات (مبدئية)


import re

def clean_text(text):
    # إزالة أي شيء غير الحروف العربية أو الإنجليزية أو الأرقام أو المسافات
    cleaned = re.sub(r'[^\w\s\u0600-\u06FF]', '', text)
    return cleaned

speech_key = os.getenv("speechkey")
service_region = "eastus2"
def text_to_speech_hugingface(text,name_model):


    client = Client("wasmdashai/DemoLahja")
    print(f"msg={text}")
    result = client.predict(
        text=text,
        name_model=name_model,
        speaking_rate=0.7,
        api_name="/predict"
    )
    return result
def text_to_speech(text, filename=None):


    print(text)
    if filename is None:
        filename = f"tts_{uuid.uuid4().hex}.wav"
    speech_config = speechsdk.SpeechConfig(subscription=speech_key,
                                           region=service_region)
    audio_config = speechsdk.audio.AudioOutputConfig(filename=filename)
    synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config,
                                              audio_config=audio_config)
    synthesizer.speak_text_async(text).get()
    return filename
endpoint = "https://lahja-dev-resource.openai.azure.com/openai/v1/"
deployment_name = "gpt-4o"
# api_key = ""
api_key = os.getenv("keyt2t")

def ask_ai(msg,name_model="wasmdashai/vits-ar-sa-huba-v2",type_sound=True):
    text = msg.get("text", "")
    client = OpenAI(base_url=endpoint, api_key=api_key)
    completion = client.chat.completions.create(
        model=deployment_name,
        messages=[{
            "role":
            "system",
            "content":
            """
إنت تمثل شركة "أسس الذكاء الاصطناعي وتقنية المعلومات"، شركة ناشئة سعودية مقرها في كود. شغلكم تطوير أنظمة وحلول مبنية على تقنيات الذكاء الاصطناعي تركّز على اللهجة والهوية المحلية.

القواعد والسلوكيات:
1.  **اللغة:**
    -   بدون ملصقات  ترد دايم باللهجة السعودية (النجدية) بشكل طبيعي.
    -   إذا كان الموقف رسمي مع جهات أو مستثمرين، تميل للفصحى بس تبقى بلمسة سعودية.
2.  **الهوية:**
    -   عرّف بنفسك كممثل رسمي للشركة.
    -   أكّد إن الشركة سعودية وتركز على حلول تدعم الثقافة واللغة المحلية.
3.  **المنتجات والإنجازات:**
    -   أبرز منتج هو "وَسْم" → مساعد افتراضي باللهجة النجدية.
    -   تذكر إن الشركة تطور نماذج صوتية ولغوية بلهجات سعودية وعربية مختلفة.
4.  **القيم:**
    -   البيانات محمية وحلول On-Premise متوفرة.
    -   الحلول مرنة، قابلة للتخصيص، وسهلة التطوير.
5.  **الرؤية والرسالة:**
    -   الرؤية: الريادة في توطين الذكاء الاصطناعي عربيًا وسعوديًا.
    -   الرسالة: ابتكار منتجات وخدمات عملية وموثوقة تخدم المجتمع.
6.  **طريقة الرد:**
    -   لو العميل سأل عن خدمات → تجاوب باختصار وبلغة واضحة.
    -   لو سأل عن المنتجات الصوتية → تذكر "وَسْم" وقدراته على إخراج صوت طبيعي باللهجة النجدية.
    -   لو طلب اقتراح تقني → تجاوب باحتراف مع أسلوب ودود.
    -   لو السؤال بعيد عن الشركة → تجاوب باحترام وتحاول تربط الموضوع بخبرة الشركة.
7.  **الإدارة:**
    -   المدير التنفيذي: مزيونة الفغم، قائدة الرؤية اللي تعزز الهوية اللغوية والثقافية بالتقنيات الذكية.
8.  **الأسلوب:**
    -   ودود، بسيط، وسعودي الطابع.
    -   رسمي وجاد وقت التعامل مع شركاء وجهات حكومية.
"""
        }, {
            "role": "user",
            "content": text,
        }],
    )
    msg=completion.choices[0].message.content
    textt=clean_text(msg)
    if type_sound:
        result=text_to_speech(textt)
    else:
         result=text_to_speech_hugingface(textt,name_model)
    return result,bodyicon,msg

def createTextToSpeech():
    with gr.Blocks() as demo:



            with gr.Row():
                with gr.Column(scale=1):



                    with gr.Accordion( "settings"):
                        model_choices = gr.Dropdown(
                                    choices=[

                                        "wasmdashai/vits-ar-sa-huba-v2",
                                        "wasmdashai/vits-ar-sa-A"

                                    ],
                                    label="اختر النموذج",
                                    value="wasmdashai/vits-ar-sa-huba-v2"
                                )
                        type_sound = gr.Checkbox(
                            label="Type Sound",
                            value=True
                        )

                        temperature_slider = gr.Slider(
                            label="temperature",
                            minimum=0.1, maximum=5, step=0.1, value=0.7
                        )
                        speech_rate_slider = gr.Slider(
                            label="max_token",
                            minimum=50, maximum=120000, step=50, value=1024
                        )
                        streaming_toggle = gr.Checkbox(
                            label="streaming",
                            value=True
                        )

                with gr.Column(scale=3):

                      bd = gr.HTML(bodyicon)

                      with gr.Row():

                          text=gr.Textbox()
                          out_audio = gr.Audio(label="Output", autoplay=True)

                      with gr.Row():





                       chat_input = gr.MultimodalTextbox(
                          interactive=True,
                           visible=True,
                          placeholder="enter_message",
                          show_label=False,
                          lines=3,
                          max_lines=6
                      )



                chat_input.submit(
                    ask_ai,
                    inputs=[chat_input,model_choices,type_sound],
                    outputs=[out_audio,bd,text]
                )

    return demo




demo = createTextToSpeech()


