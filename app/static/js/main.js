function askQuestion() {
    var question = document.getElementById('questionInput').value;
    fetch('/submit-question', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ question: question }),
    })
    .then(response => response.json())
    .then(data => {
        // Assuming the backend sends a JSON with the question and answer
        displayAnswer(data.question, data.answer);
    })
    .catch(error => console.error('Error:', error));
}

function displayAnswer(question, answer) {
    const answerSection = document.getElementById('answerSection');
    // Clear previous answers
    answerSection.innerHTML = '';
    // Display the new answer
    answerSection.innerHTML = `<p><strong>Question:</strong> ${question}</p>
                               <p><strong>Answer:</strong> ${answer}</p>`;
}