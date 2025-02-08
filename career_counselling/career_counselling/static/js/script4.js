function loadQuestions(group) {
    fetch(`/get_questions?group=${group}`)
        .then(response => response.json())
        .then(data => {
            const questionsContainer = document.getElementById('questions-container');
            questionsContainer.innerHTML = '';
            data.questions.forEach((question, index) => {
                const questionElement = document.createElement('div');
                questionElement.innerHTML = `
                    <label class="question" for="question_${index + 1}">Question ${index + 1}: ${question}</label><br>
                    <input class="option" type="radio" id="question_${index + 1}_1" name="question_${index + 1}" value="1" required> <label for="question_${index + 1}_1">1</label> <br>
                    <input class="option" type="radio" id="question_${index + 1}_2" name="question_${index + 1}" value="2" required> <label for="question_${index + 1}_2">2</label> <br>
                    <input class="option" type="radio" id="question_${index + 1}_3" name="question_${index + 1}" value="3" required> <label for="question_${index + 1}_3">3</label> <br>
                    <input class="option" type="radio" id="question_${index + 1}_4" name="question_${index + 1}" value="4" required> <label for="question_${index + 1}_4">4</label> <br>
                    <input class="option" type="radio" id="question_${index + 1}_5" name="question_${index + 1}" value="5" required> <label for="question_${index + 1}_5">5</label> <br>
                    <br><br>
                `;
                questionsContainer.appendChild(questionElement);
            });
        });
}

document.addEventListener('DOMContentLoaded', () => {
    const groupSelect = document.getElementById('group');
    groupSelect.addEventListener('change', (event) => {
        loadQuestions(event.target.value);
    });

    // Load questions for the default group on page load
    loadQuestions(groupSelect.value);
});