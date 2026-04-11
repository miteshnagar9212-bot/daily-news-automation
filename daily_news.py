import feedparser
import urllib.parse
import os
import json
import smtplib
from email.mime.text import MIMEText
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

# 🧠 AI summary
def generate_summary(text):
    try:
        response = openai.ChatCompletion.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "user", "content": f"Summarize this in 2 lines:\n{text}"}
    ]
)
return response["choices"][0]["message"]["content"].strip()
    except Exception as e:
        print("OPENAI ERROR:", e)
    return "Summary not available"

# 📰 Fetch news
def fetch_news(keyword):
    encoded_keyword = urllib.parse.quote(keyword)
    url = f"https://news.google.com/rss/search?q={encoded_keyword}"

    feed = feedparser.parse(url)

    articles = []

    for entry in feed.entries[:5]:
        title = entry.title
        link = entry.link
        summary = generate_summary(title)

        articles.append({
            "title": title,
            "link": link,
            "summary": summary
        })

    return articles

# 📊 Categories
categories = {
    "Private Equity": "private equity",
    "Private Credit": "private credit",
    "Real Estate": "real estate investment",
    "Infrastructure": "infrastructure investment"
}

# 🧾 Get all news
def get_all_news():
    all_news = []

    for category, keyword in categories.items():
        news = fetch_news(keyword)

        for article in news:
            article["category"] = category
            all_news.append(article)

    return all_news

# 📧 Format email
def format_email(news):
    content = "Daily Investment News\n\n"

    for item in news:
        content += f"{item['category']}\n"
        content += f"{item['title']}\n"
        content += f"{item['link']}\n"
        content += f"{item['summary']}\n"
        content += "-" * 40 + "\n\n"

    return content

# 📬 Send email
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

# 🚀 Main function
def run_daily():
    print("Fetching news...")
    news = get_all_news()

    print("Saving JSON...")
    with open("news_data.json", "w") as f:
        json.dump(news, f, indent=2)

    print("Sending email...")
    email_body = format_email(news)
    send_email(email_body)

    print("Done!")

# ▶️ Run
if __name__ == "__main__":
    try:
        run_daily()
    except Exception as e:
        print("Error:", e)
        raise
