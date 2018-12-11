# -*- coding: utf-8 -*-

import scrapy
import re
import time
from jingdong.items import JingdongItem, JingdongItem2

class JiadianSpider(scrapy.Spider):
    name = 'jiadian'
    allowed_domains = ['search.jd.com']
    #商品url链接列表,如
    start_urls = ['https://item.jd.com/6533301.html?jd_pop=93dbc83f-c497-434a-920c-e7bb5bdedc42&abt=0',]


    def parse(self, response):
        print(response.text)
        good_id = re.findall('/(\d+).html', response.url)[0]
        print('进入详情页的id:',good_id)
        #商品名称，有的第一个为空
        filename = response.xpath('//div[contains(@class,"itemInfo-wrap")]/div[contains(@class,"sku-name")]/text()').extract()[-1].strip()
        if '/' in filename:
            filename = filename.replace('/', '-')
        if ':' in filename:
            filename = filename.replace(':', '')
        if '?' in filename:
            filename = filename.replace('?', '')
        if '|' in filename:
            filename = filename.replace('|', '_')
        intruduce = response.xpath('//div[@id="detail"]//div[contains(@class,"p-parameter")]/ul[contains(@class,"parameter2")]/li/text()').extract()
        intruduce = self.deal_intruduce(intruduce)
        pic_ids = response.xpath('//div[@id="choose-attr-1"]/div[contains(@class,"dd")]/div/@data-sku').extract()
        pic_names = response.xpath('//div[@id="choose-attr-1"]/div[contains(@class,"dd")]/div/a/img/@alt').extract()
        if pic_ids:
            for n, value in enumerate(pic_ids):
                url = "https://item.jd.com/" + pic_ids[n] + ".html"
                print(pic_ids[n], pic_names[n])
                yield scrapy.Request(url, callback=self.detailpage, meta={'filename': filename, 'intruduce': intruduce, 'name': pic_names[n], 'good_id': pic_ids[n]}, dont_filter=True)
        else:
            item = JingdongItem()
            item['filename'] = filename
            item['intruduce'] = self.deal_intruduce(intruduce)
            img_urls1 = response.xpath('//div[@id="spec-list"]/ul/li/img/@src').extract()
            item['img_urls'] = self.deal_img(img_urls1)  # 每种款式的所有图片
            item['good_id'] = good_id
            item['img_name'] = item['filename'][-10:]
            yield item

        #评论部分
        url = "https://club.jd.com/discussion/getProductPageImageCommentList.action?productId=" + good_id + "&isShadowSku=0&page=1&pageSize=10&_=" + str(time.time() * 1000)[:-4]
        yield scrapy.Request(url, callback=self.pinglun, meta={'filename': filename, 'good_id': good_id, }, dont_filter=True)


    def detailpage(self, response):
        item = JingdongItem()
        item['filename'] = response.meta['filename']
        item['intruduce'] = response.meta['intruduce']
        item['good_id'] = response.meta['good_id']  # 每种款式的id
        img_urls1 = response.xpath('//div[@id="spec-list"]/ul/li/img/@src').extract()
        item['img_urls'] = self.deal_img(img_urls1)  # 每种款式的所有图片
        name = response.meta['name']  # 款式名称
        if "/" in name:
            name = name.replace("/", "_")
        if ':' in name:
            name = name.replace(':', '')
        if '|' in name:
            name = name.replace('|', '_')
        item['img_name'] = name
        yield item

    def pinglun(self, response):
        filename = response.meta['filename']
        good_id = response.meta['good_id']
        nums = re.findall('"imgCommentCount":(\d+)', response.text)[0]
        if nums == 0:
            return
        pages = int(nums) // 10
        # print(pages)
        for page in range(1, pages + 2):
            url = "https://club.jd.com/discussion/getProductPageImageCommentList.action?productId=" + good_id + "&isShadowSku=0&page=" + str(page) + "&pageSize=10&_=" + str(time.time() * 1000)[:-4]
            try:
                yield scrapy.Request(url, callback=self.get_content, meta={'filename': filename, 'page': page}, dont_filter=True)
            except:
                continue
    def get_content(self, response):
        item = JingdongItem2()
        item['filename'] = response.meta['filename']
        item['page'] = response.meta['page']
        item['contents_Urls'] = re.findall('"imageUrl":"(//.*?.jpg)"', response.text)
        item['contents'] = re.findall('"content":"(.*?)"', response.text)
        item['productColors'] = re.findall('"productColor":"(.*?)"', response.text)
        yield item

    def deal_img(self,lst):
        l1 = []
        for u in lst:
            i = u.replace('n5', 'n1')
            j = i.replace('50x64', '350x449')
            k = "https:" + j
            l1.append(k)
        return l1

    def deal_intruduce(self,l):
        d = {}
        for i in l:
            j = i.split('：')
            if len(j) == 1:
                j.append(' ')
            d[j[0]] = j[-1]
        return d