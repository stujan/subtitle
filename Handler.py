import sys
import re
from Sub import SubItem
from Time import TimeItem
import time
import datetime
import os
import sched

value = ""
# 字符串是每次读取一个，因此需要设置增量判断下标
p = 0
# 缓冲每一块字幕，通过缓冲数据可判断解析结果
cache = []
cache_str=""
# 判断当前处于的状态，用状态机实现的时候需要用到。
# 由于数据受限（给的字幕文件太烂了）= =   因此总共的状态有
#['id', 'bhour', 'bmin', 'bsec', 'bmsec', '-->', 'ehour', 'emin', 'esec', 'emsec']
"""
具体的文法 语法如下:<id>--(若干整数) \n 状态1
            <bhour>---(若干位整数) ： 状态2
            <bmin>---(2位整数) ： 状态3
            <bsec>---(2位整数) , 状态4
            <bmsec>---(3位整数)  状5
            -->  状态6
            <ehour>  --- 状态7
            <emin>  --- 状态8
            <esec>  --- 状态9
            <emsec>  (3整) \n 状态0

            状态1 表示获得了初始值
            状态0 表示结束了获取  因为要求content可以包含任何，因此后面无需处理
            至于content用切片就可获取到相应的值啦   content=str[p:]

    主要的分析格式为<id><\n><time><-->><time><\n>(str)
    <time>-><hour><:><min><:><sec><,><msesecond>

"""
syn = 0


