
from Time import  TimeItem

class SubItem():

    def __init__(self):
        self.id=0
        self.beginTime=TimeItem()
        self.endTime=TimeItem()
        self.content=""

    def setId(self,id):
        self.id=id

    def setBeginTime(self,time):
        self.beginTime=time

    def setEndTime(self,time):
        self.endTime=time

    def setContent(self,content):
        self.content=content

    def getId(self):
        return self.id

    def getContent(self):
        return self.content

    def getBTime(self):
        return self.beginTime

    def getETime(self):
        return self.endTime