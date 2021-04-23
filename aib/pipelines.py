import sqlite3


class AibPipeline:

    # Database setup
    conn = sqlite3.connect('aib.db')
    c = conn.cursor()

    def open_spider(self, spider):
        self.c.execute("""CREATE TABLE IF NOT EXISTS `aib`
                         (date text, title text, link text, content text)""")

    def process_item(self, item, spider):
        self.c.execute("""SELECT * FROM aib WHERE title = ?""",
                       (item.get('title'),))

        print(f"New entry added at {item['link']}")

        # Insert values
        self.c.execute("INSERT INTO aib (date, title, link, content)"
                       "VALUES (?,?,?,?)", (item.get('date'), item.get('title'), item.get('link'), item.get('content')))
        self.conn.commit()  # commit after every entry

        return item

    def close_spider(self, spider):
        self.conn.commit()
        self.conn.close()

