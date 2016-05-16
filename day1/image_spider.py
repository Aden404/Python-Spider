#-*- coding:utf-8 -*-
#Python 3.5
import re
import requests
import os

def image_spider(html,keyword):
    #img_url = re.findall('"objURL":"(.*?)",',html,re.S)
    img_url = re.findall('"objURL":"(.*?)",', html, re.S)
    i = 0
    os.system("mkdir images")
    print('find the image of : ' + keyword + ',now loading...')
    for each in img_url:
        print('now loading the image of number '+ str(i+1) + 'image, the address is : ' + str(each))
        try:
            img = requests.get(each,timeout=10)
        except requests.exceptions.ConnectionError:
            print('the image can\'t download')
            continue
        img_path = "images/%s_%d.jpg"%(keyword,i)
        f = open(img_path,'wb')
        f.write(img.content)
        f.close()
        i += 1

if __name__ == '__main__':
    word = input("Input a keyword: ")
    #print(word)
    url = 'http://image.baidu.com/search/flip?tn=baiduimage&ie=utf-8&word=' + word + '&ct=201326592&v=flip'
    result = requests.get(url)
    image_spider(result.text,word)