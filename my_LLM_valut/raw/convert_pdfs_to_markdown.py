#!/usr/bin/env python3
"""
批量将init目录下的PDF文件通过MinerU Agent API转换为Markdown文档
同时提取图片并添加图片引用
一步到位，无需分步处理
使用MinerU精准解析API获取Markdown和图片
"""

import os
import requests
import time
import json
import csv
import re
from pathlib import Path

# MinerU Agent API配置
BASE_URL = "https://mineru.net/api/v4"
API_TOKEN = "eyJ0eXBlIjoiSldUIiwiYWxnIjoiSFM1MTIifQ.eyJqdGkiOiI0MTYwNzkwMCIsInJvbCI6IlJPTEVfUkVHSVNURVIiLCJpc3MiOiJPcGVuWExhYiIsImlhdCI6MTc3NTI1OTQ1OSwiY2xpZW50SWQiOiJsa3pkeDU3bnZ5MjJqa3BxOXgydyIsInBob25lIjoiMTg3NTIwMzk1MTkiLCJvcGVuSWQiOm51bGwsInV1aWQiOiI3ZjFlYmNlMC05NWZhLTQ2ZDktYTBmNS1lMzA5NGEwMDFiMTYiLCJlbWFpbCI6IiIsImV4cCI6MTc4MzAzNTQ1Njl9.emawMhab-A-cqYq6LgQ25xXGf31n0UsKbdIduC3bu-qmXbSpOmZSg2iWNnT-kq6yKH8dOrvYCUmQlms7g5sxVw"
TIMEOUT = 300  # 请求超时时间（秒）
POLL_INTERVAL = 3  # 轮询间隔（秒）
MAX_POLL_RETRIES = 100  # 最大轮询次数
MAX_FILE_SIZE = 10 * 1024 * 1024  # Agent API限制10MB


