from dotenv import load_dotenv
load_dotenv()
from flask import Flask, g, request
from flask import jsonify
from flask_cors import CORS
from database.db_manager import Database_Manager


app = Flask("redditTopics")
CORS(app, resources={r"/api/*": {"origins": "http://localhost:5173"}})
DB_manager = Database_Manager()

@app.route('/api/tabledata')
def get_stats():
    try:

        data = DB_manager.get_table_data()
        print(jsonify(data))
        return jsonify(data)

    except Exception as e:
        print(e)
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    app.run()
