# -*- coding: utf-8 -*-
"""
Created on Sat Apr  4 21:51:53 2026

@author: mites
"""
def generate_summary(text):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": f"Summarize this in 2 lines:\n{text}"}
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return "Summary not available"
print("PROGRAM STARTED")
import feedparser
import urllib.parse  # <-- ADD THIS LINE
import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
def fetch_news(keyword):
    encoded_keyword = urllib.parse.quote(keyword)  # <-- NEW LINE
    url = f"https://news.google.com/rss/search?q={encoded_keyword}"
    
    feed = feedparser.parse(url)
    
    articles = []
    
    for entry in feed.entries[:5]:
        articles.append({
          title = entry.title
link = entry.link

summary = generate_summary(title)
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
import json  # add at top if not already

def run_daily():
    print("Step 1: Starting function")

    news = get_all_news()
    print("Step 2: News fetched")

    # 🔥 NEW: Add AI summary + structured data
    all_news = []

    for item in news:
        title = item["title"]
        link = item["link"]

        summary = generate_summary(title)

        all_news.append({
            "title": title,
            "link": link,
            "summary": summary
        })

    # ✅ SAVE for dashboard
    with open("news_data.json", "w") as f:
        json.dump(all_news, f, indent=2)

    print("Step 3: News saved for dashboard")

    # ✅ KEEP your email logic
    email_body = format_email(news)
    print("Step 4: Email formatted")

    send_email(email_body)
    print("Step 5: Email sent")

print("Starting script...")

try:
    run_daily()
    print("Finished successfully")
except Exception as e:
    print("Error:", e)
    # activate scheduler v2
