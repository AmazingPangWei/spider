# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.pipelines.images import ImagesPipeline
from urllib.parse import urlparse
from os.path import basename,dirname,join



class GithubPipeline(object):
    def process_item(self, item, spider):
        return item
class MyImagesPipeline(ImagesPipeline):
    def file_path(self, request, response=None, info=None):
        #获取相对路径
        path = urlparse(request.url).path

        # basename()
        # 去掉目录路径, 返回文件名
        # os.path.basename('c:\\test.csv')
        # 'test.csv'

        # dirname()
        # 去掉文件名, 返回目录路径
        # os.path.dirname('c:\\csv\test.csv')
        # 'c:\\'


        # join()
        # 将分离的各部分组合成一个路径名
        # os.path.join('c:\\', 'csv', 'test.csv')
        # 'c:\\csv\\test.csv'

        #https://matplotlib.org/examples/animation/animate_decay.html
        #path= /examples/animation/animate_decay.html
        #dirname(path) = /examples/animation/
        #basename(path) = animate_decay.html
        #basename(dirname(path)) = animation
        #join(basename(dirname(path)),basename(path)) = animation\animate_decay.html
        return basename(path)
