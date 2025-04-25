import fitz  # PyMuPDF for reading PDFs
from transformers import pipeline  # Hugging Face for summarizing

# Function to extract text from PDF
def extract_text_from_pdf(pdf_path):
    text = ""  # Store the extracted text
    with fitz.open(pdf_path) as doc:  # Open the PDF
        for page in doc:  # Loop through each page
            text += page.get_text()  # Extract text from each page
    return text

# Function to summarize the extracted text
def summarize_text(text):
    summarizer = pipeline("summarization")  # Load the summarizer
    summary = summarizer(text, max_length=150, min_length=50, do_sample=False)  # Summarize the text
    return summary[0]['summary_text']  # Return the summary

# Main block to test the functions
if __name__ == "__main__":
    path = "dummy.pdf"  # Put your PDF file name here
    text = extract_text_from_pdf(path)  # Extract text from the PDF
    summary = summarize_text(text)  # Summarize the extracted text
    print("Summary:")
    print(summary)  # Print the summary
