import pymysql
import pymysql.cursors
import os
from dotenv import load_dotenv

cursorType = pymysql.cursors.DictCursor

load_dotenv()
connection = pymysql.connect(
    host= os.getenv('DB_HOST'),
    user= os.getenv('DB_USER'),
    password= os.getenv('DB_PASSWORD'),
    cursorclass=cursorType,
)

cursorinstance = connection.cursor()
cursorinstance.execute("CREATE DATABASE redditkeywords")

connection = pymysql.connect(
    host= os.getenv('DB_HOST'),
    user= os.getenv('DB_USER'),
    password= os.getenv('DB_PASSWORD'),
    database = os.getenv("DB_DATABASE"),
    cursorclass=cursorType,
)
cursorinstance = connection.cursor()

sql = '''CREATE TABLE keywords(
    KEYWORD VARCHAR(255) NOT NULL,
    CONV_DATE DATE NOT NULL,
    CONV_COUNT INT NOT NULL,
    POST_ID INT NOT NULL,
    POST BOOLEAN NOT NULL,
    SUBREDDIT VARCHAR(255) NOT NULL,
    UNIQUE INDEX UNIQUE_KEYWORD_DATE (KEYWORD, CONV_DATE)
    )'''
cursorinstance.execute(sql)
