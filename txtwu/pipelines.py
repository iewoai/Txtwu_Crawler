# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class TxtwuPipeline(object):

	def process_item(self, item, spider):
		path = item['bookname'] + '.txt'
		file_path = 'F://pyData//nb_scrapy//'+path
		contents = item['bookcontents']
		with open(file_path,'a',encoding='utf-8') as f:
				f.writelines(contents)
		return item
