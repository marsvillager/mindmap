import os
import re
import json

from bs4 import BeautifulSoup
from log import logger


if __name__ == '__main__':
    directory: str = input("Please input the relative directory(in the ./data directory) of the mindmap: ")

    html_title: str = input("Please input the theme of the mindmap: ")

    data_file: str = "./data/" + directory + "/" + html_title + ".json"
    logger.debug("Directory of data file: %s", data_file)

    try:
        with open('./模板.html', 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f, 'html.parser')

            # 1. 修改 title 标签
            title = soup.find("title")
            title.string = html_title

            # 2. 定位到 mindmap 的数据区
            content = soup.find_all("script")[-1]
            # script_text = content.string

            # 3. 以 JSON 格式填写
            with open(data_file, 'r', encoding='utf-8') as json_file:
                data = json.load(json_file)

            pattern = r'{\s*"content":\s*"markmap",\s*"depth":\s*\d+,\s*"children":\s*\[\s*\]\s*}'

            # 4. 正则表达式匹配 JSON 对象并替换
            content.string.replace_with(
                re.sub(pattern, str(data), content.string))

    except FileNotFoundError:
        logger.error("Data file not found.")
        exit()

    # 5. 保存
    file_path = "./out/" + directory + "/" + html_title + ".html"

    if not os.path.exists(os.path.dirname(file_path)):
        os.makedirs(os.path.dirname(file_path))

    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(str(soup))

    logger.info(f"Congratulations! Task completed 🎉🎉🎉")
    logger.info("HTML file saved to: %s", file_path)
