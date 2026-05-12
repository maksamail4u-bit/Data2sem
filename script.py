import os
import json
import pandas as pd
from openai import OpenAI
from dotenv import load_dotenv
import time

load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")
INPUT_CSV = "input_reviews.csv"
OUTPUT_JSON = "output_result.json"

MODEL = "deepseek/deepseek-v4-flash"


if not API_KEY:
    raise ValueError("OPENROUTER_API_KEY not found in .env file")


client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=API_KEY,
)


def classify_review(review_text):

    system_prompt = """You are a review classification system. 
    Analyze the user's review and return ONLY valid JSON in this exact format:
    {"sentiment": "positive|negative|neutral", "topic": "brief topic name"}
    
    Do not add any extra text, explanations, or formatting."""

    user_prompt = f"Review: {review_text}"

    try:
        response = client.chat.completions.create(
            extra_headers={
                "HTTP-Referer": "http://localhost", 
                "X-OpenRouter-Title": "Review Classifier",
            },
            model=MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.1,
            response_format={"type": "json_object"}
        )
        
    
        reply = response.choices[0].message.content
        
        
        result = json.loads(reply)
        
        
        if "sentiment" not in result or "topic" not in result:
            raise ValueError("Missing required fields in response")
        
        return result
        
    except json.JSONDecodeError as e:
        print(f"JSON parsing error: {e}. Raw response: {reply}")
        return {"sentiment": "error", "topic": "parsing_failed"}
    except Exception as e:
        print(f"API error: {e}")
        return {"sentiment": "error", "topic": "api_failed"}

def main():
    print("Reading input CSV...")
    
    try:
        df = pd.read_csv(INPUT_CSV)
        print(f"Loaded {len(df)} reviews")
    except FileNotFoundError:
        print(f"Error: {INPUT_CSV} not found")
        return
    except Exception as e:
        print(f"Error reading CSV: {e}")
        return

    results = []
    

    for idx, row in df.iterrows():
        review_id = row.get('id', idx)
        review_text = row.get('review_text', '')
        
        if not review_text or pd.isna(review_text):
            print(f"Skipping empty review at row {idx}")
            continue
            
        print(f"Processing review #{review_id}...")
        
        classification = classify_review(review_text)
        
        result_entry = {
            "id": str(review_id),
            "review": review_text,
            "classification": classification
        }
        results.append(result_entry)
        
        print(f"   Sentiment: {classification.get('sentiment')}, Topic: {classification.get('topic')}")
        
        time.sleep(0.5)
    
    with open(OUTPUT_JSON, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print(f"\nResults saved to {OUTPUT_JSON}")
    
    sentiments = [r['classification'].get('sentiment') for r in results]
    sentiment_counts = {s: sentiments.count(s) for s in set(sentiments)}
    print(f"\nStatistics: {sentiment_counts}")

if __name__ == "__main__":
    main()