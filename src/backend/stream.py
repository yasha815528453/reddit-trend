import threading
import logging
from queue import Queue
from dotenv import load_dotenv
import os
import time
from input_stream.reddit_pipeline import RedditStreamer
from input_stream.lang_processer import small_language_processer
from database.db_manager import Database_Manager

load_dotenv()
logging.basicConfig(filename='stream_app.log', level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(message)s')


lang_processer = small_language_processer()
reddit_stream = RedditStreamer(os.getenv("INTERESTED_SUBREDDITS"), lang_processer)
DB_manager = Database_Manager()


def insert_data(queue_data, reconnect_sec = 1800):
    db_conn = DB_manager.acquire_connection()
    last_reconnect = time.time()
    while True:

        while queue_data:
            try:
                data = queue_data.get()
                DB_manager.insert_from_queue(db_conn, data)
                db_conn.commit()
                if time.time() - last_reconnect > reconnect_sec:
                    DB_manager.release_connection(db_conn)
                    db_conn = DB_manager.acquire_connection()
                    last_reconnect = time.time()
            except Exception as e:
                print(f"An error occurred: {e}")
                # Attempt to re-establish the connection on error
                DB_manager.release_connection(db_conn)
                db_conn = DB_manager.acquire_connection()
                last_reconnect = time.time()

if __name__ == "__main__":
    DB_queue = Queue()


    stream_thread = threading.Thread(target=reddit_stream.stream_submissions, args=(DB_queue,))
    stream_thread.daemon = True
    stream_thread.start()
    stream_thread = threading.Thread(target=reddit_stream.stream_comments, args=(DB_queue,))
    stream_thread.daemon = True
    stream_thread.start()

    # Thread for inserting data
    process_thread = threading.Thread(target= insert_data, args=(DB_queue,))
    process_thread.daemon = True
    process_thread.start()

    # Keep the main thread alive
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logging.info("Application stopped.")
