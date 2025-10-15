import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import json
import os
from PIL import Image, ImageTk
from api_client import ChatGLMClient
from utils import validate_image_file, preprocess_image, format_table_data, save_result_to_file

class ImageReader:
    def __init__(self, root):
        self.root = root
        self.root.title("智能表格识别器 - ImageReader")
        self.root.geometry("800x600")

        # 初始化API客户端
        try:
            self.api_client = ChatGLMClient()
        except Exception as e:
            messagebox.showerror("初始化错误", f"无法初始化API客户端: {str(e)}")

        # 创建UI组件
        self.create_widgets()

    def create_widgets(self):
        # 顶部按钮区域
        button_frame = tk.Frame(self.root)
        button_frame.pack(fill=tk.X, padx=10, pady=5)

        # 上传图片按钮
        upload_btn = tk.Button(button_frame, text="上传图片", command=self.upload_image)
        upload_btn.pack(side=tk.LEFT, padx=5)

        # 分析图片按钮
        analyze_btn = tk.Button(button_frame, text="分析表格", command=self.analyze_image)
        analyze_btn.pack(side=tk.LEFT, padx=5)

        # 保存结果按钮
        save_btn = tk.Button(button_frame, text="保存JSON", command=self.save_json)
        save_btn.pack(side=tk.LEFT, padx=5)

        # 设置按钮
        settings_btn = tk.Button(button_frame, text="设置", command=self.open_settings)
        settings_btn.pack(side=tk.RIGHT, padx=5)

        # 主内容区域
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # 左侧图片预览区域
        left_frame = tk.Frame(main_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)

        tk.Label(left_frame, text="图片预览", font=("Arial", 12, "bold")).pack()

        self.image_label = tk.Label(left_frame, bg="lightgray", width=40, height=20)
        self.image_label.pack(fill=tk.BOTH, expand=True, pady=5)

        # 右侧结果显示区域
        right_frame = tk.Frame(main_frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5)

        tk.Label(right_frame, text="识别结果", font=("Arial", 12, "bold")).pack()

        self.result_text = scrolledtext.ScrolledText(right_frame, width=40, height=20)
        self.result_text.pack(fill=tk.BOTH, expand=True, pady=5)

        # 底部状态栏
        self.status_bar = tk.Label(self.root, text="就绪", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(fill=tk.X, padx=5, pady=2)

        # 存储变量
        self.current_image = None
        self.image_path = None
        self.analysis_result = None

    def upload_image(self):
        """上传图片"""
        file_types = [
            ("图片文件", "*.jpg *.jpeg *.png *.bmp *.gif"),
            ("所有文件", "*.*")
        ]

        file_path = filedialog.askopenfilename(filetypes=file_types)

        if file_path:
            try:
                # 验证文件
                is_valid, message = validate_image_file(file_path)
                if not is_valid:
                    messagebox.showerror("错误", message)
                    return

                # 加载并预处理图片
                image = Image.open(file_path)
                processed_image = preprocess_image(image)

                # 显示图片
                display_image = processed_image.copy()
                display_image.thumbnail((400, 400), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(display_image)

                self.image_label.configure(image=photo)
                self.image_label.image = photo
                self.current_image = processed_image
                self.image_path = file_path

                self.status_bar.configure(text=f"已加载: {os.path.basename(file_path)}")

            except Exception as e:
                messagebox.showerror("错误", f"无法加载图片: {str(e)}")

    def analyze_image(self):
        """分析图片中的表格"""
        if not self.current_image:
            messagebox.showwarning("警告", "请先上传图片")
            return

        self.status_bar.configure(text="正在分析图片...")
        self.root.update()

        try:
            # 调用ChatGLM API分析图片
            result = self.analyze_with_chatglm()

            if result:
                self.analysis_result = result
                self.display_result(result)

                if result.get("is_table"):
                    self.status_bar.configure(text="识别完成: 检测到Excel表格")
                else:
                    self.status_bar.configure(text="识别完成: 未检测到表格")
            else:
                messagebox.showerror("错误", "分析失败")
                self.status_bar.configure(text="分析失败")

        except Exception as e:
            messagebox.showerror("错误", f"分析过程中出错: {str(e)}")
            self.status_bar.configure(text="分析出错")

    def analyze_with_chatglm(self):
        """调用ChatGLM 4.5v API分析图片"""
        try:
            # 使用API客户端分析图片
            result = self.api_client.analyze_image(self.current_image)

            # 格式化表格数据
            if result.get("is_table") and result.get("table_data"):
                result["table_data"] = format_table_data(result["table_data"])

            return result

        except Exception as e:
            messagebox.showerror("API错误", f"API调用失败: {str(e)}")
            return None

    def get_mock_result(self):
        """模拟API返回结果（仅用于演示）"""
        return {
            "is_table": True,
            "confidence": 0.95,
            "table_data": [
                ["姓名", "年龄", "部门", "薪资"],
                ["张三", "28", "技术部", "15000"],
                ["李四", "32", "市场部", "12000"],
                ["王五", "26", "人事部", "10000"]
            ],
            "description": "这是一个员工信息表格"
        }

    def display_result(self, result):
        """显示分析结果"""
        self.result_text.delete(1.0, tk.END)

        if result.get("is_table"):
            content = f"✅ 检测到表格 (置信度: {result.get('confidence', 0):.2f})\n\n"
            content += f"描述: {result.get('description', '')}\n\n"
            content += "表格数据:\n"
            content += json.dumps(result.get("table_data", []), indent=2, ensure_ascii=False)
        else:
            content = "❌ 未检测到表格\n\n"
            content += "此图片不包含Excel表格或类似的表格结构。"

        self.result_text.insert(1.0, content)

    def save_json(self):
        """保存结果为JSON文件"""
        if not self.analysis_result:
            messagebox.showwarning("警告", "没有可保存的结果")
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON文件", "*.json"), ("所有文件", "*.*")]
        )

        if file_path:
            success, message = save_result_to_file(self.analysis_result, file_path)
            if success:
                messagebox.showinfo("成功", f"结果已保存到: {file_path}")
                self.status_bar.configure(text=f"已保存: {os.path.basename(file_path)}")
            else:
                messagebox.showerror("错误", message)

    def open_settings(self):
        """打开设置窗口"""
        settings_window = tk.Toplevel(self.root)
        settings_window.title("设置")
        settings_window.geometry("400x200")

        # API密钥设置
        tk.Label(settings_window, text="ChatGLM API密钥:", font=("Arial", 10, "bold")).pack(pady=10)

        api_key_frame = tk.Frame(settings_window)
        api_key_frame.pack(fill=tk.X, padx=20, pady=5)

        api_key_entry = tk.Entry(api_key_frame, width=40, show="*")
        api_key_entry.insert(0, "YOUR_API_KEY_HERE")
        api_key_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)

        # 显示/隐藏密码按钮
        def toggle_password():
            if api_key_entry.cget("show") == "*":
                api_key_entry.config(show="")
            else:
                api_key_entry.config(show="*")

        toggle_btn = tk.Button(api_key_frame, text="👁", command=toggle_password, width=3)
        toggle_btn.pack(side=tk.RIGHT, padx=5)

        # 测试连接按钮
        test_btn = tk.Button(settings_window, text="测试连接", command=lambda: self.test_api_connection(api_key_entry.get()))
        test_btn.pack(pady=10)

        # 保存设置按钮
        def save_settings():
            api_key = api_key_entry.get()
            if api_key and api_key != "YOUR_API_KEY_HERE":
                self.save_api_key(api_key)
                messagebox.showinfo("成功", "设置已保存")
                settings_window.destroy()
            else:
                messagebox.showwarning("警告", "请输入有效的API密钥")

        save_btn = tk.Button(settings_window, text="保存设置", command=save_settings)
        save_btn.pack(pady=10)

    def test_api_connection(self, api_key):
        """测试API连接"""
        try:
            from config import CHATGLM_API_KEY
            original_key = CHATGLM_API_KEY

            # 临时设置API密钥进行测试
            import config
            config.CHATGLM_API_KEY = api_key

            test_client = ChatGLMClient()
            success, message = test_client.test_connection()

            # 恢复原始API密钥
            config.CHATGLM_API_KEY = original_key

            if success:
                messagebox.showinfo("连接测试", message)
            else:
                messagebox.showerror("连接测试", message)

        except Exception as e:
            messagebox.showerror("连接测试", f"测试失败: {str(e)}")

    def save_api_key(self, api_key):
        """保存API密钥到配置文件"""
        try:
            with open("config.py", "r", encoding="utf-8") as f:
                content = f.read()

            # 替换API密钥
            new_content = content.replace(
                'CHATGLM_API_KEY = "YOUR_API_KEY_HERE"',
                f'CHATGLM_API_KEY = "{api_key}"'
            )

            with open("config.py", "w", encoding="utf-8") as f:
                f.write(new_content)

            # 重新加载配置
            import importlib
            import config
            importlib.reload(config)

            # 更新API客户端
            self.api_client = ChatGLMClient()

        except Exception as e:
            messagebox.showerror("保存错误", f"无法保存API密钥: {str(e)}")

def main():
    root = tk.Tk()
    app = ImageReader(root)
    root.mainloop()

if __name__ == "__main__":
    main()