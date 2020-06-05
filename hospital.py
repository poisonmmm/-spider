
import requests
import re
from pyquery import PyQuery
from PIL import Image
from bs4 import BeautifulSoup

# 医院信息 写入 读取文件名
write_file_name = "hospital_info.txt"
read_file_name = "hospital_url_map.txt"

"""
获取医院url地图
"""
def url_map():
    """
    爬取网站页面每个详情的url
    写入文件
    :return:
    """
    map_urllist = []
    for i in range(0, 5):
        i = str(i)
        map_url = "https://www.yaofangwang.com/yiyuan/r1727/p" + i + "/"
        map_urllist.append(map_url)
    for map_url in map_urllist:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                                 "Chrome/81.0.4044.138 Safari/537.36 Edg/81.0.416.72"}
        hospital_res = requests.get(url=map_url, headers=headers)
        hospital_res.encoding = hospital_res.apparent_encoding

        doc = PyQuery(hospital_res.text)
        pure_href_urls = doc('#wrap > div:nth-child(3) > div.left > ul > li > div > a').items()
        href_urls_list = []
        urls_list = []
        base_url = "https://www.yaofangwang.com/yiyuan"
        for href_urls_class in pure_href_urls:
            two_href_urls = href_urls_class.attr("href")
            # 正则表达式筛选出url后缀
            href_url = re.search("/3(.*?)html", two_href_urls, re.S).group()
            href_urls_list.append(href_url)
        for href_url in href_urls_list:
            url = base_url + href_url
            urls_list.append(url)
        with open(read_file_name, "w", encoding="utf-8")as f:
            f.write("\n")
        with open(read_file_name, "a+", encoding="utf-8")as f:
            for url in urls_list:
                f.write(url)
                f.write("\n")
    print("url获取完成")


"""
爬取医院信息
"""


def get_hospital_info_html(hospital_url):
    # 传入url，获取医院的html
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                             "Chrome/81.0.4044.138 Safari/537.36 Edg/81.0.416.72"}
    hospital_res = requests.get(url=hospital_url, headers=headers)
    hospital_res.encoding = hospital_res.apparent_encoding
    # with open("data/hospital/hospital.html", "w", encoding="utf-8") as f:
    #     f.write(hospital_res.text)
    return hospital_res.text


def parser_hospital_info_txt(hospital_html):
    """
    传入医院html，获取医院信息
    data1:医院名称
    data2:医院详情
    """
    soup = BeautifulSoup(hospital_html, "html.parser")
    result_info_list = soup.find_all("div", class_="info")
    result_tbock_list = soup.find_all("div", class_="tbock", limit=3)
    for result in result_info_list:
        data1 = result.get_text()
    data2_list = []
    for result in result_tbock_list:
        data2 = result.get_text()
        data2_list.append(data2)
    with open(write_file_name, "a+", encoding="utf-8")as f:
        f.write(data1)
        for one in data2_list:
            f.write(one)
        f.write("#" * 50)


if __name__ == "__main__":
    url_map()
    # 清空info文件
    with open(write_file_name, "w", encoding="utf-8")as f:
        f.write("医院列表：\n")
        print("文件成功创建")

    # 执行两个函数，以追加方式写入文件
    with open(read_file_name, "r", encoding="utf-8")as f:
        url_list = f.readlines()
        # 去掉readlines()里的\n
        url_list = ''.join(url_list).strip('\n').splitlines()
        index = 1
        for href_url in url_list:
            print("已爬取医院数量：", index)
            index += 1
            hospital_html = get_hospital_info_html(href_url)
            parser_hospital_info_txt(hospital_html)
