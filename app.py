from flask import Flask, request, jsonify
from summarizer import summarize_text  # Assuming your summarizer code is in 'summarizer.py'

app = Flask(__name__)

@app.route('/')
def home():
    return "Legal Document Summarizer API is running!"

@app.route('/summarize', methods=['POST'])
def summarize():
    file = request.files['file']
    if file:
        # Save the uploaded PDF
        file_path = "uploaded_file.pdf"
        file.save(file_path)

        # Extract text from PDF and summarize it
        text = extract_text_from_pdf(file_path)  # You can reuse your existing extract_text_from_pdf function
        summary = summarize_text(text)

        return jsonify({"summary": summary})

    return jsonify({"error": "No file uploaded"}), 400

if __name__ == '__main__':
    app.run(debug=True)
