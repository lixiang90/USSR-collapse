import os
import re
import time
from datetime import datetime

def count_words_in_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            # 移除Markdown标记和特殊字符
            content = re.sub(r'#.*?\n', '', content)  # 移除标题
            content = re.sub(r'\[.*?\]\(.*?\)', '', content)  # 移除链接
            content = re.sub(r'```.*?```', '', content, flags=re.DOTALL)  # 移除代码块
            content = re.sub(r'[\*_`~]', '', content)  # 移除强调标记
            # 计算中文字符数
            chinese_chars = re.findall(r'[\u4e00-\u9fff]', content)
            # 计算英文单词数
            english_words = re.findall(r'\b[a-zA-Z]+\b', content)
            # 总字数（中文字符 + 英文单词）
            total_words = len(chinese_chars) + len(english_words)
            return total_words, len(chinese_chars), len(english_words)
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return 0, 0, 0

def count_words_in_directory(directory, log_file=None):
    total_words = 0
    total_chinese = 0
    total_english = 0
    file_count = 0
    file_stats = []
    
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.md'):
                file_path = os.path.join(root, file)
                words, chinese, english = count_words_in_file(file_path)
                total_words += words
                total_chinese += chinese
                total_english += english
                file_count += 1
                file_stats.append((file_path, words, chinese, english))
                if file != 'README.md':
                    msg = f"{file_path}: {words} 字 (中文: {chinese}, 英文: {english})"
                    print(msg)
                    if log_file:
                        log_file.write(msg + '\n')
    
    return total_words, total_chinese, total_english, file_count, file_stats

def main():
    start_time = time.time()
    base_dir = os.getcwd()
    
    # 创建输出目录
    output_dir = os.path.join(base_dir, 'statistics')
    os.makedirs(output_dir, exist_ok=True)
    
    # 创建输出文件
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = os.path.join(output_dir, f'word_count_{timestamp}.txt')
    
    with open(output_file, 'w', encoding='utf-8') as log_file:
        chapters = [d for d in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, d)) and d.startswith('第')]
        chapters.sort()
        
        grand_total = 0
        grand_chinese = 0
        grand_english = 0
        grand_file_count = 0
        chapter_stats = []
        all_files = []
        
        header = "\n===== 苏联解体原因一书字数统计 =====\n"
        print(header)
        log_file.write(header + '\n')
        
        for chapter in chapters:
            chapter_dir = os.path.join(base_dir, chapter)
            chapter_header = f"\n## {chapter} 字数统计"
            print(chapter_header)
            log_file.write(chapter_header + '\n')
            
            words, chinese, english, files, file_stats = count_words_in_directory(chapter_dir, log_file)
            grand_total += words
            grand_chinese += chinese
            grand_english += english
            grand_file_count += files
            chapter_stats.append((chapter, words, chinese, english, files))
            all_files.extend(file_stats)
            
            chapter_summary = f"\n{chapter} 总计: {words} 字 (中文: {chinese}, 英文: {english}, 共 {files} 个文件)"
            print(chapter_summary)
            log_file.write(chapter_summary + '\n')
        
        # 按字数排序文件
        all_files.sort(key=lambda x: x[1], reverse=True)
        
        summary_header = "\n===== 总体统计 =====\n"
        print(summary_header)
        log_file.write(summary_header + '\n')
        
        stats = [
            f"全书总字数: {grand_total} 字",
            f"中文字符: {grand_chinese} 字",
            f"英文单词: {grand_english} 词",
            f"总文件数: {grand_file_count} 个文件",
            f"平均每篇文章字数: {grand_total / grand_file_count:.1f} 字",
            f"统计耗时: {time.time() - start_time:.2f} 秒"
        ]
        
        for stat in stats:
            print(stat)
            log_file.write(stat + '\n')
        
        distribution_header = "\n各章节字数分布:"
        print(distribution_header)
        log_file.write(distribution_header + '\n')
        
        for chapter, words, chinese, english, files in chapter_stats:
            percentage = (words / grand_total) * 100 if grand_total > 0 else 0
            avg_words = words / files if files > 0 else 0
            chapter_stat = f"{chapter}: {words} 字 ({percentage:.1f}%), 平均每篇 {avg_words:.1f} 字"
            print(chapter_stat)
            log_file.write(chapter_stat + '\n')
        
        top_files_header = "\n字数最多的10篇文章:"
        print(top_files_header)
        log_file.write(top_files_header + '\n')
        
        for i, (file_path, words, chinese, english) in enumerate(all_files[:10], 1):
            file_name = os.path.basename(file_path)
            top_file = f"{i}. {file_name}: {words} 字 (中文: {chinese}, 英文: {english})"
            print(top_file)
            log_file.write(top_file + '\n')
        
        print(f"\n统计报告已保存到: {output_file}")

if __name__ == "__main__":
    main()