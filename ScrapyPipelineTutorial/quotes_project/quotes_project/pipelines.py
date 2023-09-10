# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import sqlite3

class QuotesToSQLitePipeline:
    def __init__(self):
        self.conn = sqlite3.connect('quotes.db')
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS quotes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                text TEXT,
                author TEXT
            )
        ''')
        self.cursor.execute('''
            INSERT INTO quotes (text, author)
            VALUES (?, ?)
        ''', (adapter['text'], adapter['author']))
        self.conn.commit()
        return item

    def close_spider(self, spider):
        self.conn.close()
