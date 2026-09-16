#!/usr/bin/env python3
"""
清理重复文件并复制所有PDF到init文件夹
"""

import os
import shutil
import json
from pathlib import Path

def load_duplicate_report(report_path):
    """加载重复检测报告"""
    with open(report_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def get_files_to_keep(duplicate_report):
    """
    确定要保留的文件
    优先级：001-感兴趣 > 其他目录
    """
    files_to_keep = set()
    files_to_delete = set()
    
    duplicates = duplicate_report['true_duplicates']
    
    for hash_value, info in duplicates.items():
        files = info['files']
        
        # 按优先级排序：优先保留001-感兴趣目录下的文件
        sorted_files = sorted(files, key=lambda x: (
            0 if '001-感兴趣' in x['full_path'] else 1,
            x['full_path']
        ))
        
        # 保留第一个，删除其他
        files_to_keep.add(sorted_files[0]['full_path'])
        for file in sorted_files[1:]:
            files_to_delete.add(file['full_path'])
    
    return files_to_keep, files_to_delete

def collect_all_pdfs(root_dir, files_to_delete):
    """
    收集所有PDF文件（不包括要删除的文件）
    """
    all_pdfs = []
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.lower().endswith('.pdf'):
                filepath = os.path.abspath(os.path.join(root, file))
                if filepath not in files_to_delete:
                    all_pdfs.append(filepath)
    return all_pdfs

def delete_duplicate_files(files_to_delete):
    """删除重复文件"""
    deleted_count = 0
    total_size = 0
    
    print("=" * 80)
    print("删除重复文件：")
    print("=" * 80)
    
    for filepath in files_to_delete:
        try:
            file_size = os.path.getsize(filepath)
            os.remove(filepath)
            total_size += file_size
            deleted_count += 1
            print(f"✓ 已删除: {filepath}")
        except Exception as e:
            print(f"✗ 删除失败 {filepath}: {e}")
    
    print("-" * 80)
    print(f"共删除 {deleted_count} 个文件，释放空间 {total_size/1024/1024:.2f} MB")
    print()

def copy_pdfs_to_init(all_pdfs, init_dir):
    """复制所有PDF到init文件夹"""
    os.makedirs(init_dir, exist_ok=True)
    
    print("=" * 80)
    print(f"复制PDF文件到 {init_dir}")
    print("=" * 80)
    
    copied_count = 0
    skipped_count = 0
    error_count = 0
    
    for filepath in all_pdfs:
        filename = os.path.basename(filepath)
        dest_path = os.path.join(init_dir, filename)
        
        try:
            # 如果目标文件已存在，添加序号
            if os.path.exists(dest_path):
                base, ext = os.path.splitext(filename)
                counter = 1
                while os.path.exists(os.path.join(init_dir, f"{base}_{counter}{ext}")):
                    counter += 1
                dest_path = os.path.join(init_dir, f"{base}_{counter}{ext}")
            
            shutil.copy2(filepath, dest_path)
            copied_count += 1
            print(f"✓ 已复制: {filename} -> {os.path.basename(dest_path)}")
        except Exception as e:
            print(f"✗ 复制失败 {filename}: {e}")
            error_count += 1
    
    print("-" * 80)
    print(f"复制完成: {copied_count} 个文件")
    if error_count > 0:
        print(f"失败: {error_count} 个文件")
    print()

def main():
    root_dir = os.path.dirname(os.path.abspath(__file__))
    report_path = os.path.join(root_dir, 'duplicate_report.json')
    init_dir = os.path.join(root_dir, 'init')
    
    print("=" * 80)
    print("清理重复文件并复制PDF到init文件夹")
    print("=" * 80)
    print()
    
    # 检查报告文件是否存在
    if not os.path.exists(report_path):
        print(f"错误: 找不到报告文件 {report_path}")
        print("请先运行 check_pdf_duplicates.py 生成重复检测报告")
        return
    
    # 加载重复报告
    print("加载重复检测报告...")
    duplicate_report = load_duplicate_report(report_path)
    
    # 确定要保留和删除的文件
    print("\n分析重复文件...")
    files_to_keep, files_to_delete = get_files_to_keep(duplicate_report)
    
    print(f"需要删除的重复文件: {len(files_to_delete)} 个")
    print(f"需要保留的文件: {len(files_to_keep)} 个")
    print()
    
    # 删除重复文件
    delete_duplicate_files(files_to_delete)
    
    # 收集所有PDF文件
    print("收集所有PDF文件...")
    all_pdfs = collect_all_pdfs(root_dir, files_to_delete)
    print(f"找到 {len(all_pdfs)} 个PDF文件")
    print()
    
    # 复制到init文件夹
    copy_pdfs_to_init(all_pdfs, init_dir)
    
    # 最终统计
    print("=" * 80)
    print("操作完成！")
    print("=" * 80)
    print(f"✓ 删除重复文件: {len(files_to_delete)} 个")
    print(f"✓ 保留PDF文件: {len(all_pdfs)} 个")
    print(f"✓ 复制到init文件夹: {len(all_pdfs)} 个")
    print(f"✓ init文件夹路径: {os.path.abspath(init_dir)}")
    print("=" * 80)

if __name__ == "__main__":
    main()