"""
ChatGLM API客户端
处理与ChatGLM 4.5v API的通信
"""

import requests
import json
import base64
import io
from PIL import Image
from config import CHATGLM_API_KEY, CHATGLM_API_URL, CHATGLM_MODEL, MAX_TOKENS, TIMEOUT

class ChatGLMClient:
    def __init__(self):
        self.api_key = CHATGLM_API_KEY
        self.api_url = CHATGLM_API_URL
        self.model = CHATGLM_MODEL

    def analyze_image(self, image):
        """
        使用ChatGLM 4.5v分析图片

        Args:
            image: PIL Image对象

        Returns:
            dict: 分析结果
        """
        if not self.api_key or self.api_key == "YOUR_API_KEY_HERE":
            raise ValueError("请先在config.py中配置ChatGLM API密钥")

        try:
            # 将图片转换为base64
            buffered = io.BytesIO()
            image.save(buffered, format="PNG")
            img_base64 = base64.b64encode(buffered.getvalue()).decode()

            # 构造请求
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }

            payload = {
                "model": self.model,
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": """请分析这张图片，判断它是否包含Excel表格或类似的表格结构。

如果是表格，请：
1. 确认这是表格
2. 提取表格的完整内容
3. 将内容组织成结构化的JSON格式

如果不是表格，请直接回复这不是表格。

表格格式要求：
- 使用二维数组表示表格数据
- 第一行通常是表头
- 保持原始数据的行和列结构
- 空单元格用空字符串表示
- 注意表格边框和网格线的识别

请用以下JSON格式回复：
{
    "is_table": true/false,
    "confidence": 0.0-1.0,
    "table_data": [
        ["表头1", "表头2", "表头3"],
        ["数据1", "数据2", "数据3"],
        ...
    ],
    "description": "表格的简要描述"
}

注意：请严格按JSON格式回复，不要包含其他文字说明。"""
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/png;base64,{img_base64}"
                                }
                            }
                        ]
                    }
                ],
                "max_tokens": MAX_TOKENS
            }

            # 发送请求
            response = requests.post(
                self.api_url,
                headers=headers,
                json=payload,
                timeout=TIMEOUT
            )
            response.raise_for_status()

            # 解析响应
            result = response.json()
            content = result['choices'][0]['message']['content']

            # 尝试解析JSON
            try:
                return json.loads(content)
            except json.JSONDecodeError:
                # 如果直接解析失败，尝试提取JSON部分
                start_idx = content.find('{')
                end_idx = content.rfind('}') + 1
                if start_idx != -1 and end_idx != 0:
                    json_str = content[start_idx:end_idx]
                    return json.loads(json_str)
                else:
                    raise ValueError("无法解析API响应中的JSON数据")

        except requests.exceptions.RequestException as e:
            raise Exception(f"API请求失败: {str(e)}")
        except Exception as e:
            raise Exception(f"分析过程中出错: {str(e)}")

    def test_connection(self):
        """测试API连接"""
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }

            payload = {
                "model": self.model,
                "messages": [
                    {
                        "role": "user",
                        "content": "测试连接"
                    }
                ],
                "max_tokens": 10
            }

            response = requests.post(
                self.api_url,
                headers=headers,
                json=payload,
                timeout=5
            )

            if response.status_code == 200:
                return True, "连接成功"
            else:
                return False, f"连接失败: {response.status_code}"

        except Exception as e:
            return False, f"连接错误: {str(e)}"