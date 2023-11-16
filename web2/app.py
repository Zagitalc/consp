from flask import Flask, render_template, request, jsonify
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
import joblib
import os

# Initialize the Flask app
app = Flask(__name__)

# Define the directory where your models are stored
models_dir = os.path.join(os.path.dirname(__file__), 'models')

# Load the pre-trained classifier and TF-IDF vectorizer
consp_classifier = joblib.load(os.path.join(models_dir, 'consp_classifier.joblib'))
tfidf_vectorizer = joblib.load(os.path.join(models_dir, 'tfidf_vectorizer.joblib'))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/classify', methods=['POST'])
def classify():
    data = request.get_json()

    if (
        "title" in data
        and "channel_title" in data
        # and "view_count" in data
        and "tags" in data
        and "description" in data
    ):
        title = data["title"]
        channel_title = data["channel_title"]
        # view_count = data["view_count"]
        tags = data["tags"]
        description = data["description"]

        # # Preprocess and vectorize the input fields

        title_tfidf = tfidf_vectorizer.transform([title])
        channel_title_tfidf = tfidf_vectorizer.transform([channel_title])
        description_tfidf = tfidf_vectorizer.transform([description])

        # Numerical features (view_count) 
        # numerical_features = np.array([[view_count]]).reshape(-1, 1)

        # Concatenate all features
        X = np.hstack((title_tfidf.toarray(), channel_title_tfidf.toarray(), description_tfidf.toarray()))






        # Classify the text
        result = consp_classifier.predict(X)

        return jsonify({'result': int(result[0])})

    else:
        return jsonify({'error': 'Invalid input format. Please provide the required fields.'})


if __name__ == '__main__':
    app.run(debug=True)
