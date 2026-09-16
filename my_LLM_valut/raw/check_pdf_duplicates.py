#!/usr/bin/env python3
"""
PDF文档重复检测脚本
通过文件大小和MD5哈希值检测重复的PDF文档
"""

import os
import hashlib
from pathlib import Path
from collections import defaultdict
import json

def get_file_hash(filepath):
    """计算文件的MD5哈希值"""
    md5_hash = hashlib.md5()
    try:
        with open(filepath, "rb") as f:
            # 分块读取大文件
            for chunk in iter(lambda: f.read(4096), b""):
                md5_hash.update(chunk)
        return md5_hash.hexdigest()
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return None

def scan_directory(root_dir):
    """扫描目录中所有PDF文件"""
    pdf_files = []
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.lower().endswith('.pdf'):
                filepath = os.path.join(root, file)
                # 获取相对路径
                rel_path = os.path.relpath(filepath, root_dir)
                pdf_files.append(rel_path)
    return pdf_files

def find_duplicates(root_dir):
    """查找重复的PDF文件"""
    print(f"扫描目录: {root_dir}")
    print("-" * 80)
    
    # 扫描所有PDF文件
    pdf_files = scan_directory(root_dir)
    print(f"找到 {len(pdf_files)} 个PDF文件\n")
    
    # 按文件大小分组
    size_groups = defaultdict(list)
    for pdf_file in pdf_files:
        filepath = os.path.join(root_dir, pdf_file)
        try:
            file_size = os.path.getsize(filepath)
            size_groups[file_size].append(pdf_file)
        except Exception as e:
            print(f"Error getting size for {pdf_file}: {e}")
    
    # 检查可能的重复（文件大小相同）
    potential_duplicates = {size: files for size, files in size_groups.items() if len(files) > 1}
    
    if potential_duplicates:
        print(f"发现 {len(potential_duplicates)} 组文件大小相同的PDF文件（可能是重复）")
        print("=" * 80)
    else:
        print("未发现文件大小相同的PDF文件")
        return
    
    # 计算哈希值确认重复
    hash_groups = defaultdict(list)
    size_details = {}
    
    for size, files in potential_duplicates.items():
        print(f"\n文件大小: {size:,} 字节 ({size/1024:.2f} KB)")
        print(f"文件数量: {len(files)}")
        print("-" * 80)
        
        for pdf_file in files:
            filepath = os.path.join(root_dir, pdf_file)
            file_hash = get_file_hash(filepath)
            
            if file_hash:
                hash_groups[file_hash].append(pdf_file)
                size_details[pdf_file] = {
                    'size': size,
                    'hash': file_hash,
                    'full_path': os.path.abspath(filepath)
                }
    
    # 找出真正的重复（哈希值相同）
    true_duplicates = {h: files for h, files in hash_groups.items() if len(files) > 1}
    
    print("\n" + "=" * 80)
    print("检测到的重复文件（哈希值相同）：")
    print("=" * 80)
    
    if true_duplicates:
        duplicate_count = 0
        for h, files in true_duplicates.items():
            print(f"\n重复组 #{duplicate_count + 1}")
            print(f"哈希值: {h}")
            print(f"文件大小: {size_details[files[0]]['size']:,} 字节")
            print("-" * 80)
            for i, file in enumerate(files, 1):
                print(f"  {i}. {file}")
            duplicate_count += 1
        
        print(f"\n总计发现 {duplicate_count} 组重复文件")
    else:
        print("\n未发现真正的重复文件（哈希值完全相同的文件）")
        print("文件大小相同的文件实际上是不同的文档")
    
    # 生成详细报告
    report = {
        'scan_directory': root_dir,
        'total_pdf_files': len(pdf_files),
        'potential_duplicates_by_size': len(potential_duplicates),
        'true_duplicates': {}
    }
    
    for h, files in true_duplicates.items():
        report['true_duplicates'][h] = {
            'size': size_details[files[0]]['size'],
            'files': [size_details[f] for f in files]
        }
    
    report_path = os.path.join(root_dir, 'duplicate_report.json')
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    print(f"\n详细报告已保存到: {report_path}")
    
    # 统计信息
    print("\n" + "=" * 80)
    print("统计信息：")
    print(f"  总PDF文件数: {len(pdf_files)}")
    print(f"  文件大小相同的组数: {len(potential_duplicates)}")
    print(f"  真正重复的组数: {len(true_duplicates)}")
    print(f"  重复文件总数: {sum(len(files) for files in true_duplicates.values())}")
    print("=" * 80)

if __name__ == "__main__":
    # 获取当前脚本所在目录
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    print("=" * 80)
    print("PDF文档重复检测工具")
    print("=" * 80)
    print()
    
    # 检测重复文件
    find_duplicates(script_dir)