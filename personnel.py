from celery import Celery
import requests

# Initialize the Celery app with Redis as the message broker
app = Celery('news_tasks', broker='redis://localhost:6379/0')

@app.task
def fetch_news_articles():
    api_url = "https://newsapi.org/v2/top-headlines?country=us&apiKey=YOUR_API_KEY"
    response = requests.get(api_url)
    news_data = response.json().get('articles', [])

    for news_item in news_data:
        article_content = news_item.get('content', '')
        store_document(article_content)
