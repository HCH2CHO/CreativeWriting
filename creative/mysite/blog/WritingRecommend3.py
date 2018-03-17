# -*- coding: utf-8 -*-
"""
Created on Fri Nov 24 20:10:22 2017

@author: HCHO
"""

from blog.models import fiction
from blog.models import history


class Apriori(object):

    def __init__(self):
        self.fictionList=[] #全部文章的列表
        self.readingList=[]  #子项为列表，“用户名，fiction，fiction，...”
        self.relatedDict={}  #key为列表



    def readData(self):
        histroyData=history.objects.all()
        #sql_select="SELECT user,readinglist FROM history"
        for hdata in historyData:
            try:
                #Apriori.cur.execute(sql_select)
                #data=Apriori.cur.fetchone()
                self.readingList.append(hdata.readinglist.split(','))
                #Apriori.conn.commit()
            except:
                print('error3')
        #Apriori.conn.close()
        
    def calculateApriori(self):       
        listCount=len(self.readingList)
        for iArtical in self.fictionList:
            for jArtical in self.fictionList:
                if iArtical !=jArtical:
                    itemCount=0
                    intersection=0
                    
                    for k in range(0,listCount):
                        if iArtical in self.readingList[k]:
                            itemCount+=1
                        if iArtical in self.readingList[k] and jArtical in self.readingList[k]:
                            intersection+=1
                            
                    support=intersection/listCount  #i对j的支持度
                    confidence=intersection/itemCount ##i对j的置信度
                    
                    if support>0.2 and confidence>0.5:
                        #print (iArtical+'-->'+jArtical,support,confidence)
                        if iArtical not in self.relatedDict:
                            self.relatedDict[iArtical]=[]
                        self.relatedDict[iArtical].append(jArtical)
                        
    def writeData(self):
        for iword in self.relatedDict:
            #sql_update="UPDATE fiction SET reArticle={0} WHERE id={1}".format(str(self.relatedDict[iword]),iword)
            fiction1=fiction.objects.get(name=iword)
            fiction.reArticle=str(self.relatedDict[iword])
            fiction.save()

    #relatedDict[iArtical]  即为iArtical的关联文章列表
if __name__ == '__main__':
    Apr=Apriori()
    Apr.calculateApriori()
    Apr.writeData()    
