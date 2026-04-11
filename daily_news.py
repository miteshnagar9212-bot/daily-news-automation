# -*- coding: utf-8 -*-
"""
Daily News Automation with AI Summaries + Dashboard JSON
"""

print("PROGRAM STARTED")

import feedparser
import urllib.parse
import os
import json
import smtplib
from email.mime.text import MIMEText
from openai import OpenAI

# ✅ OpenAI setup
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# 🔹 Generate AI Summary
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
        print("Summary error:", e)
        return "Summary not available"

# 🔹 Fetch news from Google RSS
def fetch_news(keyword):
    encoded_keyword = urllib.parse.quote(keyword)
    url = f"https://news.google.com/rss/search?q={encoded_keyword}"
    
    feed = feedparser.parse(url)
    
    articles = []
    
    for entry in feed.entries[:5]:
        articles.append({
            "title": entry.title,
            "link": entry.link
        })
        
    return articles

# 🔹 Categories
categories = {
    "Private Equity": "private equity",
    "Private Credit": "private credit",
    "Real Estate": "real estate investment",
    "Infrastructure": "infrastructure investment"
}

# 🔹 Get all news
def get_all_news():
    all_news = {}
    
    for category, keyword in categories.items():
        news = fetch_news(keyword)
        all_news[category] = news
        
    return all_news

# 🔹 Format email
def format_email(news_dict):
    content = "Daily Alternative Investment News\n\n"
    
    for category, articles in news_dict.items():
        content += f"{category}\n"
        content += "-" * 30 + "\n"
        
        for article in articles:
            content += f"{article['title']}\n"
            content += f"{article['link']}\n\n"
            
    return content

# 🔹 Send email (using GitHub secrets)
def send_email(body):
    sender = os.getenv("EMAIL_USER")
    receiver = os.getenv("EMAIL_USER")
    password = os.getenv("EMAIL_PASS")
    
    msg = MIMEText(body)
    msg["Subject"] = "Daily Investment News"
    msg["From"] = sender
    msg["To"] = receiver
    
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender, password)
        server.send_message(msg)

# 🔹 Main function
def run_daily():
    print("Step 1: Starting function")

    news = get_all_news()
    print("Step 2: News fetched")

    all_news = []

    for category, articles in news.items():
        for article in articles:
            title = article["title"]
            link = article["link"]

            summary = generate_summary(title)

            all_news.append({
                "category": category,
                "title": title,
                "link": link,
                "summary": summary
            })

    # ✅ Save JSON for dashboard
    with open("news_data.json", "w") as f:
        json.dump(all_news, f, indent=2)

    print("Step 3: News saved for dashboard")

    # ✅ Send email
    email_body = format_email(news)
    print("Step 4: Email formatted")

    send_email(email_body)
    print("Step 5: Email sent")

# 🔹 Run script
print("Starting script...")

try:
    run_daily()
    print("Finished successfully")
except Exception as e:
    print("Error:", e)
