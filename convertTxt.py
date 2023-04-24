# pdf文本解析
import pdfplumber
import os
from concurrent.futures import ThreadPoolExecutor

file_dir = r'F:\pywork\年报PDF'  # 需要遍历的文件夹路径
file_list = []
for files in os.walk(file_dir):  # 遍历文件夹及其下的所有子文件夹
    # print(files)

    for file in files[2]:
        # print(file)
        if os.path.splitext(file)[1] == '.pdf':
            file_list.append(file)
# print(file_list)
"""
    1.查找关键字‘管理层讨论与分析’，并且当前页数大于5（确保不在目录中）
    2.查找关键字‘公司治理’，并且当前页数大于第1点
    3.查找关键字‘环境与社会责任’，并且当前页数大于第二点
    4.第12点之间的内容作为txt1，第23之间的内容作为txt2
    5.全文保存
    6.无法提取txt进行统计
"""


def convert_txt(file):
    pdf = pdfplumber.open(file_dir + '\\' + file)
    pages = pdf.pages

    text_all = []  # 全文
    text_1 = []  # 管理层讨论与分析
    text_2 = []  # 公司治理
    page_start1 = 0
    page_start2 = 0
    page_end1 = 0
    page_end2 = 0
    for page in pages:
        text = page.extract_text()  # 提取当前页面文本
        if page_start1 > 5 and page_end1 == 0:
            text_1.append(text)
        if page_start2 > page_start1 and page_end2 == 0:
            text_2.append(text)
        if '管理层讨论与分析' in text and page.page_number > 5 and page_start1 == 0:
            page_start1 = page.page_number
        if '公司治理' in text and page.page_number > page_start1 + 1 and page_start1 > 5 and page_end1 == 0 and page_start2 == 0:
            page_end1 = page.page_number - 1
            page_start2 = page.page_number
        if '环境与社会责任' in text and page.page_number > page_start2 + 1 and page_end2 == 0 and page_start2 > 5:
            page_end2 = page.page_number - 1
        if page_start1 > 5 and page_start2 > 5 and page_end1 > 5 and page_end2 > 5:
            text_1 = ''.join(text_1)
            text_2 = ''.join(text_2)
            text_file1 = open(str(file).replace('.pdf', '') + "-管理层讨论与分析.txt", 'a', encoding='utf-8')
            text_file1.write(text_1)
            print(str(file) + '----管理层讨论与分析 截取成功！')
            text_file2 = open(str(file).replace('.pdf', '') + "-公司治理.txt", 'a', encoding='utf-8')
            text_file2.write(text_2)
            print(str(file) + '----公司治理 截取成功！')
            break
        if len(str(text).strip()) > 10:
            text_all.append(text)
    pdf.close()
    if len(text_all) > 1:
        text_all = ''.join(text_all)
        text_file = open(str(file).replace('.pdf', '') + "-全文.txt", 'a', encoding='utf-8')
        text_file.write(text_all)
        print(str(file) + '----全文保存成功！')
    else:
        file_name = ''.join(file).replace('.pdf', '') + ','
        text_file = open("img_files.txt",'a', encoding='utf-8')
        text_file.write(file_name)
        print(str(file) + '----纯图片，已记录！')


os.chdir('年报TXT')
with ThreadPoolExecutor(max_workers=8) as pool:
    futures = [pool.submit(convert_txt, file) for file in file_list]
