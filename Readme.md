Introduction
============

This project implemented a way to download pictures in selected topic. Then use Google Vision to recognize the main characters in the pictures and combine them into the pictures.

MiniProject 3
=============

## Usage

Get Tweets From Twitter According To Topics Via 'Screen_Name'

get_all_tweets(screen_name)

Save Pictures In To Local Directory

savepics(image_url,screen_name, filename)

Get The Topic Of Each Pictures By Google Vision

get_label(path)

## Announcement

You might need to get your own consumer keys from Twitter and credential from Google Vision. Fill then into the required place in the code and download the picture as many as you can.

MiniProject 3
=============

Using Mysql and MongoDB to store the history of searching into a local database.

## Usage

Using these functions to save the data, you can see the annotations for more information
sqlrecord(screen_name,picture_urls)
mongorecord(picture_urls)

While running your database after downloads, try
```
mysql -u root -p
```
to connect to your local database.
If you want to check the content of the database, try
```
use databasename #change to your database
select * from tablename #change to your table
```

## Things you need to do before running the program

Download MySQL database and connector from 
https://www.mysql.com/downloads/ and
https://dev.mysql.com/downloads/connector/python/
Download MongoDB from 
https://www.mongodb.com/download-center/community

!!! Mind your download path you might need to change it after the auto installation.

