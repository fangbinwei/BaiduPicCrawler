# coding=utf-8

import requests
from requests import exceptions
import json
import pprint
import os
URL = 'https://image.baidu.com/search/acjson'
headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) '
           'AppleWebKit/537.36 (KHTML, like Gecko) '
           'Chrome/56.0.2924.87 Safari/537.36',
           'Referer': 'http://image.baidu.com/'}


def getPicURL(searchWord, pn):

    params = {'tn': 'resultjson_com', 'ipn': 'rj', 'is': '',
              'fp': 'result',
              'queryWord': searchWord,
              'cl': '2',
              'lm': '-1',
              'ie': 'utf-8',
              'oe': 'utf-8',
              'adpicid': '',
              'st': '-1',
              'z': '',
              'ic': '0',
              'word': searchWord,
              's': '',
              'se': '',
              'tab': '',
              'width': '',
              'height': '',
              'face': '0',
              'istype': '2',
              'qc': '',
              'nc': '1',
              'fr': '',
              'pn': str(pn),
              'rn': '30',
              }

    response = requests.get(URL, params=params, headers=headers)
    print response.content
    print json.dumps(json.loads(response.content), indent=4)

    URLList = []
    print type(URLList)
    for num in range(30):
        try:
            picURL = response.json()['data'][num]['replaceUrl'][0]['ObjURL']
        except KeyError as e:
            print num
            print e.message, '没有ObjURL'
            picURL = response.json()['data'][num]['thumbURL']

        print picURL
        URLList.append(picURL.encode('utf-8'))

    print '>>>>url'
    print response.url
    pprint.pprint(URLList)
    print len(URLList)
    basePath = os.getcwd()+'/'+searchWord+'/'
    picIndex = len(os.listdir(basePath))+1
    for num in range(len(URLList)):
        postFix = URLList[num].split('.')[-1]
        fileName = basePath+searchWord+str(picIndex)+'.'+postFix
        downloadPic(URLList[num], fileName=fileName)
        picIndex += 1


def downloadPic(URL, fileName):
    try:
        response = requests.get(URL, headers=headers, stream=True)
        response.raise_for_status()
        with open(fileName, 'wb') as f:
            print 'download ', fileName
            for chunk in response:
                f.write(chunk)
    except exceptions.HTTPError as e:
        print e.message


def startCrawler(searchWord, startPage=1, endPage=1):
    if not os.path.isdir(searchWord):
        try:
            os.mkdir(searchWord)
            for page in range(startPage, endPage + 1):
                startPicIndex = (startPage - 1) * 30
                getPicURL(searchWord, startPicIndex)

        except OSError:
            print 'there is a file named '+searchWord+'!!!!'



if __name__ == '__main__':

    startCrawler('花', startPage=1, endPage=1)
