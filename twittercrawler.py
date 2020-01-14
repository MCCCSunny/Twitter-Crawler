#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 19 12:18:31 2018

@author: valquiria
"""
import pdb
import tweepy 
import requests
import os
import io
from datetime import datetime
#import subprocess

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

from google.cloud import vision

consumer_key = "AmNYCCKiLjGq5Na4gzFWo1lVh"
consumer_secret = "f0ghWaxemJvK97Dor5MOMPN740QHeNyb4PQ6l3Dd2dGEYZEJ1j"
access_key = "1214855339260219392-OYCZpaZMXIjZQTeL0Wr2Iz3vGDbcU4"
access_secret = "FSn3wE29YtNHQRUCv0RI5CoaCg1yrVOpYpj7hb3k8iBsX"
#insert yours

import pymongo
#import mysql
# mongodb data
client = pymongo.MongoClient(host='localhost', port=27017) #连接本地mongodb数据库
DATABASE = client["twitter_users"]


def get_label(path):
    direct='PATH_TO_JSON_CREDENTIALS'
    os.environ['GOOGLE_APPLICATION_CREDENTIALS']=direct
    client = vision.ImageAnnotatorClient()
    with io.open(path, 'rb') as image_file:
        content = image_file.read()
    image = vision.types.Image(content=content)
    response = client.label_detection(image=image)
    labels = response.label_annotations
   
    size = 20
    ttfont = ImageFont.truetype("Arial.ttf",2*size)
    im = Image.open(path)
    draw = ImageDraw.Draw(im)
    i=0
    for label in labels:
         draw.text((size,size+2*size*i),label.description, fill=(0,255,0),font=ttfont)
         i+=1
    im.save(path)



def savepics(image_url,screen_name, filename):
    path='PATH_TO_YOUR_SAVING_DIRECTORY'+screen_name+'/'
    if not os.path.exists(path):
        os.makedirs(path)
    url = image_url
    r = requests.get(url,allow_redirects=True)
    file=open(path+filename, 'wb')
    if os.path.isfile(path+filename):
        print (filename)  
    file.write(r.content)
    file.close()
    get_label(path+filename)
    


def get_all_tweets(screen_name):
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)
    
    picture_urls=[]
    new_tweets = api.user_timeline(screen_name = screen_name,count=200)
    if len(new_tweets)==0:
        print('not enough picture')
        return        
    oldest = new_tweets[-1].id - 1
    
    while len(picture_urls)<9 :
        for tweet in new_tweets:
            if 'media' not in tweet._json['entities']:
                continue
            picture_urls.append(tweet._json['entities']['media'][0]['media_url'])
        new_tweets = api.user_timeline(screen_name = screen_name,count=20,max_id=oldest) #又向前请求了早更的数据
        if len(new_tweets)==0:
            print('we have only '+str(len(picture_urls))+' pictures')
            return
        oldest = new_tweets[-1].id - 1
    '''
    for i in range(len(picture_urls)):
        filename="img00"+str(i)+".jpg"
        savepics(picture_urls[i],screen_name,filename)
    '''
    pdb.set_trace()
    return picture_urls
    #sqlrecord(screen_name,picture_urls)#upload data mysql
    #mongorecord(picture_urls)
 
'''      
def sqlrecord(screen_name,picture_urls):#upload (topic , picture_urls) to my sql
    mydb=mysql.connector.connect(
        host='localhost',
        user='root',
        passwd='yourpassword', #input your password
        database='TwitterCrawlerURLS',#build your database before using this
        auth_plugin='mysql_native_password')#this line should be added if it doesn't recognize your passwd form

    mycursor = mydb.cursor()
    sqlFormula = "INSERT INTO Twittercontent(Topic, URL) VALUES (%s,%s)"
    for url in picture_urls:
        mycursor.execute(sqlFormula,(screen_name, url))#upload to preset table
    mydb.commit()
'''   

def TweetsToList(tweets):
    picture_urls_list = []
    for tweet in tweets:
        if 'media' in tweet._json['entities']:
            urlDict = {}
            image_url = tweet._json['entities']['media'][0]['media_url']
            createdAt = tweet._json['created_at'] #时间
            publishedAt = datetime.strptime(createdAt, '%a %b %d %H:%M:%S +0000 %Y')
            urlDict['urlToImage'] = image_url
            urlDict['publishedAt'] = publishedAt
            urlDict['url'] = tweet._json['entities']['media'][0]['url']
            picture_urls_list.append(urlDict)
    pictureList = [one for one in reversed(picture_urls_list)]
    return pictureList


def get_tweets(screen_name):
    collection = DATABASE[screen_name.split('@')[-1]]
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)
    
    picture_urls=[]
    oldest = None
    for i in range(10):
        new_tweets = api.user_timeline(screen_name = screen_name,count=200, max_id=oldest)
        print (len(new_tweets))
        
        if len(new_tweets)==0:
            print('not enough picture')
            collection.insert_many(picture_urls)
            print ('%s insert %d'%(screen_name, len(picture_urls)))
            return picture_urls
        oneUrlList = TweetsToList(new_tweets)        
        picture_urls = oneUrlList + picture_urls
        oldest = new_tweets[-1].id - 1
        print (len(oneUrlList), len(picture_urls))

    collection.insert_many(picture_urls)
    print ('%s insert %d'%(screen_name, len(picture_urls)))
    return picture_urls

def mongorecord(picture_urls):
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["TwitterCrawlerUrls"]
    mycol = mydb["Twitter"]
    dp=dict(picture_urls)
    for key in picture_urls :   
        mycol.insert_one({key:dp[key]})    
    
    
if __name__ == '__main__':

    topicList=['@adidas', '@Airbus', '@airliquidegroup', '@Allianz', '@AmadeusITGroup', '@abinbev', '@ASMLcompany', '@AXA', '@bbva',
               '@bancosantander', '@BASF', '@Bayer', '@BMWGroup', '@BNPParibas', '@Daimler', '@Danone', '@DeutscheBoerse',
               '@DeutschePostDHL', '@deutschetelekom', '@EnelGroup', '@ENGIEgroup', '@eni', '@Essilor', '@Luxottica', '@Fresenius',
               '@Iberdrola_En', '@ING_news', '@intesasanpaolo', '@KeringGroup', '@AholdDelhaize', '@Lindeplc', '@Loreal',
               '@LVMH', '@nokia', '@orange', '@Philips', '@SAFRAN', '@sanofi', '@SAP', '@SchneiderNA', '@Siemens', '@SocieteGenerale',
               '@Telefonica', '@Total', '@Unilever', '@VINCI', '@vivendi', '@VWGroup', '@MunichRe']#type in your topic
    # 没有twitter账号的公司： CRH PLC
    for topic in topicList:
        result = get_tweets(topic)
