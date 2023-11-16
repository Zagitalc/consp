from flask import Flask, render_template, request, jsonify
import joblib
import os

app = Flask(__name__)

models_dir = os.path.join(os.path.dirname(__file__), 'models')

consp_classifier = joblib.load(os.path.join(models_dir, 'consp_classifier.joblib'))
tfidf_vectorizer = joblib.load(os.path.join(models_dir, 'tfidf_vectorizer.joblib'))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/classify', methods=['POST'])
def classify():
    data = request.get_json()

    if "text" in data:
        text = data["text"]

        # Vectorize the input text
        text_tfidf = tfidf_vectorizer.transform([text])

        # Classify the text
        result = consp_classifier.predict(text_tfidf)

        return jsonify({'prediction': int(result[0])})

    else:
        return jsonify({'error': 'Invalid input format. Please provide the required field "text".'})

if __name__ == '__main__':
    app.run(debug=True)
