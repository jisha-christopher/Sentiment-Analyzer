from textblob import TextBlob

history = []

while True:
    text = input("\nEnter sentence (type exit to stop): ")

    if text.lower() == "exit":
        break

    score = TextBlob(text).sentiment.polarity

    if score > 0:
        sentiment = "Positive"

    elif score < 0:
        sentiment = "Negative"

    else:
        sentiment = "Neutral"

    history.append((text, sentiment, score))

    print("Sentiment:", sentiment)
    print("Score:", round(score, 2))

print("\nAnalysis Summary")

for item in history:
    print(item)