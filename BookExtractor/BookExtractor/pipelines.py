# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import sqlite3
from itemadapter import ItemAdapter
import re


class BookextractorPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        field_names = adapter.field_names()
        for field_name in field_names:
            if field_name == 'availability':
                value = adapter.get(field_name)
                temp = ''.join(value).replace('\n','')
                adapter[field_name] = re.search(r"\s*\(\d+\s*available\)\s*",temp).group()

            elif field_name == 'star':
                star_map = {'One':'1','Two':'2','Three':'3','Four':'4','Five':'5'}
                value = adapter.get(field_name)
                adapter[field_name] = star_map.get(value.split()[-1].title())


        return item



class SaveToSqlitePipeline:

    def __init__(self):
        self.conn = sqlite3.connect("books_record.db")
        self.cur = self.conn.cursor()

        table_str = """CREATE TABLE IF NOT EXISTS bookdata (
                id INTEGER PRIMARY KEY,
                image_link TEXT,
                title TEXT,
                price NUMERIC,
                availability TEXT,
                star TEXT,
                upc TEXT 
            );
"""
        
        self.cur.execute(table_str)

    
    def process_item(self,item,spider):

        #check for duplicate record
        
        insert_str ="""INSERT INTO bookdata (image_link, title, price, availability, star,
                        upc
                        )VALUES (?, ?, ?, ?, ?, ?);
                        """
            
        self.cur.execute(insert_str,
                         (item['image_link'],item['title'],item['price'],
                          item['availability'],item['star'],item['upc'])
                          )

        self.conn.commit()

        return item
    
    def close_spider(self,spider):
        self.cur.close()
