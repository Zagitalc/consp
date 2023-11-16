document.addEventListener('DOMContentLoaded', function () {
    const textForm = document.getElementById('textForm');
    const resultDiv = document.getElementById('result');
    const userTextDiv = document.getElementById('userText');
    const userTextInput = document.getElementById('userTextInput');
    const rankedWordsDiv = document.getElementById('rankedWords');

    textForm.addEventListener('submit', async function (e) {
        e.preventDefault();
        resultDiv.innerHTML = 'Classifying...';

        // single text input 
        const inputText = document.getElementById('inputText').value;

        // JSON response format 
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

            if (data.classPred !== undefined) {
                const classification = data.classPred === 0 ? "Non Conspiracy" : "Potential Conspiracy";
                resultDiv.innerHTML = `Classification: ${classification}, prediction ${data.classPred}`;


                resultDiv.style.display = 'block';
                // display a copy of user text for highlighting purpose
                userTextInput.textContent = inputText;
                userTextDiv.style.display = 'block';
            } else {
                resultDiv.innerHTML = 'Classification failed.';
            }
            if (data.rankedWords !== undefined && data.rankedWords.length > 0) {
                const WordsRankList = document.createElement('ul');
                data.rankedWords.forEach(word => {
                    const listItem = document.createElement('li');
                    listItem.textContent = word;
                    WordsRankList.appendChild(listItem);
                });
                rankedWordsDiv.appendChild(WordsRankList);
            } else {
                rankedWordsDiv.innerHTML = `No important words found.${data.rankedWords}`;
            }
            rankedWordsDiv.style.display = 'block';
        } catch (error) {
            console.error("Error parsing JSON:", error);
            resultDiv.innerHTML = 'Classification failed due to a server error.';
        }
    });
});
