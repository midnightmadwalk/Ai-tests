import json
import pandas as pd
import re
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

with open('extracted_tickers.json', 'r') as file:
    data = json.load(file)

ignored_tokens = {
    "USDT", "USDC", "BUSD", "DAI", "TUSD", "PAX", "BCH", "ETH", "BTC", "XRP", "SOL", "USD", "M", "FDUSD", "BNB"
}

news_data = []
tickers_data = []

for entry in data:
    tickers = entry['tickers']
    filtered_tickers = [ticker for ticker in tickers if ticker not in ignored_tokens]
    
    if filtered_tickers:  
        news_data.append(entry['news'])
        tickers_data.append(filtered_tickers)

X = []
y = []

for news, tickers in zip(news_data, tickers_data):
    for ticker in tickers:
        X.append(news)
        y.append(ticker)

df = pd.DataFrame({'news': X, 'ticker': y})

vectorizer = CountVectorizer()
X_vectorized = vectorizer.fit_transform(df['news'])
X_train, X_test, y_train, y_test = train_test_split(X_vectorized, df['ticker'], test_size=0.2, random_state=42)

model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

print(f"Model accuracy: {accuracy:.2f}")

def predict_tickers(sentence, threshold=0.1):
    sentence_vector = vectorizer.transform([sentence])
    probabilities = model.predict_proba(sentence_vector)
    tickers = model.classes_
    predicted_tickers = [tickers[i] for i in range(len(tickers)) if probabilities[0][i] > threshold]
    return predicted_tickers

example_sentence = "Binance Margin Adds ASR, ATM, FIO, JUV, WAN & More BTC, FDUSD and USDC Pairs"
predicted_tickers = predict_tickers(example_sentence)
print(f"Predicted tickers: {predicted_tickers}")
