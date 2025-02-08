from flask import Flask, request, jsonify, render_template
import json

import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import spacy
import speech_recognition as sr
from textblob import TextBlob
from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import candidate as cd

# Initialize Flask app
app2 = Flask(__name__)

# Load JSON data
def load_json_data():
    with open('questions.json', 'r') as file:
        data = json.load(file)
    return data

questions_data = load_json_data()

nlp = spacy.load("en_core_web_md")
stopwords_en = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

# Function to autocorrect user input
def autocorrect_spelling(user_input):
    blob = TextBlob(user_input)
    corrected_input = str(blob.correct())
    return corrected_input

# Function to process user input using spaCy for tokenization and NLTK for stopwords and lemmatization
def process_text(text):
    doc = nlp(text.lower())  # Convert text to lowercase before processing
    tokens = [token.text for token in doc if token.is_alpha]  # Tokenize and keep alphabetic tokens
    tokens = [word for word in tokens if word not in stopwords_en]  # Remove stopwords
    tokens = [lemmatizer.lemmatize(word) for word in tokens]  # Lemmatize tokens
    return tokens

# Function to find matching question and return its answer using combined similarity and token overlap
def get_answer(input_text):

    
    input_tokens = process_text(input_text)
    input_text_processed = ' '.join(input_tokens)
    input_doc = nlp(input_text_processed)
    
    best_match = None
    best_similarity = 0.0
    
    # Iterate through questions in JSON data
    for question in questions_data:
        question_tokens = process_text(question['question'])
        question_text_processed = ' '.join(question_tokens)
        question_doc = nlp(question_text_processed)
        
        if input_doc.has_vector and question_doc.has_vector:
            similarity = input_doc.similarity(question_doc)
            token_overlap = len(set(input_tokens) & set(question_tokens)) / len(set(input_tokens) | set(question_tokens))
            combined_score = (similarity + token_overlap) / 2
            
            if combined_score > best_similarity:
                best_similarity = combined_score
                best_match = question['answer']
    
    if best_similarity > 0.1:
        # Return the response directly, without caching
        return best_match
    else:
        return "Sorry, I couldn't find an answer to your question."

# Function to convert audio input to text
def audio_to_text():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio_data = recognizer.listen(source)
        print("Processing...")
        try:
            text = recognizer.recognize_google(audio_data)
            print("Text from audio:", text)
            return text
        except sr.UnknownValueError:
            return "Could not understand the audio"
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")

# Load the questions and answers from the JSON file

def find_answer(user_input):
    if user_input.lower() == 'voice':
        text = audio_to_text()
        if text:
            user_input = autocorrect_spelling(text)
            response = "Text from audio: " + user_input + "\n\n" + get_answer(user_input)

        return response
    elif user_input:
        user_input = autocorrect_spelling(user_input)
        response = get_answer(user_input)
        return response
    else:
        return "Sorry, I can't help with that. I'm here to assist with career-related queries."

@app2.route('/')
def index():
    return render_template('index.html')

@app2.route('/chat')
def test():
    return render_template('chat.html')

@app2.route('/chat', methods=['POST'])
def chat():
    user_input = request.form.get('user_input')
    response = find_answer(user_input)
    return response

@app2.route('/course')
def course():
    return render_template('course.html')


# New route to handle career guidance
@app2.route('/aptitute', methods=['GET', 'POST'])
def career_guidance():
    if request.method == 'POST':
        try:
            # Retrieve form data
            name = request.form.get('name')
            group = request.form.get('group')
            responses = [int(request.form.get(f'question_{i}', 0)) for i in range(1, 16)]

            # Debug: Print responses
            print("Responses:", responses)

            # Get domain data
            domain_data_raw = cd.get_domain_data()
            if isinstance(domain_data_raw, tuple):
    # Assume the group data is the second element in the tuple
                domain_data = domain_data_raw[1].get(group, [])
            else:
                domain_data = domain_data_raw.get(group, [])
            print("Domain Data for Group:", domain_data)

            # Validate domain data
            if not domain_data:
                print("Error: No domain data for group")
                return f"Error: No domain data available for the group '{group}'.", 404

            # Predict career domains
            matched_domains = cd.predict_career(responses, domain_data)
            print("Matched Domains:", matched_domains)

            # Determine the best match
            best_match = None
            if matched_domains.get("exact"):
                best_match = matched_domains["exact"][0][0]
            elif matched_domains.get("close"):
                best_match = matched_domains["close"][0][0]

            print("Best Match:", best_match)

            # Store responses in the database
            if best_match:
                cd.store_responses(name, group, responses, best_match)

            return render_template('result.html', matched_domains=matched_domains, best_match=best_match)

        except Exception as e:
            print("Error occurred:", str(e))
            import traceback
            traceback.print_exc()
            return "An error occurred while processing your request. Please try again later.", 500

    group = request.args.get('group', 'CS')
    questions = cd.get_questions_by_group(group)
    return render_template('aptitude_test.html', questions=questions, enumerate=enumerate)

@app2.route('/get_questions')
def get_questions():
    group = request.args.get('group', 'CS')
    questions = cd.get_questions_by_group(group)
    return jsonify(questions=[q['question'] for q in questions])

if __name__ == '__main__':
     app2.run(debug=True, threaded=True)