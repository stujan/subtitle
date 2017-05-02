import tkinter
from tkinter import *
from tkinter import messagebox
from Handler import Handler
import threading
class GUI():

    def __init__(self):
        self.change=0
        self.handler=Handler()
        self.handler.GetList()
        self.top=tkinter.Tk()
        self.b1=Button(self.top,text="play", command=self.play)
        self.label=tkinter.Label(self.top,text="")
        self.text=Entry(self.top, bd =5)
        self.b3=Button(self.top, text="delay", command=lambda : self.delay(self.text.get()))
        self.b4=Button(self.top, text="boost", command=lambda : self.boost(self.text.get()))
        self.b5=Button(self.top,text="save",command=self.save)
        self.b6=Button(self.top,text="restart",command=self.restart)
        self.b7=Button(self.top,text="detail_true",command= lambda: self.detail(0))
        self.b8=Button(self.top,text="detail_error",command= lambda :self.detail(1))
        self.b1.pack()
        self.label.pack()
        self.text.pack()
        self.b3.pack()
        self.b4.pack()
        self.b5.pack()
        self.b6.pack()
        self.b7.pack()
        self.b8.pack()
        # b1.grid(row=0,column=1)
        # label.grid(row=1,column=0)
        # text.grid(row=2,column=0)
        # b3.grid(row=2,column=1)
        # b4.grid(row=2,column=2)
        # b5.grid(row=3,column=1)
        # b6.grid(row=3,column=2)
        tkinter.mainloop()


    def detail(self,key=1):
        print(len(self.handler.error))
        for i in self.handler.error:
            if i[0] == key:
                print(i[1])




    def changeLabel(self):
        while True:
            from Handler import value
            self.label["text"] = value
            self.top.update()

    def play(self):

        t1=threading.Thread(target=self.handler.play)
        t2=threading.Thread(target=self.changeLabel)
        t1.start()
        t2.start()

        #self.handler.play()


    def delay(self,t):
        a=self.handler.changeSub(delay=t)
        if a==0:
            messagebox.askokcancel(message="success")
        else:
            messagebox.askokcancel(message="could not delay")

    def boost(self,t):
        a=self.handler.changeSub(boost=t)
        if a==0:
            messagebox.askokcancel(message="success")
        else:
            messagebox.askokcancel(message="could not boost")


    def save(self):

        self.handler.refresh()
        messagebox.askokcancel(message="success")

    def restart(self):
        self.handler.reset()
        self.handler.GetList()

if __name__=="__main__":
    gui=GUI()
