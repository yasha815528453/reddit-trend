import pymysql
import pymysql.cursors
from dbutils.pooled_db import PooledDB
from contextlib import contextmanager
import os


class Database_Pool_Manager():
    def __init__(self):
        self.cursorType = pymysql.cursors.DictCursor
        self.pool = PooledDB(
            creator=pymysql,
            maxconnections=6,
            mincached=2,
            maxcached=5,
            blocking=True,
            host= os.getenv('DB_HOST'),
            user= os.getenv('DB_USER'),
            password= os.getenv('DB_PASSWORD'),
            database = os.getenv("DB_DATABASE"),
            cursorclass=self.cursorType,
        )

    @contextmanager
    def acquire_pool_connection(self):
        connection = self.pool.connection()
        try:
            yield connection
        finally:
            connection.close()

    def release_connection(self, connection):
        connection.close()


    def get_table_data(self) -> list:
        with self.acquire_pool_connection() as connection:
            cursor = connection.cursor()

            SQLstmt = """
            SELECT
                today.KEYWORD,
                today.CONV_COUNT AS TODAY_COUNT,
                today.SUBREDDIT,
                ROUND(today.CONV_COUNT / IFNULL(yesterday.CONV_COUNT, 1), 2) AS RATIO_24H,
                ROUND(today.CONV_COUNT / IFNULL(last_week.CONV_COUNT, 1), 2) AS RATIO_1W,
                ROUND(today.CONV_COUNT / IFNULL(last_month.CONV_COUNT, 1), 2) AS RATIO_1M
            FROM
                (SELECT KEYWORD, SUM(CONV_COUNT) AS CONV_COUNT, SUBREDDIT FROM keywords WHERE CONV_DATE = CURDATE() GROUP BY KEYWORD, SUBREDDIT) today
            LEFT JOIN
                (SELECT KEYWORD, SUM(CONV_COUNT) AS CONV_COUNT FROM keywords WHERE CONV_DATE = CURDATE() - INTERVAL 1 DAY GROUP BY KEYWORD) yesterday
            ON today.KEYWORD = yesterday.KEYWORD
            LEFT JOIN
                (SELECT KEYWORD, SUM(CONV_COUNT) AS CONV_COUNT FROM keywords WHERE CONV_DATE = CURDATE() - INTERVAL 7 DAY GROUP BY KEYWORD) last_week
            ON today.KEYWORD = last_week.KEYWORD
            LEFT JOIN
                (SELECT KEYWORD, SUM(CONV_COUNT) AS CONV_COUNT FROM keywords WHERE CONV_DATE = CURDATE() - INTERVAL 30 DAY GROUP BY KEYWORD) last_month
            ON today.KEYWORD = last_month.KEYWORD;
            """
            cursor.execute(SQLstmt)
            results = cursor.fetchall()
            data = [
                {
                    'KEYWORD': row['KEYWORD'],
                    'TODAY_COUNT': int(row['TODAY_COUNT']),  # Convert to int if this is a whole number
                    'SUBREDDIT': row['SUBREDDIT'],
                    'RATIO_24H': float(row['RATIO_24H']),  # Convert to float for serialization
                    'RATIO_1W': float(row['RATIO_1W']),
                    'RATIO_1M': float(row['RATIO_1M']),
                }
                for row in results
            ]
            print(data)
            return data


class Database_Manager():

    def acquire_connection(self):
        cursorType = pymysql.cursors.DictCursor
        connection = pymysql.connect(
            host = os.getenv('DB_HOST'),
            user = os.getenv('DB_USER'),
            password = os.getenv('DB_PASSWORD'),
            database = os.getenv("DB_DATABASE"),
            cursorclass= cursorType,
        )
        return connection

    def insert_from_queue(self, connection, tup_val):
        cursor = connection.cursor()
        SQLstmt = '''INSERT INTO keywords
        (KEYWORD, CONV_DATE, CONV_COUNT, POST_ID, POST, SUBREDDIT)
        VALUES (%s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE CONV_COUNT = CONV_COUNT + 1
        '''
        cursor.execute(SQLstmt, tup_val)

    def release_connection(self, connection):
        connection.close()
