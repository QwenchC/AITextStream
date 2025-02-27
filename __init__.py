from .Novel_Seek import VariablesInputNode, PromptInputNode, LLMNode, TextSaveNode

NODE_CLASS_MAPPINGS = {
    "VariablesInputNode": VariablesInputNode,
    "PromptInputNode": PromptInputNode,
    "LLMNode": LLMNode,
    "TextSaveNode": TextSaveNode,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "VariablesInputNode": "变量输入",
    "PromptInputNode": "提示词输入",
    "LLMNode": "大模型API",
    "TextSaveNode": "文本保存",
}
