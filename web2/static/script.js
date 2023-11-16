document.addEventListener('DOMContentLoaded', function () {
    const textForm = document.getElementById('textForm');
    const resultDiv = document.getElementById('result');

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

            if (data.prediction !== undefined) {
                const classification = data.prediction === 0 ? "Non Conspiracy" : "Potential Conspiracy";
                resultDiv.innerHTML = `Classification: ${classification}`;
            } else {
                resultDiv.innerHTML = 'Classification failed.';
            }
        } catch (error) {
            console.error("Error parsing JSON:", error);
            resultDiv.innerHTML = 'Classification failed due to a server error.';
        }
    });
});
