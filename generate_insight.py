import requests
import json
from datetime import date
import random
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv("COHERE_API_KEY")


def load_student_interests(student_id):
    with open("student_interests.json", "r") as f:
        data = json.load(f)
    return data.get(str(student_id), [])

def generate_insight(topic):
    prompt = f"Give a motivational 3-line insight on '{topic}' with a real-world application example."
    response = requests.post(
        "https://api.cohere.ai/v1/generate",
        headers={"Authorization": f"Bearer {API_KEY}"},
        json={
            "model": "command-r-plus",
            "prompt": prompt,
            "max_tokens": 100,
            "temperature": 0.7
        }
    )
    return response.json()["generations"][0]["text"].strip()

def generate_learning_link(topic):
    return f"https://www.google.com/search?q={topic.replace(' ', '+')}+course"

def create_daily_insight(student_id):
    interests = load_student_interests(student_id)
    if not interests:
        return None
    topic = random.choice(interests)
    insight = generate_insight(topic)
    link = generate_learning_link(topic)
    today = str(date.today())

    daily_data = {
        "topic": topic,
        "insight": insight,
        "link": link
    }

    # Save daily insight to JSON
    try:
        with open("dailyInsights.json", "r") as f:
            all_insights = json.load(f)
    except FileNotFoundError:
        all_insights = {}

    all_insights[today] = daily_data

    with open("dailyInsights.json", "w") as f:
        json.dump(all_insights, f, indent=2)

    return {**daily_data, "date": today}
