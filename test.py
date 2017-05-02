error = []
subt = []
p = 0
cache = []
syn = 0

from Sub import SubItem
def GetList():
    a = ""
    index = 0
    global error
    global subt
    with open("subtitle.srt") as fp:
        for line in fp:
            if (line != "\n"):
                a += line
                # a[index]+=line
            else:

                lrparser(str=a)
                a = ""


def lrparser(str=""):
    global syn
    global p
    global cache
    cache=[]
    p=0
    scaner(str)
    if syn == 1:
        while syn != 0 and p < len(str):
            scaner(str)

        if syn == 0:
            get = True
            if len(cache) != 10:
                print("error1")
                get = False
            else:
                for i in cache:
                    if i == "":
                        print("error2")
                        get = False
                        break
                    if i.find("format error")>0 :
                        print("format error")
                        get = False
                        break
            if get:
                subitem=SubItem()
                subitem.id=cache[0]
                subitem.beginTime.hour=cache[1]
                subitem.beginTime.min=cache[2]
                subitem.beginTime.sec=cache[3]
                subitem.beginTime.msec=cache[4]
                subitem.endTime.hour=cache[6]
                subitem.endTime.min=cache[7]
                subitem.endTime.sec=cache[8]
                subitem.endTime.msec=cache[9]

                subitem.content=str[p+1:]

                print("success")
                print(cache)
        else:
            print("error")
    else:
        print("lack id")


def scaner_time():
    pass


def scaner(scanner_str=""):
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


GetList()