document.addEventListener('DOMContentLoaded', function () {
    const textForm = document.getElementById('textForm');
    const resultDiv = document.getElementById('result');
    const userTextDiv = document.getElementById('userText');
    const userTextInput = document.getElementById('userTextInput');
    const rankedWordsDiv = document.getElementById('rankedWords');
    const sentenceInfoDiv = document.getElementById('sentenceInfo');

    textForm.addEventListener('submit', async function (e) {
        e.preventDefault();
        resultDiv.innerHTML = '';
        resultDiv.innerHTML = 'Classifying...';
        resultDiv.innerHTML = '';
        rankedWordsDiv.innerHTML = '';
        sentenceInfoDiv.innerHTML = '';

        const inputText = document.getElementById('inputText').value;

        const inputData = {
            "text": inputText
        };

        const response = await fetch('/classify', {
            method: 'POST',
            body: JSON.stringify(inputData),
            headers: {
                'Content-Type': 'application/json',
            },
        });

        try {
            const data = await response.json();

            if (data.overall_classification !== undefined) {
                const classification = data.overall_classification === 0 ? "Non Conspiracy" : "Potential Conspiracy";
                resultDiv.innerHTML = `Overall Classification: ${classification}, prediction ${data.overall_classification}`;
                resultDiv.style.display = 'block';

                userTextInput.textContent = inputText;
                userTextDiv.style.display = 'block';
            } else {
                resultDiv.innerHTML = 'Classification failed.';
            }

            if (data.num_sentences !== undefined && data.num_consp_sentences !== undefined) {
                const sentenceInfo = `The text's conspiracy result is ${data.overall_classification === 0 ? "Non Conspiracy" : "Potential Conspiracy"}. You have ${data.num_consp_sentences} Conspiracy Sentences in ${data.num_sentences} sentences, leading to a percentage of ${data.conspiracyPercentage}%`;
                sentenceInfoDiv.innerHTML = sentenceInfo;
                sentenceInfoDiv.style.display = 'block';
            }

            if (data.rankedWords !== undefined && data.rankedWords.length > 0) {
                data.rankedWords.forEach((words, index) => {
                    const sentences = data.sentences;

                    const sentenceData = document.createElement('div');
                    const sentenceHeader = document.createElement('h3');
                    sentenceHeader.textContent = `Sentence ${index + 1}:`;

                    sentenceData.appendChild(sentenceHeader);
                    // sentenceData.appendChild(Object.keys(sentences[index]));
                    console.log(Object.keys(sentences[index]));
                    const sentenceInfoList = document.createElement('ul');

                    words.forEach((wordObj) => {
                        const word = Object.keys(wordObj)[0];
                        const score = Object.values(wordObj)[0];
                        const listItem = document.createElement('li');
                        listItem.textContent = `Word: ${word}, Score: ${score}`;
                        sentenceInfoList.appendChild(listItem);
                    });

                    sentenceData.appendChild(sentenceInfoList);
                    rankedWordsDiv.appendChild(sentenceData);
                });

                rankedWordsDiv.style.display = 'block';
            } else {
                rankedWordsDiv.innerHTML = 'No important words found.';
            }
        } catch (error) {
            console.error("Error parsing JSON:", error);
            resultDiv.innerHTML = 'Classification failed due to a server error.';
        }
    });
});
