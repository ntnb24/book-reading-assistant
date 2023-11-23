import fitz  # PyMuPDF
from pprint import pprint
import PyPDF2
import time
from pdfminer.high_level import extract_text_to_fp
from pdfminer.layout import LAParams
from io import StringIO
FROM_WHICH_PARAGRAPH = 196
FROM_WHICH_PAGE = 11

PDF_PATH = 'data/Calinescu, George - Enigma Otiliei.pdf'
BOOK_TEXT_PATH = "data/book_text"
PAGES_PATH = "C:\\Users\\40783\\Documents\\GitHub\\book-reading-assistant\\data\\pages"
PARAGRAPHS_PATH = "C:\\Users\\40783\\Documents\\GitHub\\book-reading-assistant\\data\\paragraphs"


def correct_diacritics(text):
    # Map the incorrect characters to the correct diacritics
    corrections = {
        # Update these mappings based on the actual incorrect sequences you observe
        '[': 'ă', ']': 'î',  # t with cedilla
        '{': 'î', '}': 'Î',  # i with circumflex
        '{': 'î', '}': 'Î',  # i with circumflex
        '`': 'â',
        '=': 'ș', '\\': 'ț',
        "+": "Ș"
    }
    for incorrect, correct in corrections.items():
        text = text.replace(incorrect, correct)
    return text


def extract_full_concatenated_text_paragraphs_pdfminer(pdf_path):
    output_string = StringIO()
    with open(pdf_path, 'rb') as f:
        laparams = LAParams(line_overlap=0.5, char_margin=2.0, line_margin=0.5, word_margin=0.1, boxes_flow=0.5)
        extract_text_to_fp(f, output_string, codec="UTF-8", laparams=laparams)

    text = output_string.getvalue()
    output_string.close()
    paragraphs = [correct_diacritics(para.strip()) for para in text.split('\n') if para.strip() != '']
    paragraphs = paragraphs[FROM_WHICH_PARAGRAPH:]
    return paragraphs


def extract_full_concatenated_text_paragraphs_pdfminer_v2_paragraphs(pdf_path, from_which_paragraph=0):
    output_string = StringIO()
    with open(pdf_path, 'rb') as f:
        laparams = LAParams(line_overlap=0.5, char_margin=2.0, line_margin=0.5, word_margin=0.1, boxes_flow=0.5)
        extract_text_to_fp(f, output_string, codec="UTF-8", laparams=laparams)

    text = output_string.getvalue()
    output_string.close()
    # print(text)

    # Split text into potential paragraphs
    potential_paragraphs = [para.strip() for para in text.split('\n\n')]
    print(potential_paragraphs)
    # Filter out non-paragraph text based on your criteria
    paragraphs = [correct_diacritics(para) for para in potential_paragraphs]

    # Apply the FROM_WHICH_PARAGRAPH filter
    paragraphs = paragraphs[from_which_paragraph:]

    return paragraphs

if __name__ =="__main__":
    import time
    from pprint import pprint
    times = []
    times.append(time.perf_counter())
    paragraphs = extract_full_concatenated_text_paragraphs_pdfminer_v2_paragraphs(PDF_PATH, from_which_paragraph=0)
    pprint(paragraphs)
    times.append(time.perf_counter())
    for i in range(len(paragraphs)):
        file_name = f'paragraph-{i}.txt'
        with open(f"{PARAGRAPHS_PATH}/{file_name}", 'w', encoding="utf-8") as file:
            file.write(paragraphs[i])
    times.append(time.perf_counter())
    print([times[i] - times[i-1] for i in range(1, len(times))])
    raise AssertionError




def extract_pages_as_list(pdf_file_path):
    page_texts = []

    with open(pdf_file_path, 'rb') as pdf_file:
        pdf_reader = PyPDF2.PdfFileReader(pdf_file)

        for page_num in range(pdf_reader.getNumPages()):
            if page_num < FROM_WHICH_PAGE:
                continue
            page = pdf_reader.getPage(page_num)
            page_text = correct_diacritics(page.extract_text())
            page_texts.append(page_text)

    return page_texts


def extract_paragraphs_as_list(pdf_file_path):
    page_texts = []
    with open(pdf_file_path, 'rb') as pdf_file:
        pdf_reader = PyPDF2.PdfFileReader(pdf_file)

        for page_num in range(pdf_reader.getNumPages()):
            if page_num < FROM_WHICH_PAGE:
                continue
            page = pdf_reader.getPage(page_num)
            page_text = correct_diacritics(page.extract_text())
            page_text.split("   ")
            page_texts.append(page_text)

    return page_texts


pages_as_list = extract_pages_as_list(PDF_PATH)

for i in range(len(pages_as_list)):
    file_name = f'page-{i}.txt'
    with open(f"{PAGES_PATH}/{file_name}", 'w', encoding="utf-8") as file:
        file.write(pages_as_list[i])
paragraphs = extract_paragraphs_as_list(PDF_PATH)
for i in range(len(paragraphs)):
    file_name = f'paragraph-{i}.txt'
    with open(f"{PARAGRAPHS_PATH}/{file_name}", 'w', encoding="utf-8") as file:
        file.write(paragraphs[i])

paragraphs = extract_full_concatenated_text_paragraphs_pdfminer(PDF_PATH)
content = "\n".join(paragraphs)
print(content)

with open(BOOK_TEXT_PATH, 'w', encoding="utf-8") as file:
    file.write(content)

print(len(paragraphs))
print(type(paragraphs))
print(type(paragraphs[0]))
print(len(paragraphs))

time.sleep(1000)

def check_pdf_fonts(pdf_path):
    doc = fitz.open(pdf_path)
    font_info = []

    for page_num in range(len(doc)):
        page = doc[page_num]
        fonts = page.get_fonts(full=True)  # Retrieves all font information on the page

        for font in fonts:
            font_info.append({
                "page": page_num,
                "font_name": font[0],
                "font_file": font[3],
                "encoding": font[4]
            })

    doc.close()
    return font_info


def extract_paragraphs_from_pdf(pdf_path):
    """
    Extract paragraphs from a given PDF file, focusing only on text and
    preserving Romanian diacritics.

    :param pdf_path: Path to the PDF file.
    :return: List of paragraphs extracted from the PDF.
    """
    # Open the PDF
    doc = fitz.open(pdf_path)

    paragraphs = []
    current_paragraph = ""

    for i in range(10, len(doc)):  # Assuming you want to start from page 10
        page = doc[i]

        # Extract text as a dictionary of blocks
        blocks = page.get_text("dict")["blocks"]

        for b in blocks:
            # Check if the block is a text block
            if b["type"] == 0:  # Type 0 indicates a text block
                for line in b["lines"]:
                    # Reconstruct the line from its spans
                    line_text = "".join([span["text"] for span in line["spans"]])
                    # Check if the line ends with a full stop
                    if line_text.endswith("."):
                        current_paragraph += " " + line_text
                        paragraphs.append(current_paragraph.strip())
                        current_paragraph = ""
                    else:
                        current_paragraph += " " + line_text

    # Close the PDF document
    doc.close()

    return paragraphs

fond_info = check_pdf_fonts("data/Calinescu, George - Enigma Otiliei.pdf")
pprint(fond_info)
time.sleep(10)
paragraphs = extract_paragraphs_from_pdf("data/Calinescu, George - Enigma Otiliei.pdf")


print(paragraphs)

for paragraph in paragraphs:
    print(paragraph)
    print(len(paragraph))
