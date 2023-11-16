from flask import Flask, render_template, request, jsonify
import joblib
import os
import re

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
        text=re.sub(r'http\S+', '', text, flags=re.MULTILINE)


        # Vectorize the input text
        text_tfidf = tfidf_vectorizer.transform([text])

        # Classify the text
        result = consp_classifier.predict(text_tfidf)


        # if result is Conspiracy, find key words 
        print(result[0])
        if result[0] == 0 or result[0]== 1:  # 0 as the label for "Non Conspiracy Theory and 1 is Conspiracy Theory
            
            feature_log_probs = consp_classifier.feature_log_prob_
            class_index = 1  #index based on label encoding
            feature_names = tfidf_vectorizer.get_feature_names()
            # print(feature_names)
            feature_probabilities = dict(zip(feature_names, feature_log_probs[class_index]))
            print(feature_probabilities)
            # print(feature_probabilities,feature_names)
            sorted_features = sorted(feature_probabilities.items(), key=lambda x: x[1], reverse=True)
            print(sorted_features)
            # print(sorted_features)
            top = 10  # number of top words = 10
            rankedWords = [word for word, _ in sorted_features[:top]]
            ranked_prob = [_ for word, _ in sorted_features[:top]]
            print(rankedWords)
            # print(ranked_prob)

            word_data=[]
            for word in rankedWords:
                word_data.append(str(feature_probabilities[word])+" "+word)   
            
            print(word_data)

        else:
            rankedWords=[]


        return jsonify({'classPred': int(result[0]),'rankedWords':word_data})

    else:
        return jsonify({'error': 'Invalid input format. Please provide the required field "text".'})

if __name__ == '__main__':
    app.run(debug=True)
