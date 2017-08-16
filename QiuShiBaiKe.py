#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
from lxml import etree
from retrying import retry
import json

class QiuShiBaiKe:
    def __init__(self):
        self.temp_url = "https://www.qiushibaike.com/8hr/page/{}/"
        self.headers = {"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36"}

    # 1：获取url,一共13页
    def get_url_list(self):
        url_list = [self.temp_url.format(i) for i in range(1,14)]
        # print (url_list)
        return url_list

    # 2：发送请求，获取响应
    @retry(stop_max_attempt_number=3)
    def _parse_url(self,url):
        print("now parsing:",url)
        # 设置延迟5秒
        response = requests.get(url, headers=self.headers,timeout=5)
        # 设置状态码：
        assert response.status_code == 200
        # 把响应的对象转化为element对象
        return etree.HTML(response.content)

    # 存在没有响应的情况
    def parse_url(self,url):
        try:
            html = self._parse_url(url)
        except Exception as e:
            print(e)
            html = None
        return html

    # 3：提取数据
    def get_content_list(self,html):
        content_list = []
        # 包含div的elements列表
        div_list = html.xpath("//div[@id='content-left']/div")
        # 遍历拿到的列表：
        for div in div_list:
            item = {}
            # 获取用户头像链接：
            item["用户链接author_href："] = div.xpath("./div[@class='author clearfix']/a/@href")
            item["用户链接author_href："] = "https://www.qiushibaike.com"+item["用户链接author_href："][0] if len(item["用户链接author_href："]) > 0 else None
            # 获取用户名称：
            item["用户名user_name："] = div.xpath("./div/a/h2/text()")[0].replace("\n","") if len(div.xpath("./div/a/h2/text()")) > 0 else None
            # 获取内容：
            item["内容content："] = div.xpath(".//div[@class='content']/span/text()")[0].replace("\n","")
            # 获取点赞数
            item["stats_vote"] = div.xpath(".//div/span[@class='stats-vote']/i/text()")
            item["stats_vote"] = item["stats_vote"][0] if len(item["stats_vote"]) > 0 else 0
            # 获取评论数：
            item["评论数comment_number："] = div.xpath(".//div/span[@class='stats-comments']/a/i/text()")[0]
            content_list.append(item)

        return content_list

    # 保存数据
    def save_content_list(self, content_list):
        with open("qiubai.json","a",encoding="utf-8") as f:
            for content in content_list:
                f.write(json.dumps(content,ensure_ascii=False, indent=2))
                f.write("\n")

    def run(self):
        # 1:url_list
        url_list = self.get_url_list()
        # print(url_list)
        # 2:发送请求，获取相应
        for url in url_list:
            html = self.parse_url(url)

            # 3：提取数据
            content_list = self.get_content_list(html) if html is not None else []

            # 4：保存
            self.save_content_list(content_list)



if __name__ == '__main__':
    QiuBai = QiuShiBaiKe()
    QiuBai.run()