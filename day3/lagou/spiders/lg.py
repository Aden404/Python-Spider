# # -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
import scrapy
import json
from lagou.items import LagouItem
#from lagou.items import LagouItem
#from scrapy_redis.spiders import RedisSpider

class LgSpider(scrapy.Spider):
    name = "lg"
    #allowed_domains = ["lagou.com/zhaopin/"]
    # start_urls = (
    #     'http://www.lagou.com/jobs/positionAjax.json?gj=%E5%BA%94%E5%B1%8A%E6%AF%95%E4%B8%9A%E7%94%9F&xl=%E5%A4%A7%E4%B8%93&jd=%E6%88%90%E9%95%BF%E5%9E%8B&hy=%E7%A7%BB%E5%8A%A8%E4%BA%92%E8%81%94%E7%BD%91&px=new&city=%E4%B8%8A%E6%B5%B7',
    # )
    totalPageCount = 0
    curpage = 1
    cur = 0
    myurl = 'http://www.lagou.com/jobs/positionAjax.json?'
    city = u'北京'
    kds = [u'VB',u'Dephi','Perl','Ruby','Go','ASP','Shell',u'java',u'python','PHP','.NET','JavaScript','C#','C++','C']
    # ['Node.js',u'数据挖掘',u'自然语言处理',u'搜索算法',u'精准推荐',u'全栈工程师']
    # ['HTML5','Android','iOS',u'web前端','Flash','U3D','COCOS2D-X']
    # [u'spark','MySQL','SQLServer','Oracle','DB2','MongoDB' 'ETL','Hive',u'数据仓库','Hadoop']
    kd = kds[0]
    def start_requests(self):
        # for self.kd in self.kds:
        #
        #     scrapy.http.FormRequest(self.myurl,
        #                                 formdata={'pn':str(self.curpage),'kd':self.kd},callback=self.parse)
         return [scrapy.http.FormRequest(self.myurl,
                                        formdata={'pn':str(self.curpage),'kd':self.kd},callback=self.parse)]

    def parse(self, response):
        #print response.body
        # fp = open('1.html','w')
        # fp.write(response.body)
        item = LagouItem()
        jdict = json.loads(response.body)
        jcontent = jdict["content"]
        jposresult = jcontent["positionResult"]
        jresult = jposresult["result"]
        self.totalPageCount = jposresult['totalCount'] /15 + 1;
        # if self.totalPageCount > 30:
        #     self.totalPageCount = 30;
        for each in jresult:
            item['city']=each['city']
            item['companyName'] = each['companyName']
            item['companySize'] = each['companySize']
            item['positionName'] = each['positionName']
            item['positionType'] = each['positionType']
            sal = each['salary']
            sal = sal.split('-')
            print sal
            if len(sal) == 1:
                item['salaryMax'] = int(sal[0][:sal[0].find('k')])
            else:
                item['salaryMax'] = int(sal[1][:sal[1].find('k')])
            item['salaryMin'] = int(sal[0][:sal[0].find('k')])
            item['positionAdvantage'] = each['positionAdvantage']
            item['companyLabelList'] = each['companyLabelList']
            item['keyword'] = self.kd
            yield item
        if self.curpage <= self.totalPageCount:
            self.curpage += 1
            yield scrapy.http.FormRequest(self.myurl,
                                        formdata = {'pn': str(self.curpage), 'kd': self.kd},callback=self.parse)
        elif self.cur < len(self.kds)-1:
            self.curpage = 1
            self.totalPageCount = 0
            self.cur += 1
            self.kd = self.kds[self.cur]
            yield scrapy.http.FormRequest(self.myurl,
                                        formdata = {'pn': str(self.curpage), 'kd': self.kd},callback=self.parse)











#-------------------------------------------------------------
# import scrapy
# import json
# from lagou.items import LagouItem
#
# class LgSpider(scrapy.Spider):
#     name = "lg"
#     #allowed_domains = ["lagou.com/zhaopin/"]
#     # start_urls = (
#     #     'http://www.lagou.com/jobs/list_?px=new&gj=%E5%BA%94%E5%B1%8A%E6%AF%95%E4%B8%9A%E7%94%9F&xl=%E6%9C%AC%E7%A7%91&hy=%E7%A7%BB%E5%8A%A8%E4%BA%92%E8%81%94%E7%BD%91&city=%E5%8C%97%E4%BA%AC',
#     # )
#     totalPageCount = 0
#     curpage = 1
#     cur = 0
#     #myurl = 'http://www.lagou.com/jobs/positionAjax.json?'
#     myurl = 'http://www.lagou.com/jobs/positionAjax.json?'
#     city = u'北京'
#     kds = [u'PHP',u'java', u'python', '.NET', 'JavaScript', 'C#', 'C++', 'C', 'VB', 'Dephi', 'Perl', 'Ruby', 'Go', 'ASP',
#            'Shell']
#     kd = kds[0]
#     def start_requests(self):
#         # return [scrapy.http.FormRequest('http://www.lagou.com/jobs/positionAjax.json?gj=%E5%BA%94%E5%B1%8A%E6%AF%95%E4%B8%9A%E7%94%9F&xl=%E6%9C%AC%E7%A7%91&hy=%E7%A7%BB%E5%8A%A8%E4%BA%92%E8%81%94%E7%BD%91&px=new&city=%E5%8C%97%E4%BA%AC&',
#         #                                 formdata={'pn': '4'}, callback=self.parse)]
#         return [scrapy.http.FormRequest(self.myurl,
#                                         formdata={'pn': str(self.curpage), 'kd': self.kd}, callback=self.parse)]
#
#     def parse(self, response):
#         item = LagouItem()
#         jdict = json.loads(response.body)
#         jcontent = jdict['content']
#         jposresult = jcontent['positionResult']
#         jresult = jposresult['result']
#         self.totalPageCount = jposresult['totalCount'] / 15;
#         for each in jresult:
#             # print each['city']
#             # print each['companyName']
#             # print each['companySize']
#             # print each['positionName']
#             # print each['positionType']
#             # print each['salary']
#             # print ''
#             item['city'] = each['city']
#             item['companyName'] = each['companyName']
#             item['companySize'] = each['companySize']
#             item['positionName'] = each['positionName']
#             item['positionType'] = each['positionType']
#             item['salary'] = each['salary']
#             yield item
#             if self.curpage <= self.totalPageCount:
#                 self.curpage += 1
#                 yield scrapy.http.FormRequest(self.myurl,
#                                               formdata={'pn': str(self.curpage), 'kd': self.kd}, callback=self.parse)
#             elif self.cur < len(self.kds) - 1:
#                 self.curpage = 1
#                 self.totalPageCount = 0
#                 self.cur += 1
#                 self.kd = self.kds[self.cur]
#                 yield scrapy.http.FormRequest(self.myurl,
#                                               formdata={'pn': str(self.curpage), 'kd': self.kd}, callback=self.parse)
#
#                 # if self.curpage <= self.totalPageCount:
#             #     self.curpage += 1
#             #     yield scrapy.http.FormRequest(self.myurl,
#             #                                   formdata={'pn': str(self.curpage), 'kd': self.kd}, callback=self.parse)
#             # elif self.cur < len(self.kds) - 1:
#             #     self.curpage = 1
#             #     self.totalPageCount = 0
#             #     self.cur += 1
#             #     self.kd = self.kds[self.cur]
#             #     yield scrapy.http.FormRequest(self.myurl,
#             #                                   formdata={'pn': str(self.curpage), 'kd': self.kd}, callback=self.parse)