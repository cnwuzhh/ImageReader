"""
工具函数
提供图片处理和其他辅助功能
"""

import os
import json
from PIL import Image, ImageEnhance
from config import MAX_IMAGE_SIZE, SUPPORTED_FORMATS

def validate_image_file(file_path):
    """验证图片文件格式"""
    if not os.path.exists(file_path):
        return False, "文件不存在"

    ext = os.path.splitext(file_path)[1].lower()
    if ext not in SUPPORTED_FORMATS:
        return False, f"不支持的文件格式: {ext}"

    return True, "文件格式正确"

def preprocess_image(image):
    """预处理图片以提高识别准确率"""
    try:
        # 调整图片大小
        if image.size[0] > MAX_IMAGE_SIZE[0] or image.size[1] > MAX_IMAGE_SIZE[1]:
            image.thumbnail(MAX_IMAGE_SIZE, Image.Resampling.LANCZOS)

        # 增强对比度
        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(1.2)

        # 增强锐度
        enhancer = ImageEnhance.Sharpness(image)
        image = enhancer.enhance(1.1)

        return image

    except Exception as e:
        raise Exception(f"图片预处理失败: {str(e)}")

def format_table_data(table_data):
    """格式化表格数据，确保数据一致性"""
    if not table_data or not isinstance(table_data, list):
        return []

    formatted_data = []
    max_cols = 0

    # 找出最大列数
    for row in table_data:
        if isinstance(row, list) and len(row) > max_cols:
            max_cols = len(row)

    # 格式化每一行
    for row in table_data:
        if not isinstance(row, list):
            continue

        # 填充缺失的列
        formatted_row = []
        for i in range(max_cols):
            if i < len(row):
                # 确保数据是字符串
                cell_value = str(row[i]) if row[i] is not None else ""
                formatted_row.append(cell_value.strip())
            else:
                formatted_row.append("")

        formatted_data.append(formatted_row)

    return formatted_data

def save_result_to_file(result, file_path):
    """保存结果到文件"""
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        return True, "保存成功"
    except Exception as e:
        return False, f"保存失败: {str(e)}"

def load_result_from_file(file_path):
    """从文件加载结果"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        return None, f"加载失败: {str(e)}"

def create_excel_format(table_data):
    """将表格数据转换为Excel友好的格式"""
    if not table_data:
        return []

    excel_data = []

    # 处理表头
    if table_data:
        header = table_data[0]
        excel_data.append(header)

        # 处理数据行
        for row in table_data[1:]:
            excel_data.append(row)

    return excel_data