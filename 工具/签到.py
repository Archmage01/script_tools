#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @brief: 金币签到

import time,logging,os, prettytable,sys
from selenium import webdriver
from  selenium.webdriver.support.ui import WebDriverWait
from time import sleep
import threading

datadict = {}
lock = threading.Lock()


def  dosomethings(start, end ):
    for i in range(start, end):
        try:
            # 后台运行
            option = webdriver.ChromeOptions()
            option.add_argument('headless')  # 设置option
            option.add_experimental_option("excludeSwitches", ['enable-logging'])
            driver = webdriver.Chrome(options=option)  # 调用带参数的谷歌浏览器
            driver.get("https://xxmh193.com/#!/user/login")
            driver.find_element_by_xpath('//*[@class="item-input-wrap"]/input[@type="text"]').send_keys(
                "12345qq%02d" % (i))
            driver.find_element_by_xpath('//*[@class="item-input-wrap"]/input[@type="password"]').send_keys(
                "123456")
            # 登入
            login = driver.find_element_by_xpath('//*[@class="list"]/a')
            login.click()
            #sleep(4)
            ## 找到签到按钮签到
            #print(driver.current_url, i, "签到成功")
            signin = WebDriverWait(driver, 4, 1).until(lambda x: x.find_element_by_xpath('//*[@class="user"]/a')) #超时4秒 每1秒刷新
            #signin = driver.find_element_by_xpath('//*[@class="user"]/a')
            signin.click()
            # 获得金币数量
            coin = int(driver.find_element_by_xpath('//*[@class="value xxScion"]/span[@class="scion"]').text)
            #print("剩余金币：", coin)
            #获取锁
            lock.acquire()
            datadict[i] = coin
            lock.release() #释放锁
            #sleep(1)
            driver.close()
        except Exception as e:
            print(e)


if __name__ == '__main__':
    import time,psutil
    cpu_nums= psutil.cpu_count()
    print("computer cpu nums:{}".format(psutil.cpu_count()))

    startTime = time.time()
    threads = []
    step = 40//cpu_nums
    for i in range(cpu_nums):
        t = threading.Thread(target=dosomethings, args=(i*step, (i+1)*step))
        threads.append(t)
    for thread in threads:
        #thread.setDaemon(True)
        thread.start()


    for thread in threads:
        '''
            主线程等待子线程结束
            为了让守护线程执行结束之后，主线程再结束，我们可以使用join方法，让主线程等待子线程执行
        '''
        thread.join()

    data = sorted(datadict.items(),key=lambda x:x[0])
    # for it in data:
    #     print("账号: 12345@qq%02d 金币剩余:%d "%it)
    #格式化打印
    tb = prettytable.PrettyTable()
    tb.field_names = ["ID ", "coins"]
    for idc,coin in data:
        tb.add_row(["账号12345@qq%02d"%idc, coin])
    #print(tb)
    print(str(tb))


    endTime = time.time()
    time_differ = (endTime - startTime)
    print("总用时间:%.2f秒" % (time_differ))
    print(sum(datadict.values()))
    sys.exit([0])
    # for thread in threads:
    #     thread.

'''
    守护线程
    使用setDaemon(True)把所有的子线程都变成了主线程的守护线程，
    因此当主线程结束后，子线程也会随之结束，所以当主线程结束后，整个程序就退出了。
    所谓’线程守护’，就是主线程不管该线程的执行情况，只要是其他子线程结束且主线程执行完毕，主线程都会关闭。也就是说:主线程不等待该守护线程的执行完再去关闭。
'''
