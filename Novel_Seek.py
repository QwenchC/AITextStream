import requests
import json
import time
import os

class VariablesInputNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "variable_name": ("STRING", {"default": ""}),
                "variable_value": ("STRING", {"default": "", "multiline": True}),
            },
        }
    
    RETURN_TYPES = ("VARIABLES",)
    FUNCTION = "define_variable"
    CATEGORY = "NovelSeek"

    def define_variable(self, variable_name, variable_value):
        return ({variable_name: variable_value},)

class PromptInputNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prompt_text": ("STRING", {"default": "", "multiline": True}),
                "refresh_counter": ("INT", {"default": 0, "min": 0}),
            },
            "optional": {
                "var1": ("VARIABLES", {}),
                "var2": ("VARIABLES", {}),
                "var3": ("VARIABLES", {}),
                "var4": ("VARIABLES", {}),
                "var5": ("VARIABLES", {}),
                "var6": ("VARIABLES", {}),
                "var7": ("VARIABLES", {}),
                "var8": ("VARIABLES", {}),
                "var9": ("VARIABLES", {}),
                "var10": ("VARIABLES", {}),
            }
        }
    
    RETURN_TYPES = ("STRING",)
    FUNCTION = "process_prompt"
    CATEGORY = "NovelSeek"

    def process_prompt(self, prompt_text, refresh_counter=0, **kwargs):
        merged_vars = {}
        for key in kwargs:
            if kwargs[key] and isinstance(kwargs[key], dict):
                merged_vars.update(kwargs[key])
        
        processed = prompt_text
        for k, v in merged_vars.items():
            processed = processed.replace(f"{{{k}}}", v)
        
        print(f"\n🔧 处理后的提示词：\n{processed}\n")
        return (processed,)

class LLMNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prompt": ("STRING", {"forceInput": True}),
                "api_key": ("STRING", {"default": ""}),
                "api_url": ("STRING", {"default": "https://api.deepseek.com/v1/chat/completions"}),
                "model_name": ("STRING", {"default": "deepseek-chat"}),
                "temperature": ("FLOAT", {"default": 0.7, "min": 0.0, "max": 2.0, "step": 0.1}),
                "max_tokens": ("INT", {"default": 500, "min": 1, "max": 4096}),
            },
        }
    
    RETURN_TYPES = ("STRING",)
    FUNCTION = "generate"
    CATEGORY = "NovelSeek"

    def generate(self, prompt, api_key, api_url, model_name, temperature, max_tokens):
        print(f"\n🚀 正在调用 {model_name} 模型...")
        print(f"📝 输入提示词：\n{prompt}\n")
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
        
        payload = {
            "model": model_name,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": temperature,
            "max_tokens": max_tokens
        }
        
        try:
            response = requests.post(api_url, headers=headers, json=payload)
            response.raise_for_status()
            result = response.json()
            
            if result.get("choices"):
                answer = result["choices"][0]["message"]["content"]
                print(f"\n✅ 生成结果：\n{answer}\n")
                return (answer,)
            
            error_msg = "⚠️ 未生成有效响应"
            return (error_msg,)
        
        except Exception as e:
            error_msg = f"❌ API调用失败：{str(e)}"
            print(error_msg)
            return (error_msg,)

class TextDisplayNode:
    """
    简单的文本显示节点 - 使用原生文本输入框显示文本
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text": ("STRING", {"forceInput": True}),
                "display_text": ("STRING", {"default": "", "multiline": True}),
            },
        }
    
    RETURN_TYPES = ("STRING",)
    FUNCTION = "display"
    CATEGORY = "NovelSeek"

    def display(self, text, display_text):
        # 将输入文本复制到显示文本框
        # 注意：这里不使用UI更新，而是依赖用户手动刷新
        print(f"\n📋 文本显示节点接收到文本：\n{text[:100]}...\n")
        
        # 返回原始文本，不尝试更新UI
        return (text,)

class TextSaveNode:
    """
    将文本保存到文件的节点
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text": ("STRING", {"forceInput": True}),
                "filename": ("STRING", {"default": "output.txt"}),
                "save_path": ("STRING", {"default": "outputs"}),
            },
        }
    
    RETURN_TYPES = ("STRING",)
    OUTPUT_NODE = True
    FUNCTION = "save_text"
    CATEGORY = "NovelSeek"

    def save_text(self, text, filename, save_path):
        # 确保输出目录存在
        os.makedirs(save_path, exist_ok=True)
        
        # 构建完整文件路径
        file_path = os.path.join(save_path, filename)
        
        # 保存文本到文件
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(text)
        
        print(f"\n💾 文本已保存到：{file_path}\n")
        
        # 返回文件路径作为确认
        return (f"文本已保存到：{file_path}",)

# 节点注册
NODE_CLASS_MAPPINGS = {
    "VariablesInputNode": VariablesInputNode,
    "PromptInputNode": PromptInputNode,
    "LLMNode": LLMNode,
    "TextDisplayNode": TextDisplayNode,
    "TextSaveNode": TextSaveNode
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "VariablesInputNode": "变量输入",
    "PromptInputNode": "提示词输入",
    "LLMNode": "大模型API",
    "TextDisplayNode": "文本显示",
    "TextSaveNode": "文本保存"
}
