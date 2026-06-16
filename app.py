from flask import Flask, render_template, request
from transformers import pipeline
from pymongo import MongoClient
import pandas as pd
import plotly.express as px

app = Flask(__name__)

print("Loading AI model...")

classifier = pipeline(
    "sentiment-analysis",
    model="distilbert/distilbert-base-uncased-finetuned-sst-2-english"
)

# MongoDB
client = MongoClient(
"mongodb+srv://jishachristopher02_db_user:Sentiment2026@cluster0.8c0uhoi.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
)

db = client["sentiment_db"]
collection = db["reviews"]


@app.route("/", methods=["GET", "POST"])
def home():

    sentiment = ""
    score = ""
    chart = ""

    if request.method == "POST":

        review = request.form.get("review")

        if review:

            result = classifier(review)

            sentiment = result[0]["label"]
            score = round(result[0]["score"], 3)

            collection.insert_one({
                "text": review,
                "sentiment": sentiment,
                "score": float(score)
            })

    # READ DATA
    data = list(collection.find())

    if len(data) > 0:

        sentiments = []

        for row in data:
            sentiments.append(
                row["sentiment"]
            )

        df = pd.DataFrame({
            "sentiment": sentiments
        })

        fig = px.histogram(

            df,

            x="sentiment",

            color="sentiment",

            title="📊 Sentiment Report",

            color_discrete_map={
                "POSITIVE": "#00ff88",
                "NEGATIVE": "#ff3366",
                "NEUTRAL": "#ffd43b"
            }
        )

        fig.update_layout(

            paper_bgcolor="#ffffff",

            plot_bgcolor="#ffffff",

            height=450
        )

        chart = fig.to_html(
            full_html=False
        )

    return render_template(

        "index.html",

        sentiment=sentiment,

        score=score,

        chart=chart
    )


if __name__ == "__main__":

    app.run(
        debug=False
    )