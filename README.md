# CV Analysis System

## Overview
The CV Analysis System is a powerful tool designed to process multiple CV documents (PDF and Word), extract relevant information using OCR, and provide a chatbot interface for querying the extracted data. The system leverages Django 5.1, OpenAI GPT, and Pytesseract for OCR and natural language processing.

--

## Tech Stack
- **Python 3.12** (Conda environment)
- **Django 5.1** (Web framework)
- **Tesseract OCR (`pytesseract`)** (Text extraction)
- **OpenAI GPT API** (LLM integration)
- **PostgreSQL** (Database)
- **Celery & Redis** (Asynchronous processing)
- **Django REST Framework** (API)
- **NLTK & spaCy** (Natural Language Processing)

---

## Setup Instructions


### 0. Ensure you have Tesseract, Poppler, and the spaCy small model installed and added to the environment path
- **Tesseract Installation:** [https://github.com/tesseract-ocr/tesseract](https://github.com/tesseract-ocr/tesseract)
- **Poppler Installation:** [https://poppler.freedesktop.org/](https://poppler.freedesktop.org/)
- **spaCy small model installation:**
  ```sh
  python -m spacy download en_core_web_sm
  ```


### 1. Clone the Repository
```sh
$ git clone <your-repository-url>
$ cd 
```

### 2. Create a Conda Environment
```sh
$ conda create --name distill_resumes python=3.12
$ conda activate distill_resumes
```

### 3. Install Dependencies
```sh
$ pip install -r requirements.txt
```

### 4. Set Up Environment Variables
- Copy `.env.example` and rename it to `.env`
- Add your API keys and configurations

### 5. Set Up Database (PostgreSQL)
```sh
$ python manage.py makemigrations
$ python manage.py migrate
```

### 6. Run the Application
```sh
$ python manage.py runserver
```

---


