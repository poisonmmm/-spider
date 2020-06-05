import requests
from bs4 import BeautifulSoup
import re
from pyquery import PyQuery
from PIL import Image


def new_file(path):
    with open(path, "w", encoding="utf-8")as f:
        f.write("\n")


def map_spider(url_file_name):
    """
    :param url_file_name: 写入文件路径
    :return:
    """
    n = 1
    map_urls = []
    for i in range(1, 11):
        i = str(i)
        map_url = "https://www.yaofangwang.com/catalog-4-p" + i + ".html"
        map_urls.append(map_url)
    for map_url in map_urls:
        print("第%d页" % n)
        n += 1
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                                 "Chrome/81.0.4044.138 Safari/537.36 Edg/81.0.416.72"}
        medicine_res = requests.get(url=map_url, headers=headers)
        medicine_res.encoding = medicine_res.apparent_encoding
        doc = PyQuery(medicine_res.text)
        pure_href_urls = doc('#wrap > div.iright.mt20 > ul > li > div > a.photo').items()
        medicine_url_list = []
        for href_urls_class in pure_href_urls:
            href_url = href_urls_class.attr("href")
            print(href_url)
            href_url = "https:" + href_url
            medicine_url_list.append(href_url)
        with open(url_file_name, "a+", encoding="utf-8")as f:
            for url in medicine_url_list:
                f.write(url)
                f.write("\n")


def get_medicine(medicine_url, info_path):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/81.0.4044.138 Safari/537.36 Edg/81.0.416.72"}
    response = requests.get(url=medicine_url, headers=headers)
    print(response.status_code)
    doc = PyQuery(response.text)
    medicine_info = doc("#guide > div.guide.guide2").text()
    medicine_name = doc("#wrap > div.maininfo.clearfix > div.right > h1 > strong").text()
    pic_href_url = doc("#wrap > div.maininfo.clearfix > div.left > a").attr("href")
    pic_url1 = doc("#thumblist > a.p.first > img").attr("src")
    small_pic1_url = "http:" + pic_url1
    big_pic1_url = re.findall("(http:.*?jpg_)", small_pic1_url, re.S)[0]
    big_pic1_url = big_pic1_url + "syp.jpg"
    pic_url = "https:" + pic_href_url
    with open(info_path, "a+", encoding="utf-8")as f:
        f.write(medicine_name)
        f.write(":\n")
        f.write(pic_url)
        f.write("\n")
        f.write("大图:\n")
        f.write(big_pic1_url + "\n")
        f.write("小图:\n")
        f.write(small_pic1_url + "\n")
        f.write(medicine_info)
        f.write("\n")
        f.write("*" * 50)
        f.write("\n\n")
    # 下载图片
    # pic = requests.get(pic_url, headers=headers)
    # with open("data/medicine/medicine_pic_lists/" + medicine_name + ".jpg", "wb")as f:
    #     f.write(pic.content)


if __name__ == "__main__":
    url_file_name = "medicine_url_map.txt"
    info_file_name = "medicine_info.txt"
    new_file(url_file_name)
    map_spider(url_file_name)
    with open(info_file_name, "w", encoding="utf-8")as f:
        f.write("药品列表：")
        f.write("\n")
    with open(url_file_name, "r", encoding="utf-8")as f:
        url_list = f.readlines()
        url_list = ''.join(url_list).strip('\n').splitlines()
        index = 1
        for url in url_list:
            print(index)
            index += 1
            get_medicine(url, info_file_name)
