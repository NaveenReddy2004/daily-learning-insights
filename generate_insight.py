import requests
import json
from datetime import date
import random

# 🔑 Replace with your actual Cohere API Key
API_KEY = "fOmWK3u1vqzd0vDabODy7yKSg5NhUQmLy1pmzMMf"

def generate_cohere_insight(stage, topic):
    prompt = f"Create a 2-4 line inspiring learning insight on '{topic}' for a {stage} level student. Include one real-world use case."

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

    result = response.json()
    return result["generations"][0]["text"].strip()

def update_daily_insight(user_profile_path, topic_bank_path, output_path="dailyInsights.json"):
    with open(user_profile_path, "r") as f:
        user_profile = json.load(f)
    with open(topic_bank_path, "r") as f:
        topic_bank = json.load(f)

    today = str(date.today())
    stage = user_profile["stage"]
    interests = user_profile.get("interests", [])

    # Choose a topic not recently used if possible
    available_topics = [t for t in topic_bank[stage] if t not in interests]
    topic = random.choice(available_topics if available_topics else topic_bank[stage])

    insight = generate_cohere_insight(stage, topic)

    daily_data = {
        today: {
            "stage": stage,
            "topic": topic,
            "insight": insight,
            "link": f"https://www.google.com/search?q={topic.replace(' ', '+')}"
        }
    }

    with open(output_path, "w") as f:
        json.dump(daily_data, f, indent=2)

    print("✅ Insight generated and saved to dailyInsights.json")

if __name__ == "__main__":
    update_daily_insight("user_profile.json", "topic_bank.json")
