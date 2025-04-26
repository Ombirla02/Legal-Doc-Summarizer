from flask import Flask, render_template, request, jsonify
from summarizer import summarize_text  # Your own summarizer logic
import os
import PyPDF2

app = Flask(__name__)

def extract_text_from_pdf(file_path):
    text = ""
    with open(file_path, 'rb') as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            text += page.extract_text()
    return text

@app.route('/')
def home():
    return render_template('index.html')  # Showing the HTML form

@app.route('/summarize', methods=['POST'])
def summarize():
    input_type = request.form.get('input_type')

    if input_type == 'text':
        # Get the text input
        input_text = request.form.get('text')
    elif input_type == 'file':
        # Get the uploaded file
        uploaded_file = request.files['file']
        if uploaded_file:
            filename = uploaded_file.filename
            file_ext = os.path.splitext(filename)[1].lower()

            if file_ext == '.pdf':
                file_path = "uploaded_file.pdf"
                uploaded_file.save(file_path)
                input_text = extract_text_from_pdf(file_path)
            elif file_ext == '.txt':
                input_text = uploaded_file.read().decode('utf-8')
            else:
                return "Please upload a valid PDF or TXT file."
        else:
            return "No file uploaded."
    else:
        return "Invalid input type."

    # Summarize the extracted or entered text
    summary = summarize_text(input_text)

    return f"<h2>Summary:</h2><p>{summary}</p>"

if __name__ == '__main__':
    app.run(debug=True)
