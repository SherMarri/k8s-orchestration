import os
from fastapi import FastAPI
from pymongo import MongoClient

app = FastAPI()

# MongoDB connection
DB_USER_NAME = os.getenv("DB_USER_NAME")
DB_USER_PWD = os.getenv("DB_USER_PWD")
DB_URL = os.getenv("DB_URL")
client = MongoClient(
    f"mongodb+srv://{DB_USER_NAME}:{DB_USER_PWD}@{DB_URL}/test?retryWrites=true&w=majority"
)
db = client["news_db"]
collection = db["news"]


@app.get("/")
async def read_root():
    return {"message": "Welcome to FastAPI News App!"}


@app.post("/news/")
async def create_news(title: str, content: str):
    news = {"title": title, "content": content}
    result = collection.insert_one(news)
    return {"message": "News created successfully", "news_id": str(result.inserted_id)}


@app.get("/news/")
async def get_all_news():
    news_list = []
    for news in collection.find():
        news_list.append(news)
    return {"news": news_list}
