# -*- coding: utf-8 -*-
"""
Created on Sat Jun  1 15:53:46 2019

@author: 10670
"""

from tkinter import*
import app
import speech

def main():
    root = Tk()
    sort = App(master = root) 
    
    sort.master.title("识别")
    sort.mainloop()
    
class App(Frame):
    def __init__(self, master = None):
        
        Frame.__init__(self, master)
        self.grid()
        
        self.PicPath = StringVar()
        
        self.creat_label()  #创建标签
        self.creat_entry()  #创建输入框
        self.creat_button() #创建按钮
        
        self.flag = 1;
    
    def creat_label(self):
        Label(self, text = "请输入要识别的图片链接"). \
        grid(row = 0, column = 0, padx = 5, pady = 5, sticky = E)
        Label(self, text = "是否开启语音输出"). \
        grid(row = 0, column = 1, columnspan = 2, padx = 5, pady = 5, sticky = E)
        
    def creat_entry(self):
        a = Entry(self, width = 20, textvariable = self.PicPath). \
        grid(row = 1, column = 0,padx = 5)
        print(type(a))
        
    def creat_button(self):
        Button(self, text = "开始识别", command = self.confirm). \
        grid(row = 2, column = 0, padx = 5, pady = 5)
        speech.say('请输入图片的路径')
        Button(self, text = "开启", command = self.kaiqi). \
        grid(row = 1, column = 1, padx = 5, pady = 5)
        Button(self, text = "关闭", command = self.guanbi). \
        grid(row = 1, column = 2, padx = 5, pady = 5)
        
    def kaiqi(self):
        self.flag = 1;  # 开启语音输出
        
    def guanbi(self):
        self.flag = 0;  # 关闭语音输出
        
    def confirm(self):
#        a = self.PicPath.get()
#        print(a)
#        print(type(a))
        #application.pre_pic(a)
#        b = 'D:\pic\0.png'
#        application.pre_pic(b)
        #application.pre_pic(r'D:\pic\0.png')
#        b = r'D:\pic\0.png'
#        value = app.application(b)
#        print(self.PicPath.get())
        value = app.application(self.PicPath.get())
        if self.flag == 1:
            speech.say('识别出来的数字是')
            speech.say(value)
        Label(self, text = ["识别出的数字是：",value]). \
        grid(row = 3, column = 0, padx = 5, pady = 5)

        
if __name__ == "__main__":
    main()