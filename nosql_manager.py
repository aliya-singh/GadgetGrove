import json
import os

def setup_nosql_data(file_name="mongo_reviews.json"):
    reviews = [
        {"review_id": 1, "product_id": 101, "customer_id": 1, "rating": 5, "review_text": "Amazing watch!"},
        {"review_id": 2, "product_id": 102, "customer_id": 2, "rating": 4, "review_text": "Great sound quality."},
        {"review_id": 3, "product_id": 103, "customer_id": 1, "rating": 5, "review_text": "Perfect for work."},
        {"review_id": 4, "product_id": 101, "customer_id": 3, "rating": 2, "review_text": "Too small for my wrist."},
        {"review_id": 5, "product_id": 105, "customer_id": 4, "rating": 5, "review_text": "Best phone ever."},
        {"review_id": 6, "product_id": 104, "customer_id": 5, "rating": 3, "review_text": "Keyboard is okay, a bit loud."},
        {"review_id": 7, "product_id": 101, "customer_id": 2, "rating": 4, "review_text": "Stylish and functional."},
        {"review_id": 8, "product_id": 102, "customer_id": 6, "rating": 5, "review_text": "Immersive audio experience."},
        {"review_id": 9, "product_id": 103, "customer_id": 7, "rating": 1, "review_text": "Screen cracked after a week."},
        {"review_id": 10, "product_id": 105, "customer_id": 8, "rating": 4, "review_text": "Great camera."},
        {"review_id": 11, "product_id": 101, "customer_id": 9, "rating": 5, "review_text": "Love the fitness features."},
        {"review_id": 12, "product_id": 102, "customer_id": 10, "rating": 3, "review_text": "Average headphones."},
        {"review_id": 13, "product_id": 105, "customer_id": 1, "rating": 5, "review_text": "Second purchase, still loving it."},
        {"review_id": 14, "product_id": 102, "customer_id": 3, "rating": 4, "review_text": "Good value for money."},
        {"review_id": 15, "product_id": 104, "customer_id": 4, "rating": 2, "review_text": "Keys stuck after a month."}
    ]
    
    with open(file_name, 'w') as f:
        json.dump(reviews, f, indent=4)
    
    return f"NoSQL (JSON/Mongo Mock) initialized with {len(reviews)} reviews."