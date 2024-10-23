from flask import Flask
from pymongo import MongoClient
from routes import setup_routes

app = Flask(__name__)

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client.blog_database

setup_routes(app, db)

if __name__ == '__main__':
    app.run(debug=True)