class MinerUAgentConverter:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {API_TOKEN}'
        })
    
    def create_task(self, filename):
        """
        创建Agent解析任务
        
        参数:
            filename: PDF文件名
        
        返回:
            (success, task_id或error_message)
        """
        try:
            print(f"  正在创建Agent任务...")
            
            url = f"{BASE_URL}/agent/file"
            data = {
                "file_name": filename
            }
            
            response = self.session.post(
                url,
                json=data,
                timeout=TIMEOUT
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get('code') == 0 and 'data' in result:
                    task_id = result['data'].get('task_id')
                    if task_id:
                        print(f"  ✓ 任务创建成功，Task ID: {task_id}")
                        return True, task_id
                    else:
                        return False, f"API返回数据缺少task_id: {result}"
                else:
                    return False, f"API返回错误: {result}"
            else:
                error_msg = f"创建任务失败 (状态码 {response.status_code}): {response.text}"
                return False, error_msg
                
        except requests.exceptions.Timeout:
            return False, f"请求超时（{TIMEOUT}秒）"
        except requests.exceptions.RequestException as e:
            return False, f"请求异常: {str(e)}"
        except Exception as e:
            return False, f"未知错误: {str(e)}"
    
    def get_upload_url(self, task_id, filename):
        """
        获取上传URL
        
        参数:
            task_id: 任务ID
            filename: 文件名
        
        返回:
            (success, upload_url或error_message)
        """
        try:
            url = f"{BASE_URL}/agent/file-urls"
            data = {
                "task_id": task_id,
                "file_name": filename
            }
            
            response = self.session.post(
                url,
                json=data,
                timeout=TIMEOUT
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get('code') == 0 and 'data' in result:
                    upload_url = result['data'][0].get('upload_url')
                    if upload_url:
                        return True, upload_url
                    else:
                        return False, f"API返回数据缺少upload_url: {result}"
                else:
                    return False, f"API返回错误: {result}"
            else:
                error_msg = f"获取上传URL失败 (状态码 {response.status_code}): {response.text}"
                return False, error_msg
                
        except Exception as e:
            return False, f"获取上传URL异常: {str(e)}"
    
    def upload_file(self, upload_url, pdf_path):
        """
        上传PDF文件
        
        参数:
            upload_url: 上传URL
            pdf_path: PDF文件路径
        
        返回:
            (success, message)
        """
        try:
            print(f"  正在上传文件...")
            
            with open(pdf_path, 'rb') as f:
                response = self.session.put(
                    upload_url,
                    data=f,
                    timeout=TIMEOUT
                )
                
                if response.status_code in [200, 201]:
                    print(f"  ✓ 文件上传成功")
                    return True, "上传成功"
                else:
                    error_msg = f"文件上传失败 (状态码 {response.status_code}): {response.text}"
                    return False, error_msg
                    
        except requests.exceptions.Timeout:
            return False, f"上传超时（{TIMEOUT}秒）"
        except requests.exceptions.RequestException as e:
            return False, f"上传异常: {str(e)}"
        except Exception as e:
            return False, f"未知错误: {str(e)}"
    
    def poll_task_status(self, task_id):
        """
        轮询任务状态
        
        参数:
            task_id: 任务ID
        
        返回:
            (success, result_dict或error_message)
        """
        try:
            url = f"{BASE_URL}/agent/file/{task_id}"
            
            for attempt in range(MAX_POLL_RETRIES):
                response = self.session.get(
                    url,
                    timeout=30
                )
                
                if response.status_code == 200:
                    result = response.json()
                    
                    if result.get('code') == 0 and 'data' in result:
                        state = result['data'].get('state', '')
                        progress = result['data'].get('progress', 0)
                        
                        if state == 'done':
                            print(f"  ✓ 任务完成!")
                            return True, result['data']
                        elif state == 'failed':
                            error_msg = result['data'].get('error', '未知错误')
                            return False, f"任务失败: {error_msg}"
                        elif state in ['pending', 'processing', 'downloading']:
                            print(f"    任务状态: {state}, 进度: {progress}%")
                        else:
                            print(f"    未知状态: {state}")
                        
                        time.sleep(POLL_INTERVAL)
                    else:
                        return False, f"API返回错误: {result}"
                else:
                    error_msg = f"获取任务状态失败 (状态码 {response.status_code}): {response.text}"
                    return False, error_msg
            
            return False, "超过最大轮询次数"
            
        except requests.exceptions.RequestException as e:
            return False, f"轮询异常: {str(e)}"
        except Exception as e:
            return False, f"未知错误: {str(e)}"
    
    def download_markdown_and_images(self, result_dict):
        """
        下载Markdown内容和图片信息
        
        参数:
            result_dict: 包含下载URL的结果字典
        
        返回:
            (success, (markdown_content, images_data)或error_message)
            images_data: 图片数据列表，每个元素包含 {'url': 图片URL, 'filename': 图片名}
        """
        try:
            md_url = result_dict.get('md_url')
            if not md_url:
                return False, "结果中没有找到md_url"
            
            print(f"  正在下载Markdown...")
            
            # 下载Markdown
            response = self.session.get(md_url, timeout=300)
            if response.status_code != 200:
                return False, f"下载Markdown失败 (状态码 {response.status_code})"
            
            markdown_content = response.text
            print(f"  ✓ Markdown下载成功")
            
            # 尝试获取图片信息（精准解析API可能返回图片URL）
            images_data = []
            
            # 方法1: 检查是否有images字段
            if 'images' in result_dict:
                for idx, img_info in enumerate(result_dict['images']):
                    if 'url' in img_info:
                        images_data.append({
                            'url': img_info['url'],
                            'filename': f"image_{idx+1}.png"
                        })
            
            # 方法2: 检查是否有image_urls字段
            elif 'image_urls' in result_dict:
                for idx, img_url in enumerate(result_dict['image_urls']):
                    images_data.append({
                        'url': img_url,
                        'filename': f"image_{idx+1}.png"
                    })
            
            # 方法3: 检查是否有其他可能的图片字段
            else:
                # 检查常见的图片字段名称
                image_fields = ['img_urls', 'pictures', 'figures', 'image_list']
                for field in image_fields:
                    if field in result_dict and isinstance(result_dict[field], list):
                        for idx, img_info in enumerate(result_dict[field]):
                            url = img_info if isinstance(img_info, str) else img_info.get('url', '')
                            if url:
                                images_data.append({
                                    'url': url,
                                    'filename': f"image_{idx+1}.png"
                                })
                        break
            
            if images_data:
                print(f"  ✓ 发现 {len(images_data)} 张图片（来自API）")
            
            return True, (markdown_content, images_data)
            
        except Exception as e:
            return False, f"下载失败: {str(e)}"
    
    def download_images_from_api(self, images_data, output_dir, pdf_name):
        """
        从API下载图片到本地
        
        参数:
            images_data: 图片数据列表 [{'url': xxx, 'filename': xxx}]
            output_dir: 图片输出目录
            pdf_name: PDF文件名（用于创建子目录）
        
        返回:
            (success, image_list或error_message)
            image_list格式: [(image_filename, relative_path)]
        """
        if not images_data:
            return True, []
        
        try:
            print(f"  正在下载 {len(images_data)} 张图片...")
            
            # 为每个PDF创建子目录
            pdf_output_dir = os.path.join(output_dir, pdf_name)
            os.makedirs(pdf_output_dir, exist_ok=True)
            
            image_list = []
            
            for idx, img_data in enumerate(images_data, start=1):
                try:
                    img_url = img_data['url']
                    # 生成更规范的文件名
                    ext = os.path.splitext(img_data['filename'])[1]
                    image_filename = f"image_{idx}{ext}"
                    image_path = os.path.join(pdf_output_dir, image_filename)
                    
                    # 下载图片
                    response = self.session.get(img_url, timeout=60)
                    if response.status_code == 200:
                        with open(image_path, 'wb') as f:
                            f.write(response.content)
                        
                        # 构建相对路径（相对于markdown目录）
                        relative_path = f"../extracted_images/{pdf_name}/{image_filename}"
                        image_list.append((image_filename, relative_path))
                    else:
                        print(f"    ⚠ 图片 {idx} 下载失败 (状态码 {response.status_code})")
                
                except Exception as e:
                    print(f"    ⚠ 图片 {idx} 下载失败: {str(e)}")
            
            if image_list:
                print(f"  ✓ 成功下载 {len(image_list)} 张图片")
            else:
                print(f"  → 未成功下载任何图片")
            
            return True, image_list
            
        except Exception as e:
            return False, f"下载图片失败: {str(e)}"
    
    def extract_title_from_markdown(self, markdown_content):
        """
        从Markdown中提取论文标题
        
        参数:
            markdown_content: Markdown内容
        
        返回:
            标题字符串
        """
        lines = markdown_content.split('\n')
        for line in lines[:20]:
            line = line.strip()
            if line.startswith('# '):
                title = line[2:].strip()
                title = title.replace('â', "'").replace('€', "'")
                return title
            elif line.startswith('## '):
                return line[3:].strip()
        
        return ""
    
    def add_image_links_to_markdown(self, markdown_content, image_list):
        """
        在Markdown内容末尾添加图片引用
        
        参数:
            markdown_content: 原始Markdown内容
            image_list: 图片列表 [(filename, relative_path)]
        
        返回:
            更新后的Markdown内容
        """
        if not image_list:
            return markdown_content
        
        # 检查是否已经存在图片引用
        if '## 📷 Images' in markdown_content:
            # 移除旧的图片引用块
            markdown_content = re.sub(
                r'## 📷 Images.*?(?=\n##|\n$|$)',
                '',
                markdown_content,
                flags=re.DOTALL
            ).strip()
        
        # 添加新的图片引用块
        image_section = "\n\n## 📷 Images\n\n"
        image_section += "The following images were extracted from this PDF:\n\n"
        
        for i, (filename, relative_path) in enumerate(image_list, 1):
            # 使用Obsidian双链格式
            image_section += f"{i}. [[{relative_path}|{filename}]]\n"
        
        return markdown_content + image_section
    
    def convert_pdf_with_images(self, pdf_path, markdown_output_dir, images_output_dir):
        """
        完整的PDF转Markdown流程（包含图片提取和引用）
        一步到位，无需分步处理
        使用MinerU精准解析API获取Markdown和图片
        
        参数:
            pdf_path: PDF文件路径
            markdown_output_dir: Markdown输出目录
            images_output_dir: 图片输出目录
        
        返回:
            (success, (markdown_content, title, image_count)或error_message)
        """
        filename = os.path.basename(pdf_path)
        pdf_name = os.path.splitext(filename)[0]
        
        # 步骤1：创建任务
        success, result = self.create_task(filename)
        if not success:
            return False, result
        
        task_id = result
        
        # 步骤2：获取上传URL
        success, result = self.get_upload_url(task_id, filename)
        if not success:
            return False, result
        
        upload_url = result
        
        # 步骤3：上传文件
        success, result = self.upload_file(upload_url, pdf_path)
        if not success:
            return False, result
        
        # 步骤4：轮询任务状态
        success, result = self.poll_task_status(task_id)
        if not success:
            return False, result
        
        # 步骤5：下载Markdown和图片信息
        success, result = self.download_markdown_and_images(result)
        if not success:
            return False, result
        
        markdown_content, images_data = result
        title = self.extract_title_from_markdown(markdown_content)
        
        # 步骤6：下载图片
        image_list = []
        if images_data:
            success, image_list = self.download_images_from_api(images_data, images_output_dir, pdf_name)
            if not success:
                print(f"  ⚠ 图片下载失败: {image_list}")
        
        # 步骤7：添加图片引用到Markdown
        if image_list:
            markdown_content = self.add_image_links_to_markdown(markdown_content, image_list)
        
        return True, (markdown_content, title, len(image_list))
    
    def close(self):
        self.session.close()


def get_pdf_files(directory):
    """
    获取指定目录下所有PDF文件
    
    参数:
        directory: 目录路径
    
    返回:
        PDF文件路径列表
    """
    pdf_files = []
    
    if not os.path.exists(directory):
        print(f"错误: 目录不存在 - {directory}")
        return pdf_files
    
    for filename in os.listdir(directory):
        if filename.lower().endswith('.pdf'):
            filepath = os.path.join(directory, filename)
            if os.path.isfile(filepath):
                pdf_files.append(filepath)
    
    return sorted(pdf_files)


def load_processed_files(csv_file):
    """
    从CSV文件加载已处理的文件列表
    
    参数:
        csv_file: CSV文件路径
    
    返回:
        已处理文件名的集合
    """
    if not os.path.exists(csv_file):
        return set()
    
    processed = set()
    try:
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if 'pdf_file' in row:
                    processed.add(row['pdf_file'])
    except Exception as e:
        print(f"警告: 读取CSV文件失败: {e}")
    
    return processed


def save_to_csv(csv_file, record, headers=None):
    """
    保存记录到CSV文件
    
    参数:
        csv_file: CSV文件路径
        record: 要保存的记录字典
        headers: CSV表头（如果文件不存在）
    """
    file_exists = os.path.exists(csv_file)
    
    with open(csv_file, 'a', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        if not file_exists:
            writer.writeheader()
        writer.writerow(record)


def main():
    # 配置路径
    current_dir = os.path.dirname(os.path.abspath(__file__))
    init_dir = os.path.join(current_dir, 'init')
    markdown_dir = os.path.join(current_dir, 'markdown')
    images_dir = os.path.join(current_dir, 'extracted_images')
    csv_file = os.path.join(markdown_dir, 'processed_papers.csv')
    
    print("=" * 80)
    print("批量PDF转Markdown + 图片提取 - 一站式处理")
    print("=" * 80)
    print()
    print("功能说明:")
    print("  - 使用MinerU精准解析API转换PDF为Markdown")
    print("  - 自动提取PDF中的所有图片")
    print("  - 在Markdown末尾添加Obsidian双链图片引用")
    print("  - Agent API限制: 单个文件 ≤ 10MB")
    print()
    
    # 检查init目录
    if not os.path.exists(init_dir):
        print(f"错误: init目录不存在 - {init_dir}")
        return
    
    # 获取所有PDF文件
    print("正在扫描PDF文件...")
    pdf_files = get_pdf_files(init_dir)
    
    if not pdf_files:
        print("未找到任何PDF文件")
        return
    
    print(f"找到 {len(pdf_files)} 个PDF文件")
    print()
    
    # 创建输出目录
    os.makedirs(markdown_dir, exist_ok=True)
    os.makedirs(images_dir, exist_ok=True)
    
    # 加载已处理的文件列表
    processed_files = load_processed_files(csv_file)
    print(f"已处理文件数: {len(processed_files)}")
    print()
    
    # 初始化转换器
    converter = MinerUAgentConverter()
    
    # 统计信息
    success_count = 0
    failed_count = 0
    skipped_count = 0
    total_images = 0
    failed_files = []
    
    # 保存转换日志
    log_file = os.path.join(markdown_dir, 'conversion_log.json')
    conversion_log = {
        'start_time': time.strftime('%Y-%m-%d %H:%M:%S'),
        'total_files': len(pdf_files),
        'successful': 0,
        'failed': 0,
        'skipped': 0,
        'total_images': 0,
        'details': []
    }
    
    # 批量转换
    print("=" * 80)
    print("开始批量转换...")
    print("=" * 80)
    print()
    
    for index, pdf_path in enumerate(pdf_files, 1):
        filename = os.path.basename(pdf_path)
        
        # 检查是否已经处理过
        if filename in processed_files:
            print(f"[{index}/{len(pdf_files)}] ✓ 已处理，跳过: {filename}")
            skipped_count += 1
            conversion_log['skipped'] += 1
            conversion_log['details'].append({
                'pdf_file': filename,
                'status': 'skipped',
                'reason': 'Already processed'
            })
            continue
        
        # 检查文件大小（API限制10MB）
        file_size = os.path.getsize(pdf_path)
        if file_size > MAX_FILE_SIZE:
            print(f"[{index}/{len(pdf_files)}] ✗ 跳过: {filename} (文件大小 {file_size/1024/1024:.2f}MB > 10MB)")
            skipped_count += 1
            conversion_log['skipped'] += 1
            conversion_log['details'].append({
                'pdf_file': filename,
                'status': 'skipped',
                'reason': f'File too large ({file_size/1024/1024:.2f}MB > 10MB)'
            })
            print()
            continue
        
        print(f"[{index}/{len(pdf_files)}] 处理中: {filename} ({file_size/1024/1024:.2f}MB)")
        
        # 转换文件（包含图片提取和引用）
        success, result = converter.convert_pdf_with_images(
            pdf_path, 
            markdown_dir,
            images_dir
        )
        
        if success:
            markdown_content, title, image_count = result
            
            # 保存Markdown文件
            base_name = os.path.splitext(filename)[0]
            md_filename = f"{base_name}.md"
            md_path = os.path.join(markdown_dir, md_filename)
            
            with open(md_path, 'w', encoding='utf-8') as f:
                f.write(markdown_content)
            
            # 保存到CSV
            csv_record = {
                'pdf_file': filename,
                'title': title,
                'markdown_file': md_filename,
                'image_count': image_count,
                'convert_time': time.strftime('%Y-%m-%d %H:%M:%S'),
                'file_size_mb': f"{file_size/1024/1024:.2f}"
            }
            
            save_to_csv(csv_file, csv_record, [
                'pdf_file', 'title', 'markdown_file', 'image_count', 'convert_time', 'file_size_mb'
            ])
            
            print(f"  ✓ 转换成功 -> {md_filename}")
            print(f"    标题: {title}")
            if image_count > 0:
                print(f"    图片: {image_count} 张（已添加引用）")
            success_count += 1
            total_images += image_count
            conversion_log['successful'] += 1
            conversion_log['total_images'] += image_count
            conversion_log['details'].append({
                'pdf_file': filename,
                'status': 'success',
                'output_file': md_filename,
                'title': title,
                'image_count': image_count
            })
        else:
            print(f"  ✗ 转换失败: {result}")
            failed_count += 1
            failed_files.append((filename, result))
            conversion_log['failed'] += 1
            conversion_log['details'].append({
                'pdf_file': filename,
                'status': 'failed',
                'error': result
            })
        
        print()
        
        # 避免请求过于频繁
        if index < len(pdf_files):
            time.sleep(2)
    
    # 保存转换日志
    conversion_log['end_time'] = time.strftime('%Y-%m-%d %H:%M:%S')
    with open(log_file, 'w', encoding='utf-8') as f:
        json.dump(conversion_log, f, ensure_ascii=False, indent=2)
    
    # 关闭转换器
    converter.close()
    
    # 打印总结
    print("=" * 80)
    print("转换完成！")
    print("=" * 80)
    print(f"总文件数: {len(pdf_files)}")
    print(f"成功转换: {success_count}")
    print(f"转换失败: {failed_count}")
    print(f"跳过文件: {skipped_count}")
    print(f"提取图片总数: {total_images}")
    print(f"Markdown目录: {os.path.abspath(markdown_dir)}")
    print(f"图片目录: {os.path.abspath(images_dir)}")
    print(f"CSV记录: {os.path.abspath(csv_file)}")
    print(f"日志文件: {os.path.abspath(log_file)}")
    
    if failed_files:
        print("\n失败的文件:")
        for filename, error in failed_files:
            print(f"  - {filename}: {error}")
    
    print("\n✓ 所有功能已一站式完成：")
    print("  - PDF → Markdown（使用MinerU精准解析API）")
    print("  - 提取图片（使用MinerU精准解析API）")
    print("  - 添加图片引用（Obsidian双链格式）")
    print("=" * 80)


if __name__ == "__main__":
    main()