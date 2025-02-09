from flask import Flask, request, jsonify, send_from_directory, render_template
import wikipedia
import random
import time
import sympy as sp
import os
import nltk
from nltk.tokenize import sent_tokenize
from flask_cors import CORS
from transformers import pipeline  # AI text generation model
from bs4 import BeautifulSoup
from collections import Counter
import re

# Ensure required nltk data is downloaded
nltk.download('punkt')
nltk.download('punkt_tab')


app = Flask(__name__, static_folder="frontend", template_folder="frontend")
CORS(app)

# Ensure an "uploads" folder exists
UPLOAD_FOLDER = "uploads"
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# AI Text Generation Model (GPT-2)
ai_text_generator = pipeline("text-generation", model="gpt2")

# Function to clean and format text responses
def clean_text(text):
    text = re.sub(r"\bsource:\s?[A-Za-z0-9\s]+", "", text, flags=re.IGNORECASE)
    text = re.sub(r"\(Source:.*?\)", "", text)
    text = re.sub(r"according to\s?(Google|Wikipedia|sources)", "", text, flags=re.IGNORECASE)
    text = re.sub(r"as per\s?(Google|Wikipedia|research)", "", text, flags=re.IGNORECASE)
    text = re.sub(r"as stated by\s?(Google|Wikipedia)", "", text, flags=re.IGNORECASE)
    text = re.sub(r"\bGoogle\b|\bWikipedia\b", "", text, flags=re.IGNORECASE)
    text = re.sub(r"\b(see also|external links|references):.*", "", text, flags=re.IGNORECASE)
    text = re.sub(r"\s+", " ", text).strip()
    return text.strip()

def format_response(text):
    sentences = text.split(". ")
    return "\n".join(sentences)

def generate_ai_response(text, response_length="medium"):
    """Generates AI response with better accuracy by adjusting randomness."""
    max_length = 250 if response_length == "long" else 80 if response_length == "short" else 150
    response = ai_text_generator(text, max_length=max_length, do_sample=False, temperature=0.5)  # Reduce randomness
    cleaned_text = clean_text(response[0]['generated_text'])
    return format_response(cleaned_text)

def extract_text_from_pdf(pdf_path):
    """Extracts text from a PDF file using PyMuPDF (pymupdf)."""
    doc = pymupdf.open(pdf_path)  # Open the PDF file
    text = ""

    for page in doc:
        text += page.get_text("text") + "\n"  # Extract text from each page
    
    return text.strip()


def determine_response_length(user_message):
    long_keywords = ["brief description", "detailed explanation", "elaborate", "tell me in detail", "comprehensive"]
    short_keywords = ["short description", "quick summary", "in a nutshell", "summarize", "short explanation"]
    
    if any(word in user_message for word in long_keywords):
        return "long"
    if any(word in user_message for word in short_keywords):
        return "short"
    return "medium"

def solve_math_problem(expression):
    """Solves basic math problems and returns an accurate answer."""
    try:
        # Handle symbolic math expressions like algebraic equations
        if "=" in expression:
            lhs, rhs = expression.split("=")
            result = sp.solve(sp.sympify(lhs) - sp.sympify(rhs))
        else:
            result = sp.sympify(expression).evalf()

        return f"The answer is: {result}"
    except Exception:
        return None


def solve_geometry_problem(user_message):
    patterns = {
        "area of circle": lambda r: sp.pi * r**2,
        "perimeter of circle": lambda r: 2 * sp.pi * r,
        "area of rectangle": lambda l, w: l * w,
        "perimeter of rectangle": lambda l, w: 2 * (l + w),
        "volume of sphere": lambda r: (4/3) * sp.pi * r**3,
        "volume of cube": lambda a: a**3
    }
    
    for key, formula in patterns.items():
        if key in user_message:
            numbers = [float(s) for s in re.findall(r"\d+\.?\d*", user_message)]
            if len(numbers) == formula.__code__.co_argcount:
                return f"The {key} is: {formula(*numbers):.2f}"
    
    return None

def get_wikipedia_summary(query, response_length="medium"):
    """Fetches a Wikipedia summary with better accuracy."""
    try:
        search_results = wikipedia.search(query)
        if not search_results:
            return "I couldn't find relevant information."

        exact_match = next((result for result in search_results if query.lower() in result.lower()), None)
        selected_page = exact_match if exact_match else search_results[0]

        sentence_count = 5 if response_length == "long" else 2 if response_length == "short" else 3
        summary = wikipedia.summary(selected_page, sentences=sentence_count)

        # Explicitly specify the parser to avoid warnings
        parsed_html = BeautifulSoup(summary, features="lxml")
        return parsed_html.get_text()

    except wikipedia.exceptions.DisambiguationError as e:
        return f"Your query is too broad! Try specifying it further: {', '.join(e.options[:5])}"
    except wikipedia.exceptions.PageError:
        return "I couldn't find relevant information."

def get_ai_response(user_message):
    user_message = user_message.lower()
    response_length = determine_response_length(user_message)

    if any(greet in user_message for greet in ["hello", "hi", "hey", "what's up", "how are you"]):
        return random.choice(["Hey there! 😊", "Hello! How's your day going?", "Hi! What's on your mind?"])
    
    if (math_solution := solve_math_problem(user_message)):
        return math_solution
    
    if (geometry_solution := solve_geometry_problem(user_message)):
        return geometry_solution
    
    if (wiki_summary := get_wikipedia_summary(user_message, response_length)):
        return wiki_summary
    
    return generate_ai_response(user_message, response_length=response_length)

@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.json
    user_message = data.get("message", "")
    if not user_message:
        return jsonify({"error": "No input provided"}), 400
    time.sleep(1.5)
    bot_response = get_ai_response(user_message)
    return jsonify({"response": bot_response})

import pymupdf  # Correct import for PyMuPDF

@app.route("/api/upload", methods=["POST"])
def upload_file():
    """Handles file upload and automatically summarizes text files and PDFs."""
    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files["file"]
    
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    file_path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
    file.save(file_path)

    # Extract text from PDFs
    if file.filename.endswith(".pdf"):
        content = extract_text_from_pdf(file_path)
    
    # Extract text from .txt, .md, .csv files
    elif file.filename.endswith((".txt", ".md", ".csv")):
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

    else:
        return jsonify({"error": "Unsupported file format. Upload a .txt or .pdf file."}), 400

    # Prevent empty files from being processed
    if not content.strip():
        return jsonify({"error": "The uploaded file is empty."}), 400

    # Generate summary
    summary = summarize_text(content)

    return jsonify({
        "message": f"File '{file.filename}' uploaded successfully!",
        "file": file.filename,
        "summary": summary
    })


def summarize_text(text):
    """Summarizes the uploaded text file using frequency-based extraction."""
    sentences = sent_tokenize(text)
    if len(sentences) <= 5:
        return text  # Return full text if it's already short

    words = text.split()
    word_freq = Counter(words)
    most_common_words = {word for word, freq in word_freq.most_common(10)}

    summary = [sentence for sentence in sentences if any(word in sentence for word in most_common_words)]
    return " ".join(summary[:5])


@app.route("/")
def serve_frontend():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)