class Handler():
    def __init__(self):

        self.error = []
        self.subt = []
        # 使用正则表达式，匹配每一端字幕
        self.pattern = re.compile(r'(\d*)\n(.*?) --> (.*?)\n([\s\S]*)')

        # 使用正则表达式，匹配时间格式是否正确
        self.pattern_time = re.compile(r'(\d\d):(\d\d):(\d\d),(\d\d\d)')

        # 定时执行，主要是用于字幕的播放
        self.schedule = sched.scheduler(time.time, time.sleep)

        # self.GuiValue="fuck you"

    """
    def GetList(self):
        a = ""
        index = 0
        with open("subtitle.srt") as fp:
            for line in fp:
                if (line != "\n"):
                    a += line
                    # a[index]+=line
                else:

                    self.error.append("")
                    self.scaner(a, index)
                    index += 1
                    a = ""
    """


    """
    使用正则
    """

    #
    # def scaner(self, str, index):
    #
    #     all_result = re.match(self.pattern, str)
    #     if (all_result):
    #         Sitem = SubItem()
    #         BTitem = TimeItem()
    #         ETitem = TimeItem()
    #         beginTime_result = re.match(self.pattern_time, all_result.group(2))
    #         endTime_result = re.match(self.pattern_time, all_result.group(3))
    #
    #         if (beginTime_result and endTime_result):
    #             BTitem.setHour(int(beginTime_result.group(1)))
    #             BTitem.setMIn(int(beginTime_result.group(2)))
    #             BTitem.setSec(int(beginTime_result.group(3)))
    #             BTitem.setMsec(int(beginTime_result.group(4)))
    #
    #             ETitem.setHour(int(endTime_result.group(1)))
    #             ETitem.setMIn(int(endTime_result.group(2)))
    #             ETitem.setSec(int(endTime_result.group(3)))
    #             ETitem.setMsec(int(endTime_result.group(4)))
    #
    #         Sitem.setId(all_result.group(1))
    #         Sitem.setBeginTime(BTitem)
    #         Sitem.setEndTime(ETitem)
    #         Sitem.setContent(all_result.group(4))
    #         self.subt.append(Sitem)
    #
    #         if (not beginTime_result):
    #             self.error[index] += "beginTime error"
    #         if (not endTime_result):
    #             self.error[index] += "endTime_error"
    #
    #         elif (beginTime_result and endTime_result):
    #             if (int(beginTime_result.group(2)) > 60 and int(endTime_result.group(2)) > 60):
    #                 self.error[index] += "min error"
    #             elif ((int(beginTime_result.group(2)) == 60 and int(beginTime_result.group(3)) > 0) or (
    #                             int(beginTime_result.group(2)) == 60 and int(beginTime_result.group(4)) > 0)):
    #                 self.error[index] += "time error"
    #
    #     else:
    #         self.error[index] = "subtitle error"

    #重置函数
    def reset(self):
        global p
        global syn
        global cache
        p = 0
        syn = 0
        cache = 0
        self.error = []
        self.subt = []

    """

    使用状态机
    """

    ##获取列表，根据字幕的格式获取======一块一块提取==
    def isInteger(self,s):
        for i in range(len(s)-1):
            if not s[i].isdecimal():
                return False

        return True

    def GetList(self):
        a = ""
        fp=open("subtitle.srt","r")
        allsubtitle=fp.readlines()
        allsubtitle.append("\n")
        for line in range(len(allsubtitle)-1):
            if allsubtitle[line] == "\n"  and self.isInteger(allsubtitle[line+1]):
                self.lrparser(str=a)
                a = ""

            else:
                a += allsubtitle[line]

        #
        # with open("subtitle.srt") as fp:
        #     for line in fp:
        #         if (line != "\n"):
        #             a += line
        #             # a[index]+=line
        #         else:
        #
        #             self.lrparser(str=a)
        #             a = ""
    #自顶向下。。。。
    def lrparser(self, str=""):
        global syn
        global p
        global cache
        cache = []
        p = 0
        self.scaner(str)
        if syn == 1:
            while syn != 0 and p < len(str):
                self.scaner(str)

            if syn == 0:
                get = True
                if len(cache) != 10:
                    self.error.append([1, "explain error:" + str])

                    get = False
                else:
                    for i in cache:
                        if i == "":
                            self.error.append([1, "character error:" + str])
                            get = False
                            break
                        if i.find("format error") > 0:
                            self.error.append([1, "format error:" + str])
                            get = False
                            break
                if get:
                    subitem = SubItem()
                    subitem.id = cache[0]
                    subitem.beginTime.hour = int(cache[1])
                    subitem.beginTime.min = int(cache[2])
                    subitem.beginTime.sec = int(cache[3])
                    subitem.beginTime.msec = int(cache[4])
                    subitem.endTime.hour = int(cache[6])
                    subitem.endTime.min = int(cache[7])
                    subitem.endTime.sec = int(cache[8])
                    subitem.endTime.msec = int(cache[9])

                    subitem.content = str[p + 1:]
                    self.subt.append(subitem)
                    self.error.append([0, "success:" + str])
            else:
                self.error.append([1, "could not finish:" + str])
        else:
            self.error.append([1, "lack id:" + str])

    def scaner(self, scanner_str=""):
        global p
        global syn
        global cache
        s = ""

        if len(scanner_str) == 0:
            return
        ch = scanner_str[p]
        while ch == ' ':
            p += 1
            ch = scanner_str[p]

        if ch.isdecimal():
            while ch.isdecimal():
                s += ch
                p += 1
                ch = scanner_str[p]

            if ch == ":" or ch == "\n":
                if ch == ":" and syn in [2, 7]:
                    if int(s) >= 60:
                        s += "(format error)"
                syn += 1
                p += 1
            if ch == ',':
                if syn in [3, 8]:
                    if int(s) >= 60:
                        s += "(format error)"
                syn += 1

        elif ch == "-":
            if scanner_str[p + 1] == "-" and scanner_str[p + 2] == ">":
                syn += 1
                p += 3
                s = '-->'
            else:
                p += 1
        elif ch == ",":
            p += 1
            ch = scanner_str[p]
            while ch.isdecimal():
                s += ch
                p += 1
                ch = scanner_str[p]

            if len(s) == 3 and ch == '\n':
                syn = 0
            elif len(s) != 3 and ch == '\n':
                syn = 0
                s += "(format error)"


            elif len(s) == 3:
                syn += 1


            elif len(s) != 3:
                syn += 1
                s += "(format error)"


        else:
            p += 1
        cache.append(s)
    #推进或者延迟字幕
    def changeSub(self, delay=0, boost=0):
        self.setchange = 0
        temp = 0
        if (delay != 0):
            temp = int(delay)
        if (boost != 0):
            temp = -int(boost)

        for item in self.subt:

            btime = item.getBTime()
            etime = item.getETime()

            btime.sec += temp
            if btime.sec >= 60:
                btime.min += 1
                btime.sec -= 60
                if btime.min >= 60:
                    btime.hour += 1
                    btime.min -= 60
            if btime.sec <= 0:
                if btime.min == 0:
                    btime.sec -= temp
                    self.setchange = 1
                    print("could  not boost1")
                    break
                else:
                    btime.min -= 1
                    btime.sec += 60
            etime.sec += temp
            if etime.sec >= 60:
                etime.min += 1
                etime.sec -= 60
                if etime.min >= 60:
                    etime.hour += 1
                    btime.min -= 60
            if etime.sec <= 0:
                if etime.min == 0:
                    btime.sec -= temp
                    self.setchange = 1
                    print("could  not boost2")
                    break
                else:
                    etime.min -= 1
                    etime.sec += 60

            item.setBeginTime(btime)
            item.setEndTime(etime)
            return self.setchange
    #更新字幕文件
    def refresh(self):
        with open("subtitle.srt", "w") as fp:
            for i in self.subt:
                fp.write(i.getId() + "\n")
                fp.write(str(i.getBTime().hour).zfill(2) + ":" + str(i.getBTime().min).zfill(2) + ":" + str(
                    i.getBTime().sec).zfill(2) + "," + str(i.getBTime().msec).zfill(3) + " --> ")
                fp.write(str(i.getETime().hour).zfill(2) + ":" + str(i.getETime().min).zfill(2) + ":" + str(
                    i.getETime().sec).zfill(2) + "," + str(i.getETime().msec).zfill(3) + "\n")
                fp.write(i.getContent() + "\n")


    #点击播放的函数
    #根据时间差
    def play(self):
        year = int(datetime.datetime.now().strftime('%Y'))
        month = int(datetime.datetime.now().strftime('%m'))
        day = int(datetime.datetime.now().strftime('%d'))
        startime = datetime.datetime(year, month, day, 0, 0, 1, 0)
        for i in range(len(self.subt)):

            begintime = datetime.datetime(year, month, day, self.subt[i].getBTime().hour, self.subt[i].getBTime().min,
                                          self.subt[i].getBTime().sec, self.subt[i].getBTime().msec)
            endtime = datetime.datetime(year, month, day, self.subt[i].getETime().hour, self.subt[i].getETime().min,
                                        self.subt[i].getETime().sec, self.subt[i].getETime().msec)

            if int(self.subt[i].getId()) == 0:
                self.timming_exe(self.subt[i].getContent(), (begintime - startime).seconds,
                                 (endtime - begintime).seconds)

            if int(self.subt[i].getId()) > 0:
                endtime_pass = datetime.datetime(year, month, day, self.subt[i - 1].getETime().hour,
                                                 self.subt[i - 1].getETime().min,
                                                 self.subt[i - 1].getETime().sec, self.subt[i - 1].getETime().msec)

                self.timming_exe(self.subt[i].getContent(), (begintime - endtime_pass).seconds,
                                 (endtime - begintime).seconds)



    def perform_command(self, cmd, inc, staytime):
        print(cmd)
        global value
        value = cmd
        time.sleep(staytime)
        value = ""



    def timming_exe(self, cmd, inc=60, staytime=60):
        self.schedule.enter(inc, 0, self.perform_command, (cmd, inc, staytime))
        self.schedule.run()


"""
if __name__=="__main__":
    handler=Handler()
    handler.GetList()
    handler.changeSub(delay=40)
    handler.refresh()
"""
