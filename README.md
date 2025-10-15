# 智能表格识别器 (ImageReader)

一个基于ChatGLM 4.5v视觉模型的智能表格识别软件，能够自动识别图片中的Excel表格并转换为JSON格式。

## 功能特点

- 🖼️ **图片上传**: 支持JPG、PNG、BMP等多种图片格式
- 🤖 **智能识别**: 利用ChatGLM 4.5v大模型进行表格识别
- 📊 **表格解析**: 自动提取表格内容并结构化为JSON格式
- 💾 **数据导出**: 支持将识别结果保存为JSON文件
- ⚙️ **设置管理**: 可配置API密钥和测试连接

## 系统要求

- Python 3.8+
- Windows/Linux/macOS
- 有效的ChatGLM API密钥

## 安装步骤

### 1. 克隆或下载项目

```bash
git clone https://github.com/yourusername/ImageReader.git
cd ImageReader
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 配置API密钥

#### 方法1: 通过设置界面配置

1. 运行程序后点击"设置"按钮
2. 输入你的ChatGLM API密钥
3. 点击"测试连接"验证密钥有效性
4. 点击"保存设置"

#### 方法2: 手动编辑配置文件

编辑 `config.py` 文件，将 `YOUR_API_KEY_HERE` 替换为你的实际API密钥：

```python
CHATGLM_API_KEY = "your_actual_api_key_here"
```

### 4. 运行程序

```bash
python main.py
```

## 使用方法

### 基本操作流程

1. **上传图片**: 点击"上传图片"按钮，选择包含表格的图片文件
2. **分析表格**: 点击"分析表格"按钮，程序将自动识别图片中的表格
3. **查看结果**: 在右侧文本框中查看识别结果
4. **保存数据**: 点击"保存JSON"按钮，将结果保存为JSON文件

### 支持的图片格式

- JPG/JPEG
- PNG
- BMP
- GIF

### 输出JSON格式

```json
{
  "is_table": true,
  "confidence": 0.95,
  "table_data": [
    ["姓名", "年龄", "部门", "薪资"],
    ["张三", "28", "技术部", "15000"],
    ["李四", "32", "市场部", "12000"],
    ["王五", "26", "人事部", "10000"]
  ],
  "description": "这是一个员工信息表格"
}
```

## 配置说明

### config.py 配置项

```python
# ChatGLM API配置
CHATGLM_API_KEY = "YOUR_API_KEY_HERE"  # ChatGLM API密钥
CHATGLM_API_URL = "https://api.chatglm.com/v1/chat/completions"  # API地址
CHATGLM_MODEL = "glm-4.5v"  # 使用的模型

# 图片处理配置
MAX_IMAGE_SIZE = (1024, 1024)  # 最大图片尺寸
SUPPORTED_FORMATS = ['.jpg', '.jpeg', '.png', '.bmp', '.gif']  # 支持的格式

# API配置
MAX_TOKENS = 2000  # 最大令牌数
TIMEOUT = 30  # 请求超时时间(秒)
```

## 常见问题

### Q: 获取ChatGLM API密钥

A: 访问[智谱AI开放平台](https://open.bigmodel.cn/)注册账号并获取API密钥。

### Q: 识别准确率不高

A:
- 确保图片清晰，避免模糊或倾斜
- 表格边框清晰可见
- 光线充足，避免阴影
- 尽量使用高分辨率图片

### Q: API调用失败

A:
- 检查API密钥是否正确
- 确认网络连接正常
- 检查API余额是否充足
- 查看防火墙设置

### Q: 程序无法启动

A:
- 确认Python版本为3.8+
- 检查依赖包是否正确安装
- 查看错误信息并排查

## 项目结构

```
ImageReader/
├── main.py          # 主程序入口
├── api_client.py    # ChatGLM API客户端
├── config.py        # 配置文件
├── utils.py         # 工具函数
├── requirements.txt # 依赖包列表
└── README.md       # 说明文档
```

## 技术架构

- **界面框架**: Tkinter
- **图像处理**: Pillow (PIL)
- **API客户端**: requests
- **AI模型**: ChatGLM 4.5v
- **数据格式**: JSON

## 许可证

MIT License

## 贡献

欢迎提交Issue和Pull Request来改进这个项目。

## 联系方式

如有问题或建议，请通过以下方式联系：

- 提交GitHub Issue
- 发送邮件至: your.email@example.com

---

**注意**: 本软件需要有效的ChatGLM API密钥才能正常使用。请确保遵守相关API使用条款。