# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


import logging
import pymongo
import sqlite3

from monster.settings import MONGO_URI

class MongodbPipeline(object):

   
    collection_name = "monster_jobs"

    def open_spider(self, spider):
        self.client = pymongo.MongoClient("mongodb+srv://ritesh:261992@monster.sfg8jfo.mongodb.net/?retryWrites=true&w=majority")
        self.db = self.client["monster_jobs"]

    def close_spider(self, spider):
        self.client.close()


    def process_item(self, item, spider):
        self.db[self.collection_name].insert_one(item)
        return item

class SQLlitePipeline(object):

    def open_spider(self, spider):
        self.connection = sqlite3.connect("monster.db")
        self.c = self.connection.cursor()
        try:
            self.c.execute('''
                CREATE TABLE monster_jobs(
                    title TEXT,
                    company TEXT,
                    url TEXT,
                    experience TEXT,
                    salary TEXT,
                    posted TEXT,
                    location1 TEXT,
                    location2 TEXT
                )
            
            ''')
            self.connection.commit()
        except sqlite3.OperationalError:
            pass

    def close_spider(self, spider):
        self.connection.close()


    def process_item(self, item, spider):
        self.c.execute('''
            INSERT INTO monster_jobs (title,company,url,experience,salary,posted, location1, location2) VALUES(?,?,?,?,?,?,?,?)

        ''', (
            item.get('title'),
            item.get('company'),
            item.get('url'),
            item.get('experience'),
            item.get('salary'),
            item.get('posted'),
            item.get('location1'),
            item.get('location2')
        ))
        self.connection.commit()
        return item