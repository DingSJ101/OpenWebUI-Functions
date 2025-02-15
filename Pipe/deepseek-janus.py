"""
title: DeepSeek Janus
author: dingSJ
description: 调用本地部署的Janus-FastAPI接口
version: 0.0.1
licence: MIT
"""
import base64
import requests
from pydantic import BaseModel, Field
from open_webui.utils.misc import pop_system_message
from io import BytesIO
from PIL import Image
import re

DEBUG_MODE = False
class Pipe:
    class Valves(BaseModel):
        FASTAPI_IP: str = Field(default="127.0.0.1")
        FASTAPI_PORT: int = Field(default=8000)
        API_ENDPOINT: str = Field(default="understand_image_and_question")
        # [NOTE] : You should run the fastapi server first , gudiance can be found 
        # here : https://github.com/deepseek-ai/Janus?tab=readme-ov-file#3-quick-start
        # python demo/fastapi_app.py

    def __init__(self):
        self.valves = self.Valves()

    def pipe(self, body: dict, __event_emitter__: dict, __task__=None):
        api_url = f"http://{self.valves.FASTAPI_IP}:{self.valves.FASTAPI_PORT}/{self.valves.API_ENDPOINT}"
        if DEBUG_MODE:
            print("-----------------------------------------------------------------")
            print("Debug - Pipe Function ")
            print(f"body:{body}")
            print(f"__task__:{__task__}")
            print("-----------------------------------------------------------------")
        
        # TODO : task routing
        if __task__ is not None:
            if __task__ == "title_generation":
                return "skipped"
            elif __task__ == "tags_generation":
                return f'{{"tags":[{"Janus"}]}}'

        system_message, messages = pop_system_message(body["messages"])
        if DEBUG_MODE:
            print(f"system_message:{system_message}")

        # TODO : 历史消息处理
        message = messages[-1]
        query = ""
        image_url_base64 = None # "data:image/png;base64,iVBORw0KGgoAAAA...=="
        if isinstance(message.get("content"), list):
            for item in message["content"]:
                if item["type"] == "text":
                    query += item["text"]
                if item["type"] == "image_url":
                    image_url_base64 = item["image_url"]["url"]
        else:
            query = message.get("content", "")
        if not image_url_base64:
            return "未找到图片数据"
        
        image_url_prefix, image_data_base64 = image_url_base64.split(",")
        match = re.match(r"^data:image/([a-zA-Z0-9]+);base64", image_url_prefix)
        if match:
            image_type =  match.group(1)

        if len(image_data_base64) % 4 != 0:
            image_data_base64 += "=" * (4 - len(image_data_base64) % 4)
        try:
            image_data = base64.b64decode(image_data_base64)
            image_file = BytesIO(image_data)
        except Exception as e:
            return f"图片数据解析失败: {e}"
        
        if image_type == "png":
            # convert "RGBA" image to "RGB" format
            image = Image.open(image_file)
            image_file.seek(0)
            if image.mode == "RGBA":
                image_rgb = image.convert("RGB")
                image_rgb.save(image_file, format='PNG')
                print("convert image format from RGBA to RGB")
                image_file.seek(0)
        else:
            ... # TODO: check other image format

        data = {
            "question": query,
            "seed": 42,
            "top_p": 0.95,
            "temperature": 0.1
        }
        files = {"file": image_file}

        try:
            response = requests.post(api_url, files = files, data=data)
            response.raise_for_status()
            result = response.json()
            return result.get("response", "未获取到答案")
        except requests.exceptions.RequestException as e:
            return f"请求失败: {e}"