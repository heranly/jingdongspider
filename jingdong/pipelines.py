# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import os
from urllib.request import urlretrieve
import json

class JingdongPipeline(object):
    def process_item(self, item,spider):
        #文件保存本地的位置
        if not os.path.exists('E:\京东商品爬取\jingdong'):
            os.mkdir('E:\京东商品爬取\jingdong')
        file_path1 = '{0}/{1}'.format('E:\京东商品爬取\jingdong',item['filename'])
        if not os.path.exists(file_path1):
            os.mkdir(file_path1)
        # file_path1 = '{0}/{1}'.format(file_path0, item['filename'])
        # if not os.path.exists(file_path1):
        #     os.mkdir(file_path1)
        if 'intruduce' in item:
            print('-------------开始写商品图片和id-------------')
            file_path3 = '{0}/{1}.{2}'.format(file_path1, '商品介绍', 'txt')
            if not os.path.exists(file_path3):
                with open(file_path3, 'w') as f:
                    text = json.dumps(item['intruduce'], ensure_ascii=False) + "\n"
                    f.write(text)# 写入商品描述
                    f.close()
            file_path2 = '{0}/{1}'.format(file_path1, '商品图片')
            if not os.path.exists(file_path2):
                os.mkdir(file_path2)
            id_path = '{0}/{1}'.format(file_path2,'商品id及款式.txt')
            if not os.path.exists(id_path):
                with open(id_path, 'a+') as f:
                    if item['good_id'] not in f.read():
                        f.write(item['good_id'])
                        for i in range(1, len(item['img_urls']) + 1):
                            f.write('  ' + item['img_name'] + '_%s' % i + '.jpg')
                    f.write('\n\n')
                    f.close()
            else:
                f=open(id_path,'r')
                result = f.read()
                f.close()
                with open(id_path, 'a+') as f:
                    if item['good_id'] not in result:
                        f.write(item['good_id'])
                        for i in range(1, len(item['img_urls']) + 1):
                            f.write('  ' + item['img_name'] + '_%s' % i + '.jpg')
                    f.write('\n\n')
                    f.close()

            for i in range(1, len(item['img_urls'])+1):
                img_path = '{0}/{1}.{2}'.format(file_path2, item['img_name']+'_%s'%i, 'jpg')
                try:
                    if not os.path.exists(img_path):
                        urlretrieve(item['img_urls'][i-1], filename=img_path)
                    else:
                        print('已经存在')
                        continue
                except Exception as e:
                    print('错误：', e)
                    continue
            print(item['filename'] + '图片部分写入完毕------------------')

        else:
            print('-------------开始写用户评论和图片-------------')
            file_path4 = '{0}/{1}'.format(file_path1, '用户晒图评论')
            if not os.path.exists(file_path4):
                os.mkdir(file_path4)
            for i in range(1, len(item['contents_Urls'])+1):
                if '/' in item['productColors'][i - 1]:
                    item['productColors'][i - 1] = item['productColors'][i - 1].replace('/', '-')
                imgs_path1 = '{0}/{1}.{2}'.format(file_path4, item['productColors'][i-1]+'_'+str(item['page'])+'_%s'%str(i), 'jpg')
                try:
                    if not os.path.exists(imgs_path1):
                        urlretrieve("https:"+item['contents_Urls'][i-1], filename=imgs_path1)
                    else:
                        print('------------------已经存在啦-------------------')
                        continue
                except:
                    continue
                # 商品描述文件
                file_path5 = '{0}/{1}.{2}'.format(file_path4, str(item['page']) + '_%s' % str(i), 'txt')
                if not os.path.exists(file_path5):
                    with open(file_path5, 'w') as f:
                        f.write(item['contents'][i - 1])  # 写入商品描述
            print(item['filename'] + '评论部分写入完毕------------------')
        return item
