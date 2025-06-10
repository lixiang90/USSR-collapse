import json
import argparse
import sys

def read_chapter_data(json_file_path, chapter_title):
    """
    Reads the specified chapter data from the JSON file.

    Args:
        json_file_path (str): The path to the JSON file.
        chapter_title (str): The title of the chapter to read (e.g., '第4章 文化原因').

    Returns:
        list: A list of dictionaries, where each dictionary represents an item 
              in the chapter, or None if the chapter is not found or an error occurs.
    """
    try:
        with open(json_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        if chapter_title in data:
            return data[chapter_title]
        else:
            print(f"错误：在文件 '{json_file_path}' 中未找到章节 '{chapter_title}'。", file=sys.stderr)
            print(f"可用章节包括: {list(data.keys())}", file=sys.stderr)
            return None
    except FileNotFoundError:
        print(f"错误：文件 '{json_file_path}' 未找到。", file=sys.stderr)
        return None
    except json.JSONDecodeError:
        print(f"错误：文件 '{json_file_path}' 不是有效的JSON格式。", file=sys.stderr)
        return None
    except Exception as e:
        print(f"读取文件时发生未知错误: {e}", file=sys.stderr)
        return None

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='从JSON文件中读取指定章节的数据并输出。')
    parser.add_argument('json_file', type=str, help='JSON文件的路径 (例如: 苏联解体原因分类.json)')
    parser.add_argument('chapter_name', type=str, help='要读取的章节名称 (例如: \"第4章 文化原因\")')

    args = parser.parse_args()

    chapter_content = read_chapter_data(args.json_file, args.chapter_name)

    if chapter_content:
        # Output the chapter content as a JSON array string to stdout
        # This makes it easier for the AI to parse later
        print(json.dumps(chapter_content, ensure_ascii=False, indent=2))