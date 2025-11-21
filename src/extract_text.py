from pathlib import Path
from pypdf import PdfReader


def extract_text_from_pdf(pdf_path: str) -> str:
    pdf_file = Path(pdf_path)
    reader = PdfReader(str(pdf_file))

    pages_text = []
    for page in reader.pages:
        text = page.extract_text() or ""
        text = text.replace("\u00a0", " ")  # clean non-breaking spaces
        pages_text.append(text.strip())

    full_text = "\n\n".join(pages_text)
    return full_text


if __name__ == "__main__":
    text = extract_text_from_pdf("data/ukpga_20250022_en.pdf")
    print(text[:2000])
