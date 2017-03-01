# coding=utf-8

import requests
from requests import exceptions
import json
import pprint
import time
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

    try:
        response = requests.get(URL, params=params,
                                headers=headers, timeout=10)
        response.raise_for_status()
    except exceptions.Timeout as e:
        print e.message
    except exceptions.HTTPError as e:
        print e.message
    except Exception as e:
        print 'something wrong!'
        raise Exception
    else:
        # print json.dumps(json.loads(response.content), indent=4)
        # print response.json()
        responseContent = json.loads(response.content)
        # print type(responseContent['bdFmtDispNum'])
        # print type(responseContent['bdFmtDispNum'].encode('utf8'))
        URLList = parseResponse(responseContent)
        return URLList


def parseResponse(responseContent):
    picSum = int(filter(str.isalnum,
                        responseContent['bdFmtDispNum'].encode('utf-8')))

    if not picSum:
        print 'no picture find'
        exit()
    else:
        print 'there are about ' + str(picSum) + ' pictures'

    URLList = []
    for num in range(30):
        try:
            picURL = responseContent['data'][num
                                             ]['replaceUrl'][0]['ObjURL']
        except KeyError as e:
            print num
            print e.message, '没有ObjURL'
            picURL = responseContent['data'][num]['thumbURL']

        # print type(picURL)
        # print type(picURL.encode('utf-8'))
        URLList.append(picURL.encode('utf-8'))
    return URLList


def downloadPic(searchWord, pn):
    URLList = getPicURL(searchWord, pn)
    # print len(URLList)
    # pprint.pprint(URLList)
    basePath = os.getcwd() + '/' + searchWord + '/'
    picIndex = len(os.listdir(basePath)) + 1
    for num in range(len(URLList)):
        postFix = URLList[num].split('.')[-1]
        fileName = basePath + searchWord + str(picIndex) + '.' + postFix

        try:
            response = requests.get(URLList[num], headers=headers, stream=True)
            time.sleep(1)
            response.raise_for_status()
            with open(fileName, 'wb') as f:
                print 'download ', fileName
                for chunk in response:
                    f.write(chunk)
        except exceptions.HTTPError as e:
            print e.message

        picIndex += 1


def startCrawler(searchWord, startPage=1, endPage=1):
    if not os.path.isdir(searchWord):
        try:
            os.mkdir(searchWord)

        except OSError:
            print 'there is a file named '+searchWord+'!!!!'
            exit()

    for page in range(startPage, endPage + 1):
        startPicIndex = (page - 1) * 30
        try:
            downloadPic(searchWord, startPicIndex)
            time.sleep(5)
        except:
            print 'start download next page'


if __name__ == '__main__':

    startCrawler('angel beats', startPage=3, endPage=4)
