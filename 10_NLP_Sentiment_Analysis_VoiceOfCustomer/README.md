# 💬 Hotel Reviews Analysis & NLP

## 📌 Project Overview
Guest feedback is a goldmine of operational insights. This project uses Natural Language Processing (NLP) to automate the analysis of thousands of guest reviews, identifying sentiment trends and common complaints without manual reading.

## 💼 Business Problem
- **Issue:** Manually reading thousands of reviews is impossible and subjective.
- **Goal:** Automate the extraction of sentiment and key topics (e.g., "Cleanliness", "Staff").
- **Impact:** Faster response to operational issues and improved guest satisfaction scores.

## 🛠️ Tech Stack
- **Language:** Python
- **Libraries:** Pandas, Scikit-Learn (CountVectorizer), NumPy.
- **Visualization:** Power BI (Word Cloud & Sentiment Distribution).

## 📊 Methodology
1. **Synthetic Text Generation:** Created a dataset of realistic reviews with varying sentiments.
2. **Tokenization & Stopwords:** Cleaned text data to remove non-informative words.
3. **Bag of Words:** Used `CountVectorizer` to quantify keyword frequency.
4. **Sentiment Tagging:** Classified words into Positive and Negative categories for visualization.

## 📈 Key Results
- **Topic Detection:** Automatically highlighted "Noise" and "AC" as top negative drivers in specific periods.
- **Sentiment Tracking:** The dashboard allows monitoring of the "Positive vs. Negative" ratio over time.

## 🚀 How to Run
1. Run the script: `python project_reviews_nlp.py`
2. The script will generate `hotel_reviews_raw.csv` and `keywords_frequency.csv`.
3. Import both files into Power BI to build the Sentiment Dashboard.
