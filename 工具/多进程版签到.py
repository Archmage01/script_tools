#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @brief: 金币签到

import psutil,time
from selenium import webdriver
from time import sleep
import multiprocessing

datadict = {}
lock = multiprocessing.Lock()

def  dosomethings(start, end ):
    for i in range(start, end):
        try:
            # 后台运行
            option = webdriver.ChromeOptions()
            option.add_argument('headless')  # 设置option
            driver = webdriver.Chrome(options=option)  # 调用带参数的谷歌浏览器
            driver.get("https://xxmh193.com/#!/user/login")
            driver.find_element_by_xpath('//*[@class="item-input-wrap"]/input[@type="text"]').send_keys(
                "12345qq%02d" % (i))
            driver.find_element_by_xpath('//*[@class="item-input-wrap"]/input[@type="password"]').send_keys(
                "123456")
            # 登入
            login = driver.find_element_by_xpath('//*[@class="list"]/a')
            login.click()
            sleep(4)
            ## 找到签到按钮签到
            #print(driver.current_url, i, "签到成功")
            signin = driver.find_element_by_xpath('//*[@class="user"]/a')
            signin.click()
            # 获得金币数量
            coin = int(driver.find_element_by_xpath('//*[@class="value xxScion"]/span[@class="scion"]').text)
            #print("剩余金币：", coin)
            #获取锁
            lock.acquire()
            datadict[i] = coin
            lock.release() #释放锁
            sleep(1)
            driver.close()
        except Exception as e:
            print(e)



if __name__ == '__main__':
    cpu_nums = psutil.cpu_count()
    print("computer cpu nums: {}".format( psutil.cpu_count()))
    processlist = []
    startTime = time.time()
    step = 40//cpu_nums
    for i in range(cpu_nums):
        t = multiprocessing.Process(target=dosomethings, args=(i*step, (i+1)*step))
        processlist.append(t)
    for process in processlist:
        process.start()

    for process in processlist:
        process.join()
    data = sorted(datadict.items(),key=lambda x:x[0])
    for it in data:
        print("账号: 12345@qq%02d 金币剩余:%d "%it)
    endTime = time.time()
    time_differ = (endTime - startTime)
    print("总用时间:%.2f秒" % (time_differ))