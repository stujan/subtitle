class TimeItem():

    def __init__(self):
        self.hour=0
        self.min=0
        self.sec=0
        self.msec=0

    def setHour(self,hour):
        self.hour=hour

    def setMIn(self,min):
        self.min=min

    def setSec(self,sec):
        self.sec=sec

    def setMsec(self,msec):
        self.msec=msec

    def setTime(self,hour,min,sec,msec):
        self.hour=hour
        self.min=min
        self.sec=sec
        self.msec=msec

