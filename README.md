# OpenWebUI-Functions
Function for Open-WebUI

## Pipe Model For Deepseek Janus
Provide Janus model support and multi-turn conversations ability for single image understanding.
![demo](./images/janus-demo.png)
# Quick Start
Search functions on [official website](https://openwebui.com/), or 
- [deepseek-Janus](https://openwebui.com/f/dsj101/deepseek_janus)

Additional operations are required for special functions :
<details>
<summary><h2>deepseek-Janus</h2></summary>
You should run a backend server to run Janus model. 

There is a detailed introduction on the official repository here ([deepseek-ai/Janus](https://github.com/deepseek-ai/Janus?tab=readme-ov-file#3-quick-start)) .

In short, you can start the serve with three commands below :

```bash
git clone https://github.com/deepseek-ai/Janus.git && cd Janus
pip install -e .[gradio]
python demo/fastapi_app.py
```
> It's easy to change model from default version "Janus-1.3B" to others.
> Just replace string `model_path` in `demo/fastapi_app.py` with model name like `deepseek-ai/Janus-Pro-7B`.
</details>