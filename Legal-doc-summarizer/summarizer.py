import fitz  # PyMuPDF
from transformers import pipeline

# Initialize the summarization pipeline
summarizer = pipeline("summarization", model="facebook/bart-large-cnn", device=0)  # Change device to 0 for GPU or -1 for CPU

# Function to extract text from PDF
def extract_text_from_pdf(pdf_path):
    text = ""
    with fitz.open(pdf_path) as doc:
        for page in doc:
            text += page.get_text()
    return text

# Function to summarize text (handling token limits)
def summarize_text(text, max_token_limit=1024):
    # Split the text into smaller chunks if it exceeds the max token limit
    chunks = []
    words = text.split()
    chunk = []
    for word in words:
        chunk.append(word)
        if len(' '.join(chunk)) > max_token_limit:
            chunks.append(' '.join(chunk[:-1]))
            chunk = [word]  # Start a new chunk
    chunks.append(' '.join(chunk))  # Add remaining words as a chunk
    
    # Summarize each chunk
    summary = ""
    for chunk in chunks:
        chunk_summary = summarizer(chunk, max_length=200, min_length=50, do_sample=False)
        summary += chunk_summary[0]['summary_text'] + "\n"  # Combine summaries
    
    return summary

# Path to the PDF file
pdf_path = 'legal-document.pdf'  # Update with your actual file path

# Extract text from the PDF
text = extract_text_from_pdf(pdf_path)

# Print the extracted text (for reference)
print("Extracted Text:\n", text[:1000])  # Display first 1000 characters for preview

# Summarize the extracted text
summary = summarize_text(text)

# Print the summarized text
print("\nSummary:\n", summary)
