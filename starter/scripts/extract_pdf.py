import urllib.request
import pypdf
import json
import re
import os

pdf_url = "https://ussh.vnu.edu.vn/vi/van-ban/detail/Quy-che-dao-tao-dai-hoc-tai-Dai-hoc-Quoc-gia-Ha-Noi-Ap-dung-tu-khoa-QH-2022-X-19452/?download=1&id=0"
save_pdf_path = "starter/data/Quy-che-3626-digital.pdf"
pages_json_path = "starter/data/extracted_pages.json"

req = urllib.request.Request(pdf_url, headers={"User-Agent": "Mozilla/5.0"})
print("Downloading digital PDF...")
with urllib.request.urlopen(req) as resp:
    data = resp.read()
    with open(save_pdf_path, "wb") as f:
        f.write(data)
print(f"Saved digital PDF to {save_pdf_path} ({len(data)} bytes)")

reader = pypdf.PdfReader(save_pdf_path)
print(f"Total pages: {len(reader.pages)}")

pages_data = []
for idx, page in enumerate(reader.pages):
    page_num = idx + 1
    text = page.extract_text() or ""
    # Normalize unicode spaces
    text = re.sub(r'[\r\t\f\v]', ' ', text)
    lines = [line.strip() for line in text.split("\n") if line.strip()]
    normalized_text = "\n".join(lines)
    
    pages_data.append({
        "page": page_num,
        "char_count": len(normalized_text),
        "text": normalized_text
    })

os.makedirs("starter/data", exist_ok=True)
with open(pages_json_path, "w", encoding="utf-8") as f:
    json.dump(pages_data, f, ensure_ascii=False, indent=2)

print(f"Extracted {len(pages_data)} pages to {pages_json_path}")
total_chars = sum(p["char_count"] for p in pages_data)
print(f"Total characters: {total_chars}")

# Find chapters and articles
full_text = "\n\n".join(f"[Trang {p['page']}]\n{p['text']}" for p in pages_data)
chapters = re.findall(r'(Chương\s+[IVXLCDM]+\b[^\n]*)', full_text, flags=re.IGNORECASE)
print(f"Found {len(chapters)} chapters:")
for c in chapters:
    print(" -", c)

articles = re.findall(r'(Điều\s+\d+\b[^\n]*)', full_text)
print(f"Found {len(articles)} articles (first 10 shown):")
for a in articles[:10]:
    print(" -", a)
print(f"Total articles found: {len(articles)}")

