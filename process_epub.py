import zipfile
import os
import shutil
import re
from bs4 import BeautifulSoup

def normalize_hashes(text):
    """Collapse multiple hashes into a single one."""
    return re.sub(r'#{2,}', '#', text)

def process_paragraph_text(text):
    # 0. Protect triple periods by temporarily replacing with a placeholder
    text = text.replace('...', '[[ELLIPSIS]]')

    # 1. Add # after punctuation
    text = re.sub(r'([.?!…–—!])', r'\1#', text)

    # 2. Restore triple periods with a single trailing hash
    text = text.replace('[[ELLIPSIS]]', '...#')

    # 3. Clean up hashes around quotes
    text = re.sub(r'#([“”"\'])', r'\1', text)
    text = re.sub(r'([“”"\'])#', r'\1', text)

    # 4. Remove any hash sequences separated by whitespace (incl. non-breaking space)
    text = re.sub(r'#(?:\s|\u00A0)+#', '#', text)

    # 5. Collapse remaining multiple hashes
    text = re.sub(r'#{2,}', '#', text)

    # 6. Strip any trailing hashes and spaces
    text = re.sub(r'#*\s*$', '', text.strip())

    # 7. Add exactly one final #
    return text + '#'

def process_html(content):
    """Process full paragraph HTML instead of individual strings to handle quotes and tags cleanly."""
    soup = BeautifulSoup(content, 'html.parser')

    for p in soup.find_all('p'):
        # Get full inner HTML of <p>
        inner_html = ''.join(str(c) for c in p.contents)

        # Apply hash logic to full inner content
        processed = process_paragraph_text(inner_html)

        # Replace paragraph content
        p.clear()
        new_content = BeautifulSoup(processed, 'html.parser')
        for element in new_content.contents:
            p.append(element)

    return str(soup)

def extract_epub(epub_path, temp_dir):
    with zipfile.ZipFile(epub_path, 'r') as zip_ref:
        zip_ref.extractall(temp_dir)

def rezip_epub(temp_dir, output_path):
    with zipfile.ZipFile(output_path, 'w') as zipf:
        for root, dirs, files in os.walk(temp_dir):
            for file in files:
                filepath = os.path.join(root, file)
                arcname = os.path.relpath(filepath, temp_dir)
                zipf.write(filepath, arcname)

def process_epub(epub_path):
    temp_dir = "temp_epub"
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
    os.makedirs(temp_dir)

    extract_epub(epub_path, temp_dir)

    for root, dirs, files in os.walk(temp_dir):
        for file in files:
            if file.endswith(".xhtml") or file.endswith(".html"):
                filepath = os.path.join(root, file)
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                processed = process_html(content)
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(processed)

    output_path = os.path.splitext(epub_path)[0] + "_processed.epub"
    rezip_epub(temp_dir, output_path)
    shutil.rmtree(temp_dir)
    return output_path

if __name__ == "__main__":
    epub_path = input("📘 Enter full path to your EPUB file: ").strip()
    if not os.path.isfile(epub_path) or not epub_path.lower().endswith('.epub'):
        print("❌ Invalid .epub file path.")
    else:
        output = process_epub(epub_path)
        print(f"\n✅ Processed EPUB saved as: {output}")
