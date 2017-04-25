# -*- coding:utf-8 -*-
from __future__ import unicode_literals
from db import db
import jieba
import numpy as np
from operator import itemgetter, attrgetter
import sys
import io

class nlp:
    def __init__(self,productId):
        self.productId=productId
        d=db()
        data=np.array(d.getCommentsOfProduct(productId))
        print(str(len(data))+' comments is successfully loaded')
        #print(data[0:3,1])
        self.total=len(data)
        self.rawComments=data[:,1]
        self.score=data[:,0]
    
    def jieba_seg(self):
        self.segComment=[list(jieba.cut(c,cut_all=False, HMM=True)) for c in self.rawComments]
        #print(self.rawComments[:2])
        #print(segComment[:2])
        return self.segComment
    
    def summary(self):
        words={}
        for c in self.jieba_seg():
            for w in c:
                if w not in words.keys():
                    words[w]=1
                words[w]+=1
        words= sorted(words.items(), key=lambda x:x[1], reverse=True)
        #words=sorted(words, key=itemgetter(1))

        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf8')
        for d in words:
            if d[1]>25:
                print(d[0]+" 出现了 " + str(d[1]))
        
        


if __name__=="__main__":
    n=nlp(2384387)
    #n.jieba_seg()
    n.summary()