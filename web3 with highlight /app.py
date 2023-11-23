import nltk
from flask import Flask, render_template, request, jsonify
import joblib
import os
import re
# in the ui, allow user to choose which classifier eg nb or bert
# highlighting in the ui
# try bert for sentence classifiaction as baseline
# presentaion, use mockup demos of your ui,
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
        text = re.sub(r'http\S+', '', text, flags=re.MULTILINE)

        sentences = nltk.sent_tokenize(text)
        ranked_words = []
        num_sentences = 0
        num_consp_sentences = 0
        split_sentences=[]

        for sentence in sentences:
            sentence_tfidf = tfidf_vectorizer.transform([sentence])
            result = consp_classifier.predict(sentence_tfidf)
            probresult=consp_classifier.predict_proba(sentence_tfidf)
            print("probablity result",probresult,"predicted result",result)
            if result[0] == 0 or result[0] == 1:  # Conspiracy classification
                if result[0] == 1:
                    num_consp_sentences += 1

                feature_names = tfidf_vectorizer.get_feature_names()
                word_indices = sentence_tfidf.indices
                word_scores = sentence_tfidf.data
                #confidence value (of the classifier),heat map 
                tfidf_scores = {}
                for idx, score in zip(word_indices, word_scores):
                    word = feature_names[idx]
                    tfidf_scores[word] = score

                sorted_words = sorted(tfidf_scores.items(), key=lambda x: x[1], reverse=True)
                top_n = 10
                # append ranked words scores for each sentence
                ranked_words.append([{word[0]: round(word[1], 2)} for word in sorted_words[:top_n]])
                # append sentence and their individual result to sentenses list
                split_sentences.append({sentence: int(result[0])})
                
                print(f"Sentence {num_sentences + 1}: {sentence}")
                print(f"Classification result: {result[0]}")
                print(f"Top words: {ranked_words[-1]}")

            num_sentences += 1

        conspiracy_percentage = (num_consp_sentences / num_sentences) * 100 if num_sentences > 0 else 0
        overall_classification = 1 if conspiracy_percentage > 50 else 0
        print(f"Conspiracy Sentence Percentage: {round(conspiracy_percentage,2)}%")
        print(f"Conspiracy classification overall : {overall_classification}")

        print(f"there are {num_consp_sentences} Conspiracy Sentence in {num_sentences}")
        # print(ranked_words)
        print("split sentences",split_sentences)
        return jsonify({'overall_classification': overall_classification,
                        'sentences': split_sentences,
                        'rankedWords': ranked_words,
                        'num_consp_sentences': num_consp_sentences,
                        'num_sentences': num_sentences,
                        'conspiracyPercentage': round(conspiracy_percentage, 2)})
    
    else:
        return jsonify({'error': 'Invalid input format. Please provide the required field "text".'})

if __name__ == '__main__':
    app.run(debug=True)
