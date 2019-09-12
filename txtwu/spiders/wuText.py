# -*- coding: utf-8 -*-
import scrapy
import copy
from txtwu.items import TxtwuItem


class WutextSpider(scrapy.Spider):
	name = 'wuText'
	#allowed_domains = ['m.txtwu.org']
	allowed_domains = ['m.txtwu.org']
	# 修改目录
	offset = 7
	start_urls = ["https://m.txtwu.org/top/allvisit_"+str(offset)+"/"]
	server = "https://m.txtwu.org/"
	# 小说本数记录器
	#counter = 1
# 获得每一页书的链接，并循环到下一页
	def parse(self, response):
		url_list = response.xpath('//a[contains(@href,"/wapbook/")]/@href').extract()
		#print(url_list)
		for index,url in enumerate(url_list):
			book_url = self.server + url
			yield scrapy.Request(book_url,callback = self.parse_read_name)
			#book_name = response.xpath('//meta[@property="og:novel:book_name"]/@content').extract()
			#print(book_name)
			#item['bookname'] = book_name
			
			#print("《"+book_name+"》链接为："+book_url+"，开始下载")
			#self.counter++
			#yield scrapy.Request(book_url,callback = self.parse1,meta = {'item':copy.deepcopy(item)})
		#if (self.offset < 592):
		#	self.offset = self.offset+1
		#	next_urls = "https://m.txtwu.org/top/allvisit_"+str(self.offset)+"/"
		#	yield scrapy.Request(next_urls, callback = self.parse)
		#else:
			return None
# 获得阅读链接和书名
	def parse_read_name(self, response):
		item = TxtwuItem()
		book_name = response.xpath('//meta[@property="og:novel:book_name"]/@content').extract()[0]
		#print("《"+book_name+"》开始下载:")
		item['bookname'] = "".join(book_name).replace('/','')
		read_url = self.server+response.xpath('//span[@class="margin_right"]/a/@href').extract()[0]
		#print("《"+book_name+"》阅读链接为："+read_url)
		#item = response.meta['item']
		yield scrapy.Request(read_url,callback = self.parse_contents,meta = {'item':copy.deepcopy(item)})
# 获得文本
	def parse_contents(self, response):
		item = response.meta['item']
		contents = response.xpath('//*[@id="nr1"]/text()').extract()
		book_contents = "\n".join(contents)
		item['bookcontents'] = book_contents
		#print("\n".join(book_contents))
		# 下一页链接
		n_url = self.server+response.xpath('//*[@id="pb_next"]/@href').extract()[0]
		# 目录链接
		m_url = self.server+response.xpath('//*[@id="pt_next"]/@href').extract()[0]
		yield item
		if (m_url == n_url):
			print("全部章节下载完成")
			return 
		else:
			yield scrapy.Request(n_url,callback = self.parse_contents,meta = {'item':copy.deepcopy(item)})





