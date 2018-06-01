#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Name:         cloudmusic_playlist
Copyright:    snow
Version:      1.0
Email:        snowi@protonmail.com
'''

import os
import re
import time
import pandas as pd
from selenium import webdriver
#from urllib.request import urlretrieve


def c_file(user):
    if os.path.exists(user):
        print(user + ' folder exist')
    else:
        os.mkdir(user)
        print(user + ' folder created')

def play_list(user, url):
    driver = webdriver.Chrome()
    driver.implicitly_wait(10)    #隐式等待
    driver.get(url)
    while input('reload?y or n? ') == 'y':
        driver.get(url)
    driver.switch_to.frame('g_iframe')
    c_num = driver.find_element_by_css_selector('#cHeader > h3 > span')
    num = int(re.search(r'\d+', c_num.text).group())
    for n in range(int(input('输入滚动到底部次数：'))):
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")    #滚动到底部
        time.sleep(3)
    page = driver.page_source
    source_parser(user, num, page, driver)

def source_parser(user, num, page, driver):
    #re_img_list = re.findall(r'<img src=.+?.jpg', page)
    re_play_list = re.findall(r'<a href=./playlist.id=[0-9]+"', page)
    re_title_list = re.findall(r'class=.msk. title=.{1,20}?>', page)
    #img_list = [img[10:] for img in re_img_list]
    #img_list.pop(0)    #去除第一个头像链接
    #img_list = img_list[:num]    #歌单封面
    play_list = ['http://music.163.com/#'+url[9:-1] for url in re_play_list][:num]
    title_list = [title[19:-2] for title in re_title_list][:num]
    save_url(user, title_list, play_list)
    save_playlist(user, num, driver, title_list, play_list)

def save_playlist(user, num, driver, title_list, play_list):
    for title, url in zip(title_list, play_list):
        driver.get(url)
        while input('reload?y or n? ') == 'y':
            driver.get(url)
        driver.switch_to.frame('g_iframe')
        songs_ele = driver.find_elements_by_tag_name('tr')
        songs_ele.pop(0)
        l = []
        path = os.path.join(user,title)
        for song in songs_ele:
            re_name = song.find_element_by_class_name('txt').text
            name = re.sub(r'\n.+\n', '', re_name).replace('\n', '')    #去除网易云强制加的字符串
            l.append(name)
            df = pd.DataFrame(l, columns=['song'])
            df.to_csv(path + '.csv')
        print(title + ' saved!')
        num -= 1
        print(num + ' left')

def save_url(user, title_list, play_list):
    file_name = os.path.join(user,user) + '的歌单列表.csv'
    if os.path.exists(file_name):
        print('song list exists!')
    else:
        df = pd.DataFrame()
        title = pd.Series(title_list)
        url = pd.Series(play_list)
        df['title'] = title
        df['url'] = url
        df.to_csv(file_name)
        print('song list created!')


if __name__ == '__main__':
    home_url = 'http://music.163.com/#/user/home?id='
    user = input('输入用户昵称：')
    user_id = input('输入用户id：')
    url = home_url + user_id
    c_file(user)
    play_list(user, url)

