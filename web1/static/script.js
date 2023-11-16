document.addEventListener('DOMContentLoaded', function () {
    const textForm = document.getElementById('textForm');
    const resultDiv = document.getElementById('result');

    textForm.addEventListener('submit', async function (e) {
        e.preventDefault();
        resultDiv.innerHTML = 'Classifying...';

        // Get input values from the form fields
        const title = document.getElementById('title').value;
        const channelTitle = document.getElementById('channel_title').value;
        // const viewCount = parseFloat(document.getElementById('view_count').value);
        const tags = document.getElementById('tags').value;
        const description = document.getElementById('description').value;

        // Organize JSON data
        const inputData = {
            "title": title,
            "channel_title": channelTitle,
            // "view_count": viewCount,
            "tags": tags,
            "description": description
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

            if (data.result !== undefined) {
                const classification = data.result === -1 ? "Non Conspiracy" : "Potential Conspiracy";
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
