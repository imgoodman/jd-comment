# -*- coding:utf-8 -*-

import requests
from time import sleep
from db import db

#base_url="https://club.jd.com/comment/productPageComments.action?productId=2384387&score=0&sortType=5&page=0&pageSize=10&isShadowSku=0"
#product_id=""

class comment:
    def __init__(self,productId):
        self.productId=productId
        self.url="https://club.jd.com/comment/productPageComments.action?score=0&sortType=5&pageSize=10&isShadowSku=0"
    
    def get_paged_comment(self,page):
        self.page=page
        url=( (self.url+"&page=%d&productId=%d") % (self.page,self.productId))
        #print(url)
        response=requests.get(url)
        #print(response.text)
        #print(response.json())
        return response.json()
    
    def get_comment(self):
        currentPage=4300
        saveIndex=1
        d=db()
        first_page_comment=self.get_paged_comment(currentPage)
        if first_page_comment==None:
            print("no comment data")
            return None
        print(">>> comments of page %d" % currentPage)
        if len(first_page_comment["comments"])>0:
            for c in first_page_comment["comments"]:
                #print("id:%d; guid:%s; comment time:%s; score:%d" % (c["id"],c["guid"],c["creationTime"],c["score"]))
                #print(c["content"])
                d.saveComment(self.productId, c["id"], c["guid"], c["creationTime"], c["score"], c["content"])
                print("%d comments have been saved to db" % saveIndex)
                saveIndex+=1
            self.totalPages=first_page_comment["maxPage"]
            currentPage+=1
            print("max pages: %d" % self.totalPages)
        else:
            self.totalPages=0

        if self.totalPages>1:
            for i in range(currentPage,self.totalPages+1):
                sleep(30)
                comment_of_page=self.get_paged_comment(i)
                if comment_of_page==None:
                    continue
                print(">>> comments of page %d" % i)
                if comment_of_page["comments"] !=None:
                    for c in comment_of_page["comments"]:
                        #print("id:%d; guid:%s; comment time:%s; score:%d" % (c["id"],c["guid"],c["creationTime"],c["score"]))
                        #print(c["content"])
                        d.saveComment(self.productId, c["id"], c["guid"], c["creationTime"], c["score"], c["content"])
                        print("%d comments have been saved to db" % saveIndex)
                        saveIndex+=1
                else:
                    break