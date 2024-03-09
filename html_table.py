import json

from bs4 import BeautifulSoup
from log import logger


if __name__ == '__main__':
    # table_file: str = './table_data/NSLKDD_Basic.json'
    # table_file: str = './table_data/NSLKDD_Content_Related.json'
    # table_file: str = './table_data/NSLKDD_Time_Related_Traffic.json'
    # table_file: str = './table_data/NSLKDD_Host_Based_Traffic.json'
    table_file: str = './table_data/URI Search.json'
    output: str = './html_table.txt'

    # 代入模板中
    try:
        with open('./表格模板.html', 'r', encoding='utf-8') as file:
            table = BeautifulSoup(file, 'html.parser')

            tem_tables = table.find('tr')
            tem_table = tem_tables.extract()  # 去除原模板内容, 作为 template 供之后使用

            with open(table_file, 'r', encoding='utf-8') as f:
                data: dict = json.load(f)

                for datum in data:  # 每次循环增加行数
                    tr = table.new_tag('tr')

                    row: list = data[datum]
                    for column in row:  # 每次循环增加列数
                        tmp_table = tem_table.__copy__().find('td')  # 直接复制是传引用而非传值, __copy__() 是传值
                        new_table_label = tmp_table.find('label')
                        new_table_label.string = column

                        tr.append(tmp_table)

                    table.find('tbody').append(tr)

            # 打开文件以写入内容，如果文件不存在则创建它
            with open(output, 'w') as table_output:
                table_output.write("<div style='padding-bottom: 10px; text-align: center;'>" +
                                   table.prettify().replace('\n', '').replace('&lt;', '<').replace('&gt;', '>') +
                                   "</div>")  # 为了被收起的元素不被横线遮挡, 底部适当留空隙

            # 关闭文件
            table_output.close()
            f.close()
            file.close()

            logger.info(f"Congratulations! Task completed 🎉🎉🎉")
            logger.info("HTML file saved to: %s", output)

    except FileNotFoundError:
        logger.error("Data file not found.")
        exit()
