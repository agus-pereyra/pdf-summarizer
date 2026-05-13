# PDF Summarizer

Extracts and summarizes content from PDF files using OCR and the Gemini API.

## Features

- **Text extraction** — reads native PDF text; falls back to OCR (Tesseract) for scanned/image-based pages
- **Async summarization** — splits text into chunks and sends them concurrently to the Gemini API
- **Structured output** — saves each chunk's summary as JSON (`subjects`, `key_data`, `summary`, `date`, `author`)
- **OCR testing** — generates PDFs from arbitrary strings and validates OCR accuracy, logging results to JSON

## Stack

- [`PyMuPDF`](https://pymupdf.readthedocs.io/) — PDF parsing
- [`Tesseract`](https://github.com/tesseract-ocr/tesseract) + `pytesseract` — OCR (English & Spanish)
- [`Pillow`](https://pillow.readthedocs.io/) — image handling and PDF generation for tests
- [`google-genai`](https://ai.google.dev/) — Gemini API client
- `asyncio` — concurrent chunk processing

## Usage

```bash
# Summarize a PDF or TXT file
python src/pipeline.py docs/example.pdf
python src/pipeline.py docs/example.txt
```

Output is saved to `outputs/<filename>_summary.json`.

## OCR Tests

Each call to `test_ocr(text)` renders the string into a PDF, runs OCR on it, and appends a result to `tests/logs/ocr_log.json`.

```bash
python -m tests.ocr_test "your text here"
```

Log entry format:
```json
{
  "original_text": "...",
  "ocr_text": "...",
  "error_count": 3
}
```

`error_count` is the character-level edit distance between the original and OCR output.

## Setup

```bash
pip install -r requirements.txt
export GEMINI_API_KEY=your_key_here
```

Tesseract must be installed separately (`apt install tesseract-ocr`).
