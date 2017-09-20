# -*- coding: utf-8 -*-
"""
Created on Wed Sep 20 15:19:34 2017

@author: Kong, Seokkyu

Summary:
    naver 환율 조회 페이지를 파싱해서 국가별 환율 정보를 조회한다.
"""

import sys
import re
from bs4 import BeautifulSoup

if sys.version_info > (3, 0):
    # version 3.x
    import urllib
    from urllib.request import Request, urlopen
    from urllib.parse import quote
else:
    # version 2.x
    import urllib2
    from urllib2 import Request, quote, urlopen
    
import requests as rs


def getPage(url):
    """
    url 정보의 내용을 조회한다.
    """
    try:
        req = Request(url)
        res = urlopen(req)

        content = res.read()
        
    except:
        content = ""
        
    return content

def getExchangeOfNation(soup):
    """
    국가별 환율 정보를 dictionary로 구축한다.
    """
    dicExchange = {} # 국가별 환율정보를 저장하는 dictionary 변수
    
    alpha = '([A-Z]+)' # 국가 코드 분리 - 정규식 적용
    
    # 1, 2행의 tr은 테이블 헤더 정보이다.
    # 2행 이후부터 테이블의 컬럼값을 조회한다.
    for item in soup.table('tr')[2:]:
        
        # 정보 파싱
        nation = item('td')[0].text.strip() # 국가정보 파싱
        re_result = re.search(alpha, nation)
        nation = re_result.groups()[0]
        
        basicRateOfExchange = item('td')[1].text # 매매기준환율
        cash_buy = item('td')[2].text #  현찰 살때
        cash_sell = item('td')[3].text # 현찰 팔때
        transfer_send = item('td')[4].text # 송금 보낼 때
        transfer_receive = item('td')[5].text # 송금 받을 때
        
        dicExchange[nation] = {'basicRate':basicRateOfExchange, 'cashBuy':cash_buy, \
                   'cashSell':cash_sell, 'transferSend':transfer_send, 'transferReceive':transfer_receive}
    
    return dicExchange        

# naver 환율 페이지 조회
url = "http://info.finance.naver.com/marketindex/exchangeList.nhn"
    
# page 내용을 조회한다.
res = getPage(url)

soup = BeautifulSoup(res, 'html.parser')
#print(soup.prettify)
# soup.table('tr')[2]('td')[0].text.strip()

nationExchangeRate = getExchangeOfNation(soup)

# 환율 조회 출력
print(nationExchangeRate['USD'])
print(nationExchangeRate['JPY'])

