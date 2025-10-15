"""
配置文件
用于存储API密钥和其他配置信息
"""

# ChatGLM API配置
CHATGLM_API_KEY = "YOUR_API_KEY_HERE"  # 请替换为实际的API密钥
CHATGLM_API_URL = "https://api.chatglm.com/v1/chat/completions"
CHATGLM_MODEL = "glm-4.5v"

# 应用配置
APP_NAME = "智能表格识别器"
APP_VERSION = "1.0.0"

# 图片处理配置
MAX_IMAGE_SIZE = (1024, 1024)  # 最大图片尺寸
SUPPORTED_FORMATS = ['.jpg', '.jpeg', '.png', '.bmp', '.gif']

# API配置
MAX_TOKENS = 2000
TIMEOUT = 30  # 秒