# -*- coding: utf-8 -*-
"""
Created on Sat Apr  4 21:51:53 2026

@author: mites
"""
print("PROGRAM STARTED")
import feedparser
import urllib.parse  # <-- ADD THIS LINE

def fetch_news(keyword):
    encoded_keyword = urllib.parse.quote(keyword)  # <-- NEW LINE
    url = f"https://news.google.com/rss/search?q={encoded_keyword}"
    
    feed = feedparser.parse(url)
    
    articles = []
    
    for entry in feed.entries[:5]:
        articles.append({
            "title": entry.title,
            "link": entry.link
        })
        
    return articles
categories = {
    "Private Equity": "private equity",
    "Private Credit": "private credit",
    "Real Estate": "real estate investment",
    "Infrastructure": "infrastructure investment"
}
def get_all_news():
    all_news = {}
    
    for category, keyword in categories.items():
        news = fetch_news(keyword)
        all_news[category] = news
        
    return all_news
def format_email(news_dict):
    content = "Daily Alternative Investment News\n\n"
    
    for category, articles in news_dict.items():
        content += f"{category}\n"
        content += "-" * 30 + "\n"
        
        for article in articles:
            content += f"{article['title']}\n"
            content += f"{article['link']}\n\n"
            
    return content
import smtplib
from email.mime.text import MIMEText

def send_email(body):
    sender = "mitesh.nagar9212@gmail.com"
    receiver = "mitesh.nagar9212@gmail.com"
    password = "zfzgrtfclnzdbjpm"
    
    msg = MIMEText(body)
    msg["Subject"] = "Daily Investment News"
    msg["From"] = sender
    msg["To"] = receiver
    
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender, password)
        server.send_message(msg)
def run_daily():
    print("Step 1: Starting function")

    news = get_all_news()
    print("Step 2: News fetched")

    email_body = format_email(news)
    print("Step 3: Email formatted")

    send_email(email_body)
    print("Step 4: Email sent")
    print("Starting script...")

print("Starting script...")

try:
    run_daily()
    print("Finished successfully")
except Exception as e:
    print("Error:", e)
    # activate scheduler v2
