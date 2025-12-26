import pandas as pd
import numpy as np
import os
import re
from datetime import datetime
from sklearn.feature_extraction.text import CountVectorizer

# ==========================================
# CONFIGURATION
# ==========================================
np.random.seed(99)
OUTPUT_DIR = "outputs_nlp"
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

print(">>> Starting Project 5: Hotel Reviews Analysis (NLP)...")

# ==========================================
# 1. GENERATE SYNTHETIC REVIEWS
# ==========================================
print(f"[{datetime.now().strftime('%H:%M:%S')}] Generating synthetic guest reviews...")

# Building blocks for sentences
aspects_pos = ['breakfast', 'room', 'staff', 'location', 'pool', 'bed', 'view', 'wifi']
aspects_neg = ['bathroom', 'noise', 'ac', 'check-in', 'elevator', 'price', 'carpet']

adj_pos = ['amazing', 'excellent', 'great', 'friendly', 'delicious', 'clean', 'comfortable', 'fast']
adj_neg = ['dirty', 'loud', 'broken', 'slow', 'rude', 'expensive', 'smelly', 'old']

connectors = ['. ', ' and ', ' but ', '. However, ']

data = []
n_reviews = 3000

for i in range(n_reviews):
    review_id = f"REV_{i+1:04d}"
    
    # Decide Sentiment (0=Negative, 1=Positive)
    sentiment = np.random.choice([0, 1], p=[0.4, 0.6])
    
    # Construct Text
    if sentiment == 1:
        # Positive Pattern
        asp = np.random.choice(aspects_pos)
        adj = np.random.choice(adj_pos)
        text = f"The {asp} was {adj}"
        
        # Add a second sentence sometimes
        if np.random.rand() > 0.5:
            text += np.random.choice(connectors) + f"the {np.random.choice(aspects_pos)} was {np.random.choice(adj_pos)}"
        
        rating = np.random.randint(4, 6) # 4 or 5 stars
        
    else:
        # Negative Pattern
        asp = np.random.choice(aspects_neg)
        adj = np.random.choice(adj_neg)
        text = f"The {asp} was {adj}"
        
        # Mixed sentiment sometimes ("Room dirty BUT staff nice")
        if np.random.rand() > 0.7:
             text += f" but the {np.random.choice(aspects_pos)} was {np.random.choice(adj_pos)}"
             rating = 3
        else:
             text += f" and the {np.random.choice(aspects_neg)} was {np.random.choice(adj_neg)}"
             rating = np.random.randint(1, 3) # 1 or 2 stars

    data.append({
        'Review_ID': review_id,
        'Date': pd.to_datetime('2025-01-01') + pd.to_timedelta(np.random.randint(0, 180), unit='d'),
        'Review_Text': text,
        'Rating': rating,
        'Sentiment_Label': 'Positive' if rating >= 4 else ('Negative' if rating <= 2 else 'Neutral')
    })

df = pd.DataFrame(data)

# Save Raw Data for Power BI (Table View)
df.to_csv(f"{OUTPUT_DIR}/hotel_reviews_raw.csv", index=False)

# ==========================================
# 2. TEXT PROCESSING (Bag of Words)
# ==========================================
print(f"[{datetime.now().strftime('%H:%M:%S')}] Extracting keywords for Word Cloud...")

# Custom Stopwords List (Words to ignore)
stopwords = ['the', 'was', 'and', 'but', 'however', 'is', 'to', 'in', 'of', 'for', 'it', 'very', 'my', 'had']

# Use CountVectorizer to count word frequency
cv = CountVectorizer(stop_words=stopwords, max_features=50, ngram_range=(1,1))
X = cv.fit_transform(df['Review_Text'])

# Sum words
word_counts = X.toarray().sum(axis=0)
words = cv.get_feature_names_out()

# Create a clean DataFrame for the "Word Cloud"
word_freq_df = pd.DataFrame({
    'Word': words,
    'Frequency': word_counts
}).sort_values(by='Frequency', ascending=False)

# Classify words as Positive/Negative logic for coloring in Power BI
# (Simple dictionary look-up based on our generation lists)
all_pos_words = set(aspects_pos + adj_pos)
all_neg_words = set(aspects_neg + adj_neg)

def categorize_word(w):
    if w in all_pos_words: return 'Positive_Term'
    if w in all_neg_words: return 'Negative_Term'
    return 'Neutral_Term'

word_freq_df['Sentiment_Category'] = word_freq_df['Word'].apply(categorize_word)

# Save Keyword Data for Power BI (Word Cloud / Bar Chart)
word_freq_df.to_csv(f"{OUTPUT_DIR}/keywords_frequency.csv", index=False)

print(f"\n>>> DONE! Files saved in '{OUTPUT_DIR}'.")
print(">>> Import 'hotel_reviews_raw.csv' for the list of comments.")
print(">>> Import 'keywords_frequency.csv' for the Word Cloud/Bar Chart.")