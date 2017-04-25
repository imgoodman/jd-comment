import configparser
import pymysql
import json

class db:
    def __init__(self):
        config=configparser.ConfigParser()
        config.read("config.conf")
        self.dburl=config.get("db","url")
        self.dbusername=config.get("db","username")
        self.dbpwd=config.get("db","pwd")
        self.dbname=config.get("db","name")
        #print(self.dburl)
        #print(self.dbusername)
        #print(self.dbpwd)
        #print(self.dbname)
    

    def saveComment(self,productId,commentId,commentGuid,commentTime,score,content):
        print("productId:%d; id:%d; guid:%s; comment time:%s; score:%d" % (productId,commentId,commentGuid,commentTime,score))
        #print(content)
        conn=pymysql.connect(host=self.dburl, user=self.dbusername, passwd=self.dbpwd,db=self.dbname, port=3306, charset="utf8")
        #conn.set_charset("utf8")
        try:
            with conn.cursor() as cursor:
                #cursor.execute("set names utf8;")
                #cursor.execute("set character set utf8;")
                #cursor.execute("set character_set_connection=utf8;")
                #sql="insert into t_comment (productId,id,guid,create_time,score,content) values (%d,%d,'%s','%s',%d,'%s')" % (productId,commentId,commentGuid,commentTime,score,content)
                cursor.execute('select count(0) from t_comment where id=%s', (commentId) )
                if cursor.fetchone()[0]==0:
                    cursor.execute('insert into t_comment (productId,id,guid,create_time,score,content) values (%s,%s,%s,%s,%s,%s)', (productId,commentId,commentGuid,commentTime,score,content) )
                    #print(sql)
                    #cursor.execute(sql)
                    conn.commit()
                    print("save comment to db successfully")
                else:
                    print("this comment already exists")
        finally:
            conn.close()
    
    def getCommentsOfProduct(self, productId):
        conn=pymysql.connect(host=self.dburl, user=self.dbusername, passwd=self.dbpwd,db=self.dbname, port=3306, charset="utf8")
        try:
            with conn.cursor() as cursor:
                cursor.execute("select score,content from t_comment where productId=%s order by create_time desc, score desc",productId)
                data=cursor.fetchall()
                return [ [d[0], d[1]] for d in data]
        finally:
            conn.close()
    
    def saveCommentAsJson(self,productId):
        conn=pymysql.connect(host=self.dburl, user=self.dbusername, passwd=self.dbpwd,db=self.dbname, port=3306, charset="utf8")
        try:
            with conn.cursor() as cursor:
                cursor.execute("select score,content from t_comment where productId=%s order by create_time",productId)
                data=cursor.fetchall()
                j=[]
                for i in range(len(data)):
                    #print(data[i][0])
                    #j.append( {"score": data[i][0], "content": data[i][1]} )
                    #j.append(str(data[i][0]))
                    j.append(data[i][1])
                fp=open(str(productId)+".txt", "w", encoding='utf8')
                fp.writelines(j)
                fp.close()
        finally:
            conn.close()
    
    def test(self):
        conn=pymysql.connect(host=self.dburl, user=self.dbusername, passwd=self.dbpwd,db=self.dbname, port=3306, charset="utf8")
        #conn.set_charset("utf8")
        try:
            with conn.cursor() as cursor:
                #cursor.execute("set names utf8;")
                #cursor.execute("set character set utf8;")
                #cursor.execute("set character_set_connection=utf8;")
                sql="select count(0) from t_patent"
                cursor.execute(sql)
        finally:
            conn.close()

