import fitz
import sys

def text_from_pdf(path : str):
    doc = fitz.open(path)
    text = ''
    for pag in doc:
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