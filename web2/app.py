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


        # if result is Conspiracy, find key words 
        print(result[0])
        if result[0] == 0 or result[0]== -1 or result[0]== -1:  # -1 as the label for "Conspiracy Theory"
            
            feature_log_probs = consp_classifier.feature_log_prob_
            class_index = 0  #index based on label encoding
            feature_names = tfidf_vectorizer.get_feature_names()
            feature_probabilities = dict(zip(feature_names, feature_log_probs[class_index]))
            sorted_features = sorted(feature_probabilities.items(), key=lambda x: x[1], reverse=True)
            top_n = 10  # number of top words = 10
            rankedWords = [word for word, _ in sorted_features[:top_n]]
            print("ranked worss",rankedWords)

        else:
            rankedWords=[]

        return jsonify({'classPred': int(result[0]),'rankedWords':rankedWords})

    else:
        return jsonify({'error': 'Invalid input format. Please provide the required field "text".'})

if __name__ == '__main__':
    app.run(debug=True)
