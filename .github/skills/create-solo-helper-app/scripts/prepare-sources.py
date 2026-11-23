"""Prepare rulebook/card PDFs for transcription (create-solo-helper-app skill, Phase A).

Usage (run with `python -X utf8`, requires `pip install pymupdf`):
  prepare-sources.py inventory <resources-dir>
      Table of all PDFs: pages, text layer (chars), garbled spans -> effort estimate.
  prepare-sources.py extract <resources-dir> <out-dir>
      Text per PDF (<out-dir>/text/<name>.txt, page separators, garbled spans decoded) and
      page renders (<out-dir>/pages/<name>__pNN.png; 110 dpi for text PDFs, 150 dpi for scans).
  prepare-sources.py crop <pdf> <page> <x0> <y0> <x1> <y1> <out.png> [dpi]
      Crop of one page area (coordinates as fractions 0..1 of the page), default 250 dpi.

Never write the output into the app repo - use the session folder.
"""
import os
import re
import sys

import fitz

COMMON = re.compile(r'\b(the|and|of|to|a|is|in|on|it|its|if|from|for|with|this|that|be|or|you|your|each|one|an|at|as|by|are|not|then|will)\b')


def decode_span(text):
    """Some PDFs embed fonts with glyph codes shifted by -29 (`WKH` = `the`). Returns (text, decoded)."""
    if re.search('[a-z]', text) or not re.search('[A-Z$%&]', text):
        return text, False
    out = []
    for ch in text:
        o = ord(ch)
        if ch == ' ':
            out.append(ch)
        elif ch == '\u0193':
            out.append('fi')
        elif ch == '\u0174':
            out.append('fl')
        elif o < 0x80:
            out.append(chr(o + 29))
        else:
            out.append(ch)
    dec = ''.join(out)
    letters = re.findall('[A-Za-z]', dec)
    if COMMON.search(dec) and len(re.findall('[a-z]', dec)) > 0.6 * max(1, len(letters)):
        return dec, True
    return text, False


def pdfs(root):
    for dirpath, _, files in os.walk(root):
        for f in sorted(files):
            if f.lower().endswith('.pdf'):
                path = os.path.join(dirpath, f)
                yield path, os.path.relpath(path, root)


def is_scan(doc):
    return sum(len(p.get_text().strip()) for p in doc) < 50 * doc.page_count


def inventory(root):
    print('| pdf | pages | text chars | garbled spans | type | effort |')
    print('|-----|-------|------------|---------------|------|--------|')
    for path, rel in pdfs(root):
        doc = fitz.open(path)
        chars = 0
        garbled = 0
        for page in doc:
            for block in page.get_text('dict')['blocks']:
                for line in block.get('lines', []):
                    for span in line['spans']:
                        chars += len(span['text'].strip())
                        garbled += decode_span(span['text'])[1]
        scan = is_scan(doc)
        kind = 'scan (images only)' if scan else 'text layer'
        effort = f'high ({doc.page_count} page images)' if scan else 'low (text)'
        print(f'| {rel} | {doc.page_count} | {chars} | {garbled} | {kind} | {effort} |')


def extract(root, out):
    os.makedirs(os.path.join(out, 'text'), exist_ok=True)
    os.makedirs(os.path.join(out, 'pages'), exist_ok=True)
    for path, rel in pdfs(root):
        name = rel.replace('\\', '__').replace('/', '__')[:-4]
        doc = fitz.open(path)
        scan = is_scan(doc)
        if not scan:
            with open(os.path.join(out, 'text', name + '.txt'), 'w', encoding='utf-8') as f:
                for i, page in enumerate(doc):
                    f.write(f'\n\n===== PDF page {i + 1} =====\n')
                    for block in page.get_text('dict', sort=True)['blocks']:
                        for line in block.get('lines', []):
                            f.write(''.join(decode_span(s['text'])[0] for s in line['spans']).rstrip() + '\n')
                        f.write('\n')
        for i, page in enumerate(doc):
            page.get_pixmap(dpi=150 if scan else 110).save(os.path.join(out, 'pages', f'{name}__p{i + 1:02d}.png'))
        print(f'{rel}: {doc.page_count} pages, {"scan" if scan else "text"}')


def crop(pdf, page, x0, y0, x1, y1, out, dpi=250):
    p = fitz.open(pdf)[int(page) - 1]
    r = p.rect
    clip = fitz.Rect(r.width * float(x0), r.height * float(y0), r.width * float(x1), r.height * float(y1))
    p.get_pixmap(dpi=int(dpi), clip=clip).save(out)
    print(out)


if __name__ == '__main__':
    cmd, args = sys.argv[1], sys.argv[2:]
    {'inventory': inventory, 'extract': extract, 'crop': crop}[cmd](*args)
