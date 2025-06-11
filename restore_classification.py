#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
从苏联解体原因分类_old.json恢复数据到苏联解体原因分类.json
根据实际的章节目录结构重新组织分类
"""

import os
import json
import re
from pathlib import Path

def load_old_classification(file_path):
    """加载旧的分类文件"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"读取旧分类文件时出错: {e}")
        return {}

def find_item_by_name(old_data, name):
    """根据名称在旧数据中查找完整条目"""
    for chapter_title, items in old_data.items():
        for item in items:
            if item.get('名称') == name:
                return item
    return None

def parse_filename(filename):
    """解析文件名，提取编号和名称"""
    # 匹配格式：数字.数字_名称.md
    match = re.match(r'(\d+)\.(\d+)_(.+)\.md$', filename)
    if match:
        chapter_num = match.group(1)
        section_num = match.group(2)
        name = match.group(3)
        return f"{chapter_num}.{section_num}", name
    return None, None

def get_chapter_title(chapter_dir):
    """从章节目录名提取章节标题"""
    # 匹配格式：第X章_标题
    match = re.match(r'第(\d+)章_(.+)', chapter_dir)
    if match:
        chapter_num = match.group(1)
        title = match.group(2)
        return f"第{chapter_num}章 {title}"
    return chapter_dir

def reorganize_classification(base_dir, old_data):
    """重新组织分类数据"""
    new_classification = {}
    
    # 获取所有章节目录
    chapter_dirs = [d for d in os.listdir(base_dir) 
                   if os.path.isdir(os.path.join(base_dir, d)) and d.startswith('第') and '章_' in d]
    
    # 按章节号排序
    chapter_dirs.sort(key=lambda x: int(re.search(r'第(\d+)章', x).group(1)))
    
    for chapter_dir in chapter_dirs:
        chapter_path = os.path.join(base_dir, chapter_dir)
        chapter_title = get_chapter_title(chapter_dir)
        
        print(f"处理章节: {chapter_title}")
        
        # 获取章节下的所有md文件
        md_files = [f for f in os.listdir(chapter_path) 
                   if f.endswith('.md') and f != 'README.md']
        
        # 按编号排序
        md_files.sort(key=lambda x: (
            int(re.search(r'(\d+)\.(\d+)', x).group(1)),
            int(re.search(r'(\d+)\.(\d+)', x).group(2))
        ) if re.search(r'(\d+)\.(\d+)', x) else (999, 999))
        
        chapter_items = []
        
        for md_file in md_files:
            number, name = parse_filename(md_file)
            if number and name:
                # 从旧数据中查找完整条目
                old_item = find_item_by_name(old_data, name)
                
                if old_item:
                    # 使用旧数据的详述，但更新编号
                    item = {
                        "编号": number,
                        "名称": name,
                        "详述": old_item.get('详述', '暂无详述')
                    }
                    print(f"  找到条目: {number} - {name}")
                else:
                    # 如果找不到，创建新条目
                    item = {
                        "编号": number,
                        "名称": name,
                        "详述": "暂无详述"
                    }
                    print(f"  新增条目: {number} - {name}")
                
                chapter_items.append(item)
        
        if chapter_items:
            new_classification[chapter_title] = chapter_items
    
    return new_classification

def main():
    """主函数"""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    old_file = os.path.join(base_dir, '苏联解体原因分类_old.json')
    output_file = os.path.join(base_dir, '苏联解体原因分类.json')
    
    print("加载旧分类数据...")
    old_data = load_old_classification(old_file)
    
    if not old_data:
        print("无法加载旧分类数据，退出")
        return
    
    print("重新组织分类数据...")
    new_classification = reorganize_classification(base_dir, old_data)
    
    # 生成最终的JSON结构
    result = {
        "苏联解体原因分类": new_classification
    }
    
    # 写入JSON文件
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(f"\n成功恢复分类文件: {output_file}")
        
        # 统计信息
        total_items = sum(len(items) for items in new_classification.values())
        print(f"总共处理了 {len(new_classification)} 个章节，{total_items} 个条目")
        
        for chapter, items in new_classification.items():
            print(f"  {chapter}: {len(items)} 个条目")
            
    except Exception as e:
        print(f"写入文件时出错: {e}")

if __name__ == '__main__':
    main()