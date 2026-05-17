import feedparser
import urllib.parse
import os
import smtplib
from email.mime.text import MIMEText
from google import genai

# =========================
# GEMINI SETUP
# =========================

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

# =========================
# FETCH NEWS
# =========================

categories = {
    "Private Equity": "private equity",
    "Private Credit": "private credit",
    "Real Estate": "real estate investment",
    "Infrastructure": "infrastructure investment"
}

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

# =========================
# GET ALL NEWS
# =========================

def get_all_news():

    all_news = []

    for category, keyword in categories.items():

        news = fetch_news(keyword)

        for article in news:

            article["category"] = category

            all_news.append(article)

    return all_news

# =========================
# AI SUMMARY
# =========================

def generate_market_summary(news):

    summary = "TOP MARKET DEVELOPMENTS\n\n"

    for item in news[:10]:
        summary += f"- {item['title']}\n"

    return summary

# =========================
# FORMAT EMAIL
# =========================

def format_email(summary, news):

    content = "DAILY INVESTMENT INTELLIGENCE REPORT\n"
    content += "=" * 50 + "\n\n"

    content += summary
    content += "\n\n"

    content += "=" * 50 + "\n"
    content += "SOURCE ARTICLES\n"
    content += "=" * 50 + "\n\n"

    for item in news:

        content += f"[{item['category']}]\n"
        content += f"{item['title']}\n"
        content += f"{item['link']}\n\n"

    return content

# =========================
# SEND EMAIL
# =========================

def send_email(body):

    sender = os.getenv("EMAIL_USER")
    receiver = os.getenv("EMAIL_USER")
    password = os.getenv("EMAIL_PASS")

    msg = MIMEText(body)

    msg["Subject"] = "Daily Investment Intelligence Report"
    msg["From"] = sender
    msg["To"] = receiver

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:

        server.login(sender, password)

        server.send_message(msg)

# =========================
# MAIN
# =========================

def run_daily():

    print("Fetching news...")

    news = get_all_news()

    print("Generating AI summary...")

    summary = generate_market_summary(news)

    print("Formatting email...")

    email_body = format_email(summary, news)

    print("Sending email...")

    send_email(email_body)

    print("Done!")

# =========================
# RUN
# =========================

if __name__ == "__main__":

    run_daily()
