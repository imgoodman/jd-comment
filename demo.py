# -*- coding:utf-8 -*-

import requests

url="https://club.jd.com/comment/productPageComments.action?productId=2384387&score=0&sortType=5&page=0&pageSize=10&isShadowSku=0"
response=requests.get(url)
print("headers")
print(response.headers)
print("body")
print(response.text)
print(response.json())