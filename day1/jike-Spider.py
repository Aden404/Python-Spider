#-*- coding:utf-8 -*-
#Python 3.5

import requests
import re



class Spider:
    def __init__(self):
        print ('开始爬取极客学院课程信息。。。')

    # 获取源代码
    def getSource(self, url):
        html = requests.get(url)
        return html.text

    # 获取每个课程块信息
    def getLessons(self, source):
        lessons = re.findall('deg="0" >(.*?)</li>', source, re.S)
        return lessons

    # 获取课程信息，如课程名称、课程介绍、课程时间、课程等级、学习人数
    def getLessonInfo(self, lesson):
        info = {}
        info['title'] = re.search('<h2 class="lesson-info-h2"><a(.*?)>(.*?)</a></h2>', lesson, re.S).group(2).strip()
        info['desc'] = re.search('<p style="height: 0px; opacity: 0; display: none;">(.*?)</p>', lesson, re.S).group(
            1).strip()
        info['img'] = re.search('<img src=(.*?) class',lesson,re.S).group(1).strip()
        timeandlevel = re.findall('<em>(.*?)</em>', lesson, re.S)
        info['time'] = timeandlevel[0].strip().replace("\n", "").replace("    ", "")
        info['level'] = timeandlevel[1].strip()
        info['learnNumber'] = re.search('"learn-number">(.*?)</em>', lesson, re.S).group(1).strip()
        return info

    # 保存课程信息到文件LessionInfos.txt
    def saveLessionInfos(self, lessonInfos):
        # 'w'：只写，会覆盖之前写入的内容
        # 也可以用'a'：追加到文件末尾
        # 如果文件不存在，则自动创建文件
        f = open('MMinfo.txt', 'w')
        i = 0
        for each in lessonInfos:
            i += 1
            f.writelines('第' + str(i) + '个课程：\n')
            f.writelines('title:' + each['title'] + '\n')
            f.writelines('desc:' + each['desc'] + '\n')
            f.writelines('img: ' + each['img'] + '\n')
            f.writelines('time:' + each['time'] + '\n')
            f.writelines('level:' + each['level'] + '\n')
            f.writelines('learnNumber:' + each['learnNumber'] + '\n\n')
        f.close()


if __name__ == '__main__':
    # 定义课程信息数组
    lessonInfos = []
    # 课程信息页面url
    url = 'http://www.jikexueyuan.com/course/'
    # 实例化爬虫
    spider = Spider()
    # 取[1,21)及1到20页的课程信息
    for i in range(1, 21):
        # 构建分页URL
        pageUrl = url + '?pageNum=' + str(i)
        print ('正在处理页面：' + pageUrl)
        source = spider.getSource(pageUrl)
        lessons = spider.getLessons(source)
        for lesson in lessons:
            lessonInfo = spider.getLessonInfo(lesson)
            lessonInfos.append(lessonInfo)
            # print 'title:'+lessonInfo.get('title')
            # print 'desc:'+lessonInfo.get('desc')
            # print 'time:'+lessonInfo.get('time')
            # print 'level:'+lessonInfo.get('level')
            # print 'learnNumber:'+lessonInfo.get('learnNumber')
    spider.saveLessionInfos(lessonInfos)