import re
import json

from bs4 import BeautifulSoup


if __name__ == '__main__':
    data_file: str = "./data/cvelistV5.json"

    html_title: str = input("Please input the theme of the mindmap: ")

    with open("./模板.html") as f:
        soup = BeautifulSoup(f, 'html.parser')

        # 1. 修改 title 标签
        title = soup.find("title")
        title.string = html_title

        # 2. 定位到 mindmap 的数据区
        content = soup.find_all("script")[2]
        # script_text = content.string

        # 3. 以 JSON 格式填写
        with open(data_file) as json_file:
            data = json.load(json_file)

        # 4. 正则表达式匹配 JSON 对象并替换
        content.string.replace_with(
            re.sub(r'{\s*"v":\s*"[\w\s]*",\s*"c":\s*\[[\s\S]*\]\s*}', str(data), content.string))

    # 5. 保存
    with open(html_title + '.html', 'w') as file:
        file.write(str(soup))
