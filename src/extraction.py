import fitz # pymupdf
import sys
from PIL import Image
import pytesseract
import io

def needs_ocr(page : fitz.Page) -> bool:
    '''
    True if page needs OCR (Optical Character Recognition)
    '''
    text = page.get_text().strip()
    area = page.rect.width * page.rect.height
    density = len(text) / area
    return density < 0.001 # low text density => True

def ocr_page(page : fitz.Page) -> str:
    '''
    Translates a PDF page to plain text using Tesseract
    '''
    pixmap = page.get_pixmap(dpi=300) # pixmap (height x width x channels)
    img_bytes = pixmap.tobytes("png") # png (bytes)
    img = Image.open(io.BytesIO(img_bytes)) # object Image
    text = pytesseract.image_to_string(img, lang="eng+spa") # english & spanish
    return text

def text_from_pdf(path : str):
    doc = fitz.open(path)
    text = ''
    for pag in doc:
        if needs_ocr(pag):
            text += ocr_page(pag)
        else:
            text += pag.get_text()
    doc.close()
    return text

def save_text(text : str, path : str):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(text)

if __name__ == '__main__':
    path = sys.argv[1]
    output_path = path.replace('pdf', 'txt')
    text = text_from_pdf(path)
    save_text(text, output_path)
    print(f'Text saved in {output_path}')