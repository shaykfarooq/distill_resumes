from django.conf import settings
import pytesseract
from PIL import Image
from docx import Document
import spacy
from pdf2image import convert_from_path
import os


# Initialize spaCy NLP model
nlp = spacy.load("en_core_web_sm")

# Function to extract text from a PDF file (with images)
def extract_text_pdf_with_ocr(pdf_path):
    # Convert PDF pages to images
    pages = convert_from_path(pdf_path, 300)  # 300 DPI for better OCR accuracy
    text = ""
    
    for page in pages:
        # Perform OCR on each page
        page_text = pytesseract.image_to_string(page)
        text += page_text
    
    return text

# Function to extract text and perform OCR on images in a Word file
def extract_text_word(docx_path, image_dir):
    doc = Document(docx_path)
    text = ""

    # Ensure the image directory exists
    if not os.path.exists(image_dir):
        os.makedirs(image_dir)

    for para in doc.paragraphs:
        text += para.text + "\n"

    for rel in doc.part.rels.values():
        if "image" in rel.target_ref:
            image = rel.target_part.blob
            image_path = os.path.join(image_dir, f"image_{len(os.listdir(image_dir)) + 1}.png")
            with open(image_path, "wb") as img_file:
                img_file.write(image)
            
            # Perform OCR on the image
            ocr_text = pytesseract.image_to_string(Image.open(image_path))
            text += ocr_text + "\n"

    return text

# Function for OCR processing (for scanned PDFs or images)
def extract_text_ocr(image_path):
    image = Image.open(image_path)
    text = pytesseract.image_to_string(image)
    return text


# Main processing function
def process_document_get_text(doc_path):
    text = ""

    file_extenstion = doc_path.split('.')[-1]

    # Extract text based on the document type
    if file_extenstion == 'pdf':
        text = extract_text_pdf_with_ocr(doc_path)
    elif file_extenstion == 'jpg' or file_extenstion == 'jpeg' or file_extenstion == 'png':
        text = extract_text_ocr(doc_path)
    elif file_extenstion == 'docx' or  file_extenstion == 'doc':
        text = extract_text_word(doc_path,doc_path.replace(f'.{file_extenstion}','_images'))
    
    print(text)
    
    return text.upper()
   
